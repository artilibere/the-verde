# Template pagine — the-verde.it

Wireframe **web-app mobile-first**: app shell + card feed. Template Jinja2 in repo site — vedi [rendering-json-html.md](rendering-json-html.md).

---

## Struttura HTML comune (app shell)

```html
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ page.meta.title }}</title>
  <meta name="description" content="{{ page.meta.description }}">
  <link rel="canonical" href="{{ page.meta.canonical }}">
  <link rel="stylesheet" href="/assets/css/tokens.css">
  <link rel="stylesheet" href="/assets/css/base.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  {% include 'partials/json-ld.html' %}
</head>
<body class="tv-page tv-page--{{ page.type }} tv-page--has-bottom-nav" data-slug="{{ page.slug }}">
  {% include 'partials/app-bar.html' %}
  <main id="main" class="tv-feed">
    {% block feed %}{% endblock %}
  </main>
  {% include 'partials/bottom-nav.html' %}
  <script src="/assets/js/nav.js" defer></script>
  {% block scripts %}{% endblock %}
</body>
</html>
```

**Note:** niente footer testuale lungo su mobile; nav primaria in `tv-bottom-nav`. Script d3 solo se pagina ha chart.

---

## Home

**Template:** `pages/home.html`  
**URL:** `/`

### Wireframe (card feed)

```
tv-app-bar: The Verde
--- feed ---
tv-card (icon leaf): Esplora le varietà → /varietà/
tv-card (icon path): Percorso guidato → bancha
tv-scroll-rail: 4 entry momenti (icon cup)
tv-grid tv-grid--tiles tv-grid--2-up-md: stagioni (1 col sm, 2 col md+; solo icona + label)
tv-card: Ultima guida
tv-bottom-nav
```

Niente hero testuale lungo — entry point a card con icone grandi.

---

## Catalogo varietà

**Sorgente:** `content/varietà/*.md` + `varieties/index.json`  
**URL:** `/varietà/`

### Wireframe

```
tv-app-bar: Varietà [filtra]
tv-scroll-rail: chip filtri rapidi (origine, caffeina…)
--- feed wide (fuori max 480px) ---
H1 + lead (1 frase)
tv-grid tv-grid--cards tv-grid--2-up-md
  └── tv-variety-card × N (1 col sm, 2 col md+ — mai 3)
aria-live: {n} varietà
tv-bottom-nav
```

### Struttura

```html
{% extends 'pages/base.html' %}
{% block feed %}
<header class="tv-page-header">
  <h1>Varietà di tè verde</h1>
  <p class="tv-page-header__lead">Schede per origine, stile e preparazione — solo <em>Camellia sinensis</em>, non tisane.</p>
</header>

<div class="tv-scroll-rail tv-scroll-rail--filters" aria-label="Filtri rapidi">
  <!-- chip filtri; drawer per facet completi su mobile -->
</div>

<p class="tv-catalog-results__count" aria-live="polite">{n} varietà</p>
<div class="tv-grid tv-grid--cards tv-grid--2-up-md" id="variety-grid">
  <!-- tv-variety-card da build -->
</div>
{% endblock %}
{% block scripts %}<script src="/assets/js/filters.js" defer></script>{% endblock %}
```

**Responsive griglia:** 1 colonna su `sm` (0–599px); **2 colonne max** da `md` (600px+). **Vietato** 3 colonne su `lg` — testo card troppo stretto.
**Mobile:** bottone "Filtra" in app-bar apre drawer con `tv-filter-bar`.

---

## Scheda varietà

**Template:** `pages/variety.html`  
**URL:** `/varietà/{slug}/`

### Wireframe (card feed)

```
tv-app-bar [back] Sencha
tv-scroll-rail: Scopri | Prepara | Approfondisci (icone)
--- feed (article itemscope Article) ---
tv-card #brief — In breve (prose)
tv-card #brew — tv-metric-row
tv-card #sensory — tabella o lista
tv-card #gear — attrezzatura
tv-card #steps — tv-step-list (HowTo)
tv-card #errors — lista
tv-card #italy — In Italia
tv-card #pairings — abbinamenti
tv-card #faq — FAQ + schema
tv-scroll-rail — varietà simili
tv-path-nav (sopra bottom nav)
tv-bottom-nav
```

### Jinja2

```jinja2
{% extends 'pages/base.html' %}
{% block feed %}
<article itemscope itemtype="https://schema.org/Article">
  {% for card in page.cards %}
    {% include 'partials/card.html' %}
  {% endfor %}
</article>
{% endblock %}
{% block scripts %}
<script src="/assets/js/scroll-spy.js" defer></script>
{% if page.has_chart %}<script src="/assets/js/vendor/d3.min.js" defer></script>
<script src="/assets/js/charts.js" defer></script>{% endif %}
{% endblock %}
```

---

## Articolo editoriale

**Template:** `pages/article.html`  
**URL:** `/guide/{slug}/`

### Wireframe

```
tv-app-bar [back] Titolo articolo
--- feed ---
tv-card — lead (prose)
tv-card — sezione H2 (una card per sezione)
tv-card — sezione H2
tv-card tv-card--highlight — In sintesi
tv-bottom-nav
```

Niente colonna wiki continua: ogni `##` del MD = una `tv-card`.

### Struttura

```html
<main id="main" class="tv-main tv-main--article">
  <article class="tv-article tv-article--editorial">
    <nav class="tv-breadcrumb" aria-label="Breadcrumb">...</nav>
    <header class="tv-article__header">
      <h1>{title}</h1>
      <p class="tv-article__lead">{lead}</p>
    </header>
    <div class="tv-article__body">
      <!-- sezioni H2 dal Markdown -->
    </div>
    <aside class="tv-article__summary" aria-labelledby="summary-heading">
      <h2 id="summary-heading">In sintesi</h2>
      <ul>...</ul>
    </aside>
  </article>
  <aside class="tv-related">...</aside>
</main>
```

**Tipografia:** H1 con `tv-font-serif` opzionale per tono editoriale.

---

## Hub origine

**URL:** `/origine/{paese}/` (es. `/origine/giappone/`)

### Wireframe

```
???????????????????????????????????????????
? tv-header                               ?
???????????????????????????????????????????
? H1: Tè verde dal Giappone               ?
? Intro contesto culturale (breve)        ?
???????????????????????????????????????????
tv-grid tv-grid--cards tv-grid--2-up-md (1 col sm, 2 col md+)
???????????????????????????????????????????
? Link ad altri hub origine               ?
???????????????????????????????????????????
? tv-footer                               ?
???????????????????????????????????????????
```

---

## Hub momento

**URL:** `/per-momento/{momento}/`  
**Sorgente:** tabella momenti in [personas.md](personas.md) / cultura-italiana

### Wireframe

```
???????????????????????????????????????????
? H1: Tè verde a colazione                ?
? Lead: alternativa delicata al cappuccino?
???????????????????????????????????????????
? Varietà consigliate (tv-variety-card)   ?
???????????????????????????????????????????
? Nota onesta (no "digestivo miracoloso") ?
???????????????????????????????????????????
? tv-footer                               ?
???????????????????????????????????????????
```

---

## Hub stagione

**URL:** `/stagioni/{stagione}/`

### Wireframe

```
???????????????????????????????????????????
? tv-season-banner (hero)                 ?
? H1: Primavera                           ?
? Narrativa parallelo gastronomico IT     ?
???????????????????????????????????????????
tv-grid tv-grid--cards tv-grid--2-up-md
???????????????????????????????????????????
? tv-footer                               ?
???????????????????????????????????????????
```

---

## Pagina legale

**URL:** `/privacy/`, `/termini/`  
**Sorgente:** `content/pagine/privacy.json`, `content/pagine/termini.json`  
**Layout:** colonna singola 72ch, nessuna CTA, nessun PathNav, nessuna bottom-nav.

Monitoraggio e aggiornamento testi: [legal-compliance.md](../web-architect/legal-compliance.md) (trigger da JS, integrazioni, footer).

```html
<main id="main" class="tv-main tv-main--legal">
  <article class="tv-article tv-article--legal">
    <h1>Privacy policy</h1>
    <div class="tv-article__body">
      <!-- contenuto legale -->
    </div>
  </article>
</main>
```

---

## Riepilogo script per tipo pagina

| Tipo pagina | Script |
|-------------|--------|
| Tutte | `nav.js` |
| Scheda varietà | `scroll-spy.js` |
| Catalogo | `filters.js` |
| Home, articolo, hub, legale | solo `nav.js` |

---

## Classi body per tipo

| `tv-page--*` | Uso |
|--------------|-----|
| `home` | Hero Almost Acqua |
| `catalog` | Layout sidebar filtri |
| `variety` | Mini-nav + PathNav mobile |
| `article` | Serif H1 opzionale |
| `hub` | Griglia card |
| `legal` | Layout minimale |
