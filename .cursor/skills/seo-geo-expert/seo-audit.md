# Checklist audit SEO — the-verde.it

## Meta tag (per pagina)

| Campo | Regola | Dove |
|-------|--------|------|
| `title` | Unico, ≤60 char, keyword principale + brand | `meta.title` |
| `description` | ≤160 char, CTA implicita, intento utente | `meta.description` |
| `canonical_path` | Path assoluto con trailing slash | `meta.canonical_path` |
| `keywords` | 3–8 termini long-tail italiani | `meta.keywords` |
| `robots` | `index,follow` default; `noindex` solo form/diario privato | `seo.robots` |

## HTML head (build output)

Verifica in `dist/` dopo build:

- [ ] `<title>` = `meta.title`
- [ ] `<meta name="description">` presente
- [ ] `<link rel="canonical">` corretto
- [ ] `<meta property="og:*">` (title, description, image, url, type)
- [ ] `<meta name="twitter:card">` da `sitemap.json` social
- [ ] `<link rel="sitemap">` in `base.html`
- [ ] `Content-Language: it` via `_headers`

## Schema.org (JSON-LD)

| Tipo documento | Schema atteso | Note |
|----------------|---------------|------|
| Home | WebSite + Organization | SearchAction su `/cerca/` |
| Articolo / guida | Article | `inLanguage: it-IT`, audience Italia |
| Varietà | Article + countryOfOrigin | HowTo se blocco `steps` |
| Glossario | DefinedTerm | `termCode`, definizione nel body |
| Controversia | Article | positions con fonti |
| Hub catalogo | WebPage + ItemList | link a figli |
| FAQ nel body | FAQPage | supplementare in `@graph` |

Auto-generazione: `site_builder/enrichers/schema_org.py`. Override manuale: `seo.schema_org`.

## Sitemap e robots

- `sitemap.xml`: tutte le pagine indexabili, `priority` coerente (home 1.0, varietà 0.8, glossario 0.5)
- `robots.txt`: `Disallow: /diario/nuova/`; Sitemap assoluta
- Nessuna pagina orfana in sitemap senza link interno

## Internal linking

| Segnale | Soglia | Meccanismo |
|---------|--------|------------|
| `explore_next` | ≥3 link quando possibile | `navigation.py` |
| `related_slugs` | varietà correlate esplicite | JSON documento |
| `temi_kb` | max 2 per pagina | grafo `relazioni.json` |
| Breadcrumb | sempre presente | enricher navigation |
| Hub → foglie | ogni hub linka tutti i figli | template hub |

## Performance SEO (indiretta)

- Asset hashed con cache lunga (`_headers`)
- HTML `must-revalidate` per freshness
- Immagine OG social: `/assets/images/og-default.png` (1200×630; SVG in sito, raster per share)

## Errori comuni da correggere

1. Description duplicata tra pagine simili
2. Title generico («Tè verde» senza varietà/tema)
3. Canonical senza trailing slash
4. Glossario senza `DefinedTerm`
5. Varietà senza HowTo nonostante blocco steps
6. Hub senza ItemList
7. Pagine con <2 link interni in uscita
8. Keyword su tisane mescolate al verde
