#!/usr/bin/env python3
"""Emit structured JSON content documents (seed / bootstrap)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"


def write_variety(slug: str, doc: dict) -> Path:
    path = ROOT / "varieta" / f"{slug}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def example_bancha() -> dict:
    return {
        "schema_version": "1.0",
        "type": "variety",
        "slug": "bancha",
        "meta": {
            "title": "Bancha — il verde quotidiano e leggero",
            "description": "Profilo, preparazione e contesto italiano del bancha.",
            "keywords": ["bancha", "tè verde", "Giappone"],
            "canonical_path": "/varieta/bancha/",
        },
        "seo": {"robots": "index,follow", "og_type": "article"},
        "navigation": {
            "related_slugs": ["kukicha", "hojicha"],
            "temi_kb": ["preparazione_servizio"],
            "momenti": ["colazione"],
            "stagioni": ["estate"],
            "percorso_tappa": "dal-bancha-al-matcha",
            "explore_next": [],
        },
        "taxonomy": {
            "origine": "Giappone",
            "stile": "bancha",
            "caffeina": "Bassa",
            "stagione": "Estate",
            "brew": {"temp": 80, "grams": 3, "seconds": 60, "infusions": "2-3"},
        },
        "body": {
            "blocks": [
                {
                    "type": "paragraph",
                    "spans": [
                        {
                            "type": "text",
                            "value": "Il bancha accompagna la giornata giapponese senza pretese.",
                        }
                    ],
                },
                {
                    "type": "sensory_profile",
                    "aspetto": "Foglie larghe, verde oliva",
                    "aroma": "Vegetale leggero",
                    "gusto": "Morbido",
                    "retrogusto": "Pulito",
                },
            ]
        },
    }


def main() -> None:
    path = write_variety("bancha", example_bancha())
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
