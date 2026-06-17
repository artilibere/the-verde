# Pre-commit (the-verde.it)

## Objective

Verificare che le modifiche siano pronte per il commit nel repo **the-verde.it** (sito statico editorial sul tè verde) e proporre messaggio e comando `git`.

## Process

1. Dalla **root del repository** (`/var/www/the-verde.it`):

   ```bash
   git status
   git diff
   ```

2. **Build** (se toccati `content/`, `templates/`, `assets/`, `scripts/`):

   ```bash
   python3 scripts/fix_encoding.py   # se toccato content/ o testi italiani
   python3 scripts/build.py --content content --out dist
   ```

3. **Controlli sicurezza**:
   - Nessun segreto in file tracciati (`.env`, token Cloudflare, chiavi Supabase)
   - `.env` è in `.gitignore` — non committare
   - `books/*.pdf` ignorati; OK committare `books/knowledge-base.json`

4. **Encoding** (se toccato `content/` o template con testo IT):
   - Prosa: `tè`, `varietà`, apostrofi (`l'acqua`)
   - Slug e URL: **senza** accenti (`varieta`, `?varieta=slug`, `/varieta/bancha/`)
   - `scripts/build.py` non va processato da `fix_encoding.py` (già escluso)

5. **Coerenza editoriale** (se toccato `content/`):
   - Varietà allineate a KB dove applicabile
   - Frontmatter YAML valido (slug, brew_*, temi_kb)
   - Voce The Verde: `.cursor/skills/the-verde-expert/voice-guide.md`

6. Generare messaggio di commit (conventional, in italiano) e comando suggerito.

## Checklist

- [ ] `git status` e diff analizzati
- [ ] Build completata senza errori (se rilevante)
- [ ] Nessun segreto nel commit
- [ ] Slug `/varieta/` e query `?varieta=` preservati
- [ ] `dist/` non incluso nel commit (è generato)
- [ ] Messaggio commit chiaro sul *perché*

## Commit message (conventional)

Esempi in italiano:

| Prefisso | Uso |
|----------|-----|
| `feat:` | Nuova varietà, quiz, sezione sito |
| `fix:` | Bug build, encoding, JS rotto |
| `docs:` | Skill, README, contenuti puramente testuali |
| `style:` | CSS, layout, UX senza nuova funzionalità |
| `perf:` | Asset pipeline, caching `_headers` |
| `chore:` | Tooling, dipendenze, config Cursor |

Messaggio in **frasi complete** (1–2 righe sul perché).

## Expected output

- Esito comandi eseguiti
- Checklist sintetica
- Messaggio commit proposto + `git add …` e `git commit -m "…"`

## Usage

```
/commit
```

## Notes

- Non committare `dist/`, `.venv/`, `pagefind/`, `.wrangler/`
- Deploy produzione: `/deploy` o `bash scripts/deploy.sh` (separato dal commit)
- Repo GitHub: https://github.com/artilibere/the-verde
