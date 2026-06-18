# Code review (the-verde.it)

## Objective

Revisione del diff o dell'area indicata, adatta al sito statico **the-verde.it** (contenuti JSON, build Python, template Jinja2, asset vanilla).

## Tipo di review

Chiedi all'utente quale review eseguire:

| Opzione | Quando usarla |
|---------|----------------|
| **Checklist manuale** | Default: diff locale, contenuti, build, UX |
| **Bugbot** | Analisi automatica bug/regressioni sul diff |
| **Security** | Segreti, XSS, path injection, dipendenze |

Per Bugbot o Security: lanciare il subagent dedicato sul diff (`branch changes` o `uncommitted changes`).

## Process — checklist manuale

1. **Build e pipeline**
   - `python -m pytest tests/ -q` verde?
   - `scripts/build.py` completa senza errori?
   - JSON valida contro `content/_schemas/`?
   - `site_builder/blocks.py`: zone varietà (prepara/approfondisci), FAQ semantiche?
   - `asset_pipeline.py`: hash asset, bundle CSS coerente?

2. **Contenuti editoriali** (`content/**/*.json`)
   - Allineamento a `books/knowledge-base.json`?
   - Voce The Verde (sensoriale, non detox)?
   - UTF-8: accenti in prosa, slug senza accenti
   - `meta.keywords`, `navigation` popolati dove utile

3. **Template e UX** (`templates/`, `assets/`)
   - Schede varietà: brew card, mininav, path nav, box Italia
   - Catalogo: filtri URL-sync, reset filtri
   - Diario: query `?varieta=` e campo form `name="varieta"` allineati
   - Level-toggle su hub Impara con `level_section` deep
   - Accessibilità: breadcrumb, `aria-label`, un solo h1, landmark `main`

4. **JavaScript** (`assets/js/`)
   - `filters.js`, `diario.js`, `quiz.js`, `paths.js`, `badges.js`
   - localStorage diario: chiavi coerenti
   - Nessun innerHTML non sanitizzato da input utente

5. **Sicurezza**
   - Nessun segreto hardcoded
   - `.env` fuori dal repo
   - `content_html | safe` solo su HTML generato dal build, non da input raw

6. **Deploy** (se toccati `_headers`, `deploy.sh`)
   - Cache asset hashed vs HTML
   - `_redirects` coerenti

## Checklist sintetica

- [ ] pytest OK
- [ ] Build OK
- [ ] Encoding IT corretto; slug URL intatti
- [ ] KB rispettata per contenuti editoriali
- [ ] UX varietà/catalogo/diario funzionante
- [ ] Nessun segreto nel codice
- [ ] Regressioni Bugbot note risolte o documentate

## Expected output

- Lista finding ordinata per gravità (blocker → nice-to-have)
- File + linea + suggerimento fix concreto
- Per Bugbot: tabella Severity | Location | Finding

## Usage

```
/review
/review bugbot
/review security
```

## Notes

- Non confondere con `/build` (solo verifica build) o `/commit` (pre-commit).
- `dist/` si rigenera — revisionare sorgenti in `content/`, `templates/`, `scripts/`.
- Skill di riferimento: `the-verde-expert`, `uiux-designer`, `web-architect`.
