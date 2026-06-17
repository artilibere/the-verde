---
name: uiux-designer
description: >-
  Progetta interfaccia e struttura grafica del sito statico the-verde.it
  (HTML+JS+CSS) a partire da content/, con design system Material 3 tokens
  basato su PANTONE 13-6006 Almost Acqua, componenti tv-*, template pagina,
  personas UX e deploy Cloudflare Pages via GitHub. Usare quando si crea o
  modifica il frontend, wireframe, CSS, layout schede varietà, catalogo
  filtrabile, articoli editoriali, o si configura il repo site separato.
---

# UI/UX Designer — the-verde.it statico

Progetta l'interfaccia del sito statico HTML+JS+CSS per **The Verde**: cultura del tè verde (*Camellia sinensis*) con radicamento italiano. Il frontend vive in un **repo GitHub separato** (es. `the-verde-it-site`); questo repo è content-only o bootstrap editoriale.

Documentazione di dettaglio (progressive disclosure):

| File | Contenuto |
|------|-----------|
| [personas.md](personas.md) | 4 personas UX, matrice componenti, test di validazione |
| [design-system.md](design-system.md) | Token Material 3, Almost Acqua, tipografia, spacing, motion |
| [componenti.md](componenti.md) | Spec HTML/CSS/ARIA per ogni componente `tv-*` |
| [template-pagine.md](template-pagine.md) | Layout per tipo pagina (home, catalogo, scheda, hub) |
| [mapping-contenuti.md](mapping-contenuti.md) | Frontmatter MD ? HTML, build script, JSON index |
| [cloudflare-pages.md](cloudflare-pages.md) | Repo site, deploy, `_headers`, `_redirects` |

## Prima di progettare

Leggi in ordine:

1. [the-verde-expert/SKILL.md](../the-verde-expert/SKILL.md) — tono, formati articolo e scheda varietà, cosa evitare
2. [the-verde-expert/cultura-italiana.md](../the-verde-expert/cultura-italiana.md) — ponti Italia, momenti, stagionalità, narrativa brand
3. [personas.md](personas.md) — Elena (prioritaria), Luca, Giulia, Marco
4. [design-system.md](design-system.md) — token Almost Acqua e regole visive

## Principi UX (priorità assolute)

| Principio | Implicazione UI |
|-----------|-----------------|
| Raffinato, non pedante | Tipografia leggibile; una CTA primaria per pagina; spazio bianco generoso |
| Rispetto delle origini | Chip per paese/tradizione; mai iconografia generica "Asia" (bamboo, lanterne, font brush) |
| Radicamento italiano | Box "In Italia" sempre in scheda varietà; abbinamenti gastronomici in evidenza |
| No wellness clickbait | Niente badge detox; colori sobri; disclaimer salute sobrio se serve |
| Specialty educativo | Dati preparazione above-the-fold nella zona Scopri (°C, g/100ml, secondi) |
| Esperienza lenta | Ritmo di lettura calmo; niente urgency banner, countdown o popup |
| Distinguere tè da tisane | Label chiare; filtri e chip su *Camellia sinensis*, non camomilla/menta |

### Tre obiettivi operativi

1. **Semplicità e chiarezza** — colonna singola per il body (max 72ch); zona Scopri unificata; una sola CTA primaria
2. **Rapidità di orientamento** — mini-nav Scopri/Prepara/Approfondisci; scheda rapida preparazione; FAQ con `<details>` nativo
3. **Navigazione tra contenuti** — PathNav sticky su mobile; RelatedLinks unificato; chip origine/stile sempre cliccabili; catalogo con filtri facet e URL condivisibili

### Test persona (obbligatorio su ogni layout)

> *Elena capisce in 10 secondi? Luca non si sente venduto un detox? Giulia trova i dati tecnici?*

## Tipi di pagina

| Tipo | Sorgente | Template |
|------|----------|----------|
| Home | manifesto brand | [template-pagine.md § Home](template-pagine.md#home) |
| Catalogo varietà | `content/varietà/*.md` | [template-pagine.md § Catalogo](template-pagine.md#catalogo-varietà) |
| Scheda varietà | formato "Scheda varietà" in the-verde-expert | [template-pagine.md § Scheda](template-pagine.md#scheda-varietà) |
| Articolo | formato "Articolo per the-verde.it" | [template-pagine.md § Articolo](template-pagine.md#articolo-editoriale) |
| Hub origine | Giappone, Cina, Taiwan, Corea… | [template-pagine.md § Hub origine](template-pagine.md#hub-origine) |
| Hub momento | colazione, pausa, dopo cena (cultura-italiana) | [template-pagine.md § Hub momento](template-pagine.md#hub-momento) |
| Hub stagione | primavera–inverno | [template-pagine.md § Hub stagione](template-pagine.md#hub-stagione) |
| Legale | privacy/termini | [template-pagine.md § Legale](template-pagine.md#pagina-legale) |

## Modello scheda a 3 zone

Ogni scheda varietà segue Scopri ? Prepara ? Approfondisci:

```
Scopri        ? breadcrumb, In breve, tv-brew-card, tv-sensory-profile, chip origine/stile
Prepara       ? Attrezzatura, tv-step-list, errori comuni
Approfondisci ? tv-italy-box, abbinamenti, FAQ, varietà simili, PathNav, stagionalità
```

Percorso guidato neofiti (prev/next hardcoded in build script):

1. bancha ? 2. sencha ? 3. gyokuro ? 4. matcha

Fonte: `PATH_ORDER` in [mapping-contenuti.md](mapping-contenuti.md).

## Workflow operativo

```
Task Progress:
- [ ] 1. Leggere the-verde-expert + cultura-italiana + personas
- [ ] 2. Identificare tipo pagina e moduli obbligatori
- [ ] 3. Applicare design system (design-system.md)
- [ ] 4. Comporre HTML semantico con componenti tv-* (componenti.md)
- [ ] 5. Verificare microcopy con the-verde-expert (no detox, no tisane confuse)
- [ ] 6. Verificare SEO: title, meta, H1, JSON-LD FAQ
- [ ] 7. Test responsive (mobile-first) e accessibilità (focus, contrasto, accordion)
- [ ] 8. Aggiornare _redirects se nuovi slug
- [ ] 9. Validare build locale + preview Cloudflare
```

## Integrazione con altre skill

| Skill | Ruolo nel frontend |
|-------|-------------------|
| the-verde-expert | Label, CTA, aria-label, tono editoriale, glossario termini tè |
| (futura) seo-specialist | Meta, FAQ schema, struttura H1/H2, canonical |

**Regola di conflitto:** accessibilità e leggibilità > decorazione; tono the-verde-expert > copy marketing UI.

## Sync content ? site

Tre modalità (default consigliato: **GitHub Actions checkout**):

1. **Git submodule** — `content/` nel repo site punta al repo the-verde.it
2. **GitHub Actions checkout** — workflow scarica `content/` al build
3. **Export manuale** — script copia MD in `site/content/`

Dettaglio deploy: [cloudflare-pages.md](cloudflare-pages.md).

## Cosa NON fare

- Framework CSS pesanti (Bootstrap, Tailwind) — vanilla CSS con custom properties M3
- SPA/router client-side per contenuto indicizzabile — pagina HTML statica per ogni URL
- Estetica zen kitsch (bamboo SVG, lanterne, font brush, clipart meditazione)
- Verde neon wellness, badge "detox", before/after, copy dimagrante
- Emoji negli heading
- Multipli CTA in competizione sulla stessa pagina
- Font/icon pack esterni non necessari
- Material Web Components o bundler obbligatori — solo token M3 in CSS
- Confondere tè verde con tisane nell'UI (etichette, filtri, hero)

## Checklist finale

- [ ] Tipo pagina e moduli obbligatori identificati
- [ ] Token M3 + Almost Acqua applicati (`tokens.css`)
- [ ] Componenti `tv-*` con stati focus/hover e ARIA
- [ ] Zona Scopri scannable in 10 sec; mini-nav su scheda
- [ ] Navigazione correlati: PathNav + RelatedLinks + chip
- [ ] Microcopy verificato (the-verde-expert; no detox)
- [ ] Test persona superato (Elena, Luca, Giulia)
- [ ] SEO: title <= 60, meta <= 155, FAQ JSON-LD se presente
- [ ] Mobile-first, contrasto WCAG AA, keyboard navigabile
- [ ] `_redirects` allineati agli slug definiti
- [ ] Build locale + preview Cloudflare OK
