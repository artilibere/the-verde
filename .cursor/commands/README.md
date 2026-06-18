# Comandi Cursor — the-verde.it

Riepilogo dei **slash command** definiti ad hoc per questo repository. Ogni comando vive in un file `.md` in questa cartella e istruisce l’agente Cursor su obiettivo, processo e output atteso.

**Root del progetto:** `/var/www/the-verde.it`

---

## Panoramica rapida

| Comando | Scopo | Parametri |
|---------|--------|-----------|
| [`/build`](#build) | Validazione JSON, test pytest, build statico | — |
| [`/localhost`](#localhost) | Build + Pagefind + server HTTP locale | **porta** (obbligatoria) |
| [`/deploy`](#deploy) | Build + Pagefind + pubblicazione Cloudflare Pages | — |
| [`/commit`](#commit) | Pre-commit: verifiche, messaggio, comando git | — |
| [`/review`](#review) | Code review (manuale, Bugbot o Security) | `bugbot`, `security` (opz.) |
| [`/improve`](#improve) | Miglioramenti mirati per area | area (opz.) |
| [`/seo-geo`](#seo-geo) | Audit e ottimizzazione SEO/GEO | argomento (opz.) |

---

## Flusso di lavoro tipico

```
Modifica contenuti/template
        ↓
     /build          ← verifica test + build
        ↓
  /localhost 8080    ← anteprima locale (opzionale)
        ↓
     /review          ← revisione prima del commit
        ↓
     /commit          ← pre-commit guidato
        ↓
     /deploy          ← pubblicazione su Cloudflare Pages
```

Per ottimizzazioni editoriali o tecniche senza un flusso rigido: `/improve` o `/seo-geo`.

---

## `/build`

**File:** `build.md`

**Obiettivo:** Validare i contenuti JSON, eseguire i test e generare il sito statico in `dist/`.

**Cosa fa l’agente:**
1. Installa dipendenze Python (`requirements.txt`)
2. Esegue `pytest tests/ -q`
3. Valida JSON con `build.py --validate-only`
4. Build completa: `python3 scripts/build.py --content content --out dist`
5. (Opzionale) indicizza Pagefind per la ricerca locale

**Output atteso:** esito test/build, conteggio pagine (~70 editoriali, ~95 `index.html`), eventuali errori con file e riga.

**Uso:**
```
/build
```

**Skill correlate:** `web-architect`

---

## `/localhost`

**File:** `localhost.md`

**Obiettivo:** Buildare il sito, indicizzare la ricerca e servirlo su un server HTTP locale.

**Parametro obbligatorio:** porta TCP (1–65535), es. `8080`, `1080`, `--port 5500`.

**Cosa fa l’agente:**
1. Attiva `.venv` e dipendenze (come `scripts/deploy.sh`)
2. Build in `dist/`
3. Pagefind → `dist/pagefind/`
4. Verifica che la porta sia libera
5. Avvia `python3 -m http.server PORT --directory dist --bind 127.0.0.1` in background

**Output atteso:** URL locale (`http://127.0.0.1:PORT/`), esito build/pagefind, istruzioni per fermare il server.

**Uso:**
```
/localhost 8080
/localhost 3000
/localhost --port 5500
```

**Note:** non emula l’edge Cloudflare; per solo build senza server usare `/build`.

**Skill correlate:** `web-architect`, `uiux-designer`

---

## `/deploy`

**File:** `deploy.md`

**Obiettivo:** Buildare e pubblicare su **Cloudflare Pages**.

**Target:**
| Ambiente | URL |
|----------|-----|
| Pages | https://the-verde.pages.dev |
| Produzione | https://the-verde.it |

**Cosa fa l’agente:**
1. (Consigliato) verifica build locale
2. Esegue `bash scripts/deploy.sh` — venv, build, Pagefind, `wrangler pages deploy`
3. Segnala URL deployment o errori di autenticazione Wrangler

**Alternativa:** GitHub Actions con secrets `CLOUDFLARE_API_TOKEN` e `CLOUDFLARE_ACCOUNT_ID`.

**Uso:**
```
/deploy
```

**Note:** richiede `npx wrangler` e credenziali Cloudflare; separato da `/commit`.

---

## `/commit`

**File:** `commit.md`

**Obiettivo:** Pre-commit guidato — verifiche, checklist e proposta di messaggio git.

**Cosa fa l’agente:**
1. Analizza `git status` e `git diff`
2. Se toccati `content/`, `templates/`, `assets/`, `scripts/`: build (+ `fix_encoding.py` se testi IT)
3. Controlli sicurezza (niente `.env`, token, segreti)
4. Coerenza editoriale (KB, slug senza accenti, voce The Verde)
5. Propone messaggio conventional in italiano e comando `git commit`

**Prefissi commit:**
| Prefisso | Uso |
|----------|-----|
| `feat:` | Nuova varietà, quiz, sezione |
| `fix:` | Bug build, encoding, JS |
| `docs:` | Skill, README, testi |
| `style:` | CSS, layout, UX |
| `perf:` | Asset pipeline, `_headers` |
| `chore:` | Tooling, dipendenze, config |

**Uso:**
```
/commit
```

**Non committare:** `dist/`, `.venv/`, `pagefind/`, `.wrangler/`

---

## `/review`

**File:** `review.md`

**Obiettivo:** Revisione del diff o dell’area indicata, adatta al sito statico the-verde.it.

**Modalità:**

| Opzione | Quando |
|---------|--------|
| **Checklist manuale** (default) | Diff locale, contenuti, build, UX |
| **Bugbot** | Analisi automatica bug/regressioni |
| **Security** | Segreti, XSS, path injection, dipendenze |

**Aree controllate (manuale):**
- Build e pipeline (`pytest`, schemi JSON, `blocks.py`, `asset_pipeline.py`)
- Contenuti editoriali (`content/`, KB, UTF-8, voce The Verde)
- Template e UX (schede varietà, catalogo, diario, accessibilità)
- JavaScript (`filters.js`, `diario.js`, `quiz.js`, …)
- Sicurezza e deploy (`_headers`, `_redirects`)

**Uso:**
```
/review
/review bugbot
/review security
```

**Skill correlate:** `the-verde-expert`, `uiux-designer`, `web-architect`

---

## `/improve`

**File:** `improve.md`

**Obiettivo:** Analizzare e applicare miglioramenti mirati — contenuti, build, template, asset, skill — senza refactor gratuiti.

**Aree del progetto:**

| Area | Percorso |
|------|----------|
| Contenuti | `content/` |
| KB canonica | `books/knowledge-base.json` |
| Template | `templates/` |
| Asset | `assets/css/`, `assets/js/` |
| Build | `scripts/build.py`, `scripts/site_builder/` |
| Encoding | `scripts/fix_encoding.py` |
| Skill | `.cursor/skills/`, `.cursor/rules/` |

**Varianti per focus:**

| Invocazione | Focus |
|-------------|--------|
| `/improve` | Area dedotta dal task o dal diff |
| `/improve encoding` | Accentuazione IT, slug preservati |
| `/improve ui/ux` | Template, CSS, JS interattivo |
| `/improve speed` | Asset pipeline, `_headers`, bundle |
| `/improve seo` | Sitemap, robots, OG, JSON-LD |
| `/improve geo` | hreflang, `areaServed`, citabilità |
| `/improve seo geo` | Canonical, schema, hub, catalogo |
| `/improve social` | Open Graph, Twitter, share |
| `/improve the-verde-expert` | Skill esperto tè |
| `/improve all` | Encoding + build + UX + regressioni |

**Uso:**
```
/improve
/improve ui/ux
/improve seo
/improve all
```

**Per bug/sicurezza:** preferire `/review`. Per deploy: `/deploy`.

---

## `/seo-geo`

**File:** `seo-geo.md`

**Obiettivo:** Audit e ottimizzazione per motori di ricerca e intelligenze generative (GEO).

**Skill:** `.cursor/skills/seo-geo-expert/SKILL.md`

**Argomenti:**

| Argomento | Focus |
|-----------|--------|
| `audit` | Checklist su pagina o sezione |
| `meta` | title, description, canonical, keywords |
| `schema` | JSON-LD, FAQPage, DefinedTerm, HowTo |
| `geo` | chunk citabili, llms.txt, E-E-A-T |
| `arch` | sitemap, robots, hub, internal linking |
| `live` | Agente Cloudflare `agents/seo-geo-expert/` |

**Cosa fa l’agente:**
1. Identifica ambito (pagina, sezione, sito)
2. Legge JSON sorgente + output build
3. Applica checklist SEO e GEO
4. Propone modifiche concrete
5. Esegue `pytest tests/test_enrichers_seo.py` se tocca il build

**Uso:**
```
/seo-geo
/seo-geo audit
/seo-geo schema
/seo-geo geo
```

**Collaborazione:** `web-architect`, `the-verde-expert`, `uiux-designer`

---

## File generati e ignorati

Questi path **non vanno committati** (sono output locale o artefatti di build):

- `dist/` — sito statico generato
- `.venv/` — ambiente Python locale
- `pagefind/` — cache indicizzazione (output finisce in `dist/pagefind/`)
- `.wrangler/` — cache Wrangler

---

## Aggiungere un nuovo comando

1. Crea un file `.md` in `.cursor/commands/` (il nome del file diventa il comando, es. `localhost.md` → `/localhost`).
2. Struttura consigliata:
   - **Objective** — cosa deve ottenere l’agente
   - **Process** — passi e comandi shell
   - **Checklist** — criteri di successo
   - **Expected output** — cosa riportare all’utente
   - **Usage** — esempi di invocazione
   - **Notes** — relazioni con altri comandi e skill
3. Aggiorna questo README con una riga in tabella e una sezione dedicata.

---

## Riferimenti

- Repository: https://github.com/artilibere/the-verde
- Sito: https://the-verde.it
- Deploy script: `scripts/deploy.sh`
- Build script: `scripts/build.py`
