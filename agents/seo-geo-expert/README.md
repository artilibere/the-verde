# SEO/GEO Expert Agent — the-verde.it

Agente Cloudflare (Agents SDK) per audit SEO e ottimizzazione GEO del sito [the-verde.it](https://the-verde.it).

## Mansione

- **SEO**: meta tag, canonical, schema.org, sitemap, internal linking
- **GEO**: citabilità per LLM, chunk strutturati, E-E-A-T, FAQ/HowTo

Skill Cursor correlata: `.cursor/skills/seo-geo-expert/`

## Prerequisiti

- Node.js 18+
- Account Cloudflare con Workers AI abilitato
- `wrangler login`

## Setup

```bash
cd agents/seo-geo-expert
npm install
npm run dev
```

- Health check: `http://localhost:8787/health`
- WebSocket: `ws://localhost:8787/agents/SeoGeoAgent/default`

## Tool disponibili

| Tool | Funzione |
|------|----------|
| `auditPage` | Meta, h1, JSON-LD, link interni su una URL |
| `fetchSitemap` | Elenco URL da sitemap.xml |
| `batchAudit` | Campiona N pagine e riporta criticità P0/P1 |
| `scheduleTask` | Audit ricorrenti (cron) |
| `runSiteAudit` | RPC `@callable` per audit programmatico |

## Deploy

```bash
npm run deploy
```

Configura `SITE_BASE_URL` in `wrangler.jsonc` vars.

## Esempio WebSocket (chat)

```javascript
const ws = new WebSocket("wss://the-verde-seo-geo.<account>.workers.dev/agents/SeoGeoAgent/audit-session");

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: "message",
    parts: [{ type: "text", text: "Audita /varieta/gyokuro/ e suggerisci miglioramenti GEO" }],
  }));
};

ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

## Flusso consigliato

1. Agente audita il sito **live** (post-deploy)
2. Raccomandazioni applicate nel repo (`content/`, `site_builder/`)
3. Rebuild + redeploy
4. Nuovo audit per verifica

I fix strutturali restano nel repository statico; l'agente non modifica i contenuti direttamente.
