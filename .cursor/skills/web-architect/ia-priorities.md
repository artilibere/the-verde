# Information architecture — priorità

## 1. Accessibilità

- Un solo `<h1>` per pagina (template o blocco `heading` level 1)
- Landmark `<main>` in `base.html`
- Breadcrumb con `<nav aria-label="Breadcrumb">`
- FAQ: `<details>` / `<summary>` (non solo div cliccabili)
- Link con testo descrittivo (no "clicca qui")
- Test: `tests/test_build_output.py`, `tests/test_blocks.py`

## 2. Completezza

- JSON Schema impone sezioni minime per tipo (es. varietà: sensory, steps, callout italia)
- Glossario: `level_section` intro + deep
- Controversie: blocco `positions` con fonti KB

## 3. Interattività

- Config runtime in `dist/assets/js/config/` (quiz, paths, badges, seasons)
- `has_levels` quando esiste `level_section` deep
- Catalogo: `varieta/index.json` per filtri client-side

## 4. Navigazione interna / permanenza

### Grafo

- [`content/relazioni.json`](../../content/relazioni.json): temi, relazioni, `varieta_temi`
- Ogni documento: `navigation.related_slugs`, `temi_kb`, `controversie`

### `explore_next`

Calcolato in `site_builder/enrichers/navigation.py`:

1. `navigation.explore_next` esplicito nel JSON (override)
2. Varietà correlate (`related_slugs`)
3. Temi KB (max 2 da `relazioni.temi`)
4. Controversie collegate (max 1)
5. Backfill dal grafo `relazioni` se < 3 link

Limite: 4 link in sidebar "Potrebbe interessarti".

### Path nav varietà

Ordine pedagogico: `bancha` → `sencha` → `gyokuro` → `matcha` (`PATH_ORDER` in builder).

### Prefetch navigazione

Per ridurre la latenza percepita tra pagine statiche:

1. **Head** — `partials/prefetch-hints.html`: `rel=prefetch` su `path_nav.next` e primi 2 `explore_next`
2. **Core JS** — `assets/js/prefetch.js` nel bundle `core`: prefetch su hover/focus/touch su link di navigazione; hub bottom-nav con `data-tv-prefetch="high"`; hub principali in `requestIdleCallback`
3. **Catalogo** — prefetch intent-only sulle card varietà (no prefetch massivo)

Target: breadcrumb, explore_next, path nav, bottom nav, header nav — non ogni link del body.

### Hub impara

Link automatici a varietà con `temi_kb` corrispondente e controversie del tema.
