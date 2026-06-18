# Personas UX — the-verde.it

Riferimento per l'agente UI/UX Designer. Le personas sono **inferite** da [cultura-italiana.md](../the-verde-expert/cultura-italiana.md) e dai formati contenuto in [the-verde-expert/SKILL.md](../the-verde-expert/SKILL.md).

## Principio guida

Scrivi e progetta prima per **Elena** (curiosa del gusto). La stessa pagina deve servire anche Luca, Giulia e Marco **senza versioni separate**  modulazione per sezione, non per URL.

---

## Elena  la Curiosa del Gusto (prioritaria)

| Campo | Dettaglio |
|-------|-----------|
| Età | 38 |
| Contesto | Milano o Torino; appassionata di vino e olio EVO; legge Slow Food e guide gastronomiche |
| Obiettivo | Capire se un tè verde vale l'investimento; confrontarlo con abitudini italiane (caffè, degustazione) |
| Frustrazioni | Bustine scadenti che "sanno di erba"; marketing detox; nomi esotici senza spiegazione |
| Scenario | Cerca "sencha vs gyokuro" dopo un pranzo in un ristorante giapponese; vuole scheda rapida e abbinamenti |

**Priorità UI:** `tv-metric-row`, `tv-card` sensory, card `italy`, `tv-data-table` per confronti.

---

## Luca  il Neofita Scettico

| Campo | Dettaglio |
|-------|-----------|
| Età | 32 |
| Contesto | Ha provato tè verde in bustina al supermercato; curioso sul benessere ma allergico all'hype |
| Obiettivo | Capire se il tè verde è per lui senza sentirsi in un funnel wellness |
| Frustrazioni | Badge "detox", promesse dimagranti, tono da guru |
| Scenario | Atterra da Google su "tè verde fa bene"; deve trovare tono sobrio e dati onesti |

**Priorità UI:** copy sobrio; box "miti da sfatare" in Approfondisci; niente CTA detox; disclaimer salute leggero se pertinente.

---

## Giulia  l'Appassionata Specialty

| Campo | Dettaglio |
|-------|-----------|
| Età | 29 |
| Contesto | Ha kyusu o teiera occidentale; segue tea shop e corsi; conosce differenza sencha/gyokuro/matcha |
| Obiettivo | Perfezionare preparazione (°C, grammi, tempi); esplorare varietà e rituali |
| Frustrazioni | Guide superficiali; temperature sbagliate consigliate; fusione generica "tè orientale" |
| Scenario | Vuole scheda tecnica completa e percorso guidato dal bancha al matcha |

**Priorità UI:** `tv-step-list`, `tv-term`, `tv-path-nav`, `tv-scroll-rail` sezioni, `tv-chart`+tabella per confronti tecnici.

---

## Marco  il Regalo Consapevole

| Campo | Dettaglio |
|-------|-----------|
| Età | 45 |
| Contesto | Compra regali per Natale, compleanni, ospiti; cerca qualità senza kitsch orientale |
| Obiettivo | Scegliere un set degustazione o varietà regalo con fiducia |
| Frustrazioni | Packaging esotico kitsch; difficoltà a capire differenze tra varietà |
| Scenario | Cerca "regalo tè verde" a novembre; ha bisogno di card chiare e hub stagionali |

**Priorità UI:** `tv-variety-card`, hub stagione, `tv-cta` leggero ("Scopri i set" non "Compra ora"); profilo sintetico su ogni card.

---

## Matrice persona × componente

| Componente | Elena | Luca | Giulia | Marco |
|------------|:-----:|:----:|:------:|:-----:|
| `tv-metric-row` | ★★★ | ★★ | ★★★ | ★★ |
| `tv-card` (sensory) | ★★★ | ★ | ★★ | ★★ |
| `tv-card` (italy) | ★★★ | ★★ | ★ | ★★ |
| `tv-step-list` | ★★ | ★★ | ★★★ | ★ |
| `tv-data-table` | ★★ | ★★ | ★★★ | ★★ |
| `tv-chart` | ★★ | ★ | ★★ | ★ |
| `tv-bottom-nav` | ★★ | ★★ | ★★ | ★★★ |
| `tv-origin-chips` | ★★ | ★★ | ★★★ | ★★ |
| `tv-faq` | ★★ | ★★★ | ★★ | ★ |
| `tv-path-nav` | ★ | ★★ | ★★★ | ★ |
| `tv-variety-card` | ★★★ | ★★ | ★★ | ★★★ |
| `tv-scroll-rail` | ★★ | ★ | ★★ | ★★ |

Legenda: ★ = utile; ★★★ = critico.

---

## Modulazione UI (stessa pagina, enfasi diversa)

| Sezione pagina | Enfasi Elena | Enfasi Luca | Enfasi Giulia | Enfasi Marco |
|----------------|--------------|-------------|---------------|--------------|
| Prima card feed | Profilo sensoriale | Tono sobrio | Metriche preparazione | Card compatte |
| Scroll / nav | Bottom nav + scan card | No hype in card | Step card dettagliata | Entry hub stagione |

Non servono landing separate per persona: la gerarchia visiva (ordine, peso tipografico) orienta ciascun profilo.

---

## Test di validazione UX

Prima di considerare un layout completo, verifica:

### Mobile e app (tutte le personas)
- [ ] Navigazione possibile con una mano (bottom nav + thumb)?
- [ ] Informazione chiave in prima card senza scroll?
- [ ] Icone riconoscibili con label testuale?
- [ ] Touch target ≥ 44px su tab e CTA?

### Scan 10 secondi (Elena)
- [ ] Origine e stile visibili senza scroll?
- [ ] Profilo sensoriale o scheda rapida above-the-fold?
- [ ] "In Italia" raggiungibile con massimo uno scroll?

### Fiducia senza hype (Luca)
- [ ] Nessun badge detox, dimagrante o "miracolo"?
- [ ] CTA primaria educativa ("Esplora", "Scopri") non commerciale aggressiva?
- [ ] Salute citata con sobrietà, non come hook?

### Profondità tecnica (Giulia)
- [ ] °C, g/100ml, secondi in `tv-metric-row`?
- [ ] Passaggi preparazione numerati con tempi?
- [ ] Termini tecnici con glossa al primo uso?

### Dati comparativi (Giulia / Elena)
- [ ] Tabella leggibile su 390px (scroll orizzontale ok)?
- [ ] Chart solo se presente tabella fallback?
### Scelta guidata (Marco)
- [ ] Card catalogo con profilo sintetico e icona?
- [ ] Hub stagione o momento da bottom nav?

---

## Momenti d'uso (da cultura-italiana)

Collegare hub e filtri ai momenti italiani documentati:

| Momento | Varietà tipica | Hub |
|---------|----------------|-----|
| Colazione | Bancha, kukicha, genmaicha | `/per-momento/colazione/` |
| Pausa (10:00, 16:00) | Sencha, oolong leggero | `/per-momento/pausa/` |
| Dopo cena | Hojicha, kukicha | `/per-momento/dopo-cena/` |
| Aperitivo | Cold brew gyokuro, hojicha freddo | `/per-momento/aperitivo/` |

Questi hub servono Elena (abbinamenti) e Marco (contesto regalo/stagione) senza escludere Giulia.
