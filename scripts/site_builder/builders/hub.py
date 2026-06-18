"""Hub pages — Impara pillars, Italia context, and index listings."""

from __future__ import annotations

from site_builder.blocks import has_level_sections
from site_builder.builders._render import render_page_document
from site_builder.document import document_to_meta


def _tema_for_slug(temi: list[dict], slug: str) -> dict | None:
    return next((t for t in temi if slug in t.get("url", "")), None)


def _linked_varieties(builder, tema: dict | None) -> list[dict]:
    if not tema:
        return []
    linked = [v for v in builder.varieties if tema["id"] in v.get("temi_kb", [])]
    if linked:
        return linked
    relazioni = builder.relazioni if isinstance(builder.relazioni, dict) else {}
    vt = relazioni.get("varieta_temi", {})
    for vs, ts in vt.items():
        if tema["id"] in ts:
            lv = next((v for v in builder.varieties if v["slug"] == vs), None)
            if lv:
                linked.append(lv)
    return linked


def _linked_controversies(builder, tema: dict | None) -> list[dict]:
    if not tema:
        return []
    return [c for c in builder.controversies if c["slug"] in tema.get("controversie", [])]


def _linked_relazioni(builder, tema: dict | None) -> list[dict]:
    if not tema or not isinstance(builder.relazioni, dict):
        return []
    tema_id = tema["id"]
    return [
        r
        for r in builder.relazioni.get("relazioni", [])
        if r["da"] == tema_id or r["a"] == tema_id
    ]


def build_impara(builder) -> None:
    temi = builder.relazioni.get("temi", []) if isinstance(builder.relazioni, dict) else []

    for _path, doc in builder.docs_in("impara", doc_type="hub"):
        slug = doc["slug"]
        url = f"/impara/{slug}/"
        meta = document_to_meta(doc, url=url)
        tema = _tema_for_slug(temi, slug)
        linked_varieties = _linked_varieties(builder, tema)
        linked_controversies = _linked_controversies(builder, tema)
        relazioni = _linked_relazioni(builder, tema)
        builder.hubs.append(meta)

        html = render_page_document(
            builder,
            doc,
            url,
            page_type="hub",
            template="hub.html",
            meta=meta,
            breadcrumbs=builder.breadcrumbs(("Impara", "/impara/"), (meta["title"], url)),
            hub_extras={
                "items": [
                    {"title": v["title"], "url": v["url"], "brief": v.get("brief", "")}
                    for v in linked_varieties[:6]
                ],
                "controversies": linked_controversies,
                "relazioni": relazioni,
            },
            extra={"has_levels": has_level_sections(doc.get("body", {}).get("blocks", []))},
        )
        builder.write_page(builder.out_dir / "impara" / slug, html)
        builder.all_pages.append({"title": meta["title"], "url": url, "type": "impara"})
        builder.track_sitemap(url, priority=0.7, changefreq="monthly")

    index = builder.render(
        "hub.html",
        page_type="hub",
        title="Impara",
        lead="Otto pilastri di conoscenza sul tè verde, dalla storia alla scienza.",
        url="/impara/",
        items=[{"title": t["nome"], "url": t["url"], "brief": ""} for t in temi],
        breadcrumbs=builder.breadcrumbs(("Impara", "/impara/")),
    )
    builder.write_page(builder.out_dir / "impara", index)
    builder.track_sitemap("/impara/", priority=0.8, changefreq="weekly")


def build_italia(builder) -> None:
    doc = builder.doc_at("italia", "index.json")
    if doc:
        meta = document_to_meta(doc, url="/italia/")
        html = render_page_document(
            builder,
            doc,
            "/italia/",
            page_type="hub",
            template="hub.html",
            meta=meta,
            breadcrumbs=builder.breadcrumbs(("In Italia", "/italia/")),
        )
        builder.write_page(builder.out_dir / "italia", html)
        builder.track_sitemap("/italia/", priority=0.7, changefreq="weekly")

    for sub, prefix in [("momenti", "/italia/momenti/"), ("stagioni", "/italia/stagioni/")]:
        for _path, doc in builder.docs_in(f"italia/{sub}", doc_type="hub"):
            slug = doc["slug"]
            url = f"{prefix}{slug}/"
            meta = document_to_meta(doc, url=url)
            linked = [
                v
                for v in builder.varieties
                if slug in v.get("momenti", []) or slug in v.get("stagioni", [])
            ]
            html = render_page_document(
                builder,
                doc,
                url,
                page_type="hub",
                template="hub.html",
                meta=meta,
                breadcrumbs=builder.breadcrumbs(("In Italia", "/italia/"), (meta["title"], url)),
                hub_extras={
                    "items": [
                        {"title": v["title"], "url": v["url"], "brief": v.get("brief", "")}
                        for v in linked
                    ],
                },
            )
            builder.write_page(builder.out_dir / "italia" / sub / slug, html)
            builder.all_pages.append({"title": meta["title"], "url": url, "type": "italia"})
            builder.track_sitemap(url, priority=0.6, changefreq="monthly")
