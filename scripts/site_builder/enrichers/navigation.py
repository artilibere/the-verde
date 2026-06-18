"""Internal navigation: explore_next, path_nav, graph backfill."""

from __future__ import annotations

from typing import Any

PATH_ORDER = ["bancha", "sencha", "gyokuro", "matcha"]
MAX_EXPLORE = 4
MIN_EXPLORE = 3


def path_nav(slug: str, variety_title_fn) -> dict | None:
    if slug not in PATH_ORDER:
        return None
    idx = PATH_ORDER.index(slug)
    nav: dict[str, Any] = {"current": slug, "index": idx + 1, "total": len(PATH_ORDER)}
    if idx > 0:
        prev_slug = PATH_ORDER[idx - 1]
        nav["prev"] = {
            "slug": prev_slug,
            "title": variety_title_fn(prev_slug),
            "url": f"/varieta/{prev_slug}/",
        }
    if idx < len(PATH_ORDER) - 1:
        next_slug = PATH_ORDER[idx + 1]
        nav["next"] = {
            "slug": next_slug,
            "title": variety_title_fn(next_slug),
            "url": f"/varieta/{next_slug}/",
        }
    return nav


def _link_key(link: dict) -> str:
    return link.get("url", "") or link.get("title", "")


def explore_next(
    slug: str,
    meta: dict,
    *,
    varieties: list[dict],
    controversies: list[dict],
    relazioni: dict,
    hubs: list[dict] | None = None,
    glossary: list[dict] | None = None,
) -> list[dict]:
    nav = meta.get("navigation") or {}
    explicit = nav.get("explore_next") or meta.get("explore_next")
    if explicit:
        return explicit[:MAX_EXPLORE]

    links: list[dict] = []
    seen: set[str] = set()

    def add(link: dict) -> None:
        key = _link_key(link)
        if key and key not in seen and len(links) < MAX_EXPLORE:
            seen.add(key)
            links.append(link)

    for rs in meta.get("related_slugs", nav.get("related_slugs", [])):
        v = next((x for x in varieties if x["slug"] == rs), None)
        if v:
            add(
                {
                    "type": "varieta",
                    "title": v["title"],
                    "url": v["url"],
                    "brief": v.get("brief", ""),
                }
            )

    temi = meta.get("temi_kb", nav.get("temi_kb", []))
    if temi and relazioni:
        tema_map = {t["id"]: t for t in relazioni.get("temi", [])}
        for tid in temi[:2]:
            if tid in tema_map:
                t = tema_map[tid]
                add({"type": "tema", "title": t["nome"], "url": t["url"], "brief": ""})

    for cid in meta.get("controversie", nav.get("controversie", []))[:1]:
        c = next((x for x in controversies if x["slug"] == cid), None)
        if c:
            add(
                {
                    "type": "controversia",
                    "title": c["title"],
                    "url": c["url"],
                    "brief": c.get("meta_description", c.get("brief", "")),
                }
            )

    if len(links) < MIN_EXPLORE and relazioni:
        for rel in relazioni.get("relazioni", []):
            if len(links) >= MAX_EXPLORE:
                break
            for tema in relazioni.get("temi", []):
                if tema["id"] in (rel.get("da"), rel.get("a")):
                    tid_match = any(t in temi for t in (rel.get("da"), rel.get("a")))
                    if not tid_match:
                        add(
                            {
                                "type": "tema",
                                "title": tema["nome"],
                                "url": tema["url"],
                                "brief": rel.get("descrizione", "")[:80],
                            }
                        )

    if len(links) < MIN_EXPLORE and hubs:
        for h in hubs[:2]:
            if h.get("slug") == slug:
                continue
            add(
                {
                    "type": "hub",
                    "title": h.get("title", ""),
                    "url": h.get("url", ""),
                    "brief": h.get("meta_description", ""),
                }
            )

    if len(links) < MIN_EXPLORE and glossary:
        for g in glossary[:2]:
            if g.get("slug") == slug:
                continue
            add(
                {
                    "type": "glossario",
                    "title": g.get("title", ""),
                    "url": g.get("url", ""),
                    "brief": g.get("meta_description", ""),
                }
            )

    return links[:MAX_EXPLORE]
