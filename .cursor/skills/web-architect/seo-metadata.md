# SEO e metadati — the-verde.it

## Nel JSON (manuale)

```json
"meta": {
  "title": "...",
  "description": "...",
  "keywords": ["sencha", "tè verde", "preparazione"],
  "canonical_path": "/varieta/sencha/"
},
"seo": {
  "robots": "index,follow",
  "og_type": "article",
  "schema_org": null
}
```

- `keywords` → `<meta name="keywords">` (opzionale, non penalizzante)
- `description` troncata a 160 caratteri in build se più lunga

## Auto-generato (build)

Se `seo.schema_org` è assente:

| Condizione | Schema |
|------------|--------|
| Home | WebSite + Organization |
| Breadcrumb | BreadcrumbList |
| Articolo / guida | Article |
| Italia | Article + `about: Italy` |
| Varietà | Article + countryOfOrigin |
| Glossario | DefinedTerm |
| FAQ nel body | FAQPage |
| Steps nel body (varietà) | HowTo (supplementare) |
| Catalogo | WebPage + ItemList |

Sempre: `inLanguage: it-IT`, audience Italia dove pertinente.

## Open Graph

Da `meta.title`, `meta.description`, `canonical_path`, `og_image` in sitemap.json.

## Robots

- Default: `index,follow`
- `/cerca/`, `/diario/nuova/`: `noindex,follow`
