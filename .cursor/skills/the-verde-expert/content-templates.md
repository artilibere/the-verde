# Template JSON — popolamento contenuti

Playbook operativo per popolare `content/` secondo voice-guide e knowledge base.

## Checklist pre-commit

- [ ] JSON valida (`pytest tests/test_schemas.py`)
- [ ] KB consultata; nessun placeholder «Consulta le schede»
- [ ] Fonti in `heading` + `list` finale — formato preciso: id + tema KB + sotto-tema + pp. (vedi [bibliografia.md](bibliografia.md))
- [ ] `navigation.temi_kb` e `explore_next` popolati
- [ ] Voce: tu, poetico-evocativo, Per iniziare + Approfondimento
- [ ] `python scripts/build.py` senza errori

## Glossario (`type: glossary`)

Percorso: `content/glossario/{slug}.json`

```json
{
  "schema_version": "1.0",
  "type": "glossary",
  "slug": "esempio",
  "meta": {
    "title": "Titolo termine",
    "description": "Definizione in una riga per meta/lead.",
    "keywords": ["termine", "tè verde", "Camellia sinensis"],
    "canonical_path": "/glossario/esempio/"
  },
  "seo": { "robots": "index,follow", "og_type": "article" },
  "navigation": {
    "related_slugs": ["termine-correlato"],
    "temi_kb": ["preparazione_servizio"],
    "controversie": [],
    "explore_next": [
      { "name": "Scheda varietà", "url": "/varieta/sencha/", "reason": "contesto pratico" }
    ]
  },
  "taxonomy": {},
  "body": {
    "blocks": [
      {
        "type": "level_section",
        "level": "intro",
        "blocks": [
          { "type": "paragraph", "spans": [{ "type": "text", "value": "Per iniziare: 2–4 frasi, tu, zero gergo." }] }
        ]
      },
      {
        "type": "level_section",
        "level": "deep",
        "blocks": [
          { "type": "heading", "level": 2, "spans": [{ "type": "text", "value": "Contesto" }] },
          { "type": "paragraph", "spans": [{ "type": "text", "value": "Prosa evocativa…" }] },
          { "type": "list", "ordered": false, "items": [{ "spans": [{ "type": "text", "value": "Punto chiave" }] }] },
          {
            "type": "related_links",
            "items": [{ "name": "Sencha", "url": "/varieta/sencha/", "reason": "esempio" }]
          },
          {
            "type": "faq",
            "items": [{
              "question": "Domanda frequente?",
              "answer_spans": [{ "type": "text", "value": "Risposta breve." }]
            }]
          },
          { "type": "heading", "level": 2, "spans": [{ "type": "text", "value": "Fonti" }] },
          { "type": "list", "ordered": false, "items": [
            { "spans": [{ "type": "text", "value": "Pellegrino — Manuale per la preparazione del tè, tema pellegrino-via-del-te «Umami, quinto sapore», p. 67" }] },
            { "spans": [{ "type": "text", "value": "Treccani — voce «umami»" }] }
          ]}
        ]
      }
    ]
  }
}
```

**Completezza:** intro ≥ 40 parole; deep ≥ 150 parole; ≥ 2 `related_links`.

## Varietà (`type: variety`)

Percorso: `content/varieta/{slug}.json`

Ordine blocchi:

1. `paragraph` — lead sensoriale
2. `sensory_profile`
3. `brew_params`
4. `equipment`, `steps`, `errors`
5. `callout` (variant `italia`), `pairings`, `faq` (≥ 2)
6. `level_section` deep (lavorazione/storia)
7. `related_links`
8. `heading` Fonti + `list`

`taxonomy.brew` deve coincidere con `brew_params`.

## Quiz (`content/_config/quizzes.json`)

```json
{
  "slug": "esempio",
  "title": "Titolo",
  "description": "Obiettivo didattico",
  "badge": "quiz-id",
  "questions": [
    {
      "q": "Domanda?",
      "options": ["A", "B", "C"],
      "correct": 1,
      "explain": "Due frasi didattiche, tono non punitivo.",
      "url": "/varieta/sencha/"
    }
  ]
}
```

Target: 8–10 domande (6–8 per `che-varieta-sei`).

## Percorso

**Articolo:** `content/gioca/percorsi/{slug}.json` — intro, obiettivi, deep «Cosa hai imparato».

**Config:** `content/_config/paths.json` — ogni step `varieta` con `quiz.question`, `options`, `correct`, `explain`.
