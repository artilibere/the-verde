# Icone — the-verde.it

Vocabolario iconografico per navigazione guidata da **simboli + label**. Lineari, geometriche, dominio tè — mai clipart zen (bamboo, lanterne, meditazione).

Vedi: [app-shell.md](app-shell.md), [componenti.md](componenti.md).

---

## Asset

- File sprite: `assets/icons/tv-icons.svg`
- Pattern: `<symbol id="tv-icon-*" viewBox="0 0 24 24">` con path stroke
- Stile: stroke **1.5px**, `stroke-linecap="round"`, `fill="none"`, `currentColor`
- ViewBox: 24×24
- Nessun font-icon pack (Font Awesome, Material Icons font, ecc.)

---

## Setta semantica

| ID symbol | Uso UI |
|-----------|--------|
| `tv-icon-leaf` | Varietà, catalogo, bottom nav Varietà |
| `tv-icon-cup` | Preparazione, momenti, bottom nav Momenti |
| `tv-icon-book` | Guide editoriali, bottom nav Guide |
| `tv-icon-thermo` | Temperatura °C |
| `tv-icon-scale` | Dosaggio g/100ml |
| `tv-icon-timer` | Secondi infusione |
| `tv-icon-map` | Origine geografica |
| `tv-icon-italy` | Box In Italia |
| `tv-icon-nose` | Profilo aroma |
| `tv-icon-drop` | Profilo gusto / retrogusto |
| `tv-icon-sun` | Stagione primavera/estate, bottom nav Stagioni |
| `tv-icon-snow` | Stagione autunno/inverno |
| `tv-icon-path` | Percorso guidato, PathNav |
| `tv-icon-filter` | Filtri catalogo |
| `tv-icon-chevron-left` | Back, prev |
| `tv-icon-chevron-right` | Next |
| `tv-icon-grid` | Panoramica / Scopri |
| `tv-icon-list` | Prepara / passaggi |
| `tv-icon-info` | Approfondisci |

---

## Componente `tv-icon`

```html
<svg class="tv-icon tv-icon--md" aria-hidden="true" focusable="false">
  <use href="/assets/icons/tv-icons.svg#tv-icon-leaf"></use>
</svg>
```

### Dimensioni

| Classe | Size | Uso |
|--------|------|-----|
| `tv-icon--sm` | 16px | Inline in chip, badge |
| `tv-icon--md` | 24px | Header card, bottom nav |
| `tv-icon--lg` | 32px | Entry point home |

```css
.tv-icon {
  display: inline-block;
  width: 1.5rem;
  height: 1.5rem;
  vertical-align: middle;
  color: var(--md-sys-color-primary);
}
.tv-icon--sm { width: 1rem; height: 1rem; }
.tv-icon--lg { width: 2rem; height: 2rem; }
```

---

## Regole d'uso

### Obbligatorio

- **Ogni card** nel feed: icona nell'header (`tv-card__icon`)
- **Ogni tab** bottom-nav: icona sopra label
- **Ogni tab** mininav sezione: icona + label breve
- **Ogni metrica** in `tv-metric-row`: icona dedicata (thermo, scale, timer)
- **Label testuale sempre presente** accanto o sotto l'icona — mai UI solo-icona senza testo accessibile

### Accessibilità

- Icone decorative: `aria-hidden="true"`
- Tab bottom-nav: label in `<span class="tv-bottom-nav__label">` + `aria-label` sul link se label visivamente piccola
- Bottone solo icona (back, filtra): `aria-label` obbligatorio in italiano ("Indietro", "Filtra varietà")
- Contrasto icona: `currentColor` su sfondo card/surface — verificare WCAG AA

### Coerenza

- Stesso simbolo = stesso significato su tutto il sito
- Non riusare `tv-icon-leaf` per "bio" o wellness generico
- Non aggiungere icone decorative senza funzione semantica

---

## Bottom nav markup

```html
<nav class="tv-bottom-nav" aria-label="Navigazione principale">
  <a href="/varietà/" class="tv-bottom-nav__item" aria-current="page">
    <svg class="tv-icon tv-icon--md" aria-hidden="true">
      <use href="/assets/icons/tv-icons.svg#tv-icon-leaf"></use>
    </svg>
    <span class="tv-bottom-nav__label">Varietà</span>
  </a>
  <!-- Momenti, Stagioni, Guide -->
</nav>
```

---

## Card header con icona

```html
<article class="tv-card" id="brew">
  <header class="tv-card__header">
    <svg class="tv-icon tv-icon--md tv-card__icon" aria-hidden="true">
      <use href="/assets/icons/tv-icons.svg#tv-icon-thermo"></use>
    </svg>
    <h2 class="tv-card__title">Preparazione</h2>
  </header>
  <div class="tv-card__body">...</div>
</article>
```

---

## Anti-pattern icone

- Font icon esterni
- Emoji come icone UI
- Illustrazioni raster in header card
- Icone zen (bamboo, loto, persona in meditazione)
- Icone senza label su azioni principali
- Set misti (lineari + filled da famiglie diverse)

---

## Checklist icone

- [ ] Sprite self-hosted in repo site
- [ ] Ogni sezione feed ha icona header
- [ ] Bottom nav 4 tab con icona + label
- [ ] Bottoni icon-only hanno `aria-label`
- [ ] Stroke e dimensioni coerenti in tutto lo sprite
