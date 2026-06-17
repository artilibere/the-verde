# Guida alla knowledge base — `books/knowledge-base.json`

Fonte canonica ed esaustiva dell'esperto The Verde. **Leggere il file JSON completo** (o le sezioni pertinenti) prima di rispondere a domande sostanziali.

## Struttura

| Sezione | Contenuto |
|---------|-----------|
| `meta` | Tema centrale, data, descrizione, elenco `fonti` (5 libri con id e PDF) |
| `libri` | Per ogni libro: `id`, `angolo_principale`, array `temi` |
| `temi_trasversali` | 8 temi incrociati tra libri: convergenze e divergenze |
| `relazioni` | 12 collegamenti tra temi trasversali (`presuppone`, `approfondisce`, `complementa`, `contrasta`) |
| `prospettive_contrastanti` | 6 questioni aperte con posizioni per fonte e sintesi |

## I 5 libri (id)

| id | Titolo | Angolo | Quando privilegiarlo |
|----|--------|--------|----------------------|
| `rosen` | Il libro del tè verde (Diana Rosen) | Divulgazione poetica e pratica | Storia, poesia, cucina, bellezza, quotidianità |
| `sommelier` | Manuale del sommelier del tè (Bisogno/Pettigrew) | Prospettiva professionale e sensoriale | Degustazione, schede sensoriali, servizio |
| `pellegrino` | Manuale per la preparazione del tè (Davide Pellegrino) | Agronomico-pratico, dalla pianta alla tazza | Preparazione, varietà, acqua, teiere |
| `onuma` | El secreto japones del tè verde (Izumi Forasté Onuma) | Vita quotidiana giapponese, cerimonia, mindfulness | Cultura JP quotidiana, Chanoyu, famiglia |
| `hara` | Health Benefits of Green Tea (Yukihiko Hara) | Evidence-based, catechine, trial clinici | Salute, meccanismi molecolari, cautela scientifica |

**Nota lingue:** Onuma è in spagnolo; Hara in inglese. La KB normalizza in italiano — consultare `citazioni[].lingua_originale` per il testo fonte.

## 8 temi trasversali (id)

| id | Nome | Domande tipiche |
|----|------|-----------------|
| `storia_cultura` | Storia e cultura | Origini, Shen Nong, diffusione, Eisai |
| `lavorazione_qualità` | Lavorazione e qualità | Wok vs vapore, ombreggiamento, catechine |
| `preparazione_servizio` | Preparazione e servizio | Temperatura, tempo, kyusu, gong fu cha |
| `degustazione_sensoriale` | Degustazione | Umami, astringenza, schede professionali |
| `salute_catechine` | Salute e catechine | EGCG, cancro, cuore, integratori |
| `cerimonia_spiritualita` | Cerimonia e spiritualità | Chanoyu, gong fu cha, etichetta |
| `caffeina_tannini` | Caffeina e tannini | Teina, stimolazione, L-teanina |
| `cucina_usi_pratici` | Cucina e usi pratici | Matcha in ricette, kombucha, cosmetica |

## Schema di ogni tema libro

Ogni elemento in `libri[].temi[]` contiene:

- `id`, `nome`, `descrizione`
- `sotto_temi[]` con `nome` e `pagine[]` (riferimento al PDF)
- `punti_di_vista[]` — tesi sintetiche
- `citazioni[]` — testo, `pagina`, `lingua_originale`

## Workflow di consultazione (6 passi)

1. **Classifica la domanda** → tema trasversale più vicino (tabella sopra).
2. **Leggi** `temi_trasversali[id]`: `convergenze`, `divergenze`, `temi_libro` collegati.
3. **Approfondisci** nei `libri[].temi` referenziati (per id tema).
4. **Traccia relazioni** in `relazioni` dove `da` o `a` coincidono col tema trasversale.
5. **Se controversa**, consulta `prospettive_contrastanti` e presenta posizioni con `sintesi`.
6. **Cita** con id libro (`rosen`, `pellegrino`, `sommelier`, `onuma`, `hara`) + pagina.

## Query pattern — domanda → percorso KB

| Domanda utente | Tema trasversale | Temi libro da aprire |
|----------------|------------------|----------------------|
| «Sencha troppo amaro» | `preparazione_servizio` | `pellegrino-via-del-te`, `sommelier-degustazione` |
| «Matcha fa bene?» | `salute_catechine` | `hara-*`, `rosen-salute`, prospettiva bevanda-vs-integratore |
| «Differenza Cina e Giappone» | `lavorazione_qualità` | `sommelier-produzione-verde`, `pellegrino-pianta` |
| «Cerimonia del tè» | `cerimonia_spiritualita` | `onuma-cerimonia`, `sommelier-cerimonie`, prospettiva cerimonia-cina-vs-giappone |
| «Quanto caffeina?» | `caffeina_tannini` | temi sommelier/hara, prospettiva caffeina-stimolazione |
| «Dragon well come si prepara» | `preparazione_servizio` + `degustazione_sensoriale` | `sommelier-degustazione` (Lung Ching), `pellegrino-varietà` |
| «Tè verde e dimagrimento» | `salute_catechine` | temi hara, prospettiva salute-scienza-vs-tradizione |

## Mappa varietà → temi KB

Da `content/relazioni.json` → `varieta_temi`. Usare per schede sito e risposte mirate:

| Slug varietà | Temi trasversali |
|--------------|------------------|
| bancha | preparazione_servizio, caffeina_tannini |
| sencha | preparazione_servizio, degustazione_sensoriale |
| gyokuro | lavorazione_qualità, degustazione_sensoriale |
| matcha | cerimonia_spiritualita, cucina_usi_pratici |
| genmaicha | cucina_usi_pratici, preparazione_servizio |
| hojicha | lavorazione_qualità, caffeina_tannini |
| kukicha | caffeina_tannini, preparazione_servizio |
| dragon-well | storia_cultura, degustazione_sensoriale |
| gunpowder | storia_cultura, preparazione_servizio |
| bi-luo-chun | lavorazione_qualità, degustazione_sensoriale |
| darjeeling-verde | storia_cultura, degustazione_sensoriale |
| cold-brew-gyokuro | preparazione_servizio, caffeina_tannini |

## Varietà per libro (schede sensoriali in KB)

| Libro | Varietà con scheda dedicata |
|-------|----------------------------|
| `sommelier` | Lung Ching, Sencha, Gyokuro, Matcha, Nilgiri verde |
| `pellegrino` | Verdi cinesi (Long Jing, Bi Lo Chun, Gunpowder…), verdi giapponesi (Sencha, Matcha, Gyokuro, Bancha…), Jeoncha |
| `rosen` | Gyokuro, Matcha, Bancha, Sencha (lavorazione) |
| `onuma` | Matcha, tè giapponesi quotidiani, cerimonia |

Dettaglio operativo: [varietà.md](varietà.md).

## 6 prospettive contrastanti (id)

| id | Questione | Come presentarla |
|----|-----------|------------------|
| `salute-scienza-vs-tradizione` | Quanto è dimostrato che il tè verde faccia bene? | hara cauta vs rosen/onuma entusiaste; sintesi equilibrata |
| `bevanda-vs-integratore` | Meglio bere tè verde o assumere estratti? | Matcha come foglia intera vs pillole; biodisponibilità |
| `cerimonia-cina-vs-giappone` | Come si confrontano Gongfu Cha e Chanoyu? | Gestualità, estetica, non gerarchia |
| `qualità-sensoriale-vs-chimica` | Cosa definisce un buon tè verde? | Palato vs analisi catechine |
| `caffeina-stimolazione` | Il tè verde stimola o rilassa? | Teina + L-teanina; varietà conta |
| `consumo-quotidiano-vs-rituale` | Abitudine quotidiana o esperienza speciale? | Bancha in bottiglia vs Chado (onuma) |

## 12 relazioni tra temi (tipi)

| Tipo | Significato operativo |
|------|----------------------|
| `presuppone` | Leggi il tema `da` prima di rispondere su `a` |
| `approfondisce` | Il tema `a` è dettaglio tecnico di `da` |
| `complementa` | Affianca prospettive diverse sullo stesso argomento |
| `contrasta` | Presenta entrambe le posizioni; non scegliere un vincitore |

Esempio: `cucina_usi_pratici` → `lavorazione_qualità` (`presuppone`): per matcha da cucina, prima qualità della polvere.

## Esempio walkthrough

**Domanda:** «Il mio sencha è sempre amaro, cosa sbaglio?»

1. Tema: `preparazione_servizio`
2. Convergenze KB: acqua 60–80 °C, non bollente
3. Temi libro: `pellegrino-via-del-te`, `sommelier-degustazione` (scheda Sencha)
4. Relazione: `preparazione_servizio` → `degustazione_sensoriale` (`approfondisce`)
5. Contesto IT: acqua del rubinetto dura in molte città italiane; filtrare o usare minerale leggera
6. Fonti: `pellegrino`, `sommelier`; varietà alternativa se serve meno amaro: bancha, genmaicha

## Regole di utilizzo

- Non inventare contenuti assenti dal JSON; se un dettaglio manca, dichiararlo.
- Preferire **convergenze** come base della risposta; esporre **divergenze** quando arricchiscono.
- Per salute: bilanciare `hara` (cautela scientifica) con `rosen`/`onuma` (tradizione/divulgazione).
- Per preparazione tecnica: priorità a `pellegrino` e `sommelier`.
- Per cultura giapponese quotidiana: priorità a `onuma`.
- Incrociare con contestualizzazione italiana (vedi `cultura-italiana.md`).
