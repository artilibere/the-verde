# Componenti UI — the-verde.it

Libreria componenti HTML/CSS vanilla con prefisso BEM `tv-*`. Token: [design-system.md](design-system.md). Shell: [app-shell.md](app-shell.md). Icone: [icone.md](icone.md).

---

## App shell e feed (priorità mobile)

### AppBar (`tv-app-bar`)

Header compatto mobile — sostituisce `tv-header` su `sm`.

```html
<header class="tv-app-bar" role="banner">
  <div class="tv-app-bar__inner">
    <a href="/varietà/" class="tv-app-bar__back" aria-label="Indietro">
      <svg class="tv-icon" aria-hidden="true"><use href="/assets/icons/tv-icons.svg#tv-icon-chevron-left"/></svg>
    </a>
    <h1 class="tv-app-bar__title">Sencha</h1>
    <button type="button" class="tv-app-bar__action" aria-label="Filtra varietà">
      <svg class="tv-icon" aria-hidden="true"><use href="/assets/icons/tv-icons.svg#tv-icon-filter"/></svg>
    </button>
  </div>
</header>
```

**CSS:** `height: var(--tv-app-bar-height); position: sticky; top: 0; z-index: 100;`

### BottomNav (`tv-bottom-nav`)

```html
<nav class="tv-bottom-nav" aria-label="Navigazione principale">
  <a href="/varietà/" class="tv-bottom-nav__item tv-bottom-nav__item--active">
    <svg class="tv-icon tv-icon--md" aria-hidden="true"><use href="/assets/icons/tv-icons.svg#tv-icon-leaf"/></svg>
    <span class="tv-bottom-nav__label">Varietà</span>
  </a>
  <!-- Momenti, Stagioni, Guide -->
</nav>
```

**CSS:** `position: fixed; bottom: 0; left: 0; right: 0; height: calc(var(--tv-bottom-nav-height) + var(--tv-safe-bottom)); padding-bottom: var(--tv-safe-bottom);`

### Feed (`tv-feed`)

```html
<main id="main" class="tv-feed">
  <!-- tv-card × N -->
</main>
```

**CSS:** `display: flex; flex-direction: column; gap: var(--tv-feed-gap); max-width: var(--tv-feed-max-width); margin: 0 auto; padding: var(--tv-spacing-3);`

### Card (`tv-card`)

```html
<article class="tv-card" id="brew">
  <header class="tv-card__header">
    <svg class="tv-icon tv-icon--md tv-card__icon" aria-hidden="true"><use href="...#tv-icon-thermo"/></svg>
    <h2 class="tv-card__title">Preparazione</h2>
  </header>
  <div class="tv-card__body">
    <!-- partial: prose, metrics, table, chart -->
  </div>
</article>
```

**CSS:** `background: var(--md-sys-color-surface); border-radius: var(--tv-card-radius); box-shadow: var(--md-sys-elevation-1); padding: var(--tv-spacing-3);`

### MetricRow (`tv-metric-row`)

```html
<div class="tv-metric-row" role="group" aria-label="Parametri preparazione">
  <div class="tv-metric-row__item">
    <svg class="tv-icon tv-icon--sm" aria-hidden="true"><use href="...#tv-icon-thermo"/></svg>
    <span class="tv-metric-row__value">75</span><span class="tv-metric-row__unit">°C</span>
  </div>
  <!-- scale, timer -->
</div>
```

### DataTable (`tv-data-table`)

```html
<div class="tv-data-table-wrap">
  <table class="tv-data-table">
    <caption class="visually-hidden">Confronto varietà</caption>
    <thead><tr><th>Varietà</th><th>°C</th><th>g</th></tr></thead>
    <tbody>...</tbody>
  </table>
</div>
```

**Mobile:** wrapper `overflow-x: auto; -webkit-overflow-scrolling: touch;`

### Chart (`tv-chart`)

Vedi [charts-d3.md](charts-d3.md). Sempre affiancato a `tv-data-table`.

```html
<table class="tv-data-table">...</table>
<div class="tv-chart" data-chart="{...}" role="img" aria-label="..."></div>
```

### Grid (`tv-grid`)

Griglia responsive per card catalogo, tile home, meta in scheda. **Mai 3+ colonne** con testo leggibile — vedi [design-system.md § Griglie](design-system.md#griglie-responsive-tv-grid).

```html
<!-- Catalogo: 1 col mobile, 2 col da md -->
<div class="tv-grid tv-grid--cards tv-grid--2-up-md" id="variety-grid">
  <!-- tv-variety-card × N -->
</div>

<!-- Home entry point (solo icona + label breve, no paragrafi) -->
<div class="tv-grid tv-grid--tiles tv-grid--2-up-md" role="list">
  <a href="/stagioni/primavera/" class="tv-card tv-card--tile" role="listitem">…</a>
</div>
```

**Modificatori:**

| Classe | Uso |
|--------|-----|
| `tv-grid--cards` | Lista `tv-variety-card` in catalogo/hub |
| `tv-grid--tiles` | Entry point compatti (home stagioni, hub correlati) |
| `tv-grid--2-up-md` | 2 colonne solo da `min-width: 600px` |
| *(nessun `--3-up`)* | **Vietato** — testo troppo stretto |

**CSS:**

```css
.tv-grid { display: grid; gap: var(--tv-feed-gap); grid-template-columns: 1fr; }
@media (min-width: 600px) {
  .tv-grid--2-up-md {
    grid-template-columns: repeat(2, minmax(min(100%, var(--tv-grid-min-col-width)), 1fr));
  }
}
```

**Anti-pattern:** `grid-template-columns: repeat(3, 1fr)` o `repeat(4, 1fr)` su box con `tv-prose__p`, brief card o meta testuali.

### ScrollRail (`tv-scroll-rail`)

```html
<div class="tv-scroll-rail" role="tablist" aria-label="Sezioni">
  <a href="#brief" class="tv-scroll-rail__item tv-scroll-rail__item--active" role="tab">
    <svg class="tv-icon tv-icon--sm" aria-hidden="true"><use href="...#tv-icon-grid"/></svg>
    <span>Scopri</span>
  </a>
  <!-- Prepara, Approfondisci -->
</div>
```

### Prose (partial)

Markup generato da [rendering-json-html.md](rendering-json-html.md) — classi `tv-prose__*`.

---

## SiteHeader (`tv-header`)

Barra superiore sticky. Top app bar M3.

```html
<header class="tv-header" role="banner">
  <div class="tv-header__inner">
    <a href="/" class="tv-header__logo" aria-label="The Verde - Home">
      <span class="tv-header__logo-text">The Verde</span>
    </a>
    <button type="button" class="tv-header__menu-btn" aria-expanded="false" aria-controls="tv-nav-drawer" aria-label="Apri menu">
      <!-- SVG hamburger -->
    </button>
    <nav class="tv-header__nav" aria-label="Navigazione principale">
      <ul class="tv-header__nav-list">
        <li><a href="/varietà/">Varietà</a></li>
        <li class="tv-header__nav-item--has-submenu">
          <button type="button" aria-expanded="false" aria-controls="tv-submenu-momento">Per momento</button>
          <ul id="tv-submenu-momento" class="tv-header__submenu" hidden>
            <li><a href="/per-momento/colazione/">Colazione</a></li>
            <li><a href="/per-momento/pausa/">Pausa</a></li>
            <li><a href="/per-momento/dopo-cena/">Dopo cena</a></li>
            <li><a href="/per-momento/aperitivo/">Aperitivo</a></li>
          </ul>
        </li>
        <li><a href="/stagioni/">Stagioni</a></li>
        <li><a href="/guide/">Guide</a></li>
      </ul>
    </nav>
  </div>
</header>
```

**CSS:** `position: sticky; top: 0; z-index: 100; background: var(--md-sys-color-surface); border-bottom: 1px solid var(--md-sys-color-outline-variant); height: var(--tv-header-height);`

**JS (`nav.js`):** toggle drawer mobile; focus trap nel drawer; chiudi con Esc; submenu keyboard-navigable.

**ARIA:** `aria-expanded` su menu button e submenu; `aria-current="page"` sul link attivo.

---

## Breadcrumb (`tv-breadcrumb`)

```html
<nav class="tv-breadcrumb" aria-label="Breadcrumb">
  <ol class="tv-breadcrumb__list" itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a href="/" itemprop="item"><span itemprop="name">Home</span></a>
      <meta itemprop="position" content="1">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a href="/varietà/" itemprop="item"><span itemprop="name">Varietà</span></a>
      <meta itemprop="position" content="2">
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem" aria-current="page">
      <span itemprop="name">Sencha</span>
      <meta itemprop="position" content="3">
    </li>
  </ol>
</nav>
```

**Mobile:** tronca con `
` se troppo lungo; ultimo item sempre visibile.

---

## BrewCard (`tv-brew-card`)

Scheda rapida preparazione  critica per Elena e Giulia. Sostituisce QuickInfoTable per il dominio tè.

```html
<dl class="tv-brew-card" aria-label="Parametri di preparazione">
  <div class="tv-brew-card__row">
    <dt class="tv-brew-card__label">Temperatura</dt>
    <dd class="tv-brew-card__value"><span class="tv-brew-card__number">75</span>°C</dd>
  </div>
  <div class="tv-brew-card__row">
    <dt class="tv-brew-card__label">Dosaggio</dt>
    <dd class="tv-brew-card__value"><span class="tv-brew-card__number">3</span> g / 100 ml</dd>
  </div>
  <div class="tv-brew-card__row">
    <dt class="tv-brew-card__label">Prima infusione</dt>
    <dd class="tv-brew-card__value"><span class="tv-brew-card__number">60</span> sec</dd>
  </div>
  <div class="tv-brew-card__row">
    <dt class="tv-brew-card__label">Infusioni</dt>
    <dd class="tv-brew-card__value">23</dd>
  </div>
</dl>
```

**CSS:** sfondo `--md-sys-color-primary-container`; border-radius `--md-sys-shape-corner-medium`; numeri con `font-variant-numeric: tabular-nums; font: var(--md-sys-typescale-title-large);`

**Layout responsive (legacy `.tv-scopri__meta`):** 1 colonna su `sm`; 2 colonne max su `md`+ — **non** 3 o 4 colonne (metriche illeggibili).

---

## SensoryProfile (`tv-sensory-profile`)

Profilo sensoriale da scheda varietà the-verde-expert.

```html
<dl class="tv-sensory-profile" aria-label="Profilo sensoriale">
  <div class="tv-sensory-profile__row">
    <dt class="tv-sensory-profile__label">Aspetto</dt>
    <dd class="tv-sensory-profile__value">Ago sottili, verde brillante</dd>
  </div>
  <div class="tv-sensory-profile__row">
    <dt class="tv-sensory-profile__label">Aroma</dt>
    <dd class="tv-sensory-profile__value">Vegetale, erba tagliata, note marine leggere</dd>
  </div>
  <div class="tv-sensory-profile__row">
    <dt class="tv-sensory-profile__label">Gusto</dt>
    <dd class="tv-sensory-profile__value">Umami delicato, amaro controllato</dd>
  </div>
  <div class="tv-sensory-profile__row">
    <dt class="tv-sensory-profile__label">Retrogusto</dt>
    <dd class="tv-sensory-profile__value">Persistente, fresco</dd>
  </div>
</dl>
```

**Nota:** usare lessico degustazione italiano (the-verde-expert), non anglicismi inutili.

---

## ItalyBox (`tv-italy-box`)

Box "In Italia"  obbligatorio in scheda varietà.

```html
<aside class="tv-italy-box" aria-labelledby="italy-heading">
  <h2 id="italy-heading" class="tv-italy-box__title">In Italia</h2>
  <div class="tv-italy-box__content">
    <p>Trovabile nei tea shop specialty di Milano, Roma e Torino. Abbinamento sensato con pesce crudo o sashimi.</p>
    <p><strong>Errore comune:</strong> acqua bollente  amaro eccessivo e pregiudizio sul verde.</p>
  </div>
</aside>
```

**CSS:** `background: color-mix(in srgb, var(--tv-color-almost-acqua) 40%, var(--md-sys-color-surface)); border-left: 4px solid var(--md-sys-color-primary); padding: var(--tv-spacing-4); border-radius: var(--md-sys-shape-corner-small);`

---

## OriginChips (`tv-origin-chips`)

Assist chip M3  link verso hub origine e stile.

```html
<div class="tv-origin-chips" role="list" aria-label="Origine e stile">
  <a href="/origine/giappone/" class="tv-chip" role="listitem">Giappone</a>
  <a href="/stile/sencha/" class="tv-chip" role="listitem">Sencha</a>
  <a href="/caffeina/media/" class="tv-chip" role="listitem">Caffeina media</a>
  <a href="/stagioni/primavera/" class="tv-chip" role="listitem">Primavera</a>
</div>
```

**CSS:** `display: inline-flex; padding: 6px 12px; border-radius: var(--md-sys-shape-corner-full); border: 1px solid var(--md-sys-color-outline); font: var(--md-sys-typescale-label-medium);`

---

## MiniNav (`tv-mininav`)

Tab bar anchor per zone Scopri / Prepara / Approfondisci. Sticky sotto header su `lg+`.

```html
<nav class="tv-mininav" aria-label="Sezioni della scheda">
  <ul class="tv-mininav__list">
    <li><a href="#scopri" class="tv-mininav__link tv-mininav__link--active">Scopri</a></li>
    <li><a href="#prepara" class="tv-mininav__link">Prepara</a></li>
    <li><a href="#approfondisci" class="tv-mininav__link">Approfondisci</a></li>
  </ul>
</nav>
```

**Label UI in produzione:** "Panoramica", "Preparazione", "Approfondisci" (non "Scopri/Prepara/Approfondisci" se troppo interni  valutare con personas).

**JS (`scroll-spy.js`):** aggiorna `--active` su scroll; `scroll-margin-top` sulle sezioni.

---

## Scopri block (`tv-scopri`)

Contenitore zona Scopri unificata.

```html
<section id="scopri" class="tv-scopri tv-zone" aria-labelledby="page-title">
  <!-- breadcrumb, in breve, brew-card, sensory-profile, origin-chips -->
  <p class="tv-scopri__brief"><strong>In breve</strong>  Il sencha è il tè verde quotidiano del Giappone...</p>
</section>
```

---

## StepList (`tv-step-list`)

Passaggi preparazione numerati con badge tempo.

```html
<ol class="tv-step-list">
  <li class="tv-step">
    <span class="tv-step__number" aria-hidden="true">1</span>
    <div class="tv-step__content">
      <p class="tv-step__action">Scalda l'acqua a 75°C e raffredda leggermente se necessario</p>
      <span class="tv-step__time">2 min</span>
    </div>
  </li>
  <li class="tv-step">
    <span class="tv-step__number" aria-hidden="true">2</span>
    <div class="tv-step__content">
      <p class="tv-step__action">Infusiona 3 g per 100 ml per 60 secondi</p>
      <span class="tv-step__time">1 min</span>
    </div>
  </li>
</ol>
```

**CSS:** numero in cerchio `--md-sys-color-primary-container`; tempo come chip ridotto.

---

## FaqAccordion (`tv-faq`)

Preferire `<details>` nativo (zero JS, accessibile).

```html
<section class="tv-faq" aria-labelledby="faq-heading">
  <h2 id="faq-heading">Domande frequenti</h2>
  <details class="tv-faq__item">
    <summary class="tv-faq__question">Il sencha fa bene alla salute?</summary>
    <div class="tv-faq__answer">
      <p>Il sencha contiene catechine e caffeina in quantità moderate. Le evidenze scientifiche...</p>
    </div>
  </details>
</section>
```

**Tono:** sobrio, no hype detox (persona Luca). JSON-LD generato in build.

---

## PathNav (`tv-path-nav`)

Prev/next percorso guidato neofiti. Sticky bottom su mobile.

```html
<nav class="tv-path-nav" aria-label="Percorso guidato">
  <a href="/varietà/bancha/" class="tv-path-nav__prev">
    <span class="tv-path-nav__label">Precedente</span>
    <span class="tv-path-nav__title">Bancha</span>
  </a>
  <a href="/varietà/gyokuro/" class="tv-path-nav__next">
    <span class="tv-path-nav__label">Successiva</span>
    <span class="tv-path-nav__title">Gyokuro</span>
  </a>
</nav>
```

**PATH_ORDER:** bancha ? sencha ? gyokuro ? matcha

**CSS mobile:** `position: fixed; bottom: 0; left: 0; right: 0; padding-bottom: env(safe-area-inset-bottom); box-shadow: var(--md-sys-elevation-2);`

---

## RelatedLinks (`tv-related`)

Varietà simili, correlati, torna al catalogo.

```html
<aside class="tv-related" aria-labelledby="related-heading">
  <h2 id="related-heading" class="visually-hidden">Varietà correlate</h2>

  <div class="tv-related__group">
    <h3 class="tv-related__title">Varietà simili</h3>
    <ul class="tv-related__list">
      <li>
        <a href="/varietà/gyokuro/" class="tv-card tv-card--outlined tv-related__link">
          <span class="tv-related__name">Gyokuro</span>
          <span class="tv-related__reason">più umami e ombreggiato del sencha</span>
        </a>
      </li>
    </ul>
  </div>

  <p class="tv-related__back">
    <a href="/varietà/" class="tv-btn tv-btn--outlined">Esplora tutte le varietà</a>
  </p>
</aside>
```

---

## VarietyCard (`tv-variety-card`)

Card catalogo con elevation-1.

```html
<article class="tv-variety-card" data-slug="sencha" data-origine="giappone" data-stile="sencha" data-caffeina="media" data-stagione="primavera">
  <h2 class="tv-variety-card__title">
    <a href="/varietà/sencha/">Sencha  il verde quotidiano del Giappone</a>
  </h2>
  <p class="tv-variety-card__brief">Ago verdi, profilo vegetale equilibrato, preparazione accessibile.</p>
  <div class="tv-origin-chips tv-variety-card__chips">
    <span class="tv-chip tv-chip--static">Giappone</span>
    <span class="tv-chip tv-chip--static">75°C · 3 g</span>
  </div>
</article>
```

**Hover:** `box-shadow: var(--md-sys-elevation-2);` transizione breve.

---

## FilterBar (`tv-filter-bar`)

Facet client-side sul catalogo.

```html
<aside class="tv-filter-bar" aria-label="Filtra varietà">
  <fieldset class="tv-filter-bar__group">
    <legend>Origine</legend>
    <div class="tv-origin-chips">
      <button type="button" class="tv-chip tv-chip--filter" data-filter="origine" data-value="giappone" aria-pressed="false">Giappone</button>
      <button type="button" class="tv-chip tv-chip--filter" data-filter="origine" data-value="cina" aria-pressed="false">Cina</button>
    </div>
  </fieldset>
  <fieldset class="tv-filter-bar__group">
    <legend>Caffeina</legend>
    <div class="tv-origin-chips">
      <button type="button" class="tv-chip tv-chip--filter" data-filter="caffeina" data-value="bassa" aria-pressed="false">Bassa</button>
      <button type="button" class="tv-chip tv-chip--filter" data-filter="caffeina" data-value="media" aria-pressed="false">Media</button>
      <button type="button" class="tv-chip tv-chip--filter" data-filter="caffeina" data-value="alta" aria-pressed="false">Alta</button>
    </div>
  </fieldset>
  <button type="button" class="tv-filter-bar__clear">Rimuovi filtri</button>
</aside>
```

**JS (`filters.js`):** filtra via `data-*`; sync `URLSearchParams`; `aria-live="polite"` per conteggio.

**Mobile:** drawer `.tv-drawer` da bottone "Filtra".

---

## SeasonBanner (`tv-season-banner`)

Hub stagionalità  utile per Marco e narrativa cultura-italiana.

```html
<aside class="tv-season-banner" aria-labelledby="season-heading">
  <h2 id="season-heading" class="tv-season-banner__title">Primavera in tazza</h2>
  <p class="tv-season-banner__text">Shincha e sencha dei primi raccolti  parallelo con asparagi e fave.</p>
  <a href="/stagioni/primavera/" class="tv-btn tv-btn--outlined">Varietà di primavera</a>
</aside>
```

**CSS:** sfondo wash Almost Acqua leggero; no immagini stock.

---

## CtaBlock (`tv-cta`)

Una sola CTA filled per pagina. Copy educativo, non detox.

```html
<section class="tv-cta" aria-labelledby="cta-heading">
  <h2 id="cta-heading" class="tv-cta__title">E adesso?</h2>
  <p class="tv-cta__text">Inizia dal sencha per capire il profilo vegetale del tè verde giapponese.</p>
  <a href="/varietà/sencha/" class="tv-btn tv-btn--filled">Scopri il sencha</a>
</section>
```

**CSS filled button:**

```css
.tv-btn--filled {
  background: var(--md-sys-color-primary);
  color: var(--md-sys-color-on-primary);
  padding: 12px 24px;
  border-radius: var(--md-sys-shape-corner-full);
  font: var(--md-sys-typescale-label-large);
  text-decoration: none;
  border: none;
}
```

**Evitare:** "Inizia il detox", "Perdi peso", "Compra ora".

---

## SiteFooter (`tv-footer`)

```html
<footer class="tv-footer" role="contentinfo">
  <div class="tv-footer__inner">
    <nav aria-label="Link footer">
      <ul class="tv-footer__nav">
        <li><a href="/varietà/">Catalogo varietà</a></li>
        <li><a href="/guide/">Guide</a></li>
        <li><a href="/stagioni/">Stagioni</a></li>
        <li><a href="/privacy/">Privacy</a></li>
        <li><a href="/termini/">Termini</a></li>
      </ul>
    </nav>
    <p class="tv-footer__copy">The Verde  cultura del tè verde in Italia</p>
  </div>
</footer>
```

---

## Term tooltip (`tv-term`)

Glossario termini tè al primo uso.

```html
<abbr title="Tè verde giapponese in foglia, non macinato" class="tv-term">sencha</abbr>
```

**CSS:** `text-decoration: underline dotted; cursor: help; text-decoration-color: var(--md-sys-color-outline);`

---

## Utility classes

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

.tv-zone { scroll-margin-top: calc(var(--tv-header-height) + var(--tv-mininav-height)); }
```

---

## Mappa componente ? modulo scheda varietà

| Sezione Markdown | Componente |
|------------------|------------|
| Breadcrumb | `tv-breadcrumb` |
| In breve | `tv-scopri__brief` |
| Parametri preparazione | `tv-brew-card` |
| Profilo sensoriale | `tv-sensory-profile` |
| Origine / stile / chip | `tv-origin-chips` |
| Attrezzatura | sezione H2 + lista |
| Passaggi preparazione | `tv-step-list` |
| Errori comuni | sezione H2 + lista |
| In Italia | `tv-italy-box` |
| Abbinamenti | sezione H2 + lista |
| FAQ | `tv-faq` |
| Varietà simili | `tv-related` |
| Percorso guidato | `tv-path-nav` |
| Torna al catalogo | `tv-related__back` |
| Catalogo | `tv-variety-card` + `tv-filter-bar` |
| CTA editoriale | `tv-cta` |
| Hub stagione | `tv-season-banner` |
