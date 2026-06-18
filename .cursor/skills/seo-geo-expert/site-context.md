# Contesto sito — SEO/GEO

## URL e tipi

| Sezione | Pattern URL | Tipo JSON | Priority sitemap |
|---------|-------------|-----------|------------------|
| Home | `/` | page | 1.0 |
| Varietà | `/varieta/{slug}/` | variety | 0.8 |
| Catalogo | `/varieta/` | hub | 0.9 |
| Impara | `/impara/{slug}/` | article/hub | 0.7–0.8 |
| Controversie | `/impara/controversie/{slug}/` | controversy | 0.6 |
| Glossario | `/glossario/{slug}/` | glossary | 0.5 |
| Italia | `/italia/`, momenti, stagioni | article/hub | 0.6–0.7 |
| Guide | `/guide/{slug}/` | article | 0.7 |
| Gioca | `/gioca/`, percorsi, quiz | article/hub | 0.4–0.6 |
| Legale | `/privacy/`, `/termini/` | page | 0.2 |

## Config globale

- Base URL: `https://the-verde.it` (`content/_config/sitemap.json`)
- Locale: `it-IT`, hreflang `it`, audience Italia
- OG default: `/assets/images/og-default.svg`
- Search: `/cerca/?q=` (noindex)

## Enrichers SEO (build)

| Modulo | Ruolo |
|--------|-------|
| `_seo_core.py` | Schemi base, sitemap XML, robots.txt |
| `schema_org.py` | HowTo, supplementary JSON-LD |
| `seo_context.py` | Contesto template (robots, og) |
| `navigation.py` | Breadcrumb, explore_next |

## Query target (long-tail IT)

Esempi di intenti da coprire:

- «come preparare il sencha»
- «differenza gyokuro sencha»
- «tè verde caffeina quanto»
- «matcha in Italia dove comprare» (contestualizzato)
- «tè verde fa bene» (con qualifiche, no hype)
- «bancha cos'è»
- «cerimonia del tè giapponese chanoyu»

Ogni hub deve linkare alle foglie che rispondono a questi intenti.

## Pagine noindex

- `/cerca/` — risultati dinamici
- `/diario/nuova/` — form utente

## Test di regressione

```bash
pytest tests/test_enrichers_seo.py tests/test_build_integration.py -q
python3 scripts/build.py --content content --out dist
```
