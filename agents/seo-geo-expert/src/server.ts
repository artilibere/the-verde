import { createWorkersAI } from "workers-ai-provider";
import { routeAgentRequest, type Schedule } from "agents";
import { getSchedulePrompt, scheduleSchema } from "agents/schedule";
import { AIChatAgent, type OnChatMessageOptions } from "@cloudflare/ai-chat";
import { convertToModelMessages, pruneMessages, stepCountIs, streamText, tool } from "ai";
import { z } from "zod";
import { seoGeoSystemPrompt } from "./prompts";
import {
  auditPageInput,
  batchAudit,
  batchAuditInput,
  fetchAndAuditPage,
  fetchSitemapInput,
  fetchSitemapUrls,
} from "./seo-tools";

export class SeoGeoAgent extends AIChatAgent<Env> {
  maxPersistedMessages = 80;

  async onStart() {
  }

  async runSiteAudit(limit = 10) {
    const baseUrl = this.env.SITE_BASE_URL;
    const result = await batchAudit(baseUrl, Math.min(limit, 20));
    const p0 = result.audited.flatMap((p) => p.issues.filter((i) => i.startsWith("P0")));
    const p1 = result.audited.flatMap((p) => p.issues.filter((i) => i.startsWith("P1")));
    return {
      site: baseUrl,
      sampled: result.audited.length,
      totalInSitemap: result.totalInSitemap,
      criticalP0: p0.length,
      warningsP1: p1.length,
      pages: result.audited.map((p) => ({
        url: p.url,
        title: p.title,
        issues: p.issues,
        jsonLdTypes: p.jsonLdTypes,
      })),
    };
  }

  async onChatMessage(_onFinish: unknown, options?: OnChatMessageOptions) {
    const baseUrl = this.env.SITE_BASE_URL;
    const workersai = createWorkersAI({ binding: this.env.AI });

    const result = streamText({
      model: workersai("@cf/meta/llama-3.3-70b-instruct-fp8-fast", {
        sessionAffinity: this.sessionAffinity,
      }),
      system: `${seoGeoSystemPrompt(baseUrl)}

${getSchedulePrompt({ date: new Date() })}

Puoi schedulare audit settimanali con scheduleTask (cron: "0 8 * * 1" = lunedì 8:00 UTC).`,
      messages: pruneMessages({
        messages: await convertToModelMessages(this.messages),
        toolCalls: "before-last-2-messages",
      }),
      tools: {
        auditPage: tool({
          description:
            "Analizza meta tag, canonical, h1, JSON-LD e link interni di una pagina del sito",
          inputSchema: auditPageInput,
          execute: async ({ path }) => fetchAndAuditPage(baseUrl, path),
        }),

        fetchSitemap: tool({
          description: "Elenca tutti gli URL nella sitemap.xml del sito",
          inputSchema: fetchSitemapInput,
          execute: async () => {
            const urls = await fetchSitemapUrls(baseUrl);
            return { count: urls.length, urls: urls.slice(0, 50) };
          },
        }),

        batchAudit: tool({
          description: "Campiona N pagine dalla sitemap e le audita per problemi SEO",
          inputSchema: batchAuditInput,
          execute: async ({ limit }) => batchAudit(baseUrl, limit),
        }),

        scheduleTask: tool({
          description: "Schedula un audit SEO/GEO ricorrente o differito",
          inputSchema: scheduleSchema,
          execute: async ({ when, description }) => {
            if (when.type === "no-schedule") return "Input non valido";
            const input =
              when.type === "scheduled"
                ? when.date
                : when.type === "delayed"
                  ? when.delayInSeconds
                  : when.type === "cron"
                    ? when.cron
                    : null;
            if (!input) return "Tipo schedule non valido";
            try {
              this.schedule(input, "executeScheduledAudit", description, {
                idempotent: true,
              });
              return `Audit schedulato: "${description}" (${when.type})`;
            } catch (error) {
              return `Errore scheduling: ${error}`;
            }
          },
        }),

        getScheduledTasks: tool({
          description: "Elenca audit schedulati",
          inputSchema: z.object({}),
          execute: async () => {
            const tasks = this.getSchedules();
            return tasks.length > 0 ? tasks : "Nessun task schedulato";
          },
        }),

        cancelScheduledTask: tool({
          description: "Cancella un task schedulato per ID",
          inputSchema: z.object({
            taskId: z.string().describe("ID del task"),
          }),
          execute: async ({ taskId }) => {
            try {
              this.cancelSchedule(taskId);
              return `Task ${taskId} cancellato`;
            } catch (error) {
              return `Errore: ${error}`;
            }
          },
        }),
      },
      stopWhen: stepCountIs(6),
      abortSignal: options?.abortSignal,
    });

    return result.toUIMessageStreamResponse();
  }

  async executeScheduledAudit(description: string, _task: Schedule) {
    const report = await this.runSiteAudit(15);
    this.broadcast(
      JSON.stringify({
        type: "seo-geo-audit",
        description,
        timestamp: new Date().toISOString(),
        report,
      })
    );
  }
}

export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);

    if (url.pathname === "/audit") {
      const limit = Math.min(Number(url.searchParams.get("limit") ?? "10"), 20);
      const result = await batchAudit(env.SITE_BASE_URL, limit);
      const p0 = result.audited.flatMap((p) => p.issues.filter((i) => i.startsWith("P0")));
      const p1 = result.audited.flatMap((p) => p.issues.filter((i) => i.startsWith("P1")));
      return Response.json({
        site: env.SITE_BASE_URL,
        sampled: result.audited.length,
        totalInSitemap: result.totalInSitemap,
        criticalP0: p0.length,
        warningsP1: p1.length,
        pages: result.audited,
      });
    }

    if (url.pathname === "/health") {
      return Response.json({
        agent: "SeoGeoAgent",
        site: env.SITE_BASE_URL,
        status: "ok",
      });
    }

    return (
      (await routeAgentRequest(request, env)) ||
      new Response(
        JSON.stringify({
          agent: "the-verde-seo-geo-expert",
          endpoints: {
            health: "/health",
            audit: "/audit?limit=10",
            websocket: "/agents/SeoGeoAgent/{session-id}",
          },
          docs: "https://developers.cloudflare.com/agents/",
        }),
        { headers: { "content-type": "application/json" } }
      )
    );
  },
} satisfies ExportedHandler<Env>;
