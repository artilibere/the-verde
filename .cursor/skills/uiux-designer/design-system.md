# Design system — the-verde.it

Design system basato su **Material 3 tokens** implementati come CSS custom properties. Palette brand: **PANTONE 13-6006 TCX Almost Aqua** (`#CAD3C1`). Nessun framework CSS, nessun bundler obbligatorio. Riferimento semantico: [Material 3 color system](https://m3.material.io/styles/color/overview).

## Filosofia visiva

| Principio | Scelta |
|-----------|--------|
| Editoriale gastronomico | Serif misurato per titoli; sans per UI e schede tecniche |
| Calma e lentezza | Spazio bianco generoso; superfici piatte; niente urgency |
| Ponte culturale | Almost Acqua come wash naturale; verde foglia scuro per interazione |
| Specialty, non wellness | Niente verde neon, gradient detox, stock meditazione |
| Performance | System font stack; font serif self-hosted opzionale |

**Estetica:** rivista gastronomica italiana (aria, tipografia curata) + minimalismo funzionale. **Non:** zen kitsch, clipart bamboo, estetica integratore.

---

## Token file: `assets/css/tokens.css`

```css
:root {
  /* Brand — PANTONE 13-6006 TCX Almost Aqua */
  --tv-color-almost-acqua: #cad3c1;
  --tv-color-almost-acqua-rgb: 202, 211, 193;

  /* Color - light scheme */
  --md-sys-color-primary: #3e5c4e;
  --md-sys-color-on-primary: #ffffff;
  --md-sys-color-primary-container: #cad3c1;
  --md-sys-color-on-primary-container: #1a2e24;

  --md-sys-color-secondary: #5a6b55;
  --md-sys-color-on-secondary: #ffffff;
  --md-sys-color-secondary-container: #dde5d8;
  --md-sys-color-on-secondary-container: #1a2118;

  --md-sys-color-tertiary: #4a6359;
  --md-sys-color-on-tertiary: #ffffff;
  --md-sys-color-tertiary-container: #cce8db;
  --md-sys-color-on-tertiary-container: #062018;

  --md-sys-color-surface: #fafaf7;
  --md-sys-color-on-surface: #1c1f1d;
  --md-sys-color-surface-variant: #f0f2ee;
  --md-sys-color-on-surface-variant: #434845;

  --md-sys-color-outline: #737875;
  --md-sys-color-outline-variant: #c3c7c2;

  --md-sys-color-error: #ba1a1a;
  --md-sys-color-on-error: #ffffff;

  /* Typography scale */
  --md-sys-typescale-display-large: 700 2.25rem/1.2 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-headline-large: 600 1.75rem/1.3 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-headline-medium: 600 1.375rem/1.35 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-title-large: 600 1.125rem/1.4 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-title-medium: 600 1rem/1.5 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-body-large: 400 1.0625rem/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-body-medium: 400 1rem/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-label-large: 500 0.875rem/1.4 system-ui, -apple-system, "Segoe UI", sans-serif;
  --md-sys-typescale-label-medium: 500 0.75rem/1.3 system-ui, -apple-system, "Segoe UI", sans-serif;

  /* Editorial serif (self-hosted, optional) */
  --tv-font-serif: "Source Serif 4", Georgia, "Times New Roman", serif;

  /* Shape */
  --md-sys-shape-corner-none: 0;
  --md-sys-shape-corner-extra-small: 4px;
  --md-sys-shape-corner-small: 8px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-full: 9999px;

  /* Elevation (box-shadow) */
  --md-sys-elevation-0: none;
  --md-sys-elevation-1: 0 1px 2px rgba(0, 0, 0, 0.06), 0 1px 3px rgba(0, 0, 0, 0.1);
  --md-sys-elevation-2: 0 2px 6px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.06);

  /* Motion */
  --md-sys-motion-duration-short: 150ms;
  --md-sys-motion-duration-medium: 250ms;
  --md-sys-motion-easing-standard: cubic-bezier(0.2, 0, 0, 1);

  /* Layout - the-verde.it extensions */
  --tv-content-max-width: 72ch;
  --tv-page-max-width: 1200px;
  --tv-spacing-1: 4px;
  --tv-spacing-2: 8px;
  --tv-spacing-3: 16px;
  --tv-spacing-4: 24px;
  --tv-spacing-5: 32px;
  --tv-spacing-6: 48px;
  --tv-spacing-7: 64px;

  /* Sticky offsets */
  --tv-header-height: 64px;
  --tv-mininav-height: 48px;
}
```

### Perché primary scuro e non Almost Acqua

Almost Acqua (`#CAD3C1`) ha luminosità ~79% — insufficiente per testo e bottoni (contrasto WCAG AA). Usarlo come **brand wash** (`primary-container`, hero, chip soft); il verde foglia scuro `#3E5C4E` su sfondo `#FAFAF7` raggiunge ~7.5:1 (AA/AAA body text come link/CTA).

### Dark scheme (opzionale, `prefers-color-scheme`)

```css
@media (prefers-color-scheme: dark) {
  :root {
    --md-sys-color-primary: #8fb5a0;
    --md-sys-color-on-primary: #1a2e24;
    --md-sys-color-primary-container: #2d4036;
    --md-sys-color-on-primary-container: #cad3c1;
    --md-sys-color-surface: #1a1c1a;
    --md-sys-color-on-surface: #e2e3e1;
    --md-sys-color-surface-variant: #2a2c2a;
    --md-sys-color-on-surface-variant: #c4c7c2;
    --md-sys-color-outline-variant: #444746;
    --tv-color-almost-acqua: #3d4a3e;
  }
}
```

---

## Tipografia

| Elemento | Token / stile | Uso |
|----------|---------------|-----|
| H1 pagina | `tv-font-serif` + `headline-large` | Titolo varietà, hero home |
| H2 sezione | `headline-medium` | Prepara, Approfondisci, In Italia |
| H3 FAQ | `title-medium` | Domanda singola (in `<summary>`) |
| Body | `body-large` | Paragrafi, In breve |
| Meta / chip | `label-medium` | Origine, caffeina, stagione |
| Dati preparazione | `title-large` + tabular nums | °C, grammi, secondi in brew-card |

**Regole:**

- Max **72ch** per blocchi di testo (`max-width: var(--tv-content-max-width)`)
- Grassetto solo su parole chiave (the-verde-expert), non interi paragrafi
- Link: colore `--md-sys-color-primary`, sottolineatura al focus/hover
- Termini tecnici: `<abbr class="tv-term" title="...">` con stile tratteggio sottile

---

## Spacing e layout

```
Pagina
??? tv-header (sticky, --tv-header-height)
??? main.tv-main (max-width: --tv-page-max-width, margin auto, padding --tv-spacing-4)
?   ??? tv-breadcrumb
?   ??? article.tv-article (max-width: --tv-content-max-width per body)
?   ??? aside (solo catalogo desktop: filtri)
??? tv-footer
```

| Breakpoint | Valore | Comportamento |
|------------|--------|---------------|
| `sm` | 0–599px | Colonna singola; filtri in drawer; PathNav sticky bottom |
| `md` | 600–899px | Griglia catalogo 2 colonne |
| `lg` | 900px+ | Sidebar filtri catalogo; griglia 3 colonne; mini-nav sticky sotto header |

```css
/* Breakpoint helpers (in base.css) */
@media (min-width: 600px) { /* md */ }
@media (min-width: 900px) { /* lg */ }
```

---

## Zone scheda varietà

### Scopri (above the fold)

- Hero leggero con wash `--tv-color-almost-acqua` opzionale (10–15% opacity su surface)
- Blocco unificato `.tv-scopri`: breadcrumb + In breve + `tv-brew-card` + `tv-sensory-profile` + `tv-origin-chips`
- Obiettivo: orientamento in **10 secondi** senza scroll (test Elena)

### Prepara (agire)

- Passaggi in `.tv-step-list` con numeri prominenti e badge tempo
- Lista attrezzatura compatta; max 5 item

### Approfondisci (restare sul sito)

- `tv-italy-box` con sfondo `--md-sys-color-primary-container` leggero
- FAQ in `<details>` (elevation-0)
- RelatedLinks in card outlined (bordo `--md-sys-color-outline-variant`)
- PathNav: barra fissa in basso su mobile (`position: fixed; bottom: 0`)

---

## Componenti M3 mappati

| Pattern M3 | Implementazione tv-* |
|------------|---------------------|
| Top app bar | `tv-header` |
| Filled button | `tv-btn--filled` (CTA unica) |
| Outlined button | `tv-btn--outlined` (nav secondaria) |
| Assist chip | `tv-chip` (link a hub origine/stile) |
| Filter chip | `tv-chip--filter` (catalogo, stato attivo) |
| Card elevated | `tv-card` (catalogo) |
| Card outlined | `tv-card--outlined` (correlati) |
| Navigation drawer | `tv-drawer` (menu mobile) |

---

## Stati interattivi

Tutti i controlli focusabili:

```css
:focus-visible {
  outline: 2px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}
```

### Contrasto verificato (light scheme)

| Coppia | Rapporto | Uso |
|--------|----------|-----|
| `#3E5C4E` su `#FAFAF7` | ~7.5:1 | Link, CTA, focus |
| `#1C1F1D` su `#FAFAF7` | ~16:1 | Body text |
| `#1A2E24` su `#CAD3C1` | ~8:1 | Testo su primary-container |
| `#FFFFFF` su `#3E5C4E` | ~7.5:1 | Testo su bottone filled |

- Contrasto minimo **WCAG AA** (4.5:1 body, 3:1 large text)
- `:hover` su link e chip: leggero cambio background (`--md-sys-color-surface-variant`)
- Transizioni: solo `color`, `background-color`, `box-shadow` con `--md-sys-motion-duration-short`

---

## Fotografia e immagini

| Fare | Non fare |
|------|----------|
| Luce naturale, ceramica, vapore, foglia | Modelli in posa yoga/meditazione |
| Macro texture tè secco | Stock "donna con tazza zen" |
| Teiere kyusu/gaiwan in contesto | Filtri verdi neon, overlay detox |
| Aspect ratio coerente (3:2 o 4:3) | Clip art bamboo, lanterne |

Placeholder: sfondo `--md-sys-color-surface-variant` con rapporto d'aspetto fisso; `alt` descrittivo (es. "Foglie di sencha prima infusione").

---

## Icone

Preferire **SVG inline** minimali (freccia, menu, close, termometro stilizzato) — nessun icon font esterno. Colore: `currentColor` ereditato da testo.

---

## Anti-pattern visivi

- Emoji negli heading o nei chip
- Ombre pesanti o gradienti wellness (verde?lime)
- Più di un colore accento in competizione
- Card annidate eccessivamente
- Font size sotto 16px per body su mobile
- Estetica "Asia generica" (pattern wave, font brush)
- Badge "detox", "dimagrante", "superfood"
- Almost Acqua come colore testo su sfondo chiaro (contrasto insufficiente)
