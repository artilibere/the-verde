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
  seoSignals: SeoSignals;
  geoSignals: GeoSignals;
  issues: string[];
}

export interface SeoSignals {
  hasHreflang: boolean;
  hasOgImage: boolean;
  hasOgTitle: boolean;
  hasOgDescription: boolean;
  hasTwitterCard: boolean;
  canonicalMatchesUrl: boolean;
  hasBreadcrumbHtml: boolean;
  hasBreadcrumbList: boolean;
  hasKeywords: boolean;
  hasSitemapLink: boolean;
  hasRssLink: boolean;
  hasLlmsLink: boolean;
  robotsIndexable: boolean;
}

export interface GeoSignals {
  hasFaqHtml: boolean;
  hasQuizReference: boolean;
  hasLearningResource: boolean;
  hasHowTo: boolean;
  hasDefinedTerm: boolean;
  hasBrewProperties: boolean;
}

export interface MetaComparison {
  title: string | null;
  description: string | null;
  titleLength: number;
  descriptionLength: number;
  titleOk: boolean;
  descriptionOk: boolean;
  suggestions: string[];
}

export interface RobotsAudit {
  url: string;
  status: number;
  hasSitemap: boolean;
  disallowsDiarioNuova: boolean;
  mentionsLlmsTxt: boolean;
  issues: string[];
}

export interface SitemapSeoAudit {
  url: string;
  status: number;
  urlCount: number;
  urlsWithoutTrailingSlash: number;
  urlsWithHreflang: number;
  prioritySpread: { min: number; max: number };
  issues: string[];
}

export interface DuplicateMetaAudit {
  scanned: number;
  duplicateTitles: Array<{ title: string; urls: string[] }>;
  duplicateDescriptions: Array<{ description: string; urls: string[] }>;
  longTitles: Array<{ url: string; length: number; title: string }>;
  longDescriptions: Array<{ url: string; length: number }>;
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
  const m = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  return m ? m[1].replace(/<[^>]+>/g, "").trim() : null;
}

function hasLinkRel(html: string, rel: string): boolean {
  const re = new RegExp(`<link[^>]+rel=["'][^"']*\\b${rel}\\b[^"']*["']`, "i");
  return re.test(html);
}

function countHreflangLinks(html: string): number {
  return (html.match(/rel=["']alternate["'][^>]+hreflang=/gi) || []).length;
}

function normalizeUrl(url: string): string {
  try {
    const parsed = new URL(url);
    parsed.hash = "";
    let path = parsed.pathname;
    if (path !== "/" && !path.endsWith("/")) path += "/";
    parsed.pathname = path;
    return parsed.toString();
  } catch {
    return url.replace(/\/$/, "") + "/";
  }
}

function extractJsonLdBlocks(html: string): unknown[] {
  const blocks: unknown[] = [];
  const matches = html.matchAll(
    /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi
  );
  for (const block of matches) {
    try {
      blocks.push(JSON.parse(block[1]));
    } catch {
      /* skip malformed */
    }
  }
  return blocks;
}

function extractJsonLdTypes(html: string): string[] {
  const types = new Set<string>();
  for (const data of extractJsonLdBlocks(html)) {
    const node = data as Record<string, unknown>;
    const graphs = Array.isArray(node["@graph"]) ? node["@graph"] : [node];
    for (const item of graphs) {
      const t = (item as Record<string, unknown>)["@type"];
      if (typeof t === "string") types.add(t);
      else if (Array.isArray(t)) t.forEach((x) => types.add(String(x)));
    }
  }
  return [...types];
}

function jsonLdHasAdditionalProperty(html: string, name: string): boolean {
  for (const data of extractJsonLdBlocks(html)) {
    const node = data as Record<string, unknown>;
    const graphs = Array.isArray(node["@graph"]) ? node["@graph"] : [node];
    for (const item of graphs) {
      const props = (item as Record<string, unknown>).additionalProperty;
      if (!Array.isArray(props)) continue;
      for (const prop of props) {
        const propName = (prop as Record<string, unknown>).name;
        if (propName === name) return true;
      }
    }
  }
  return false;
}

function detectSeoSignals(
  html: string,
  jsonLdTypes: string[],
  canonical: string | null,
  pageUrl: string,
  robots: string | null
): SeoSignals {
  const hreflangCount = countHreflangLinks(html);
  return {
    hasHreflang: hreflangCount >= 2,
    hasOgImage: Boolean(extractMeta(html, "property", "og:image")),
    hasOgTitle: Boolean(extractMeta(html, "property", "og:title")),
    hasOgDescription: Boolean(extractMeta(html, "property", "og:description")),
    hasTwitterCard: Boolean(extractMeta(html, "name", "twitter:card")),
    canonicalMatchesUrl: Boolean(canonical && normalizeUrl(canonical) === normalizeUrl(pageUrl)),
    hasBreadcrumbHtml: html.includes("tv-breadcrumb") || html.includes('aria-label="Breadcrumb"'),
    hasBreadcrumbList: jsonLdTypes.includes("BreadcrumbList"),
    hasKeywords: Boolean(extractMeta(html, "name", "keywords")),
    hasSitemapLink: hasLinkRel(html, "sitemap"),
    hasRssLink: hasLinkRel(html, "alternate") && html.includes("application/rss+xml"),
    hasLlmsLink: html.includes('type="text/plain"') && html.includes("llms.txt"),
    robotsIndexable: !robots || !/noindex/i.test(robots),
  };
}

function detectGeoSignals(html: string, jsonLdTypes: string[]): GeoSignals {
  return {
    hasFaqHtml: /class=["'][^"']*tv-faq[^"']*["']/i.test(html) || /<details[^>]+summary/i.test(html),
    hasQuizReference: html.includes("tv-quiz-reference") || html.includes("Risposte di riferimento"),
    hasLearningResource: jsonLdTypes.includes("LearningResource"),
    hasHowTo: jsonLdTypes.includes("HowTo"),
    hasDefinedTerm: jsonLdTypes.includes("DefinedTerm"),
    hasBrewProperties:
      jsonLdHasAdditionalProperty(html, "Temperatura acqua") ||
      jsonLdHasAdditionalProperty(html, "Dosaggio"),
  };
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

function pagePath(url: string): string {
  try {
    return new URL(url).pathname;
  } catch {
    return url;
  }
}

function isHomePath(path: string): boolean {
  return path === "/" || path === "";
}

function isNoindexPath(path: string): boolean {
  return path.startsWith("/cerca") || path.startsWith("/diario/nuova");
}

function buildIssues(meta: Omit<PageMeta, "issues">): string[] {
  const issues: string[] = [];
  const path = pagePath(meta.url);

  if (!meta.title) issues.push("P0 SEO: title mancante");
  else if (meta.title.length > 60)
    issues.push(`P1 SEO: title lungo (${meta.title.length} char, max 60)`);
  else if (meta.title.length < 15 && !isHomePath(path))
    issues.push(`P2 SEO: title corto (${meta.title.length} char)`);

  if (!meta.description) issues.push("P0 SEO: meta description mancante");
  else if (meta.description.length > 160)
    issues.push(`P1 SEO: description lunga (${meta.description.length} char, max 160)`);
  else if (meta.description.length < 50)
    issues.push(`P2 SEO: description corta (${meta.description.length} char)`);

  if (!meta.canonical) issues.push("P1 SEO: canonical mancante");
  else if (!meta.seoSignals.canonicalMatchesUrl)
    issues.push("P1 SEO: canonical non coincide con URL pagina");
  else if (!meta.canonical.endsWith("/"))
    issues.push("P1 SEO: canonical senza trailing slash");

  if (!meta.h1) issues.push("P0 SEO: h1 mancante");
  if (meta.jsonLdTypes.length === 0) issues.push("P1 SEO: nessun JSON-LD");
  if (meta.internalLinkCount < 2 && !isHomePath(path))
    issues.push("P2 SEO: pochi link interni (<2)");

  if (!meta.seoSignals.hasOgImage) issues.push("P1 SEO: og:image mancante");
  if (!meta.seoSignals.hasOgTitle) issues.push("P1 SEO: og:title mancante");
  if (!meta.seoSignals.hasOgDescription) issues.push("P1 SEO: og:description mancante");
  if (!meta.seoSignals.hasTwitterCard) issues.push("P2 SEO: twitter:card mancante");
  if (!meta.seoSignals.hasHreflang) issues.push("P1 SEO: hreflang incompleto (attesi it + x-default)");
  if (!meta.seoSignals.hasSitemapLink) issues.push("P2 SEO: link rel=sitemap assente in head");
  if (!meta.seoSignals.hasRssLink) issues.push("P2 SEO: feed RSS non linkato in head");

  if (isNoindexPath(path)) {
    if (meta.seoSignals.robotsIndexable)
      issues.push("P0 SEO: pagina privata indicizzabile (atteso noindex)");
  } else if (!meta.seoSignals.robotsIndexable) {
    issues.push("P1 SEO: pagina pubblica con noindex");
  }

  if (isHomePath(path)) {
    if (!meta.jsonLdTypes.includes("WebSite"))
      issues.push("P1 SEO: home senza WebSite JSON-LD");
    if (!meta.jsonLdTypes.includes("Organization"))
      issues.push("P1 SEO: home senza Organization JSON-LD");
  } else if (!isNoindexPath(path)) {
    if (!meta.seoSignals.hasBreadcrumbList)
      issues.push("P1 SEO: BreadcrumbList JSON-LD assente");
    if (!meta.seoSignals.hasBreadcrumbHtml)
      issues.push("P2 SEO: breadcrumb HTML assente");
  }

  if (path.startsWith("/gioca/quiz/")) {
    if (!meta.jsonLdTypes.includes("FAQPage"))
      issues.push("P1 GEO: quiz senza FAQPage JSON-LD");
    if (!meta.geoSignals.hasQuizReference)
      issues.push("P1 GEO: quiz senza sezione HTML crawlable (Risposte di riferimento)");
  }
  if (path.startsWith("/gioca/percorsi/") && path !== "/gioca/percorsi/") {
    if (!meta.geoSignals.hasLearningResource)
      issues.push("P1 GEO: percorso senza LearningResource JSON-LD");
  }
  if (path.startsWith("/varieta/") && path !== "/varieta/") {
    if (!meta.geoSignals.hasHowTo) issues.push("P2 GEO: varietà senza HowTo");
    if (!meta.geoSignals.hasBrewProperties)
      issues.push("P2 GEO: varietà senza additionalProperty infusione");
  }
  if (path.startsWith("/glossario/") && path !== "/glossario/") {
    if (!meta.geoSignals.hasDefinedTerm)
      issues.push("P1 GEO: glossario senza DefinedTerm JSON-LD");
  }

  return issues;
}

export function compareMeta(title: string | null, description: string | null): MetaComparison {
  const titleLength = title?.length ?? 0;
  const descriptionLength = description?.length ?? 0;
  const suggestions: string[] = [];
  if (!title) suggestions.push("Aggiungi un title unico con keyword principale");
  else if (titleLength > 60)
    suggestions.push(`Accorcia il title di ${titleLength - 60} caratteri (max 60 con brand)`);
  else if (titleLength < 20)
    suggestions.push("Arricchisci il title con varietà/tema e intento italiano");

  if (!description) suggestions.push("Aggiungi meta description con risposta diretta e CTA implicita");
  else if (descriptionLength > 160)
    suggestions.push(`Accorcia la description di ${descriptionLength - 160} caratteri`);
  else if (descriptionLength < 70)
    suggestions.push("Espandi la description fino a 120–155 caratteri");

  return {
    title,
    description,
    titleLength,
    descriptionLength,
    titleOk: Boolean(title && titleLength <= 60 && titleLength >= 15),
    descriptionOk: Boolean(description && descriptionLength <= 160 && descriptionLength >= 50),
    suggestions,
  };
}

export interface LlmsTxtAudit {
  url: string;
  status: number;
  hasTitle: boolean;
  hasSummary: boolean;
  hasCamelliaSinensis: boolean;
  hasSitemap: boolean;
  hasFeed: boolean;
  sectionCount: number;
  inventorySections: string[];
  issues: string[];
}

function countMarkdownSections(text: string): number {
  return (text.match(/^## /gm) || []).length;
}

function detectInventorySections(text: string): string[] {
  const expected = [
    "Varietà",
    "Glossario",
    "Impara",
    "Controversie",
    "Guide",
    "In Italia",
    "Gioca — percorsi guidati",
    "Gioca — quiz",
    "Entità chiave",
    "Domande tipiche",
  ];
  return expected.filter((s) => text.includes(`## ${s}`) || text.includes(s));
}

export function auditLlmsTxtContent(text: string, baseUrl: string): Omit<LlmsTxtAudit, "url" | "status"> {
  const hasTitle = /^# .+/m.test(text);
  const hasSummary = /^> .+/m.test(text);
  const hasCamelliaSinensis = /Camellia sinensis/i.test(text);
  const hasSitemap = text.includes("/sitemap.xml");
  const hasFeed = text.includes("/feed.xml");
  const sectionCount = countMarkdownSections(text);
  const inventorySections = detectInventorySections(text);
  const issues: string[] = [];
  if (!hasTitle) issues.push("P0: titolo H1 mancante");
  if (!hasSummary) issues.push("P1: blockquote riassuntivo mancante");
  if (!hasCamelliaSinensis) issues.push("P0: entità Camellia sinensis assente");
  if (!hasSitemap) issues.push("P1: link sitemap assente");
  if (!hasFeed) issues.push("P2: link feed RSS assente");
  if (sectionCount < 8) issues.push(`P1: poche sezioni H2 (${sectionCount}, attese ≥8)`);
  if (!text.includes("Domande tipiche")) issues.push("P1: mappa intenti/domande tipiche assente");
  if (!text.includes("Entità chiave")) issues.push("P1 GEO: sezione disambiguazione entità assente");
  if (!text.includes("Gioca — percorsi")) issues.push("P2 GEO: inventario percorsi Gioca assente");
  if (!text.includes("Gioca — quiz")) issues.push("P2 GEO: inventario quiz Gioca assente");
  if (!text.includes(baseUrl.replace(/\/$/, ""))) issues.push("P1: URL assoluti base_url assenti");
  return {
    hasTitle,
    hasSummary,
    hasCamelliaSinensis,
    hasSitemap,
    hasFeed,
    sectionCount,
    inventorySections,
    issues,
  };
}

export async function fetchAndAuditLlmsTxt(baseUrl: string): Promise<LlmsTxtAudit> {
  const url = `${baseUrl.replace(/\/$/, "")}/llms.txt`;
  const res = await fetch(url, {
    headers: { "User-Agent": "TheVerde-SeoGeoAgent/1.0" },
  });
  const text = await res.text();
  return { url, status: res.status, ...auditLlmsTxtContent(text, baseUrl) };
}

export function auditRobotsTxtContent(text: string, baseUrl: string): Omit<RobotsAudit, "url" | "status"> {
  const issues: string[] = [];
  const hasSitemap = /Sitemap:\s*https?:\/\//i.test(text);
  const disallowsDiarioNuova = /Disallow:\s*\/diario\/nuova\/?/i.test(text);
  const mentionsLlmsTxt = /llms\.txt/i.test(text);
  if (!hasSitemap) issues.push("P0 SEO: Sitemap assoluta mancante in robots.txt");
  if (!disallowsDiarioNuova) issues.push("P1 SEO: Disallow /diario/nuova/ mancante");
  if (!text.includes("User-agent:")) issues.push("P1 SEO: User-agent mancante");
  if (!mentionsLlmsTxt) issues.push("P2 GEO: commento llms.txt assente in robots.txt");
  if (!text.includes(baseUrl.replace(/\/$/, ""))) issues.push("P2 SEO: base_url non presente in Sitemap");
  return { hasSitemap, disallowsDiarioNuova, mentionsLlmsTxt, issues };
}

export async function fetchAndAuditRobotsTxt(baseUrl: string): Promise<RobotsAudit> {
  const url = `${baseUrl.replace(/\/$/, "")}/robots.txt`;
  const res = await fetch(url, { headers: { "User-Agent": "TheVerde-SeoGeoAgent/1.0" } });
  const text = await res.text();
  return { url, status: res.status, ...auditRobotsTxtContent(text, baseUrl) };
}

export function auditSitemapXmlContent(xml: string): Omit<SitemapSeoAudit, "url" | "status"> {
  const locs = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
  const priorities = [...xml.matchAll(/<priority>([^<]+)<\/priority>/g)].map((m) => Number(m[1]));
  const hreflangCount = (xml.match(/hreflang=/g) || []).length;
  const urlsWithoutTrailingSlash = locs.filter((loc) => {
    try {
      const path = new URL(loc).pathname;
      return path !== "/" && !path.endsWith("/");
    } catch {
      return !loc.endsWith("/");
    }
  }).length;

  const issues: string[] = [];
  if (locs.length === 0) issues.push("P0 SEO: sitemap vuota");
  if (urlsWithoutTrailingSlash > 0)
    issues.push(`P1 SEO: ${urlsWithoutTrailingSlash} URL senza trailing slash`);
  if (hreflangCount < locs.length * 2)
    issues.push("P1 SEO: hreflang xhtml:link incompleto nella sitemap");
  if (priorities.length > 0 && priorities.length < locs.length)
    issues.push("P2 SEO: priority mancante su alcune URL");

  const min = priorities.length ? Math.min(...priorities) : 0;
  const max = priorities.length ? Math.max(...priorities) : 0;

  return {
    urlCount: locs.length,
    urlsWithoutTrailingSlash,
    urlsWithHreflang: hreflangCount,
    prioritySpread: { min, max },
    issues,
  };
}

export async function fetchAndAuditSitemap(baseUrl: string): Promise<SitemapSeoAudit> {
  const url = `${baseUrl.replace(/\/$/, "")}/sitemap.xml`;
  const res = await fetch(url, { headers: { "User-Agent": "TheVerde-SeoGeoAgent/1.0" } });
  const xml = await res.text();
  return { url, status: res.status, ...auditSitemapXmlContent(xml) };
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
  const jsonLdTypes = extractJsonLdTypes(html);
  const canonical = extractCanonical(html);
  const robots = extractMeta(html, "name", "robots");

  const partial = {
    url,
    status: res.status,
    title: extractTitle(html),
    description: extractMeta(html, "name", "description"),
    canonical,
    robots,
    ogTitle: extractMeta(html, "property", "og:title"),
    ogDescription: extractMeta(html, "property", "og:description"),
    ogImage: extractMeta(html, "property", "og:image"),
    h1: extractH1(html),
    internalLinkCount: countInternalLinks(html, baseUrl),
    jsonLdTypes,
    seoSignals: detectSeoSignals(html, jsonLdTypes, canonical, url, robots),
    geoSignals: detectGeoSignals(html, jsonLdTypes),
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

export async function auditDuplicateMeta(
  baseUrl: string,
  limit = 30
): Promise<DuplicateMetaAudit> {
  const urls = await fetchSitemapUrls(baseUrl);
  const sample = urls.slice(0, Math.min(limit, urls.length));
  const titleMap = new Map<string, string[]>();
  const descMap = new Map<string, string[]>();
  const longTitles: DuplicateMetaAudit["longTitles"] = [];
  const longDescriptions: DuplicateMetaAudit["longDescriptions"] = [];

  for (const pageUrl of sample) {
    const res = await fetch(pageUrl, { headers: { "User-Agent": "TheVerde-SeoGeoAgent/1.0" } });
    const html = await res.text();
    const title = extractTitle(html);
    const description = extractMeta(html, "name", "description");
    if (title) {
      const list = titleMap.get(title) ?? [];
      list.push(pageUrl);
      titleMap.set(title, list);
      if (title.length > 60) longTitles.push({ url: pageUrl, length: title.length, title });
    }
    if (description) {
      const list = descMap.get(description) ?? [];
      list.push(pageUrl);
      descMap.set(description, list);
      if (description.length > 160) longDescriptions.push({ url: pageUrl, length: description.length });
    }
  }

  const duplicateTitles = [...titleMap.entries()]
    .filter(([, pages]) => pages.length > 1)
    .map(([title, pages]) => ({ title, urls: pages }));
  const duplicateDescriptions = [...descMap.entries()]
    .filter(([, pages]) => pages.length > 1)
    .map(([description, pages]) => ({ description, urls: pages }));

  const issues: string[] = [];
  if (duplicateTitles.length) issues.push(`P0 SEO: ${duplicateTitles.length} title duplicati nel campione`);
  if (duplicateDescriptions.length)
    issues.push(`P1 SEO: ${duplicateDescriptions.length} description duplicate nel campione`);
  if (longTitles.length) issues.push(`P1 SEO: ${longTitles.length} title oltre 60 char`);
  if (longDescriptions.length) issues.push(`P1 SEO: ${longDescriptions.length} description oltre 160 char`);

  return {
    scanned: sample.length,
    duplicateTitles,
    duplicateDescriptions,
    longTitles,
    longDescriptions,
    issues,
  };
}

export const auditPageInput = z.object({
  path: z.string().describe("Path relativo es. /varieta/sencha/ o URL assoluta"),
});

export const fetchSitemapInput = z.object({});

export const batchAuditInput = z.object({
  limit: z.number().min(1).max(20).default(5).describe("Max pagine da campionare"),
});

export const duplicateMetaInput = z.object({
  limit: z.number().min(5).max(50).default(30).describe("Quante URL sitemap analizzare"),
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
