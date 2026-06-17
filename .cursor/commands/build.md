# Build locale (the-verde.it)

## Objective

Generare il sito statico in `dist/` e verificare che la build sia pulita.

## Process

1. Dalla root del repository:

   ```bash
   cd /var/www/the-verde.it

   # Opzionale: correggere accenti in content/ prima del build
   python3 scripts/fix_encoding.py

   # Build HTML + asset
   python3 scripts/build.py --content content --out dist
   ```

2. **Opzionale** — rigenerare contenuti da script:

   ```bash
   python3 scripts/generate_content.py
   ```

3. **Opzionale** — indicizzazione Pagefind (ricerca locale):

   ```bash
   npx --yes pagefind --site dist --output-path dist/pagefind
   ```

4. Verificare output:
   - Messaggio finale: `Built N pages → dist`
   - Campione: `dist/varieta/sencha/index.html`, `dist/index.html`
   - Breadcrumb «Varietà», link diario `?varieta=`, frecce path nav

## Checklist

- [ ] Exit code 0
- [ ] ~69 pagine generate
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

- `dist/` è in `.gitignore` — output locale/deploy only
- Dipendenze: `pip install -r requirements.txt` (venv consigliato)
- Per deploy completo: `/deploy`
