"""Document helpers: slugify, meta normalization for templates."""

from __future__ import annotations

import re
from html import escape
from typing import Any


def slugify(text: str) -> str:
    text = text.lower().strip()
    for old, new in [
        ("\u00e0", "a"),
        ("\u00e8", "e"),
        ("\u00e9", "e"),
        ("\u00ec", "i"),
        ("\u00f2", "o"),
        ("\u00f9", "u"),
    ]:
        text = text.replace(old, new)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def variety_breadcrumb_title(title: str) -> str:
    for sep in (" — ", " - "):
        if sep in title:
            return title.split(sep, 1)[0].strip()
    return title.strip()


def spans_to_plain(spans: list[dict]) -> str:
    parts = []
    for span in spans:
        parts.append(span.get("value", ""))
    return "".join(parts)


def extract_from_blocks(blocks: list[dict]) -> dict[str, Any]:
    """Extract structured fields from blocks for template meta."""
    out: dict[str, Any] = {
        "sensory": {},
        "steps": [],
        "faqs": [],
        "related_varieties": [],
        "positions": [],
    }

    def walk(blks: list[dict]) -> None:
        for block in blks:
            btype = block.get("type")
            if btype == "sensory_profile":
                out["sensory"] = {
                    "aspetto": block.get("aspetto", ""),
                    "aroma": block.get("aroma", ""),
                    "gusto": block.get("gusto", ""),
                    "retrogusto": block.get("retrogusto", ""),
                }
            elif btype == "steps":
                for item in block.get("items", []):
                    out["steps"].append(
                        {
                            "action": item.get("text", ""),
                            "time": item.get("duration", ""),
                        }
                    )
            elif btype == "faq":
                for item in block.get("items", []):
                    out["faqs"].append(
                        {
                            "question": item.get("question", ""),
                            "answer": spans_to_plain(item.get("answer_spans", [])),
                        }
                    )
            elif btype == "related_links":
                for item in block.get("items", []):
                    out["related_varieties"].append(
                        {
                            "url": item.get("url", ""),
                            "name": item.get("name", ""),
                            "reason": item.get("reason", ""),
                        }
                    )
            elif btype == "positions":
                out["positions"] = block.get("items", [])
            elif btype == "level_section":
                walk(block.get("blocks", []))

    walk(blocks)
    return out


def collect_faq_items(
    *,
    doc: dict | None = None,
    page: dict | None = None,
) -> list[dict]:
    """Merge FAQ entries from document blocks, page cards, and meta."""
    items: list[dict] = []
    seen: set[str] = set()

    def add(question: str, answer: str) -> None:
        q = (question or "").strip()
        if not q or q in seen:
            return
        seen.add(q)
        items.append({"question": q, "answer": (answer or "").strip()})

    if doc:
        blocks = doc.get("body", {}).get("blocks", [])
        for faq in extract_from_blocks(blocks).get("faqs", []):
            add(faq.get("question", ""), faq.get("answer", ""))
        for faq in (doc.get("meta") or {}).get("faqs", []):
            add(faq.get("question", ""), faq.get("answer", ""))

    if page:
        for card in page.get("cards", []):
            if card.get("id") != "faq":
                continue
            for item in card.get("body", {}).get("items", []):
                add(
                    item.get("question", ""),
                    spans_to_plain(item.get("answer_spans", [])),
                )

    return items


def document_to_meta(doc: dict, *, url: str | None = None) -> dict[str, Any]:
    """Normalize JSON document to template meta dict."""
    meta = dict(doc.get("meta", {}))
    nav = doc.get("navigation") or {}
    tax = doc.get("taxonomy") or {}
    blocks = doc.get("body", {}).get("blocks", [])
    extracted = extract_from_blocks(blocks)

    slug = doc.get("slug", "")
    meta["slug"] = slug
    meta["url"] = url or meta.get("canonical_path") or meta.get("url", "")
    meta["meta_description"] = meta.get("description", meta.get("meta_description", ""))
    meta["title"] = meta.get("title", "")

    for key in (
        "related_slugs",
        "temi_kb",
        "controversie",
        "momenti",
        "stagioni",
        "percorso_tappa",
        "badge_sblocco",
    ):
        if key in nav:
            meta[key] = nav[key]

    explore = nav.get("explore_next") or []
    if explore:
        meta["explore_next"] = [
            {
                "title": link.get("title") or link.get("name", ""),
                "url": link.get("url", ""),
                "type": link.get("type") or link.get("reason", ""),
                "brief": link.get("brief", ""),
            }
            for link in explore
        ]

    if doc.get("type") == "variety":
        brew = tax.get("brew", {})
        meta.update(
            {
                "origine": tax.get("origine", ""),
                "stile": tax.get("stile", ""),
                "caffeina": tax.get("caffeina", ""),
                "stagione": tax.get("stagione", ""),
                "cultivar": tax.get("cultivar", ""),
                "sort_order": tax.get("sort_order"),
                "brew_temp": brew.get("temp"),
                "brew_grams": brew.get("grams"),
                "brew_seconds": brew.get("seconds"),
                "brew_infusions": brew.get("infusions"),
                "origine_slug": slugify(tax.get("origine", "")),
                "stile_slug": slugify(tax.get("stile", "")),
                "caffeina_slug": slugify(tax.get("caffeina", "")),
                "stagione_slug": slugify(tax.get("stagione", "")),
            }
        )

    meta.update(
        {
            k: v
            for k, v in extracted.items()
            if v or k in ("sensory", "steps", "faqs", "related_varieties")
        }
    )

    if doc.get("type") == "controversy" and meta.get("positions"):
        meta["posizioni"] = meta["positions"]

    if not meta.get("brief"):
        for block in blocks:
            if block.get("type") == "paragraph":
                meta["brief"] = spans_to_plain(block.get("spans", []))[:160]
                break

    seo = doc.get("seo") or {}
    if seo.get("robots"):
        meta["seo_robots"] = seo["robots"]

    return meta


def plain_text_from_blocks(blocks: list[dict]) -> str:
    parts: list[str] = []
    for block in blocks:
        btype = block.get("type")
        if btype == "paragraph":
            parts.append(spans_to_plain(block.get("spans", [])))
        elif btype == "heading":
            parts.append(spans_to_plain(block.get("spans", [])))
        elif btype == "level_section":
            parts.append(plain_text_from_blocks(block.get("blocks", [])))
    return " ".join(parts).strip()
