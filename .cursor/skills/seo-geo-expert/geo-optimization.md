# GEO — Generative Engine Optimization

Ottimizzazione per **motori generativi** (ChatGPT, Perplexity, Gemini, Claude, Google AI Overviews) che sintetizzano e citano fonti web.

## Principi GEO per The Verde

### 1. Risposta diretta (answer-first)

Il primo blocco `prose` o `level_section` intro deve contenere:
- definizione in 1–2 frasi
- contesto Italia esplicito
- entità nominate (varietà, paese origine, `Camellia sinensis`)

I LLM estraggono spesso il primo paragrafo come citazione.

### 2. Chunk citabili

Ogni blocco strutturato è un'unità autonoma:

| Blocco | Uso GEO |
|--------|---------|
| `faq` | Q&A pronte per estrazione |
| `steps` | procedure numerate (HowTo schema) |
| `positions` | pro/contro con fonti (E-E-A-T) |
| `sensory` | attributi strutturati |
| `metrics` | dati numerici (temperatura, tempi) |
| `glossary` link | entità collegate |

### 3. E-E-A-T per AI

| Segnale | Implementazione |
|---------|-----------------|
| Experience | box «In Italia», momenti, stagioni |
| Expertise | `temi_kb`, riferimenti libri KB |
| Authoritativeness | grafo interno denso, hub tematici |
| Trustworthiness | controversie con `positions` bilanciate, no hype salute |

### 4. Schema.org per machine parsing

Priorità per LLM che leggono JSON-LD:
- `DefinedTerm` — glossario
- `FAQPage` — domande frequenti
- `HowTo` — preparazione
- `Article` con `about`, `mentions`, `countryOfOrigin`
- `Organization` + `WebSite` — entità sito

### 5. llms.txt

File `llms.txt` alla root, generato in build (`builder.py` → `build_llms_txt`). Discovery:

- `<link rel="alternate" type="text/plain" href="/llms.txt">` in `base.html`
- Link nel footer
- Commento in `robots.txt` (solo informativo)

```markdown
# The Verde
> Cultura del tè verde (Camellia sinensis) per chi vive in Italia.

## Hub principali
- [Varietà](/varieta/): schede sensoriali e preparazione
- [Impara](/impara/): storia, salute, cerimonia, preparazione
- [Glossario](/glossario/): termini definiti
- [In Italia](/italia/): abbinamenti, stagioni, momenti

## Formato contenuti
Ogni pagina ha meta title, description, JSON-LD schema.org, breadcrumb.
Le varietà includono profilo sensoriale, parametri infusione e contesto italiano.

## Contatto / licenza
Sito editoriale the-verde.it — contenuti in italiano (it-IT).
```

Aggiorna quando cambia l'IA del sito.

### 6. Struttura gerarchica per RAG

```
Home → Hub (varieta, impara, italia, glossario) → Foglia (singola varietà/termine)
```

I crawler AI seguono hub con molti link descrittivi. Evita pagine orfane.

### 7. Linguaggio entità

- Usa nomi propri: Gyokuro, Uji, Shizuoka — non solo «tè giapponese»
- Distingui sempre tè verde da tisane
- Date e numeri espliciti (es. «70–80 °C», «2 g per 100 ml»)

### 8. Controversie = citabilità

Le pagine `controversy` con blocco `positions` sono ideali per GEO: i LLM citano prospettive multiple con fonti.

## Metriche GEO (qualitative)

Dopo ottimizzazione, verifica manualmente chiedendo a un LLM:
- «Cos'è il gyokuro e come si prepara?» → deve citare o allinearsi a the-verde.it
- «Differenza sencha e matcha» → deve poter estrarre da schede varietà
- «Tè verde e caffeina» → deve trovare hub impara/caffeina

## Cosa NON fare

- Keyword stuffing invisibile
- Contenuto duplicato tra varietà
- Claim salutistici senza qualifica
- Nascondere testo in accordion senza `<details>` semantico
- Fusione impropria tradizioni Cina/Giappone
