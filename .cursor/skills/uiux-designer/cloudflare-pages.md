# Cloudflare Pages — the-verde.it site

Configurazione del repo GitHub separato per il frontend statico. Il repo content (`the-verde.it`) resta la sorgente Markdown; il repo site compila e deploya.

---

## Struttura repo `the-verde-it-site`

```
the-verde-it-site/
??? .github/
?   ??? workflows/
?       ??? deploy.yml
??? scripts/
?   ??? build.py                 # MD ? HTML + index.json
??? templates/                   # Jinja2 (opzionale)
?   ??? base.html
?   ??? variety.html
?   ??? catalog.html
?   ??? article.html
?   ??? hub.html
??? assets/
?   ??? css/
?   ?   ??? tokens.css           # da design-system.md
?   ?   ??? base.css
?   ?   ??? components.css
?   ??? js/
?   ?   ??? nav.js
?   ?   ??? filters.js
?   ?   ??? scroll-spy.js
?   ??? fonts/                   # Source Serif 4 self-hosted (opzionale)
??? content/                     # vuoto in repo; popolato in CI
??? dist/                        # output build (gitignored)
??? _headers
??? _redirects
??? .gitignore
??? requirements.txt             # se build Python
??? README.md
```

**Output deploy:** directory `dist/` (build command popola questa cartella).

---

## Sync content ? site

### Default: GitHub Actions checkout (consigliato)

Il workflow scarica il repo content al build. Nessun submodule da mantenere.

```yaml
- name: Checkout content repo
  uses: actions/checkout@v4
  with:
    repository: YOUR_ORG/the-verde.it
    path: content-src
    token: ${{ secrets.GH_PAT }}
```

Poi: `python scripts/build.py --content content-src/content --out dist`

### Alternativa: git submodule

```bash
git submodule add https://github.com/YOUR_ORG/the-verde.it.git content
git submodule update --init --recursive
```

Build: `--content content/content`

### Alternativa: export manuale

```bash
rsync -av /path/to/the-verde.it/content/ ./content/
python scripts/build.py --content content --out dist
```

---

## Cloudflare Pages (dashboard)

| Impostazione | Valore |
|--------------|--------|
| Production branch | `main` |
| Build command | `pip install -r requirements.txt && python scripts/build.py --content content-src/content --out dist` |
| Build output directory | `dist` |
| Root directory | `/` |

Variabili ambiente (se repo content privato): `GH_PAT`.

---

## GitHub Actions workflow

`.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  deployments: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout site repo
        uses: actions/checkout@v4

      - name: Checkout content repo
        uses: actions/checkout@v4
        with:
          repository: YOUR_ORG/the-verde.it
          path: content-src
          token: ${{ secrets.GH_PAT }}

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Build
        run: |
          pip install -r requirements.txt
          python scripts/build.py --content content-src/content --out dist

      - name: Publish to Cloudflare Pages
        uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: the-verde-it
          directory: dist
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

**Secrets richiesti:**

- `CLOUDFLARE_API_TOKEN` — token con permesso Cloudflare Pages Edit
- `CLOUDFLARE_ACCOUNT_ID` — ID account Cloudflare
- `GH_PAT` — solo se repo content privato

---

## `_headers`

File in root del output `dist/_headers`:

```
# Cache asset statici (1 anno)
/assets/*
  Cache-Control: public, max-age=31536000, immutable

# HTML: sempre revalidare
/*.html
  Cache-Control: public, max-age=0, must-revalidate

/
  Cache-Control: public, max-age=0, must-revalidate

# Security
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
```

CSP base (opzionale, aggiungere quando stabile):

```
/*
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'
```

---

## `_redirects`

Sintassi Cloudflare Pages (Netlify-compatible). Aggiornare man mano che cresce il sito.

```
# Trailing slash coerente
/varietà/:slug  /varietà/:slug/  301
/guide/:slug  /guide/:slug/  301
/origine/:slug  /origine/:slug/  301
/stagioni/:slug  /stagioni/:slug/  301
/per-momento/:slug  /per-momento/:slug/  301

# Alias senza accento (se necessario per compatibilità)
/varieta/:slug  /varietà/:slug/  301
/varieta  /varietà/  301
```

**Processo aggiornamento redirect:**

1. Per ogni URL cambiato, aggiungi riga `vecchio  nuovo  301`
2. Testa in preview CF prima di merge su `main`
3. Trailing slash ovunque (`/varietà/sencha/`)

---

## Preview e validazione

1. **Locale:** `python scripts/build.py ... && npx serve dist` oppure `python -m http.server -d dist`
2. **CF Preview:** ogni PR genera URL preview (se abilitato su project Pages)
3. **Checklist pre-deploy:**
   - [ ] Schede in `dist/varietà/{slug}/index.html`
   - [ ] Catalogo `dist/varietà/index.html`
   - [ ] Hub origine e stagione
   - [ ] Articoli in `dist/guide/{slug}/index.html`
   - [ ] Home, privacy, termini
   - [ ] `_redirects` copiato in dist
   - [ ] Link interni con trailing slash
   - [ ] Contrasto WCAG su token Almost Acqua (verificare in browser)
   - [ ] Nessun copy detox negli HTML generati

---

## Dominio custom

In Cloudflare Pages ? Custom domains ? `the-verde.it` + `www.the-verde.it`

- DNS: CNAME `the-verde.it` ? `the-verde-it.pages.dev`
- Redirect `www` ? apex (o viceversa, coerente con canonical in content)

---

## README minimo repo site

Il `README.md` del repo site deve documentare:

1. Prerequisiti (Python 3.12, pip)
2. Build locale con path al content repo
3. Struttura `dist/`
4. Come aggiornare `_redirects`
5. Link alla skill uiux-designer nel repo content: `.cursor/skills/uiux-designer/SKILL.md`

---

## Anti-pattern deploy

- Deployare Markdown grezzo senza build (CF Pages non renderizza MD nativamente)
- Dimenticare di copiare `_headers` e `_redirects` in `dist/`
- Build output su root repo senza `dist/` (confonde asset e sorgenti)
- Force push su `main` per fix deploy — usare nuovo commit
- SPA fallback `/* /index.html 200` — **non usare** (sito multi-pagina statico)
- Google Fonts esterni obbligatori — preferire system stack + self-host serif
