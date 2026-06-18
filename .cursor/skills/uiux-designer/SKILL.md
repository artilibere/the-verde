---
name: uiux-designer
description: >-
  Progetta interfaccia web-app mobile-first per the-verde.it (HTML+JS+CSS):
  card feed a scorrimento, navigazione iconica, d3.js per dati analitici,
  pipeline JSON→HTML con template Jinja2 uniformi, schema.org, deploy
  Cloudflare Pages, pagine legali e link footer. Usare per frontend, wireframe,
  CSS, schede varietà, catalogo, build script o repo site separato.
---

# UI/UX Designer — the-verde.it

Progetta l'esperienza **web-app mobile-first** per **The Verde**: cultura del tè verde (*Camellia sinensis*) con radicamento italiano. Paradigma: **feed di schede** a scorrimento, non wiki a colonna lunga.

Il frontend vive in un **repo GitHub separato** (es. `the-verde-it-site`). Build: MD → `PageDocument` JSON → template Jinja2 → HTML statico.

Documentazione (progressive disclosure):

| File | Contenuto |
|------|-----------|
| [app-shell.md](app-shell.md) | Web-app shell, bottom nav, card feed, mobile-first 390px |
| [icone.md](icone.md) | Sprite SVG, navigazione iconica, accessibilità |
| [charts-d3.md](charts-d3.md) | Tabelle, chart d3.js, matrice decisione |
| [rendering-json-html.md](rendering-json-html.md) | Pipeline JSON, template, prosa uniforme, schema.org |
| [personas.md](personas.md) | 4 personas UX, matrice componenti |
| [design-system.md](design-system.md) | Token Almost Acqua, mobile, prosa, chart |
| [componenti.md](componenti.md) | Libreria `tv-*` |
| [template-pagine.md](template-pagine.md) | Wireframe per tipo pagina |
| [mapping-contenuti.md](mapping-contenuti.md) | Indice MD → PageDocument |
| [cloudflare-pages.md](cloudflare-pages.md) | Repo site, deploy |

## Prima di progettare

1. [the-verde-expert/SKILL.md](../the-verde-expert/SKILL.md) — tono, formati, cosa evitare
2. [cultura-italiana.md](../the-verde-expert/cultura-italiana.md) — ponti Italia
3. [personas.md](personas.md) — Elena (prioritaria), Luca, Giulia, Marco
4. [app-shell.md](app-shell.md) + [rendering-json-html.md](rendering-json-html.md)

## Principi UX (priorità assolute)

| Principio | Implicazione UI |
|-----------|-----------------|
| Web-app, non wiki | Card feed; bottom nav; niente pareti di testo |
| Mobile-first | Design 390px prima; desktop = colonna app 480px |
| Icone guidano | Ogni sezione/tab/azione chiave: simbolo + label |
| Schede scorrevoli | Ogni blocco = `tv-card`; scroll verticale tra schede |
| Dati leggibili | Tabella default; chart d3 solo se [charts-d3.md](charts-d3.md) lo consiglia |
| Colonne leggibili | Griglie max 1 col (`sm`) o 2 col (`md`+); mai 3 colonne con testo |
| Rendering uniforme | Solo template Jinja2 + PageDocument; prosa e schema.org unici |
| Rispetto origini | Chip paese/tradizione; no iconografia zen kitsch |
| Radicamento italiano | Card `italy` obbligatoria in scheda varietà |
| No wellness clickbait | No badge detox; metriche sobrie |
| Specialty educativo | Metriche preparazione in prima card tecnica |
| Distinguere tè/tisane | Label e filtri su *Camellia sinensis* |

### Tre obiettivi operativi

1. **Scorrimento a schede** — feed verticale; una idea per card; teaser max 3 righe
2. **Navigazione iconica** — bottom nav + icone header card; thumb zone rispettata
3. **Dati chiari** — tabella prima del chart; metric-row per singola varietà; formato scelto con matrice charts

### Test persona

> *Elena capisce in 10 secondi? Luca non si sente venduto un detox? Giulia trova i dati tecnici? Navigazione possibile con una mano?*

## Tipi di pagina

| Tipo | Template Jinja2 | Wireframe |
|------|-----------------|-----------|
| Home | `pages/home.html` | [template-pagine.md § Home](template-pagine.md#home) |
| Catalogo | `pages/catalog.html` | [template-pagine.md § Catalogo](template-pagine.md#catalogo-varietà) |
| Scheda varietà | `pages/variety.html` | [template-pagine.md § Scheda](template-pagine.md#scheda-varietà) |
| Articolo | `pages/article.html` | [template-pagine.md § Articolo](template-pagine.md#articolo-editoriale) |
| Hub | `pages/hub.html` | [template-pagine.md § Hub](template-pagine.md#hub-origine) |
| Legale | `pages/legal.html` | [template-pagine.md § Legale](template-pagine.md#pagina-legale) |

## Privacy e Termini (UI e accessibilità)

- Link **Privacy** e **Termini** obbligatori nel footer (`templates/base.html`) su ogni pagina
- `page_type=legal`: niente bottom-nav; layout minimale, prosa leggibile (~72ch)
- Nuove funzioni che raccolgono dati (form, script terzi, banner cookie) → segnala a **web-architect** per aggiornare i JSON legali ([legal-compliance.md](../web-architect/legal-compliance.md))
- Non aggiungere analytics o widget di tracciamento senza coordinamento privacy

## Modello scheda varietà (card feed)

Ordine card fisso in `variety.html` (vedi [rendering-json-html.md](rendering-json-html.md)):

```
brief → brew → sensory → gear → steps → errors → italy → pairings → faq → related
```

Percorso guidato: bancha → sencha → gyokuro → matcha (`PATH_ORDER` in mapping-contenuti.md).

## Workflow operativo

```
Task Progress:
- [ ] 1. Leggere the-verde-expert + personas + app-shell
- [ ] 2. Identificare tipo pagina e ordine card
- [ ] 3. Definire PageDocument JSON (mapping-contenuti.md)
- [ ] 4. Scegliere formato dati (charts-d3.md): card / tabella / chart
- [ ] 5. Applicare design system + componenti tv-*
- [ ] 6. Render via template Jinja2 (rendering-json-html.md) — no HTML ad hoc
- [ ] 7. Verificare prosa uniforme e schema.org = JSON-LD
- [ ] 8. Test mobile 390px, touch 44px, chart fallback senza JS
- [ ] 9. SEO, _redirects, preview Cloudflare
```

## Integrazione skill

| Skill | Ruolo |
|-------|-------|
| the-verde-expert | Microcopy, glossario, no detox |
| web-architect | JSON privacy/termini, trigger da `assets/js` |
| seo-geo-expert | Meta legali, E-E-A-T, audit post-deploy |

**Conflitto:** accessibilità > decorazione; tono the-verde-expert > marketing; tabella > chart se dubbio.

## Cosa NON fare

- Layout wiki 72ch come default mobile
- HTML concatenato nel build script (solo Jinja2)
- Chart senza tabella fallback
- Nav solo testuale senza icone su mobile
- Bootstrap/Tailwind; SPA router per contenuto indicizzabile
- Zen kitsch; verde neon detox; emoji negli heading
- JSON-LD scritto a mano diverso dal body visibile
- d3 per singola varietà (usa metric-row)
- Griglie a 3+ colonne su box con prosa o card testuali (usa 1 col `sm`, max 2 col `md`+)

## Checklist finale

- [ ] PageDocument validato; template Jinja2 usato
- [ ] App shell: app-bar + bottom-nav + feed card
- [ ] Mobile-first 390px; touch ≥ 44px
- [ ] Griglie `tv-grid`: 1 col mobile, max 2 col tablet+; nessun box a 3 colonne con testo
- [ ] Icone sezioni + label accessibili
- [ ] Prosa via render_prose; strong/em/quote uniformi
- [ ] Schema.org: microdata = JSON-LD
- [ ] Tabella presente se chart d3
- [ ] Test persona superato
- [ ] Token Almost Acqua applicati
- [ ] Build + preview Cloudflare OK
- [ ] Footer con `/privacy/` e `/termini/`; se nuovi script dati → privacy rivista ([legal-compliance.md](../web-architect/legal-compliance.md))
