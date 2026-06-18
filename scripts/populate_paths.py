#!/usr/bin/env python3
"""Populate path article JSON files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_builder.citations import bibliography_block, legacy_to_bib_entry

OUT = ROOT / "content" / "gioca" / "percorsi"


def fonti(items: list[str], *, slug: str | None = None) -> list[dict]:
    entries = []
    seen: set[str] = set()
    for text in items:
        entry = legacy_to_bib_entry(text, slug=slug)
        if not entry:
            continue
        key = f"{entry['author']}|{entry['tema']}"
        if key in seen:
            continue
        seen.add(key)
        entries.append(entry)
    return [bibliography_block(entries)] if entries else []


def p(t: str) -> dict:
    return {"type": "paragraph", "spans": [{"type": "text", "value": t}]}


def article(slug: str, title: str, desc: str, intro_blocks: list, deep_blocks: list, explore: list) -> dict:
    return {
        "schema_version": "1.0",
        "type": "article",
        "slug": slug,
        "meta": {
            "title": title,
            "description": desc,
            "keywords": [slug.replace("-", " "), "tè verde", "percorso", "Camellia sinensis"],
            "canonical_path": f"/gioca/percorsi/{slug}/",
        },
        "seo": {"robots": "index,follow", "og_type": "article"},
        "navigation": {
            "related_slugs": [],
            "temi_kb": ["preparazione_servizio"],
            "controversie": [],
            "explore_next": [{"name": n, "url": u, "reason": r} for n, u, r in explore],
        },
        "taxonomy": {},
        "body": {
            "blocks": [
                {"type": "level_section", "level": "intro", "blocks": intro_blocks},
                {"type": "level_section", "level": "deep", "blocks": deep_blocks},
            ]
        },
    }


ARTICLES = {
    "dal-bancha-al-matcha": article(
        "dal-bancha-al-matcha",
        "Dal bancha al matcha",
        "Quattro tappe dal verde più leggero al matcha cerimoniale: caffeina, ombra e foglia intera.",
        [
            p("Quattro tappe, un arco di sapore: dal bancha quotidiano al matcha che bevi intero. Non è una gara di pregi: è capire come la stessa pianta cambia voce."),
            p("Durata stimata: 30–45 minuti tra lettura e infusioni. Badge: Esploratore del verde."),
            {
                "type": "list",
                "ordered": False,
                "items": [
                    {"spans": [{"type": "text", "value": "Riconoscere caffeina bassa vs alta nei verdi giapponesi"}]},
                    {"spans": [{"type": "text", "value": "Capire ombreggiatura e umami (gyokuro)"}]},
                    {"spans": [{"type": "text", "value": "Distinguere infusionato e matcha (foglia intera)"}]},
                ],
            },
        ],
        [
            {"type": "heading", "level": 2, "spans": [{"type": "text", "value": "Cosa hai imparato"}]},
            p("Il tè verde giapponese non è monolite: bancha e sencha al sole, gyokuro all'ombra, matcha da tencha macinato. Ogni tappa ha temperatura e gesto propri."),
            p("Completa i micro-quiz sotto ogni step per sbloccare il badge. Se sbagli, rileggi la scheda: l'errore è parte del metodo."),
            *fonti(
                ["onuma, consumo quotidiano", "pellegrino, verdi giapponesi"],
                slug="dal-bancha-al-matcha",
            ),
        ],
        [
            ("Quiz sensoriale", "/gioca/quiz/che-varieta-sei/", "profilo"),
            ("Percorso palato italiano", "/gioca/percorsi/palato-italiano/", "successivo"),
        ],
    ),
    "palato-italiano": article(
        "palato-italiano",
        "Il palato italiano",
        "Degustazione consapevole: tre verdi per allenare occhio, naso e memoria del gusto.",
        [
            p("Conosci già vino o olio? Hai metà strada fatta. Il tè verde si legge con lo stesso rispetto: aspetto, aroma, corpo, persistenza."),
            p("Durata: 40 minuti. Badge: Sommelier in erba."),
            {
                "type": "list",
                "ordered": False,
                "items": [
                    {"spans": [{"type": "text", "value": "Metodo di degustazione in 4 passi"}]},
                    {"spans": [{"type": "text", "value": "Confronto sencha, gyokuro, dragon well"}]},
                    {"spans": [{"type": "text", "value": "Lessico italiano del gusto (vegetale, umami, astrigente)"}]},
                ],
            },
        ],
        [
            {"type": "heading", "level": 2, "spans": [{"type": "text", "value": "Cosa hai imparato"}]},
            p("Tre verdi, tre grammatiche: vapore giapponese al sole, ombra umami, nocciola cinese in padella. Il palato italiano trova ponti senza snaturare le origini."),
            *fonti(["sommelier, degustazione"], slug="palato-italiano"),
        ],
        [
            ("Degustazione", "/impara/degustazione/", "hub"),
            ("Abbinamenti Italia", "/italia/abbinamenti/", "gastronomia"),
        ],
    ),
    "scienza-tradizione": article(
        "scienza-tradizione",
        "Scienza o tradizione",
        "Tre controversie dalla knowledge base: leggere il tè verde con spirito critico.",
        [
            p("Il tè verde fa bene? Sì e no — dipende da cosa chiedi, a chi e con quale evidenza. Questo percorso attraversa tre dibattiti aperti senza fazioni."),
            p("Durata: 35 minuti. Badge: Lettore critico."),
            {
                "type": "list",
                "ordered": False,
                "items": [
                    {"spans": [{"type": "text", "value": "Salute: scienza (hara) vs tradizione (rosen, onuma)"}]},
                    {"spans": [{"type": "text", "value": "Bevanda vs integratore di EGCG"}]},
                    {"spans": [{"type": "text", "value": "Caffeina: stimolazione o calma?"}]},
                ],
            },
        ],
        [
            {"type": "heading", "level": 2, "spans": [{"type": "text", "value": "Cosa hai imparato"}]},
            p("Tradizione e laboratorio convergono sul potenziale preventivo, divergono su dosi e certezze. Bevi per piacere; eventuali benefici sono un plus, non una promessa."),
            *fonti(
                [
                    "hara, temi salute",
                    "prospettive_contrastanti in books/knowledge-base.json",
                ],
                slug="scienza-tradizione",
            ),
        ],
        [
            ("Quiz miti", "/gioca/quiz/mito-verita/", "verifica"),
            ("Salute", "/impara/salute/", "hub"),
        ],
    ),
    "rituale-quotidiano": article(
        "rituale-quotidiano",
        "Rituale è quotidiano",
        "Dal gong fu cinese al chanoyu: il gesto lento convive con il bancha in bottiglia.",
        [
            p("Non serve una sala di cerimonia per bere con attenzione. E il chanoyu non annulla il sencha al lavoro: due registri, stessa pianta."),
            p("Durata: 45 minuti. Badge: Maestro del gesto."),
            {
                "type": "list",
                "ordered": False,
                "items": [
                    {"spans": [{"type": "text", "value": "Differenza gong fu cha e chanoyu"}]},
                    {"spans": [{"type": "text", "value": "Strumenti: chasen, kyusu, gaiwan"}]},
                    {"spans": [{"type": "text", "value": "Mini-rituale quotidiano accessibile in Italia"}]},
                ],
            },
        ],
        [
            {"type": "heading", "level": 2, "spans": [{"type": "text", "value": "Cosa hai imparato"}]},
            p("Il tè è insieme pane quotidiano e occasione straordinaria. Scegli il registro che ti serve oggi — bancha veloce o matcha lento — senza moralismi."),
            *fonti(
                ["onuma, cerimonia", "sommelier, cerimonie"],
                slug="rituale-quotidiano",
            ),
        ],
        [
            ("Cerimonia", "/impara/cerimonia/", "hub"),
            ("Consumo vs rituale", "/impara/controversie/consumo-quotidiano-vs-rituale/", "KB"),
        ],
    ),
}


def main() -> None:
    for slug, doc in ARTICLES.items():
        path = OUT / f"{slug}.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {path.name}")


if __name__ == "__main__":
    main()
