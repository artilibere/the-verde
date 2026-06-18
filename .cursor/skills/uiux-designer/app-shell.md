# App shell — the-verde.it

Paradigma **web-app mobile-first**: scroll feed di schede, non pagina documento o wiki. Riferimento visivo: app nativa di cultura gastronomica, non blog a colonna lunga.

Vedi anche: [design-system.md](design-system.md), [icone.md](icone.md), [componenti.md](componenti.md).

---

## Filosofia

| Wiki / sito classico | Web-app The Verde |
|--------------------|-------------------|
| Colonna 72ch di prose | Feed verticale di `tv-card` |
| Nav testuale in header | Bottom nav iconica + app bar compatta |
| Sidebar filtri desktop | `tv-scroll-rail` swipe su mobile |
| Hero testuale lungo | Griglia card entry point |
| Scroll infinito di testo | Scroll a **blocchi** scansionabili |

Ogni blocco informativo = una **card autonoma** con header (icona + titolo) e corpo compatto. L'utente scorre tra schede, non attraversa un articolo.

---

## App shell (ogni pagina)

```
┌─────────────────────────────┐
│ tv-app-bar          [back?] │  56px sticky top
├─────────────────────────────┤
│ tv-scroll-rail (opzionale)  │  tab / filtri orizzontali
├─────────────────────────────┤
│                             │
│ main.tv-feed                │  scroll verticale
│   tv-card                   │
│   tv-card                   │
│   tv-card                   │
│                             │
├─────────────────────────────┤
│ tv-bottom-nav               │  64px + safe-area fixed bottom
└─────────────────────────────┘
```

### `tv-app-bar`

- Altezza: `var(--tv-app-bar-height)` (56px)
- Contenuto: logo o titolo pagina + max 1 azione (back, filtra, condividi)
- **No** menu hamburger con lista testuale lunga su mobile — la navigazione primaria è nel bottom nav
- Desktop: può espandersi leggermente; mobile resta compatto

### `tv-bottom-nav`

- 4 tab fissi con **icona + label corta**:

| Tab | Icona | URL | `aria-current` |
|-----|-------|-----|----------------|
| Varietà | `tv-icon-leaf` | `/varietà/` | su catalogo e schede |
| Momenti | `tv-icon-cup` | `/per-momento/` | su hub momento |
| Stagioni | `tv-icon-sun` | `/stagioni/` | su hub stagione |
| Guide | `tv-icon-book` | `/guide/` | su articoli |

- `position: fixed; bottom: 0; left: 0; right: 0`
- `padding-bottom: var(--tv-safe-bottom)`
- Touch target min **44×44px** per ogni tab
- Presente su: home, catalogo, scheda, hub, articolo — **non** su pagine legale

### `main.tv-feed`

- `padding-bottom: calc(var(--tv-bottom-nav-height) + var(--tv-safe-bottom) + var(--tv-spacing-3))`
- `gap: var(--tv-feed-gap)` tra card
- Opzionale: `scroll-snap-type: y proximity` su `.tv-card` per snap leggero
- Desktop: `max-width: var(--tv-feed-max-width)` (480px) centrato — **colonna app**, non layout wide

---

## Mobile-first obbligatorio

1. **Progetta prima a 390px** (iPhone standard)
2. Breakpoint `md` (600px) e `lg` (900px) aggiungono spazio, non cambiano paradigma
3. Nessun contenuto critico solo su hover o sidebar desktop
4. Filtri catalogo: `tv-scroll-rail` su mobile; drawer opzionale su tap "Filtra"
5. `tv-mininav` (Scopri / Prepara / Approfondisci): rail orizzontale sticky sotto app-bar, icone + label breve

### Thumb zone

- Bottom nav nella zona del pollice
- CTA primaria preferibilmente in fondo alla card o in bottom sheet, non in alto
- PathNav prev/next: sopra bottom nav o integrato nel feed (non competere con tab bar)

---

## Card feed

### Regole card

- Max **3 righe** di teaser nel body senza expand
- Dettaglio lungo: `<details>` dentro card o card figlia
- Ogni card ha `id` per anchor (`#brew`, `#italy`) e scroll-margin per app-bar + mininav
- Ordine card **fisso per tipo pagina** (vedi [rendering-json-html.md](rendering-json-html.md))

### `tv-scroll-rail`

Scroll orizzontale nativo per:
- Tab sezione (Scopri / Prepara / Approfondisci)
- Chip filtri catalogo
- Card correlate (varietà simili)
- Entry point home (momenti, stagioni)

```css
.tv-scroll-rail {
  display: flex;
  gap: var(--tv-spacing-2);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.tv-scroll-rail > * { scroll-snap-align: start; flex-shrink: 0; }
```

---

## Transizioni (progressive enhancement)

- `view-transition-name` opzionale su tap card → dettaglio (browser che supportano)
- Nessuna transizione obbligatoria per funzionalità core
- `prefers-reduced-motion`: disabilita snap e transizioni

---

## Body class per shell

| Classe | Quando |
|--------|--------|
| `tv-page--has-bottom-nav` | padding-bottom extra |
| `tv-page--has-path-nav` | PathNav sticky sopra bottom nav |
| `tv-page--variety` | mininav + feed scheda |

---

## Anti-pattern shell

- Layout wiki a colonna 72ch come default mobile
- Menu hamburger come unica nav su mobile
- Hero full-viewport con paragrafo lungo
- Popup, modal interstitial, urgency banner
- Bottom nav con più di 5 voci
- Tab solo testuali senza icona

---

## Checklist app shell

- [ ] Progettato e verificato a 390px prima di desktop
- [ ] `tv-app-bar` + `tv-bottom-nav` su tutte le pagine principali
- [ ] Feed a card, non prose continua
- [ ] Touch target ≥ 44px su tab e CTA
- [ ] Safe area rispettata su iOS
- [ ] Scroll orizzontale solo in `tv-scroll-rail`, non su tutta la pagina
