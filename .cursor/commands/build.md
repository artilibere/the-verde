# Build locale (the-verde.it)

## Objective

Validare i contenuti JSON, generare il sito statico in `dist/` e verificare che build e test siano puliti.

## Process

1. Dalla root del repository:

   ```bash
   cd /var/www/the-verde.it

   pip install -r requirements.txt

   # Test (obbligatorio prima del build)
   python3 -m pytest tests/ -q

   # Solo validazione JSON
   python3 scripts/build.py --validate-only

   # Build HTML + asset
   python3 scripts/build.py --content content --out dist
   ```

2. **Opzionale** — indicizzazione Pagefind (ricerca locale):

   ```bash
   npx --yes pagefind --site dist --output-path dist/pagefind
   ```

3. Verificare output:
   - Messaggio finale: `Built 70 pages → dist` (pagine editoriali in `all_pages`)
   - **95** file `index.html` unici in `dist/` (hub, cataloghi, utility incluse)
   - **91** URL in `dist/sitemap.xml` (escluse diario, community, cerca)
   - Campione: `dist/varieta/sencha/index.html`, `dist/index.html`
   - Breadcrumb «Varietà», link diario `?varieta=`, frecce path nav

## Checklist

- [ ] `pytest` exit code 0
- [ ] Build exit code 0
- [ ] 95 pagine HTML (`index.html`) generate
- [ ] Nessun errore UTF-8 in template
- [ ] Asset CSS/JS hashed in `dist/assets/`

## Expected output

- Esito comandi
- Eventuali errori con file e riga
- Suggerimento fix se build fallisce

## Usage

```
/build
```

## Notes

- Contenuti editoriali in `content/**/*.json` (non Markdown)
- Schemi in `content/_schemas/`
- `dist/` è in `.gitignore` — output locale/deploy only
- Per deploy completo: `/deploy`
- Agente architettura: skill `web-architect`
