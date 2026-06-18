"""Parity checks for migrated JSON content rendering."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from site_builder.blocks import render_variety_body
from site_builder.document import document_to_meta

from conftest import CONTENT_DIR


@pytest.mark.parametrize(
    "rel_path,needle",
    [
        ("varieta/sencha.json", "Ago verdi"),
        ("glossario/umami.json", "Quinto gusto"),
        ("impara/controversie/caffeina-stimolazione.json", "caffeina"),
    ],
)
def test_json_content_contains_expected_text(rel_path: str, needle: str):
    doc = json.loads((CONTENT_DIR / rel_path).read_text(encoding="utf-8"))
    from site_builder.document import plain_text_from_blocks

    text = plain_text_from_blocks(doc["body"]["blocks"])
    assert needle.lower() in text.lower()


def test_sencha_meta_extracts_brew():
    doc = json.loads((CONTENT_DIR / "varieta/sencha.json").read_text(encoding="utf-8"))
    meta = document_to_meta(doc, url="/varieta/sencha/")
    assert meta["brew_temp"] == 75
    assert meta["origine_slug"] == "giappone"
    assert len(meta.get("steps", [])) >= 1


def test_sencha_variety_html_has_zones():
    doc = json.loads((CONTENT_DIR / "varieta/sencha.json").read_text(encoding="utf-8"))
    html = render_variety_body(doc["body"]["blocks"])
    assert "prepara" in html
    assert "approfondisci" in html
