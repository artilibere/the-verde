"""Content depth quality gates for populated JSON."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from site_builder.document import plain_text_from_blocks, spans_to_plain

from conftest import CONTENT_DIR

PLACEHOLDER = "Consulta le schede"


def _word_count(text: str) -> int:
    return len(text.split())


def _all_text_from_blocks(blocks: list[dict]) -> str:
    parts: list[str] = []
    for block in blocks:
        btype = block.get("type")
        if btype in ("paragraph", "heading", "callout"):
            parts.append(spans_to_plain(block.get("spans", [])))
        elif btype == "list":
            for item in block.get("items", []):
                parts.append(spans_to_plain(item.get("spans", [])))
        elif btype == "faq":
            for item in block.get("items", []):
                parts.append(item.get("question", ""))
                parts.append(spans_to_plain(item.get("answer_spans", [])))
        elif btype == "related_links":
            for item in block.get("items", []):
                parts.append(item.get("name", ""))
                parts.append(item.get("reason", ""))
        elif btype == "level_section":
            parts.append(_all_text_from_blocks(block.get("blocks", [])))
    return " ".join(parts)


def _deep_text(doc: dict) -> str:
    blocks = doc["body"]["blocks"]
    parts: list[str] = []
    for block in blocks:
        if block.get("type") == "level_section" and block.get("level") == "deep":
            parts.append(_all_text_from_blocks(block.get("blocks", [])))
    return " ".join(parts)


@pytest.mark.parametrize("path", sorted((CONTENT_DIR / "glossario").glob("*.json")))
def test_glossary_no_placeholder(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    text = plain_text_from_blocks(doc["body"]["blocks"])
    assert PLACEHOLDER not in text, f"{path.name} still has placeholder"


@pytest.mark.parametrize("path", sorted((CONTENT_DIR / "glossario").glob("*.json")))
def test_glossary_depth(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    intro = ""
    for block in doc["body"]["blocks"]:
        if block.get("type") == "level_section" and block.get("level") == "intro":
            intro = plain_text_from_blocks(block.get("blocks", []))
    deep = _deep_text(doc)
    assert _word_count(intro) >= 20, f"{path.name} intro too short"
    assert _word_count(deep) >= 70, f"{path.name} deep too short ({_word_count(deep)} words)"
    assert doc["navigation"].get("temi_kb"), f"{path.name} missing temi_kb"
    assert len(doc["navigation"].get("explore_next", [])) >= 1, f"{path.name} explore_next"


@pytest.mark.parametrize("path", sorted((CONTENT_DIR / "varieta").glob("*.json")))
def test_variety_completeness(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    blocks = doc["body"]["blocks"]
    assert blocks[0].get("type") == "paragraph", f"{path.name} missing lead paragraph"
    lead = plain_text_from_blocks([blocks[0]])
    assert len(lead) >= 40, f"{path.name} lead too short"

    faq_count = 0
    has_deep = False
    for block in blocks:
        if block.get("type") == "faq":
            faq_count += len(block.get("items", []))
        if block.get("type") == "level_section" and block.get("level") == "deep":
            has_deep = True

    assert faq_count >= 2, f"{path.name} needs >= 2 FAQ"
    assert has_deep, f"{path.name} missing deep section"
    assert len(doc["navigation"].get("explore_next", [])) >= 3, f"{path.name} explore_next"
    assert doc["taxonomy"].get("cultivar"), f"{path.name} missing cultivar"


def test_quizzes_config_depth():
    data = json.loads((CONTENT_DIR / "_config" / "quizzes.json").read_text(encoding="utf-8"))
    for quiz in data["quizzes"]:
        slug = quiz["slug"]
        n = len(quiz["questions"])
        if slug == "che-varieta-sei":
            assert n >= 6, f"{slug} needs >= 6 questions"
        else:
            assert n >= 8, f"{slug} needs >= 8 questions"
        if slug != "che-varieta-sei":
            for q in quiz["questions"]:
                assert "explain" in q, f"{slug} missing explain"
                assert "url" in q, f"{slug} missing url"


def test_paths_microquiz_explain():
    data = json.loads((CONTENT_DIR / "_config" / "paths.json").read_text(encoding="utf-8"))
    for path in data["paths"]:
        for step in path["steps"]:
            if step.get("quiz"):
                assert "explain" in step["quiz"], f"{path['slug']}/{step['slug']} missing explain"
                assert len(step["quiz"].get("options", [])) >= 3, (
                    f"{path['slug']}/{step['slug']} needs >= 3 options"
                )


@pytest.mark.parametrize("path", sorted((CONTENT_DIR / "gioca" / "percorsi").glob("*.json")))
def test_path_articles_rich(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    intro_blocks = []
    for block in doc["body"]["blocks"]:
        if block.get("type") == "level_section" and block.get("level") == "intro":
            intro_blocks = block.get("blocks", [])
    assert len(intro_blocks) >= 2, f"{path.name} intro too thin"
    deep = _deep_text(doc)
    assert "Cosa hai imparato" in deep, f"{path.name} missing synthesis"


@pytest.mark.parametrize("path", sorted((CONTENT_DIR / "impara").glob("*.json")))
def test_impara_hub_depth(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("type") != "hub":
        pytest.skip("not a hub")
    text = _all_text_from_blocks(doc["body"]["blocks"])
    assert "Esplora le varietà collegate" not in text, f"{path.name} placeholder"
    intro = ""
    for block in doc["body"]["blocks"]:
        if block.get("type") == "level_section" and block.get("level") == "intro":
            intro = _all_text_from_blocks(block.get("blocks", []))
    assert _word_count(intro) >= 30, f"{path.name} intro too short"
    deep = _deep_text(doc)
    assert _word_count(deep) >= 100, f"{path.name} deep too short ({_word_count(deep)} words)"
    assert doc["navigation"].get("temi_kb"), f"{path.name} missing temi_kb"


def _controversy_text(doc: dict) -> str:
    parts = [_all_text_from_blocks(doc["body"]["blocks"])]
    for block in doc["body"]["blocks"]:
        if block.get("type") == "positions":
            for item in block.get("items", []):
                parts.append(item.get("tesi", ""))
    return " ".join(parts)


@pytest.mark.parametrize("path", sorted((CONTENT_DIR / "impara" / "controversie").glob("*.json")))
def test_controversy_depth(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    text = _controversy_text(doc)
    positions = [b for b in doc["body"]["blocks"] if b.get("type") == "positions"]
    assert positions, f"{path.name} missing positions"
    for item in positions[0]["items"]:
        assert len(item.get("tesi", "")) >= 80, f"{path.name} tesi too short for {item.get('fonte')}"
    assert _word_count(text) >= 210, f"{path.name} total too short ({_word_count(text)} words)"
    assert "Il cuore della questione" in text, f"{path.name} missing cuore section"
    desc = doc.get("meta", {}).get("description", "")
    assert len(desc) >= 90, f"{path.name} description too short ({len(desc)} chars)"
    assert len(doc["navigation"].get("explore_next", [])) >= 3, f"{path.name} explore_next"


@pytest.mark.parametrize("path", sorted((CONTENT_DIR / "guide").glob("*.json")))
def test_guide_depth(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    intro = ""
    for block in doc["body"]["blocks"]:
        if block.get("type") == "level_section" and block.get("level") == "intro":
            intro = _all_text_from_blocks(block.get("blocks", []))
    deep = _deep_text(doc)
    text = _all_text_from_blocks(doc["body"]["blocks"])
    assert _word_count(intro) >= 35, f"{path.name} intro too short ({_word_count(intro)} words)"
    assert _word_count(deep) >= 150, f"{path.name} deep too short ({_word_count(deep)} words)"
    assert _word_count(text) >= 250, f"{path.name} total too short ({_word_count(text)} words)"
    assert doc["navigation"].get("temi_kb"), f"{path.name} missing temi_kb"
    assert len(doc["navigation"].get("explore_next", [])) >= 2, f"{path.name} explore_next"
    faq_blocks = [b for b in doc["body"]["blocks"] if b.get("type") == "faq"]
    faq_in_deep = []
    for block in doc["body"]["blocks"]:
        if block.get("type") == "level_section":
            faq_in_deep.extend(b for b in block.get("blocks", []) if b.get("type") == "faq")
    faq_count = sum(len(b.get("items", [])) for b in faq_blocks + faq_in_deep)
    assert faq_count >= 2, f"{path.name} needs >= 2 FAQ"
    assert "Fonti" in text, f"{path.name} missing Fonti section"
