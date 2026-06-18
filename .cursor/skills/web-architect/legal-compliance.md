# Privacy e Termini — monitoraggio e aggiornamento

Documento condiviso per **web-architect**, **seo-geo-expert**, **uiux-designer** e **the-verde-expert**. Non sostituisce consulenza legale.

## Dove vivono i contenuti

| Pagina | JSON | URL build | Pipeline |
|--------|------|-----------|----------|
| Privacy policy | `content/pagine/privacy.json` | `/privacy/` | `builder.build_legal()` |
| Termini di utilizzo | `content/pagine/termini.json` | `/termini/` | `builder.build_legal()` |

- Tipo documento: `page` (schema `content/_schemas/page.schema.json`)
- Template: `article.html`, `page_type=legal`
- Sitemap: priority `0.2`, `changefreq=yearly`
- Modello di riferimento editoriale: [liberating.it privacy/termini](/var/www/liberating.it/content/v1/pagine/)

## Titolare (da mantenere allineato)

- **Titolare:** Carlo Gandolfo
- **Email:** ciao@carlogandolfo.it
- **Sede:** Milano, Lombardia, Italia
- **Sito:** https://the-verde.it

Se cambiano titolare, email, sede o ragione sociale → aggiornare **entrambi** i JSON e la data in fondo.

## Trigger obbligatori di revisione

Aggiorna privacy e/o termini **prima del merge** quando introduci o modifichi:

| Area | File tipici | Cosa documentare |
|------|-------------|------------------|
| Dati locali | `assets/js/diario.js`, `paths.js`, `badges.js`, `poll.js` | Nuove chiavi `localStorage`, export, cancellazione |
| Community | `assets/js/giscus.js`, `templates/community.html` | Giscus, GitHub, cookie terze parti |
| Diario cloud | `assets/js/supabase-config.js`, `diario.js` | Supabase, auth, RLS, trasferimenti dati |
| Analytics / cookie | `templates/base.html`, nuovi script JS | GA, GTM, pixel, banner consenso |
| Ricerca | Pagefind, `/cerca/` | Indice locale vs query a terzi |
| Condivisione | `assets/js/share.js`, `includes/share.html` | Link esterni (WhatsApp, ecc.) |
| Form / newsletter | nuovi template o endpoint | Base giuridica, conservazione, opt-out |
| Hosting / CDN | deploy Cloudflare, `_headers` | Nuovi subprocessori |
| Contenuti salute | articoli `salute`, controversie | Allineamento disclaimer con `termini.json` §3 |
| Footer / link legale | `templates/base.html`, `componenti.md` | URL `/privacy/`, `/termini/` sempre raggiungibili |

## Checklist di monitoraggio

### A ogni modifica impattante (vedi tabella sopra)

- [ ] Privacy: sezione dati raccolti aggiornata (finalità, base giuridica, conservazione)
- [ ] Privacy: cookie/localStorage elencati con chiavi reali (`tv-diario`, `tv-badges`, …)
- [ ] Privacy: destinatari/subprocessori aggiornati
- [ ] Termini: funzioni interattive e limiti di responsabilità coerenti
- [ ] Termini: disclaimer salute allineato al tono the-verde-expert (no miracoli)
- [ ] `meta.description` e `meta.published` aggiornati in entrambi i JSON
- [ ] Data «ultimo aggiornamento» in fondo al body
- [ ] `pytest` + `python scripts/build.py` verdi
- [ ] Verifica HTML in `dist/privacy/` e `dist/termini/`

### Revisione periodica (almeno ogni 6 mesi, o a gennaio/giugno)

- [ ] Confronto con Linee guida Garante cookie e novità GDPR rilevanti
- [ ] Verifica che il sito deployato non tratti dati non dichiarati (audit script/asset)
- [ ] Link footer presenti su tutte le pagine (`templates/base.html`)
- [ ] Riferimento incrociato privacy ↔ termini ancora valido

## Ruoli per agente

| Agente | Competenza |
|--------|------------|
| **web-architect** | Owner tecnico: JSON, build, validazione schema, test, trigger da `assets/js` e pipeline |
| **seo-geo-expert** | Meta title/description, canonical, JSON-LD Article, sitemap, robots; audit post-deploy |
| **uiux-designer** | Layout legale (`tv-page--legal`), footer, assenza bottom-nav su legale, link accessibili |
| **the-verde-expert** | Coerenza disclaimer salute/wellness tra contenuti editoriali e termini §3 |

## Workflow di aggiornamento

1. Identifica il trigger (tabella sopra)
2. **web-architect** aggiorna `content/pagine/privacy.json` e/o `termini.json` (`body.blocks`: `heading`, `paragraph`, `list`, `link`)
3. **the-verde-expert** rivede paragrafi salute/responsabilità se toccati articoli controversi o salute
4. **seo-geo-expert** verifica `meta`, date, description ≤160 char
5. **uiux-designer** verifica resa mobile, footer, leggibilità 72ch
6. Build + test; opzionale audit worker `agents/seo-geo-expert/` post-deploy

## Cosa non fare

- Non inventare trattamenti dati assenti nel codice
- Non promettere in termini ciò che i contenuti editoriali smentiscono (e viceversa)
- Non rimuovere riferimento al Garante Privacy o diritti GDPR
- Non pubblicare analytics senza aggiornare privacy e (se serve) banner cookie
