# SEO/GEO Expert (the-verde.it)

## Objective

Audit e ottimizzazione per **motori di ricerca** e **intelligenze generative** su the-verde.it.

## Skill

Applica `.cursor/skills/seo-geo-expert/SKILL.md` e riferimenti:

- [seo-audit.md](../skills/seo-geo-expert/seo-audit.md)
- [geo-optimization.md](../skills/seo-geo-expert/geo-optimization.md)
- [site-context.md](../skills/seo-geo-expert/site-context.md)

## Argomenti

| Argomento | Focus |
|-----------|--------|
| `audit` | Checklist su pagina o sezione (`content/`, `dist/`) |
| `meta` | title, description, canonical, keywords |
| `schema` | JSON-LD, FAQPage, DefinedTerm, HowTo |
| `geo` | chunk citabili, llms.txt, E-E-A-T, FAQ |
| `arch` | sitemap, robots, hub, internal linking, orphan pages |
| `live` | Agente Cloudflare `agents/seo-geo-expert/` |

## Process

1. Identifica ambito (singola pagina, sezione, sito intero)
2. Leggi JSON sorgente + output build se disponibile
3. Applica checklist SEO e GEO
4. Proponi modifiche concrete (`meta`, `navigation`, enrichers)
5. `pytest tests/test_enrichers_seo.py` se tocchi build
6. `python3 scripts/build.py` per verificare output

## Collaborazione

- **web-architect**: implementazione enrichers e schemi
- **the-verde-expert**: arricchimento contenuto per E-E-A-T
- **uiux-designer**: semantica HTML in template
