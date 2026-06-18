# Collaborazione SEO/GEO Expert

## Flusso tipico

```
Utente chiede ottimizzazione SEO/GEO
        ↓
seo-geo-expert: audit + raccomandazioni
        ↓
    ┌───┴───┐
    ↓       ↓
web-architect   the-verde-expert
(JSON, build)   (contenuto, KB)
    ↓       ↓
uiux-designer (se serve template/semantica)
        ↓
seo-geo-expert: verifica post-build
```

## Handoff verso web-architect

Quando proponi modifiche tecniche, specifica:

1. **File esatto** — es. `content/varieta/gyokuro.json`, `schema_org.py`
2. **Campo JSON** — path completo (`meta.description`, `navigation.related_slugs`)
3. **Schema richiesto** — tipo JSON-LD e proprietà mancanti
4. **Test da aggiornare** — es. `test_enrichers_seo.py`

Non modificare direttamente la pipeline build senza coordinarti: web-architect ha priorità su accessibilità e validazione schema.

## Handoff verso the-verde-expert

Quando manca profondità editoriale per E-E-A-T:

- Segnala gap di contenuto (non solo meta)
- Indica query target e intento di ricerca
- Suggerisci blocchi da aggiungere (`faq`, `positions`, `callout` italia)
- Non inventare fatti botanici: rimanda alla KB

## Handoff verso uiux-designer

Quando il problema è semantico/HTML:

- h1 duplicati o assenti
- FAQ non in `<details>`
- breadcrumb senza `aria-label`
- card senza heading linkabile
- OG image mancante nel template

## Conflitti di priorità

1. Accuratezza editoriale (the-verde-expert) > keyword optimization
2. Accessibilità (web-architect/uiux) > rich snippet tricks
3. Validazione JSON Schema > velocità pubblicazione
4. Citabilità GEO > densità keyword

## Worker Cloudflare

L'agente in `agents/seo-geo-expert/` esegue audit live sul sito deployato. Usalo per:

- Verificare meta/tag reali post-deploy
- Confrontare sitemap vs pagine raggiungibili
- Schedulare audit settimanali

I fix vanno applicati nel repo (content + build), non solo nel worker.
