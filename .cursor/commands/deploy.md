# Deploy (the-verde.it)

## Objective

Buildare e pubblicare su **Cloudflare Pages** il sito the-verde.it.

## Target

| Ambiente | URL |
|----------|-----|
| Pages | https://the-verde.pages.dev |
| Produzione | https://the-verde.it (quando DNS/SSL attivi) |

Account Cloudflare: `artilibere` — vedi `README.md`.

## Process

1. **Verificare build locale** (consigliato prima del deploy):

   ```bash
   python3 scripts/build.py --content content --out dist
   ```

2. **Deploy** (script unificato):

   ```bash
   bash scripts/deploy.sh
   ```

   Lo script:
   - attiva/crea `.venv` e installa dipendenze se necessario
   - esegue `build.py`
   - indicizza con Pagefind
   - pubblica con `wrangler pages deploy dist --project-name=the-verde`

3. **GitHub Actions** (alternativa): push su branch configurato con secrets:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`

## Checklist pre-deploy

- [ ] Build locale OK
- [ ] Nessun segreto in file committati
- [ ] `_headers` e `_redirects` aggiornati se cambia caching/routing
- [ ] Spot-check post-deploy: home, catalogo varietà, scheda sencha

## Expected output

- Esito `deploy.sh` (URL deployment Wrangler)
- Eventuali errori autenticazione Wrangler da segnalare

## Usage

```
/deploy
```

## Notes

- Richiede `npx wrangler` e credenziali Cloudflare configurate
- Non committare `.env` né token
- Il deploy non sostituisce `/commit` — versionare sorgenti separatamente
