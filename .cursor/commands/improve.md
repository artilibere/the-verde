# Miglioramenti (the-verde.it)

## Objective

Analizzare e applicare miglioramenti mirati al sito statico **the-verde.it**: contenuti editoriali, build, template, asset frontend e skill Cursor — senza refactor gratuiti.

## Contesto progetto

| Area | Percorso | Note |
|------|----------|------|
| Contenuti | `content/` | Markdown + frontmatter YAML |
| KB canonica | `books/knowledge-base.json` | Fonte di verità editoriale |
| Template | `templates/` | Jinja2 → HTML in `dist/` |
| Asset | `assets/css/`, `assets/js/` | Vanilla CSS/JS, design system `tv-*` |
| Build | `scripts/build.py`, `html_enrich.py`, `asset_pipeline.py` | Generatore statico |
| Encoding | `scripts/fix_encoding.py` | Accentuazione italiana; preserva slug `/varieta/` e `?varieta=` |
| Skill esperto | `.cursor/skills/the-verde-expert/` | Voce, varietà, cultura IT |
| Skill UI | `.cursor/skills/uiux-designer/` | Design system M3, componenti, personas |

## Process

1. **Identificare l'area** in base al task o al diff:
   - **Editoria**: `content/varieta/`, `content/impara/`, `content/guide/`, glossario
   - **UX/UI**: `templates/`, `assets/css/`, `assets/js/`
   - **Build**: `scripts/build.py`, `html_enrich.py`, `asset_pipeline.py`
   - **Skill/agenti**: `.cursor/skills/`, `.cursor/rules/`
2. **Contenuti editoriali** (se toccati):
   - Consultare `books/knowledge-base.json` e `.cursor/skills/the-verde-expert/`
   - Voce: Per iniziare + Approfondimento; rotare varietà (non solo matcha/sencha/gyokuro)
   - Slug URL senza accenti (`/varieta/bancha/`); prosa con UTF-8 corretto
   - Distinguere *Camellia sinensis* da tisane; niente hype detox
3. **Frontend** (se toccati):
   - Token in `assets/css/tokens.css`; componenti `tv-*` in `components.css`
   - Personas UX (Elena prioritaria): `.cursor/skills/uiux-designer/personas.md`
   - Schede varietà: zone Scopri / Prepara / Approfondisci; brew card; box «In Italia»
   - Accessibilità: focus ring, `aria-*`, contrasto WCAG
4. **Build** (se toccati):
   - Verificare che `python3 scripts/build.py --content content --out dist` completi senza errori
   - Dopo edit su `content/`: `python3 scripts/fix_encoding.py` (non corrompe `scripts/build.py`)
   - Controllare una pagina campione: `dist/varieta/sencha/index.html`
5. Evitare di «pulire» file non toccati dal task.

## Aree di miglioramento tipiche

| Comando implicito | Focus |
|-------------------|--------|
| `/improve encoding` | `fix_encoding.py`, prosa in `content/`, template UTF-8, `build.py` |
| `/improve ui/ux` | template, CSS, JS interattivo (filtri, quiz, diario, level-toggle) |
| `/improve speed` | `asset_pipeline.py`, `_headers`, bundle CSS, minify HTML/JSON |
| `/improve seo` | `sitemap.xml`, `robots.txt`, Open Graph, JSON-LD, meta/canonical |
| `/improve geo` | hreflang, `areaServed` Italia, origine varietà, sezione In Italia |
| `/improve seo geo` | canonical, schema, sitemap, hreflang, `og:image`, hub/catalogo |
| `/improve social` | Open Graph/Twitter, share, `theme-color`, `sameAs` |
| `/improve the-verde-expert` | skill in `.cursor/skills/the-verde-expert/` |
| `/improve all` | encoding + build + UX + fix regressioni note |

## Checklist

- [ ] Miglioramenti pertinenti al task corrente
- [ ] KB consultata per contenuti editoriali sostanziali
- [ ] Slug e path `/varieta/` intatti dopo fix encoding
- [ ] Build OK: `python3 scripts/build.py --content content --out dist`
- [ ] Nessun segreto in codice (`.env` non committato)
- [ ] Nessun refactor di massa non richiesto

## Verifica post-modifica

```bash
cd /var/www/the-verde.it
python3 scripts/fix_encoding.py    # se toccato content/ o testi IT
python3 scripts/build.py --content content --out dist
```

## Expected output

- Elenco miglioramenti prioritizzati (o diff applicato)
- Esito build e note su pagine campione verificate

## Usage

```
/improve
/improve encoding
/improve ui/ux
/improve speed
/improve seo
/improve geo
/improve social
/improve .cursor/skills/the-verde-expert
/improve all
```

## Notes

- Per revisione bug/sicurezza usare `/review`.
- Per commit guidato usare `/commit`.
- Per deploy Cloudflare Pages usare `/deploy`.
- `dist/` è in `.gitignore` — non committare l'output build.
