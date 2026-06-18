import { z } from "zod";

export interface PageMeta {
  url: string;
  status: number;
  title: string | null;
  description: string | null;
  canonical: string | null;
  robots: string | null;
  ogTitle: string | null;
  ogDescription: string | null;
  ogImage: string | null;
  h1: string | null;
  internalLinkCount: number;
  jsonLdTypes: string[];
  issues: string[];
}

function extractMeta(html: string, attr: string, name: string): string | null {
  const re = new RegExp(
    `<meta[^>]+(?:name|property)=["']${name}["'][^>]+content=["']([^"']*)["']`,
    "i"
  );
  const m = html.match(re);
  if (m) return m[1];
  const re2 = new RegExp(
    `<meta[^>]+content=["']([^"']*)["'][^>]+(?:name|property)=["']${name}["']`,
    "i"
  );
  const m2 = html.match(re2);
  return m2 ? m2[1] : null;
}

function extractTitle(html: string): string | null {
  const m = html.match(/<title[^>]*>([^<]*)<\/title>/i);
  return m ? m[1].trim() : null;
}

function extractCanonical(html: string): string | null {
  const m = html.match(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']*)["']/i);
  if (m) return m[1];
  const m2 = html.match(/<link[^>]+href=["']([^"']*)["'][^>]+rel=["']canonical["']/i);
  return m2 ? m2[1] : null;
}

function extractH1(html: string): string | null {
  const m = html.match(/<h1[^>]*>([^<]*)<\/h1>/i);
  return m ? m[1].replace(/<[^>]+>/g, "").trim() : null;
}

function extractJsonLdTypes(html: string): string[] {
  const types = new Set<string>();
  const blocks = html.matchAll(
    /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi
  );
  for (const block of blocks) {
    try {
      const data = JSON.parse(block[1]);
      const graphs = data["@graph"] ? data["@graph"] : [data];
      for (const node of graphs) {
        const t = node["@type"];
        if (typeof t === "string") types.add(t);
        else if (Array.isArray(t)) t.forEach((x) => types.add(x));
      }
    } catch {
      /* skip malformed */
    }
  }
  return [...types];
}

function countInternalLinks(html: string, baseHost: string): number {
  const host = new URL(baseHost).host;
  let count = 0;
  const links = html.matchAll(/<a[^>]+href=["']([^"']*)["']/gi);
  for (const link of links) {
    const href = link[1];
    if (href.startsWith("/") || href.includes(host)) count++;
  }
  return count;
}

function buildIssues(meta: Omit<PageMeta, "issues">): string[] {
  const issues: string[] = [];
  if (!meta.title) issues.push("P0: title mancante");
  else if (meta.title.length > 60) issues.push(`P1: title lungo (${meta.title.length} char, max 60)`);
  if (!meta.description) issues.push("P0: meta description mancante");
  else if (meta.description.length > 160)
    issues.push(`P1: description lunga (${meta.description.length} char, max 160)`);
  if (!meta.canonical) issues.push("P1: canonical mancante");
  if (!meta.h1) issues.push("P0: h1 mancante");
  if (meta.jsonLdTypes.length === 0) issues.push("P1: nessun JSON-LD");
  if (meta.internalLinkCount < 2) issues.push("P2: pochi link interni (<2)");
  return issues;
}

export async function fetchAndAuditPage(
  baseUrl: string,
  path: string
): Promise<PageMeta> {
  const url = path.startsWith("http") ? path : `${baseUrl.replace(/\/$/, "")}${path.startsWith("/") ? path : `/${path}`}`;
  const res = await fetch(url, {
    headers: { "User-Agent": "TheVerde-SeoGeoAgent/1.0" },
  });
  const html = await res.text();

  const partial = {
    url,
    status: res.status,
    title: extractTitle(html),
    description: extractMeta(html, "name", "description"),
    canonical: extractCanonical(html),
    robots: extractMeta(html, "name", "robots"),
    ogTitle: extractMeta(html, "property", "og:title"),
    ogDescription: extractMeta(html, "property", "og:description"),
    ogImage: extractMeta(html, "property", "og:image"),
    h1: extractH1(html),
    internalLinkCount: countInternalLinks(html, baseUrl),
    jsonLdTypes: extractJsonLdTypes(html),
  };

  return { ...partial, issues: buildIssues(partial) };
}

export async function fetchSitemapUrls(baseUrl: string): Promise<string[]> {
  const res = await fetch(`${baseUrl.replace(/\/$/, "")}/sitemap.xml`);
  if (!res.ok) return [];
  const xml = await res.text();
  const urls: string[] = [];
  const matches = xml.matchAll(/<loc>([^<]+)<\/loc>/g);
  for (const m of matches) urls.push(m[1]);
  return urls;
}

export const auditPageInput = z.object({
  path: z.string().describe("Path relativo es. /varieta/sencha/ o URL assoluta"),
});

export const fetchSitemapInput = z.object({});

export const batchAuditInput = z.object({
  limit: z.number().min(1).max(20).default(5).describe("Max pagine da campionare"),
});

export async function batchAudit(
  baseUrl: string,
  limit: number
): Promise<{ audited: PageMeta[]; totalInSitemap: number }> {
  const urls = await fetchSitemapUrls(baseUrl);
  const sample = urls.slice(0, limit);
  const audited: PageMeta[] = [];
  for (const url of sample) {
    const path = url.replace(baseUrl.replace(/\/$/, ""), "") || "/";
    audited.push(await fetchAndAuditPage(baseUrl, path));
  }
  return { audited, totalInSitemap: urls.length };
}
