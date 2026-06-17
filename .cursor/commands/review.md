# Code review (the-verde.it)

## Objective

Revisione del diff o dell'area indicata, adatta al sito statico **the-verde.it** (contenuti Markdown, build Python, template Jinja2, asset vanilla).

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
   - `scripts/build.py` completa senza errori?
   - `html_enrich.py`: sezioni varietà (prepara/approfondisci), FAQ, varietà simili non perse?
   - `parse_related_varieties`: path plain `(/varieta/slug/)` oltre a `href`?
   - `asset_pipeline.py`: hash asset, bundle CSS coerente?

2. **Contenuti editoriali** (`content/`)
   - Allineamento a `books/knowledge-base.json`?
   - Voce The Verde (sensoriale, non detox)?
   - UTF-8: accenti in prosa, slug senza accenti
   - `fix_encoding.py`: regole non troppo aggressive (es. «ristorante» ≠ «ristorantè»)?

3. **Template e UX** (`templates/`, `assets/`)
   - Schede varietà: brew card, mininav, path nav, box Italia
   - Catalogo: filtri URL-sync, reset filtri, `getAll` vs `get`
   - Diario: query `?varieta=` e campo form `name="varieta"` allineati
   - Level-toggle su hub Impara con Approfondimento
   - Accessibilità: breadcrumb, `aria-label`, focus visibile

4. **JavaScript** (`assets/js/`)
   - `filters.js`, `diario.js`, `quiz.js`, `paths.js`, `badges.js`
   - localStorage diario: chiavi coerenti (`varietà` vs `varietà`)
   - Nessun innerHTML non sanitizzato da input utente

5. **Sicurezza**
   - Nessun segreto hardcoded
   - `.env` fuori dal repo
   - `content_html | safe` solo su HTML generato dal build, non da input raw

6. **Deploy** (se toccati `_headers`, `deploy.sh`)
   - Cache asset hashed vs HTML
   - `_redirects` coerenti

## Checklist sintetica

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
- Skill di riferimento: `the-verde-expert`, `uiux-designer`.
