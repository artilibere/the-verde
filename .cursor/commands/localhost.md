# Server locale (the-verde.it)

## Objective

Buildare il sito in `dist/`, indicizzare la ricerca con Pagefind e servire il progetto su un server HTTP locale sulla porta indicata.

## Parametro obbligatorio

| Parametro | Descrizione |
|-----------|-------------|
| **porta** | Numero intero TCP (1–65535), es. `8080` |

Estrai la porta dal messaggio dell'utente (primo numero dopo `/localhost`, oppure `--port 8080` / `-p 8080`).

Se la porta **manca** o **non è valida**, chiedi all'utente quale porta usare — non avviare il server senza un valore esplicito.

## Process

1. Dalla root del repository, imposta ambiente e dipendenze (come `scripts/deploy.sh`):

   ```bash
   cd /var/www/the-verde.it

   if [[ ! -d .venv ]]; then python3 -m venv .venv; fi
   source .venv/bin/activate

   if [[ ! -f .venv/.deps_ok ]] || [[ requirements.txt -nt .venv/.deps_ok ]]; then
     pip install -q -r requirements.txt
     touch .venv/.deps_ok
   fi
   ```

2. **Build** del sito statico:

   ```bash
   python3 scripts/build.py --content content --out dist
   ```

3. **Pagefind** (ricerca locale su `/cerca/`):

   ```bash
   npx --yes pagefind --site dist --output-path dist/pagefind
   ```

4. **Verifica porta libera** — sostituisci `PORT` con la porta richiesta:

   ```bash
   ss -ltn "sport = :PORT" | grep -q LISTEN && echo "PORTA OCCUPATA" || echo "PORTA LIBERA"
   ```

   Se la porta è occupata, segnala quale processo la usa (`ss -ltnp "sport = :PORT"`) e chiedi un'altra porta — non sovrascrivere un server esistente.

5. **Avvia il server** in background sulla porta richiesta (`PORT`):

   ```bash
   python3 -m http.server PORT --directory dist --bind 127.0.0.1
   ```

   Esegui il comando con `block_until_ms: 0` (background). Il processo resta attivo finché l'utente non lo interrompe.

6. **Conferma** all'utente:
   - URL: `http://127.0.0.1:PORT/` (o `http://localhost:PORT/`)
   - Pagine di spot-check: home, `/varieta/sencha/`, `/cerca/`
   - Come fermare: terminare il job in background o `kill` del processo sulla porta

## Checklist

- [ ] Porta valida e libera
- [ ] Build exit code 0
- [ ] Pagefind indicizzato in `dist/pagefind/`
- [ ] Server in ascolto su `127.0.0.1:PORT`
- [ ] URL comunicato all'utente

## Expected output

- Porta usata e URL locale
- Esito build e pagefind
- Eventuali errori (porta occupata, build fallita, dipendenze mancanti)
- Istruzioni per fermare il server

## Usage

```
/localhost 8080
/localhost 3000
/localhost --port 5500
```

## Notes

- `dist/` è in `.gitignore` — output locale only
- Per solo build senza server: `/build`
- Per deploy remoto: `/deploy`
- Il server Python serve file statici; non emula Cloudflare Workers/Pages edge
- Skill di riferimento: `web-architect`, `uiux-designer`
