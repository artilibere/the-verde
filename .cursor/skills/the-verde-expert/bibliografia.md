# Bibliografia — fonti di ispirazione e documentazione

L'esperto The Verde si fonda su **cinque opere di riferimento**, incrociate in `books/knowledge-base.json`. Questo file è l'indice bibliografico operativo: per contenuti, temi, citazioni letterali e prospettive contrastanti **consultare sempre la KB**; qui trovi le schede libro, l'indice dei temi e il **formato canonico delle citazioni**.

## Le cinque fonti

### Rosen — `rosen`

| Campo | Valore |
|-------|--------|
| **Titolo** | *Il libro del tè verde* |
| **Autore** | Diana Rosen |
| **Lingua** | Italiano |
| **Ruolo** | Divulgazione poetica e pratica: storia, rituali, preparazione, salute, bellezza, cucina |
| **Quando privilegiarlo** | Narrativa storica, filosofia del tè, quotidianità culturale, ricette, cosmetica domestica |
| **KB** | `libri[id=rosen]` · PDF: `Il libro del tè verde - Diana Rosen.pdf` |

| id tema | Nome | Pagine chiave (da `sotto_temi`) |
|---------|------|----------------------------------|
| `rosen-poesia` | Poesia e filosofia del tè verde | 97, 146–151, 153–174, 181, 189 |
| `rosen-storia` | Storia e tradizioni | 47–51, 50–171, 398, 473, 1698 |
| `rosen-lavorazione` | Lavorazione e varietà | 1575 (gyokuro), 1585 (matcha), 1592 (bancha/sencha) |
| `rosen-preparazione` | Acquisto, conservazione, preparazione | 2300–2351 (Yixing), 2385–2432 (gung fu), 2435–2448 |
| `rosen-salute` | Salute e benessere | 2714–2838, 2724–2796, 2770–2786, 2807–2819 |
| `rosen-bellezza-cucina` | Bellezza e cucina | 57–58, 3099–3109 |

---

### Sommelier — `sommelier`

| Campo | Valore |
|-------|--------|
| **Titolo** | *Manuale del sommelier del tè* |
| **Autore** | Victoria Bisogno, Jane Pettigrew |
| **Lingua** | Italiano |
| **Ruolo** | Prospettiva professionale: storia, tecnica produttiva, analisi sensoriale, servizio, cerimonie |
| **Quando privilegiarlo** | Degustazione, schede sensoriali, servizio in sala, confronto varietà, cerimonie |
| **KB** | `libri[id=sommelier]` · PDF: `Manuale del sommelier del tè - Victoria Bisogno, Jane Pettigrew.pdf` |

| id tema | Nome | Pagine chiave |
|---------|------|---------------|
| `sommelier-storia` | Storia e cultura del tè | 190–200 |
| `sommelier-produzione-verde` | Produzione del tè verde | vedi `sotto_temi` in KB |
| `sommelier-degustazione` | Analisi sensoriale e varietà | schede Lung Ching, Sencha, Gyokuro, Matcha, Nilgiri |
| `sommelier-proprieta` | Proprietà chimiche e salute | vedi `sotto_temi` in KB |
| `sommelier-cerimonie` | Cerimonie e galateo | 4358 (galateo ospitalità) |

---

### Pellegrino — `pellegrino`

| Campo | Valore |
|-------|--------|
| **Titolo** | *Manuale per la preparazione del tè* |
| **Autore** | Davide Pellegrino |
| **Lingua** | Italiano |
| **Ruolo** | Agronomico-pratico: dalla pianta alla tazza, schede varietali, tradizioni mondiali, salute |
| **Quando privilegiarlo** | Preparazione tecnica, acqua, teiere, parametri brew, varietà, contesto italiano |
| **KB** | `libri[id=pellegrino]` · PDF: `Manuale per la preparazione del tè - Davide Pellegrino.pdf` |

| id tema | Nome | Pagine chiave |
|---------|------|---------------|
| `pellegrino-pianta` | Coltivazione e lavorazione | 15–17, 20–27, 33 |
| `pellegrino-via-del-te` | Acqua, teiere, preparazione | 11, 45–46, 50–62, 67, 69 |
| `pellegrino-tradizioni` | Tradizioni mondiali | 85–86 (Gong Fu Cha), 91–93 (Chanoyu), 2692–2697 (Rikyu), 2698–2727 (Jeoncha) |
| `pellegrino-salute` | Salute | 2811–2824, 2907–2924, 2938–2964, 2976–2986, 3014–3058 |
| `pellegrino-varietà` | Schede varietà | 76–81 (cucina), 112–122 (cinesi), 123–128 (giapponesi) |

---

### Onuma — `onuma`

| Campo | Valore |
|-------|--------|
| **Titolo** | *El secreto japones del tè verde* |
| **Autore** | Izumi Forasté Onuma |
| **Lingua** | Spagnolo (KB normalizzata in italiano) |
| **Ruolo** | Vita quotidiana giapponese, cerimonia, mindfulness, consumo consapevole |
| **Quando privilegiarlo** | Cultura JP quotidiana, Chanoyu dal vissuto, matcha in cucina, qualità foglie |
| **KB** | `libri[id=onuma]` · PDF: `El secreto japones del te verde - Izumi Foraste Onuma.pdf` |

| id tema | Nome | Pagine chiave |
|---------|------|---------------|
| `onuma-vincolo` | Legame familiare con il tè | 108–131, 123, 165–172 |
| `onuma-storia` | Storia del tè in Giappone | 70, 179–198 (Eisai) |
| `onuma-cerimonia` | Cerimonia e protocollo | 15, 21–22 |
| `onuma-salute-pratica` | Consumo consapevole | 1202–1241, 1242–1253, 1267–1275, 1279–1309, 1312–1348 |
| `onuma-matcha-cucina` | Matcha, pelle, riuso | 23–24, 26, 3600–3619 |

**Nota:** per citazioni letterali verificare `citazioni[].lingua_originale` e `traduzione_it` nel JSON.

---

### Hara — `hara`

| Campo | Valore |
|-------|--------|
| **Titolo** | *Health Benefits of Green Tea* |
| **Autore** | Yukihiko Hara (a cura di) |
| **Lingua** | Inglese (KB in italiano) |
| **Ruolo** | Evidence-based: catechine, meccanismi molecolari, trial clinici, cautela scientifica |
| **Quando privilegiarlo** | Salute, EGCG, cancro, metabolismo, biodisponibilità, integratori vs bevanda |
| **KB** | `libri[id=hara]` · PDF: `Health Benefits of Green Tea - Yukihiko Hara.pdf` |

| id tema | Nome | Pagine chiave |
|---------|------|---------------|
| `hara-panoramica` | Prospettiva scientifica globale | 71, 74, 76–78, 89 |
| `hara-anticancer` | Effetti anticancerogeni | 102–104, 106–108, 110, 113 |
| `hara-metabolismo` | Obesità, metabolismo, cuore | 118, 121, 124, 131 |
| `hara-altri-effetti` | Immunità, fegato, cervello, oral health | 136, 139, 142, 145, 148–152, 165, 171 |

---

## Come citare — regole obbligatorie

### Nel corpo del testo

**Nessuna citazione esplicita** («come scrive Pellegrino…»). La voce resta unitaria; l'ancoraggio alla fonte va in **Fonti** a piè di pagina.

### In sezione Fonti (risposte, articoli, JSON)

Ogni voce deve contenere **almeno due elementi** tra: id libro, id tema KB, sotto-tema, pagina/e.

**Formato canonico:**

```
{id}, tema `{tema_id}`, «{sotto_tema}», pp. {X–Y}
```

**Esempi corretti:**

| Contenuto | Citazione Fonti |
|-----------|-----------------|
| Chanoyu koicha/usucha | `pellegrino`, tema `pellegrino-tradizioni`, «Chanoyu giapponese», pp. 91–93 |
| Umami nel gyokuro | `pellegrino`, tema `pellegrino-via-del-te`, «Umami, quinto sapore», p. 67 |
| EGCG e trial clinici | `hara`, tema `hara-anticancer`, «Trial clinici», p. 113 |
| Eisai elisir della salute | `onuma`, tema `onuma-storia`, «Eisai», p. 196 |
| Terapia in tazza | `rosen`, tema `rosen-poesia`, «Terapia in tazza», p. 181 |
| Scheda sensoriale sencha | `sommelier`, tema `sommelier-degustazione`, pp. (da KB) |

**Esempi da evitare** (troppo vaghi):

- ~~`pellegrino, chanoyu`~~
- ~~`rosen, lavorazione sencha`~~
- ~~`hara, salute`~~

### Workflow prima di scrivere

1. Identifica il **tema trasversale** in `temi_trasversali` (vedi [knowledge-base-guide.md](knowledge-base-guide.md)).
2. Apri i **temi libro** collegati (`temi_libro` o tabella sopra).
3. Individua il **sotto_tema** pertinente e le **pagine** in `sotto_temi[].pagine`.
4. Se serve una citazione letterale, usa `citazioni[]` del tema (testo + `pagina` + `lingua_originale`).
5. In Fonti, riporta id + tema + sotto-tema + pagine.

### Citazioni letterali dalla KB

Quando riporti testo dalla KB in Approfondimento o controversie:

- Usa le virgolette italiane «…»
- Indica sempre: `{id}`, p. {pagina}
- Se `lingua_originale` ≠ `it`, aggiungi traduzione o nota (es. onuma ES, hara EN)

Esempio da `rosen-poesia`:

> «Il tè è letteralmente «terapia in tazza»…» — Rosen, p. 181 (`rosen-poesia`)

### Controversie e più fonti

Presenta posizioni per id libro; in Bibliografia elenca **solo le opere di riferimento** (Rosen, Bisogno/Pettigrew, Pellegrino, Onuma, Hara, Treccani) — non citare `books/knowledge-base.json` nel testo pubblicato.

```
Bibliografia
- hara, tema `hara-anticancer`, pp. 102–104
- rosen, tema `rosen-salute`, «Integratori vs bevanda», pp. 2807–2819
- onuma, tema `onuma-salute-pratica`, «Quantità giornaliera», pp. 1242–1253
```

### JSON del sito (`content/*.json`)

Blocco strutturato `bibliography` (render → sezione **Bibliografia** formale):

```json
{
  "type": "bibliography",
  "items": [
    {
      "author": "Pellegrino, Davide",
      "title": "Manuale per la preparazione del tè",
      "tema": "pellegrino-tradizioni",
      "sotto_tema": "Chanoyu giapponese: koicha e usucha",
      "pages": "91–93"
    }
  ]
}
```

Helper Python: `site_builder.citations.bib_item()` + `bibliography_block()`.

---

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
| `sommelier` | Lung Ching, Sencha, Gyokuro, Matcha, Nilgiri verde |
| `pellegrino` | Long Jing, Bi Lo Chun, Gunpowder, Sencha, Matcha, Gyokuro, Bancha, Jeoncha |
| `rosen` | Gyokuro, Matcha, Bancha, Sencha (lavorazione) |
| `onuma` | Matcha, tè giapponesi quotidiani, cerimonia |
| `hara` | Matcha (catechine), verde generico (salute) |

Parametri brew del sito: [varietà.md](varietà.md).

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

## Riferimenti esterni (secondarie)

| Fonte | Uso | Regola |
|-------|-----|--------|
| [Treccani](https://www.treccani.it) | Definizioni botaniche, chimiche, linguistiche | Solo in **Fonti**; mai unica fonte senza ancoraggio KB |
| *The Story of Tea* (Heiss) | Enciclopedia generale | Integrazione, non primaria |
| *Tea: History, Terroirs, Varieties* (Gascoyne) | Riferimento visivo | Non sostituisce KB |

## Note operative

- **Pellegrino** è l'unico autore italiano nella KB — priorità per acqua, mercato locale, contestualizzazione tecnica.
- **Onuma (ES)** e **Hara (EN)**: la KB estrae in italiano; per trial o citazioni letterali usare pagine e `lingua_originale` nel JSON.
- I PDF non sono nel repository pubblico; i riferimenti puntano alla KB come indice autoritativo delle pagine.
