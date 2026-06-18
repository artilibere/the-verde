# Charts d3.js — the-verde.it

Standard per **dati analitici**: tabella HTML come default e fonte di verità; chart d3.js solo quando semplifica la lettura comparativa.

Vedi: [componenti.md](componenti.md) (`tv-data-table`, `tv-chart`), [design-system.md](design-system.md) (token chart).

---

## Stack

| Asset | Path |
|-------|------|
| d3.js v7 | `assets/js/vendor/d3.min.js` (self-hosted, no CDN obbligatorio) |
| Modulo charts | `assets/js/charts.js` |
| Init pagina | `defer` dopo DOM; lazy via `IntersectionObserver` |

### API

```javascript
// charts.js
const TvChart = {
  init(container, spec) { /* ... */ },
  destroy(container) { /* ... */ }
};
```

`spec` da attributo `data-chart` (JSON) o generato in build nel `PageDocument`.

```html
<div class="tv-chart"
     data-chart='{"type":"bar-horizontal","series":[{"label":"Sencha","value":75}],"dimension":"brew_temp","unit":"°C"}'
     role="img"
     aria-label="Confronto temperature di infusione per varietà">
</div>
```

---

## Matrice decisione (obbligatoria)

Prima di ogni visualizzazione, l'agente applica questa tabella:

| Scenario | Formato primario | Chart d3 |
|----------|------------------|----------|
| Parametri 1 varietà (°C, g, sec) | `tv-metric-row` con icone | **Mai** |
| Confronto 2–4 varietà, 2–3 parametri | `tv-data-table` | Barre raggruppate se confronto visivo aiuta |
| Confronto 5+ varietà, 1 parametro | Tabella ordinata | Barre orizzontali |
| Profilo sensoriale 4 assi, 1 varietà | Tabella / lista | **Mai** |
| Profilo sensoriale, 2 varietà | Tabella | Radar **opzionale** |
| Infusioni multiple (tempi per round) | Tabella step | Linea a gradini |
| Ranking caffeina | Tabella | Barre orizzontali con scala comune |
| Stagionalità / calendario | Card per stagione | Griglia icone, no chart forzato |

**Regola:** se il chart non supera la tabella in chiarezza per la persona Elena (scan 10 sec), resta solo tabella.

---

## Regola d'oro: tabella fallback

Ogni `tv-chart` **deve** avere tabella HTML associata:

```html
<div class="tv-card" id="confronto">
  <header class="tv-card__header">...</header>
  <div class="tv-card__body">
    <table class="tv-data-table">
      <caption class="visually-hidden">Confronto parametri preparazione</caption>
      <thead>...</thead>
      <tbody>...</tbody>
    </table>
    <div class="tv-chart" data-chart="..." role="img" aria-label="..."></div>
  </div>
</div>
```

- Senza JS: tabella visibile, chart assente — sito usabile
- Con JS: chart sotto o accanto; tabella resta per screen reader e copy/export
- Opzione CSS: `.tv-chart ~ .tv-data-table` visibile sempre; chart come enhancement sopra su `md+`

---

## Tipi chart supportati

| `type` | d3 modules | Uso |
|--------|------------|-----|
| `bar-horizontal` | scales, axis, selection | Ranking, caffeina, un parametro |
| `bar-grouped` | scales, axis | 2–4 varietà × 2–3 metriche |
| `line-step` | line, curveStepAfter | Infusioni multiple nel tempo |
| `radar` | line, radial | Solo confronto 2 varietà sensoriale |

Non implementare: pie chart decorativi, gauge wellness, donut "percentuale salute".

---

## Palette chart (token)

```css
:root {
  --tv-chart-primary: #3e5c4e;
  --tv-chart-secondary: #5a6b55;
  --tv-chart-container: #cad3c1;
  --tv-chart-grid: var(--md-sys-color-outline-variant);
  --tv-chart-label: var(--md-sys-color-on-surface-variant);
  --tv-chart-font: system-ui, sans-serif;
}
```

- Barre: fill `--tv-chart-primary`; hover leggermente più scuro
- Griglia: stroke `--tv-chart-grid`, opacity 0.5
- Testo assi: `--tv-chart-label`, min 12px mobile
- Max 4 serie colori distinte; oltre → solo tabella

---

## Accessibilità

- Container: `role="img"` + `aria-label` descrittivo con i valori chiave
- Non trasmettere informazione **solo** colore — etichette su assi o legenda testuale
- Tabella sempre nel DOM con stessi numeri del chart
- `prefers-reduced-motion`: non animare transizioni d3
- Focus: chart non interattivo per default; se drill-down, serve alternativa keyboard

---

## Performance

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      TvChart.init(entry.target, JSON.parse(entry.target.dataset.chart));
      observer.unobserve(entry.target);
    }
  });
}, { rootMargin: '100px' });

document.querySelectorAll('.tv-chart[data-chart]').forEach((el) => observer.observe(el));
```

- Init solo quando card entra in viewport
- `destroy` su navigazione se SPA parziale in futuro; su statico non critico
- Dimensioni SVG/container: `width: 100%`; altezza fissa da spec (es. 200px mobile, 280px desktop)

---

## Spec JSON esempi

### Barre orizzontali (caffeina)

```json
{
  "type": "bar-horizontal",
  "dimension": "caffeina",
  "unit": "mg approx",
  "series": [
    { "label": "Bancha", "value": 10 },
    { "label": "Sencha", "value": 30 },
    { "label": "Gyokuro", "value": 25 }
  ]
}
```

### Barre raggruppate (preparazione)

```json
{
  "type": "bar-grouped",
  "dimensions": [
    { "key": "brew_temp", "label": "°C" },
    { "key": "brew_grams", "label": "g/100ml" }
  ],
  "series": [
    { "label": "Sencha", "values": [75, 3] },
    { "label": "Gyokuro", "values": [60, 4] }
  ]
}
```

### Nel PageDocument (card body)

```json
{
  "id": "confronto",
  "title": "Confronto",
  "body": {
    "type": "comparison",
    "table": { "headers": [...], "rows": [...] },
    "chart": { "type": "bar-grouped", ... }
  }
}
```

---

## Anti-pattern chart

- Chart per singola varietà (usa metric-row)
- Chart senza tabella
- Pie chart decorativi
- Gauge "livello detox" o salute
- Animazioni lunghe (> 500ms)
- CDN d3 senza fallback offline build
- Colori fuori palette brand

---

## Checklist chart

- [ ] Matrice decisione applicata
- [ ] Tabella HTML presente con stessi dati
- [ ] `aria-label` sul container chart
- [ ] Palette token Almost Acqua / primary scuro
- [ ] Lazy init con IntersectionObserver
- [ ] Funziona senza JS (solo tabella)
