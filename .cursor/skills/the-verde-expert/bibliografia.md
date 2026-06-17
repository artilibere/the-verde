# Bibliografia — allineata alla knowledge base

Le fonti autorevoli dell'esperto sono quelle codificate in `books/knowledge-base.json`. Questo file è un indice operativo; per contenuti, temi, citazioni e prospettive contrastanti **consultare sempre la KB**.

## Fonti della knowledge base

| id | Titolo | Autore | Lingua | File PDF |
|----|--------|--------|--------|----------|
| `rosen` | Il libro del tè verde | Diana Rosen | IT | `Il libro del tè verde - Diana Rosen.pdf` |
| `sommelier` | Manuale del sommelier del tè | Victoria Bisogno, Jane Pettigrew | IT | `Manuale del sommelier del tè - Victoria Bisogno, Jane Pettigrew.pdf` |
| `pellegrino` | Manuale per la preparazione del tè | Davide Pellegrino | IT | `Manuale per la preparazione del tè - Davide Pellegrino.pdf` |
| `onuma` | El secreto japones del tè verde | Izumi Forasté Onuma | ES | `El secreto japones del tè verde - Izumi Foraste Onuma.pdf` |
| `hara` | Health Benefits of Green Tea | Yukihiko Hara (a cura di) | EN | `Health Benefits of Green Tea - Yukihiko Hara.pdf` |

## Quando citare quale fonte

| Domanda | id prioritari |
|---------|---------------|
| Storia, poesia, cucina, bellezza | `rosen` |
| Degustazione, servizio, cerimonie | `sommelier` |
| Preparazione, varietà, schede tecniche | `pellegrino` |
| Cultura giapponese quotidiana, mindfulness | `onuma` |
| Catechine, trial clinici, meccanismi molecolari | `hara` |
| Temi incrociati o dibattiti aperti | `temi_trasversali` + `prospettive_contrastanti` |

## Copertura varietà per libro

| Libro | Varietà con contenuto dedicato in KB |
|-------|-------------------------------------|
| `sommelier` | Lung Ching (Dragon Well), Sencha, Gyokuro, Matcha, Nilgiri verde |
| `pellegrino` | Long Jing, Bi Lo Chun, Gunpowder, Sencha, Matcha, Gyokuro, Bancha, Jeoncha |
| `rosen` | Gyokuro, Matcha, Bancha, Sencha (lavorazione) |
| `onuma` | Matcha, tè giapponesi quotidiani, cerimonia |
| `hara` | Matcha (concentrazione catechine), verde generico (salute) |

Per parametri brew e profili del sito: [varietà.md](varietà.md).

## Percorsi di lettura per obiettivo

### Imparare a preparare

1. `pellegrino` → via del tè, acqua, teiere (tema `pellegrino-via-del-te`)
2. `pellegrino` → varietà (schede cinesi e giapponesi)
3. `sommelier` → degustazione (parametri sensoriali)
4. Sito: schede in `content/varieta/` + [varietà.md](varietà.md)

### Capire salute senza hype

1. `hara` → catechine, trial, cautela
2. `prospettive_contrastanti` → salute-scienza-vs-tradizione, bevanda-vs-integratore
3. `rosen` → tradizione e quotidianità (bilanciamento)
4. Mai saltare il disclaimer (voice-guide)

### Scrivere per the-verde.it

1. [voice-guide.md](voice-guide.md) → tono e calibrazione
2. [varietà.md](varietà.md) → profili e rotazione esempi
3. KB → `temi_trasversali` + `varieta_temi` in `content/relazioni.json`
4. [cultura-italiana.md](cultura-italiana.md) → ponti Italia

### Esplorare per origine

| Percorso | Varietà | Fonti |
|----------|---------|-------|
| Giappone quotidiano | bancha → sencha → genmaicha | `onuma`, `pellegrino` |
| Giappone premium | sencha → gyokuro → matcha | `sommelier`, `onuma` |
| Cina classica | gunpowder → dragon well → bi luo chun | `pellegrino`, `sommelier` |
| Sera / bassa caffeina | kukicha → hojicha | `pellegrino`, KB caffeina |
| Mondo | darjeeling verde → Nilgiri (KB) | `sommelier`, `pellegrino` |
| Estate | cold brew gyokuro | `pellegrino`, sito |

## Tabella incrociata libro × tema trasversale

| Tema trasversale | rosen | sommelier | pellegrino | onuma | hara |
|------------------|:-----:|:---------:|:----------:|:-----:|:----:|
| storia_cultura | ● | ● | ● | ● | |
| lavorazione_qualità | ● | ● | ● | ● | |
| preparazione_servizio | ● | ● | ● | ● | |
| degustazione_sensoriale | | ● | ● | ● | |
| salute_catechine | ● | ● | ● | ● | ● |
| cerimonia_spiritualita | ● | ● | ● | ● | |
| caffeina_tannini | | ● | ● | | ● |
| cucina_usi_pratici | ● | | ● | ● | |

● = libro con temi collegati in `temi_trasversali[].libri_correlati`

## Riferimenti esterni (non in KB)

| Opera | Autore | Uso |
|-------|--------|-----|
| *The Story of Tea* | Mary Lou e Robert J. Heiss | Enciclopedia generale; integrazione, non fonte primaria |
| *Tea: History, Terroirs, Varieties* | Gascoyne et al. | Riferimento visivo varietà; non sostituisce KB |

## Note operative

- **Onuma (ES):** la KB estrae in italiano; per citazioni letterali verificare `lingua_originale` nel JSON.
- **Hara (EN):** traduzione italiana nella KB; per trial specifici usare pagine indicate in `sotto_temi`.
- **Pellegrino:** unico autore italiano nella KB — priorità per contestualizzazione tecnica locale (acqua, mercato).
- Non citare fonti esterne alla KB come primarie in contenuti the-verde.it senza esplicita richiesta.
