---
name: Knowledge base the verde
overview: Costruire una base di conoscenza JSON originale sul tema \"the verde\", estraendo i temi libro per libro dai 5 PDF, normalizzandoli in italiano e mettendoli in relazione con un grafo cross-libro e una sezione di prospettive contrastanti.
todos:
  - id: extract-text
    content: Esportare il testo dei 5 PDF in file temporanei con pdftotext per la lettura a blocchi
    status: completed
  - id: themes-rosen
    content: Estrarre temi, sotto-temi, angolo e citazioni da 'Il libro del tè verde' (Rosen)
    status: completed
  - id: themes-sommelier
    content: Estrarre temi da 'Manuale del sommelier del tè' (Bisogno/Pettigrew)
    status: completed
  - id: themes-pellegrino
    content: Estrarre temi da 'Manuale per la preparazione del tè' (Pellegrino)
    status: completed
  - id: themes-onuma
    content: Estrarre temi da 'El secreto japones del tè verde' (Onuma), normalizzando da ES a IT
    status: completed
  - id: themes-hara
    content: Estrarre temi da 'Health Benefits of Green Tea' (Hara), normalizzando da EN a IT
    status: completed
  - id: canonical-themes
    content: Definire i temi trasversali canonici e mappare i temi dei singoli libri
    status: completed
  - id: relations
    content: Costruire le relazioni tipizzate tra temi (complementa/contrasta/approfondisce/presuppone)
    status: completed
  - id: perspectives
    content: Redigere le prospettive contrastanti su questioni chiave
    status: completed
  - id: assemble-json
    content: Assemblare e validare il JSON finale in books/knowledge-base.json e rimuovere i file temporanei
    status: completed
isProject: false
---

## Knowledge base "the verde"

### Obiettivo
Generare un singolo file JSON in `/var/www/the-verde.it/books/knowledge-base.json` che rappresenti una base di conoscenza originale sul tè verde, costruita leggendo i contenuti reali dei 5 libri (testo gia estraibile, ~280k parole totali) e collegando i temi tra loro.

### Fonti
- `Il libro del tè verde - Diana Rosen.pdf` (IT) - divulgativo: storia, varietà, salute, ricette, bellezza
- `Manuale del sommelier del tè - Victoria Bisogno, Jane Pettigrew.pdf` (IT) - tecnico: degustazione, varietà, servizio
- `Manuale per la preparazione del tè - Davide Pellegrino.pdf` (IT) - pratico: coltivazione, lavorazione, infusione, cerimonie
- `El secreto japones del tè verde - Izumi Foraste Onuma.pdf` (ES) - culturale: Giappone, rituali, benessere
- `Health Benefits of Green Tea - Yukihiko Hara.pdf` (EN) - scientifico: catechine, evidenze, patologie

### Metodo di estrazione
1. Per ogni libro, esportare il testo con `pdftotext` in file temporanei e leggerlo a blocchi (indice/capitoli + campionamento dei contenuti) per identificare temi, sotto-temi, angolo dell'autore, punti di vista e citazioni rappresentative con numero di pagina.
2. Normalizzare i temi in italiano, mappando concetti equivalenti tra ES/EN/IT su un vocabolario canonico condiviso (es. "catechine", "cerimonia", "varietà", "salute").
3. Costruire i collegamenti: temi trasversali, relazioni tipizzate e questioni con posizioni contrastanti.
4. Pulire i file temporanei al termine.

### Struttura del JSON
- `meta`: tema centrale, lingua, data, elenco fonti.
- `libri[]`: per ciascun libro `id`, `titolo`, `autore`, `lingua_originale`, `angolo_principale`, e `temi[]` con `nome`, `descrizione`, `sotto_temi[]` (con `pagine`), `punti_di_vista[]`, `citazioni[]`.
- `temi_trasversali[]`: tema canonico con `descrizione`, `libri_correlati`, `convergenze`, `divergenze`.
- `relazioni[]`: archi `{ da, a, tipo, descrizione }` con `tipo` in `complementa | contrasta | approfondisce | presuppone`.
- `prospettive_contrastanti[]`: `{ questione, posizioni[ { fonte, tesi } ], sintesi }` per dare "tanti angoli diversi" (es. salute: evidenza scientifica vs tradizione; cerimonia: Giappone vs Cina; qualità: sensoriale vs chimica).

### Schema concettuale

```mermaid
flowchart TD
  subgraph libri [Per libro]
    Tema --> SottoTema
    Tema --> PuntiDiVista
    Tema --> Citazioni
  end
  Tema --> TemaCanonico[Temi trasversali]
  TemaCanonico --> Relazioni
  TemaCanonico --> Prospettive[Prospettive contrastanti]
```

### Deliverable
- Un file: `/var/www/the-verde.it/books/knowledge-base.json` (UTF-8, indentato), autoconsistente e validabile.
- Nessuna modifica ai PDF esistenti.

### Note
- Le citazioni saranno tradotte/normalizzate in italiano; dove utile verra indicata la lingua originale della fonte e la pagina.
- Stima dimensione: file ricco ma gestibile (decine di KB), proporzionato all'approccio intermedio scelto.