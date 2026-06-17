# the-verde.it

Repo: https://github.com/artilibere/the-verde

Sito editoriale sul te verde (*Camellia sinensis*) con knowledge base, percorsi gamificati e diario.

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

GitHub Actions in `.github/workflows/deploy.yml` (Cloudflare Pages + Pagefind).

## Configurazione fase 3

- `assets/js/supabase-config.js` - sync diario
- `assets/js/giscus.js` - community (impostare repo-id)
