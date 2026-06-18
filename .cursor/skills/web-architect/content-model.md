# Content model JSON — the-verde.it

## Envelope comune

Ogni documento editoriale in `content/**/*.json` (escluso `_config/` e `_schemas/`) segue:

```json
{
  "schema_version": "1.0",
  "type": "variety",
  "slug": "sencha",
  "meta": {
    "title": "...",
    "description": "...",
    "keywords": ["..."],
    "canonical_path": "/varieta/sencha/",
    "published": "2026-03-15"
  },
  "seo": {
    "robots": "index,follow",
    "og_type": "article"
  },
  "navigation": {
    "related_slugs": [],
    "temi_kb": [],
    "controversie": [],
    "momenti": [],
    "stagioni": [],
    "percorso_tappa": null,
    "explore_next": []
  },
  "taxonomy": {},
  "body": { "blocks": [] }
}
```

## Tipi documento

| `type` | Cartella | Template |
|--------|----------|----------|
| `variety` | `varieta/` | `variety.html` |
| `article` | `guide/`, `italia/abbinamenti`, `gioca/percorsi/` | `article.html` |
| `glossary` | `glossario/` | `glossary.html` |
| `controversy` | `impara/controversie/` | `controversy.html` |
| `hub` | `impara/`, `italia/` | `hub.html` |
| `page` | `pagine/` | `home.html` / `article.html` |

## Blocchi (`body.blocks[]`)

Testo **solo strutturato** — niente Markdown inline.

### Span inline

```json
{ "type": "text", "value": "testo" }
{ "type": "strong", "value": "grassetto" }
{ "type": "em", "value": "corsivo" }
{ "type": "link", "value": "etichetta", "href": "/varieta/sencha/" }
```

### Tipi blocco

| `type` | Campi principali |
|--------|------------------|
| `heading` | `level` (1-3), `spans` |
| `paragraph` | `spans` |
| `list` | `ordered`, `items[]` (ogni item: `spans`) |
| `sensory_profile` | `aspetto`, `aroma`, `gusto`, `retrogusto` |
| `brew_params` | `temp`, `grams`, `seconds`, `infusions` |
| `equipment` | `items[]` (stringhe) |
| `steps` | `items[]` → `text`, `duration` |
| `errors` | `items[]` (stringhe) |
| `callout` | `variant`: `italia` \| `warning` \| `tip`, `spans` |
| `pairings` | `items[]` (stringhe) |
| `faq` | `items[]` → `question`, `answer_spans` |
| `related_links` | `items[]` → `name`, `url`, `reason` |
| `level_section` | `level`: `intro` \| `deep`, `blocks[]` |
| `positions` | `items[]` → `fonte`, `tesi` |

## Normalizzazione verso template

1. **Content JSON** → `document_to_meta()` → dict `meta` legacy
2. **Content JSON** → `document_to_page()` → **PageDocument** con `cards[]` e `schema.@graph`

I template preferiscono `page.cards` (card feed). Fallback: `content_html` da `blocks.py` per pagine non ancora migrate al feed.

Implementazione: [`scripts/site_builder/page_document.py`](../../../scripts/site_builder/page_document.py)

## Varietà — layout zone

`blocks.render_variety_body()` produce `content_html` con:
- lead (primo paragrafo)
- `#prepara` — attrezzatura, errori, passaggi
- `#approfondisci` — callout Italia, abbinamenti, FAQ, correlati

Profilo sensoriale e brew card restano in `meta` per la zona Scopri del template.
