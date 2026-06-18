"""PageDocument transformation tests."""

from __future__ import annotations

import json

from site_builder.page_document import (
    CONTROVERSY_CARD_ORDER,
    GLOSSARY_CARD_ORDER,
    HUB_CARD_ORDER,
    VARIETY_CARD_ORDER,
    blocks_to_controversy_cards,
    blocks_to_glossary_cards,
    blocks_to_variety_cards,
    document_to_page,
    merge_hub_cards,
)

from conftest import CONTENT_DIR


def test_variety_card_order():
    doc = json.loads((CONTENT_DIR / "varieta/sencha.json").read_text(encoding="utf-8"))
    meta = {"brew_temp": 75, "sensory": {}}
    cards = blocks_to_variety_cards(doc["body"]["blocks"], meta)
    ids = [c["id"] for c in cards]
    assert ids == sorted(ids, key=lambda x: VARIETY_CARD_ORDER.index(x))


def test_document_to_page_has_schema_graph():
    doc = json.loads((CONTENT_DIR / "varieta/sencha.json").read_text(encoding="utf-8"))
    page = document_to_page(
        doc,
        url="/varieta/sencha/",
        base_url="https://the-verde.it",
        page_type="variety",
        breadcrumbs=[{"name": "Home", "url": "/"}],
    )
    assert page["schema"]["@context"] == "https://schema.org"
    assert "@graph" in page["schema"]
    assert len(page["cards"]) >= 5


def test_glossary_page_has_intro_and_faq_cards():
    doc = json.loads((CONTENT_DIR / "glossario/umami.json").read_text(encoding="utf-8"))
    page = document_to_page(
        doc,
        url="/glossario/umami/",
        base_url="https://the-verde.it",
        page_type="glossary",
    )
    ids = [c["id"] for c in page["cards"]]
    assert "intro" in ids
    assert "deep" in ids
    assert "faq" in ids
    assert ids == sorted(ids, key=lambda x: GLOSSARY_CARD_ORDER.index(x))


def test_controversy_page_has_positions_card():
    doc = json.loads(
        (CONTENT_DIR / "impara/controversie/caffeina-stimolazione.json").read_text(encoding="utf-8")
    )
    page = document_to_page(
        doc,
        url="/impara/controversie/caffeina-stimolazione/",
        base_url="https://the-verde.it",
        page_type="controversy",
    )
    ids = [c["id"] for c in page["cards"]]
    assert "positions" in ids
    assert "intro" in ids
    assert ids == sorted(ids, key=lambda x: CONTROVERSY_CARD_ORDER.index(x))


def test_hub_page_merges_link_cards():
    doc = json.loads((CONTENT_DIR / "impara/preparazione.json").read_text(encoding="utf-8"))
    cards = merge_hub_cards(
        doc["body"]["blocks"],
        {
            "items": [{"title": "Sencha", "url": "/varieta/sencha/", "brief": "Test"}],
            "controversies": [{"title": "Caffeina", "url": "/impara/controversie/caffeina-stimolazione/", "meta_description": "Test"}],
        },
    )
    ids = [c["id"] for c in cards]
    assert "intro" in ids
    assert "varieties" in ids
    assert "controversies" in ids
    assert ids == sorted(ids, key=lambda x: HUB_CARD_ORDER.index(x))


def test_italia_hub_includes_child_sections():
    doc = json.loads((CONTENT_DIR / "italia/index.json").read_text(encoding="utf-8"))
    cards = merge_hub_cards(
        doc["body"]["blocks"],
        {
            "sections": [
                {
                    "id": "momenti",
                    "title": "Momenti della giornata",
                    "items": [{"title": "Colazione", "url": "/italia/momenti/colazione/", "brief": "Mattino"}],
                },
                {
                    "id": "stagioni",
                    "title": "Le stagioni in Italia",
                    "items": [{"title": "Estate", "url": "/italia/stagioni/estate/", "brief": "Freddo"}],
                },
            ],
            "items": [{"title": "Bancha", "url": "/varieta/bancha/", "brief": "Quotidiano"}],
        },
    )
    ids = [c["id"] for c in cards]
    assert "momenti" in ids
    assert "stagioni" in ids
    assert "varieties" in ids

