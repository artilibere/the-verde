# the-verde.it

Repo: https://github.com/artilibere/the-verde

Sito editoriale sul tè verde (*Camellia sinensis*) con knowledge base, percorsi gamificati e diario.

## Build locale

```bash
pip install -r requirements.txt
python scripts/generate_content.py   # rigenera content/ da script
python scripts/build.py --content content --out dist
```

## Struttura

- `content/` - Markdown sorgente (varietà, guide, impara, glossario, gioca)
- `books/knowledge-base.json` - KB canonica
- `templates/` - Jinja2
- `assets/` - CSS/JS vanilla
- `scripts/build.py` - generatore HTML statico
- `dist/` - output deploy

## Deploy

**Live:** https://the-verde.pages.dev (custom domain: https://the-verde.it quando DNS e SSL sono attivi)

### Deploy rapido (Wrangler, account artilibere)

```bash
bash scripts/deploy.sh
```

Account Cloudflare: `artilibere` (`9d6667327f2b656718e75db0808133f7`)

### GitHub Actions (opzionale)

Secrets in GitHub → Settings → Secrets:

- `CLOUDFLARE_API_TOKEN` — token con permesso Pages Edit
- `CLOUDFLARE_ACCOUNT_ID` — `9d6667327f2b656718e75db0808133f7`

Workflow: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)

## Configurazione fase 3

- `assets/js/supabase-config.js` - sync diario
- `assets/js/giscus.js` - community (impostare repo-id)
