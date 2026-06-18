"""PageDocument — unified page model for Jinja2 rendering (uiux-designer contract)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from site_builder.citations import enrich_position_items, is_kb_bibliography_entry
from site_builder.document import document_to_meta, spans_to_plain, collect_faq_items
from site_builder.enrichers._seo_core import (
    article_schema,
    breadcrumb_schema,
    defined_term_schema,
    faq_schema,
    item_list_schema,
    italia_article_schema,
    learning_resource_schema,
    variety_schema,
    webpage_schema,
)
from site_builder.enrichers.schema_org import howto_schema

VARIETY_CARD_ORDER = (
    "brief",
    "brew",
    "sensory",
    "gear",
    "steps",
    "errors",
    "italy",
    "pairings",
    "faq",
    "related",
)

GLOSSARY_CARD_ORDER = ("intro", "deep", "related", "faq")
CONTROVERSY_CARD_ORDER = ("intro", "positions", "deep", "synthesis")
HUB_CARD_ORDER = ("intro", "deep", "momenti", "stagioni", "gastronomia", "varieties", "controversies", "themes")

CARD_TITLES = {
    "brief": "In breve",
    "brew": "Preparazione",
    "sensory": "Profilo sensoriale",
    "gear": "Attrezzatura",
    "steps": "I passaggi",
    "errors": "Errori comuni",
    "italy": "In Italia",
    "pairings": "Abbinamenti",
    "faq": "Domande frequenti",
    "related": "Collegamenti",
    "intro": "Per iniziare",
    "deep": "Approfondimento",
    "content": "Contenuto",
    "positions": "Prospettive",
    "varieties": "Varietà collegate",
    "momenti": "Momenti della giornata",
    "stagioni": "Le stagioni in Italia",
    "gastronomia": "Gastronomia",
    "controversies": "Controversie collegate",
    "themes": "Collegamenti tematici",
    "synthesis": "In sintesi",
}


def spans_to_prose_blocks(spans: list[dict]) -> list[dict]:
    """Normalize inline spans to prose block list for partials/prose.html."""
    if not spans:
        return []
    return [{"type": "paragraph", "spans": spans}]


def _card(card_id: str, body: dict, *, title: str | None = None) -> dict:
    return {
        "id": card_id,
        "title": title or CARD_TITLES.get(card_id, card_id.replace("_", " ").title()),
        "body": body,
    }


def blocks_to_variety_cards(blocks: list[dict], meta: dict) -> list[dict]:
    cards: dict[str, dict] = {}

    for block in blocks:
        btype = block.get("type")
        if btype == "paragraph" and "brief" not in cards:
            cards["brief"] = _card(
                "brief",
                {"type": "prose", "blocks": spans_to_prose_blocks(block.get("spans", []))},
            )
        elif btype == "sensory_profile":
            cards["sensory"] = _card(
                "sensory",
                {
                    "type": "sensory",
                    "aspetto": block.get("aspetto", ""),
                    "aroma": block.get("aroma", ""),
                    "gusto": block.get("gusto", ""),
                    "retrogusto": block.get("retrogusto", ""),
                },
            )
        elif btype == "brew_params":
            cards["brew"] = _card(
                "brew",
                {
                    "type": "metrics",
                    "temp": block.get("temp", meta.get("brew_temp")),
                    "grams": block.get("grams", meta.get("brew_grams")),
                    "seconds": block.get("seconds", meta.get("brew_seconds")),
                    "infusions": block.get("infusions", meta.get("brew_infusions")),
                },
            )
        elif btype == "equipment":
            cards["gear"] = _card("gear", {"type": "list", "items": block.get("items", [])})
        elif btype == "steps":
            cards["steps"] = _card("steps", {"type": "howTo", "items": block.get("items", [])})
        elif btype == "errors":
            cards["errors"] = _card("errors", {"type": "list", "items": block.get("items", [])})
        elif btype == "callout" and block.get("variant") == "italia":
            cards["italy"] = _card(
                "italy",
                {"type": "prose", "blocks": spans_to_prose_blocks(block.get("spans", []))},
            )
        elif btype == "pairings":
            cards["pairings"] = _card("pairings", {"type": "list", "items": block.get("items", [])})
        elif btype == "faq":
            cards["faq"] = _card("faq", {"type": "faq", "items": block.get("items", [])})
        elif btype == "related_links":
            cards["related"] = _card(
                "related",
                {"type": "related", "items": block.get("items", [])},
                title="Varietà simili",
            )

    if "brew" not in cards and meta.get("brew_temp") is not None:
        cards["brew"] = _card(
            "brew",
            {
                "type": "metrics",
                "temp": meta.get("brew_temp"),
                "grams": meta.get("brew_grams"),
                "seconds": meta.get("brew_seconds"),
                "infusions": meta.get("brew_infusions"),
            },
        )

    if "sensory" not in cards and meta.get("sensory"):
        s = meta["sensory"]
        cards["sensory"] = _card(
            "sensory",
            {
                "type": "sensory",
                "aspetto": s.get("aspetto", ""),
                "aroma": s.get("aroma", ""),
                "gusto": s.get("gusto", ""),
                "retrogusto": s.get("retrogusto", ""),
            },
        )

    return [cards[cid] for cid in VARIETY_CARD_ORDER if cid in cards]


def _prose_blocks_from_list(blocks: list[dict]) -> list[dict]:
    prose: list[dict] = []
    for block in blocks:
        btype = block.get("type")
        if btype == "paragraph":
            prose.extend(spans_to_prose_blocks(block.get("spans", [])))
        elif btype == "heading":
            prose.append(
                {
                    "type": "heading",
                    "level": block.get("level", 2),
                    "spans": block.get("spans", []),
                }
            )
        elif btype == "list":
            prose.append(
                {
                    "type": "list",
                    "ordered": block.get("ordered", False),
                    "items": block.get("items", []),
                }
            )
        elif btype == "bibliography":
            items = [
                item
                for item in block.get("items", [])
                if not is_kb_bibliography_entry(item)
            ]
            if items:
                prose.append({"type": "bibliography", "items": items})
        elif btype == "callout":
            prose.extend(spans_to_prose_blocks(block.get("spans", [])))
    return prose


def blocks_to_glossary_cards(blocks: list[dict]) -> list[dict]:
    cards: dict[str, dict] = {}

    for block in blocks:
        btype = block.get("type")
        if btype == "level_section":
            level = block.get("level", "intro")
            card_id = "intro" if level == "intro" else "deep"
            inner = block.get("blocks", [])
            prose_blocks: list[dict] = []
            for ib in inner:
                ib_type = ib.get("type")
                if ib_type == "related_links":
                    cards["related"] = _card(
                        "related",
                        {"type": "related", "items": ib.get("items", [])},
                        title="Approfondimenti collegati",
                    )
                elif ib_type == "faq":
                    cards["faq"] = _card("faq", {"type": "faq", "items": ib.get("items", [])})
                else:
                    prose_blocks.extend(_prose_blocks_from_list([ib]))
            if prose_blocks:
                if card_id in cards:
                    existing = cards[card_id]["body"]["blocks"]
                    cards[card_id]["body"]["blocks"] = existing + prose_blocks
                else:
                    cards[card_id] = _card(card_id, {"type": "prose", "blocks": prose_blocks})
        elif btype == "related_links":
            cards["related"] = _card("related", {"type": "related", "items": block.get("items", [])})
        elif btype == "faq":
            cards["faq"] = _card("faq", {"type": "faq", "items": block.get("items", [])})

    return [cards[cid] for cid in GLOSSARY_CARD_ORDER if cid in cards]


def blocks_to_controversy_cards(blocks: list[dict]) -> list[dict]:
    cards: dict[str, dict] = {}

    for block in blocks:
        btype = block.get("type")
        if btype == "positions":
            cards["positions"] = _card(
                "positions",
                {"type": "positions", "items": enrich_position_items(block.get("items", []))},
            )
        elif btype == "level_section":
            level = block.get("level", "intro")
            if level == "intro":
                card_id = "intro"
            elif level == "deep":
                card_id = "deep"
            else:
                card_id = "synthesis"
            prose = _prose_blocks_from_list(block.get("blocks", []))
            if prose:
                cards[card_id] = _card(card_id, {"type": "prose", "blocks": prose})

    return [cards[cid] for cid in CONTROVERSY_CARD_ORDER if cid in cards]


def blocks_to_hub_cards(blocks: list[dict]) -> list[dict]:
    cards: dict[str, dict] = {}

    for block in blocks:
        if block.get("type") != "level_section":
            continue
        level = block.get("level", "intro")
        card_id = "intro" if level == "intro" else "deep"
        prose = _prose_blocks_from_list(block.get("blocks", []))
        if prose:
            cards[card_id] = _card(card_id, {"type": "prose", "blocks": prose})

    return [cards[cid] for cid in ("intro", "deep") if cid in cards]


def hub_extras_to_cards(
    *,
    items: list[dict] | None = None,
    controversies: list[dict] | None = None,
    relazioni: list[dict] | None = None,
    sections: list[dict] | None = None,
) -> list[dict]:
    extras: list[dict] = []
    if sections:
        for section in sections:
            section_items = section.get("items") or []
            if not section_items:
                continue
            extras.append(
                _card(
                    section["id"],
                    {
                        "type": "linkGrid",
                        "items": [
                            {
                                "title": i.get("title", ""),
                                "url": i.get("url", ""),
                                "brief": i.get("brief", ""),
                            }
                            for i in section_items
                        ],
                    },
                    title=section.get("title"),
                )
            )
    if items:
        extras.append(
            _card(
                "varieties",
                {
                    "type": "linkGrid",
                    "items": [
                        {"title": i.get("title", ""), "url": i.get("url", ""), "brief": i.get("brief", "")}
                        for i in items
                    ],
                },
            )
        )
    if controversies:
        extras.append(
            _card(
                "controversies",
                {
                    "type": "linkGrid",
                    "items": [
                        {
                            "title": c.get("title", ""),
                            "url": c.get("url", ""),
                            "brief": c.get("meta_description", c.get("brief", "")),
                        }
                        for c in controversies
                    ],
                },
            )
        )
    if relazioni:
        extras.append(
            _card(
                "themes",
                {
                    "type": "themeLinks",
                    "items": [
                        {"tipo": r.get("tipo", ""), "descrizione": r.get("descrizione", "")}
                        for r in relazioni
                    ],
                },
            )
        )
    return extras


def merge_hub_cards(blocks: list[dict], hub_extras: dict | None) -> list[dict]:
    cards = blocks_to_hub_cards(blocks)
    if hub_extras:
        cards.extend(
            hub_extras_to_cards(
                items=hub_extras.get("items"),
                controversies=hub_extras.get("controversies"),
                relazioni=hub_extras.get("relazioni"),
                sections=hub_extras.get("sections"),
            )
        )
    by_id = {c["id"]: c for c in cards}
    return [by_id[cid] for cid in HUB_CARD_ORDER if cid in by_id]


ARTICLE_CARD_ORDER = ("intro", "content", "deep", "positions", "related", "faq")


def blocks_to_article_cards(blocks: list[dict]) -> list[dict]:
    cards: list[dict] = []
    content_blocks: list[dict] = []

    for block in blocks:
        btype = block.get("type")
        if btype == "level_section":
            level = block.get("level", "intro")
            card_id = "intro" if level == "intro" else "deep"
            inner = _prose_blocks_from_list(block.get("blocks", []))
            if inner:
                cards.append(_card(card_id, {"type": "prose", "blocks": inner}))
        elif btype == "positions":
            cards.append(
                _card(
                    "positions",
                    {"type": "positions", "items": enrich_position_items(block.get("items", []))},
                )
            )
        elif btype == "related_links":
            cards.append(_card("related", {"type": "related", "items": block.get("items", [])}))
        elif btype == "faq":
            cards.append(_card("faq", {"type": "faq", "items": block.get("items", [])}))
        elif btype == "heading":
            content_blocks.append(
                {
                    "type": "heading",
                    "level": block.get("level", 2),
                    "spans": block.get("spans", []),
                }
            )
        elif btype == "paragraph":
            content_blocks.extend(spans_to_prose_blocks(block.get("spans", [])))
        elif btype == "list":
            content_blocks.append(
                {
                    "type": "list",
                    "ordered": block.get("ordered", False),
                    "items": block.get("items", []),
                }
            )

    if content_blocks:
        cards.insert(
            0 if not any(c["id"] == "intro" for c in cards) else 1,
            _card("content", {"type": "prose", "blocks": content_blocks}),
        )

    ordered: list[dict] = []
    for cid in ARTICLE_CARD_ORDER:
        ordered.extend(c for c in cards if c["id"] == cid)
    for c in cards:
        if c not in ordered:
            ordered.append(c)
    return ordered


def build_schema_graph(
    page: dict,
    *,
    base_url: str,
    page_type: str,
    breadcrumbs: list[dict] | None = None,
    doc: dict | None = None,
) -> dict:
    meta = page.get("meta", {})
    url = meta.get("url") or meta.get("canonical_path", "")
    title = meta.get("title", "")
    description = meta.get("description") or meta.get("meta_description", "")
    graph: list[dict] = []

    if page_type == "variety":
        graph.append(
            variety_schema(
                base_url,
                title=title,
                description=description,
                url=url,
                origin_slug=meta.get("origine_slug", ""),
                origin_label=meta.get("origine", ""),
                brew_temp=meta.get("brew_temp"),
                brew_grams=meta.get("brew_grams"),
                brew_seconds=meta.get("brew_seconds"),
                brew_infusions=meta.get("brew_infusions"),
            )
        )
        faq_items = collect_faq_items(doc=doc, page=page)
        faq = faq_schema(faq_items or meta.get("faqs", []))
        if faq:
            graph.append(faq)
        steps = []
        for card in page.get("cards", []):
            if card.get("id") == "steps":
                for item in card.get("body", {}).get("items", []):
                    steps.append({"action": item.get("text", ""), "text": item.get("text", "")})
        howto = howto_schema(base_url, title=title, url=url, steps=steps or meta.get("steps", []))
        if howto:
            graph.append(howto)
    elif page_type == "glossary":
        graph.append(
            defined_term_schema(base_url, name=title, description=description, url=url)
        )
    elif page_type in ("article", "controversy", "legal"):
        if url.startswith("/italia/"):
            graph.append(
                italia_article_schema(base_url, title=title, description=description, url=url)
            )
        else:
            graph.append(article_schema(base_url, title=title, description=description, url=url))
        path_cfg = meta.get("path_config")
        if url.startswith("/gioca/percorsi/") and path_cfg:
            lr = learning_resource_schema(
                base_url,
                title=title,
                description=description,
                url=url,
                steps=path_cfg.get("steps") or [],
            )
            if lr:
                graph.append(lr)
    elif page_type == "hub":
        if url.startswith("/italia/"):
            graph.append(
                italia_article_schema(base_url, title=title, description=description, url=url)
            )
        else:
            graph.append(
                webpage_schema(base_url, title=title, description=description, url=url, italy_context=True)
            )
        hub_items: list[dict] = []
        seen_urls: set[str] = set()
        for card in page.get("cards", []):
            body = card.get("body") or {}
            if body.get("type") not in ("linkGrid", "related"):
                continue
            for item in body.get("items") or []:
                item_url = (item.get("url") or "").strip()
                item_title = (item.get("title") or item.get("name") or "").strip()
                if not item_url or item_url in seen_urls:
                    continue
                seen_urls.add(item_url)
                hub_items.append({"title": item_title, "url": item_url})
        if hub_items:
            graph.append(item_list_schema(base_url, name=title, url=url, items=hub_items))

    faq_types = ("article", "controversy", "glossary", "hub", "legal", "guide")
    if page_type in faq_types or page_type == "variety":
        faq_items = collect_faq_items(doc=doc, page=page)
        if page_type != "variety":
            faq = faq_schema(faq_items or meta.get("faqs", []))
            if faq and not any(n.get("@type") == "FAQPage" for n in graph):
                graph.append(faq)

    if breadcrumbs and len(breadcrumbs) > 1:
        graph.append(breadcrumb_schema(base_url, breadcrumbs))

    custom = page.get("schema")
    if custom:
        if isinstance(custom, dict) and "@graph" in custom:
            return custom
        if isinstance(custom, list):
            graph.extend(custom)
        elif isinstance(custom, dict):
            graph.append(custom)

    return {"@context": "https://schema.org", "@graph": graph}


def document_to_page(
    doc: dict,
    *,
    url: str,
    base_url: str,
    page_type: str,
    meta: dict | None = None,
    breadcrumbs: list[dict] | None = None,
    navigation: dict | None = None,
    hub_extras: dict | None = None,
) -> dict:
    """Transform content JSON document into PageDocument for templates."""
    meta = meta or document_to_meta(doc, url=url)
    meta["url"] = url
    blocks = doc.get("body", {}).get("blocks", [])
    doc_type = doc.get("type", page_type)

    if doc_type == "variety" or page_type == "variety":
        cards = blocks_to_variety_cards(blocks, meta)
    elif doc_type == "glossary" or page_type == "glossary":
        cards = blocks_to_glossary_cards(blocks)
    elif doc_type == "controversy" or page_type == "controversy":
        cards = blocks_to_controversy_cards(blocks)
    elif doc_type == "hub" or page_type == "hub":
        cards = merge_hub_cards(blocks, hub_extras)
    else:
        cards = blocks_to_article_cards(blocks)

    page: dict[str, Any] = {
        "type": doc.get("type", page_type),
        "slug": doc.get("slug", meta.get("slug", "")),
        "meta": {
            "title": meta.get("title", ""),
            "description": meta.get("description") or meta.get("meta_description", ""),
            "keywords": meta.get("keywords", []),
            "canonical": f"{base_url}{url}",
            "canonical_path": url,
            "published": meta.get("published"),
        },
        "cards": cards,
        "navigation": {
            "breadcrumb": breadcrumbs or [],
            "pathNav": meta.get("path_nav"),
            "exploreNext": meta.get("explore_next", []),
            **(navigation or {}),
        },
        "_meta": meta,
    }

    page["schema"] = build_schema_graph(
        {**page, "meta": {**page["meta"], **meta, "url": url}},
        base_url=base_url,
        page_type=page_type,
        breadcrumbs=breadcrumbs,
        doc=doc,
    )
    return page
