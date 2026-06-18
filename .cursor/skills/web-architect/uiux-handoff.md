# Handoff Web Architect ↔ UI/UX Designer

## Contratto PageDocument

Il build trasforma ogni documento JSON in un **PageDocument** consumato dai template Jinja2:

```json
{
  "type": "variety",
  "slug": "sencha",
  "meta": { "title": "...", "description": "...", "canonical": "https://..." },
  "cards": [
    { "id": "brief", "title": "In breve", "body": { "type": "prose", "blocks": [] } },
    { "id": "brew", "title": "Preparazione", "body": { "type": "metrics", "temp": 75 } }
  ],
  "navigation": { "breadcrumb": [], "pathNav": {}, "exploreNext": [] },
  "schema": { "@context": "https://schema.org", "@graph": [] }
}
```

Implementazione: [`scripts/site_builder/page_document.py`](../../../scripts/site_builder/page_document.py)

## Ordine card varietà (uiux-designer)

```
brief → brew → sensory → gear → steps → errors → italy → pairings → faq → related
```

Card assenti = omesse (no slot vuoti).

## Divisione responsabilità

| Task | Web Architect | UI/UX Designer |
|------|---------------|----------------|
| JSON schema sorgente | ✓ | consulto |
| PageDocument + @graph | ✓ | review ordine card |
| Template + partials | struttura dati | ✓ markup `tv-*` |
| App shell CSS | token base | ✓ layout feed |
| Test pytest | ✓ | checklist persona |
| SEO keywords | ✓ enricher | meta in head |

## Flusso collaborativo

1. **UI/UX** definisce ordine card e wireframe → [`template-pagine.md`](../uiux-designer/template-pagine.md)
2. **Web Architect** implementa `blocks → cards` e validazione
3. **UI/UX** crea/aggiorna partial Jinja2 e CSS
4. **Web Architect** aggiorna test integrazione
5. Entrambi: review accessibilità (h1, landmark, FAQ semantiche)

## Riferimenti UI/UX

- [rendering-json-html.md](../uiux-designer/rendering-json-html.md) — pipeline uniforme
- [app-shell.md](../uiux-designer/app-shell.md) — bottom nav, tv-feed
- [mapping-contenuti.md](../uiux-designer/mapping-contenuti.md) — blocco → componente
