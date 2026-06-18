"""Controversy pages and index."""

from __future__ import annotations

from site_builder.builders._render import render_page_document
from site_builder.document import document_to_meta


def collect(builder) -> None:
    """Pre-load controversy metadata for explore_next and hub linking."""
    for _path, doc in builder.docs_in("impara/controversie", doc_type="controversy"):
        slug = doc["slug"]
        url = f"/impara/controversie/{slug}/"
        meta = document_to_meta(doc, url=url)
        builder.controversies.append(meta)


def build_pages(builder) -> None:
    if not builder.controversies:
        collect(builder)

    for meta in builder.controversies:
        slug = meta["slug"]
        url = meta["url"]
        doc = builder.doc_at("impara", "controversie", f"{slug}.json")
        if not doc:
            continue
        html = render_page_document(
            builder,
            doc,
            url,
            page_type="controversy",
            template="controversy.html",
            meta=meta,
            breadcrumbs=builder.breadcrumbs(
                ("Impara", "/impara/"),
                ("Controversie", "/impara/controversie/"),
                (meta["title"], url),
            ),
        )
        builder.write_page(builder.out_dir / "impara" / "controversie" / slug, html)
        builder.all_pages.append({"title": meta["title"], "url": url, "type": "controversia"})
        builder.track_sitemap(url, priority=0.6, changefreq="monthly")

    if builder.controversies:
        index = builder.render(
            "hub.html",
            page_type="hub",
            title="Controversie",
            lead="Questioni aperte sul tè verde: prospettive contrastanti dalle fonti.",
            url="/impara/controversie/",
            items=[
                {"title": c["title"], "url": c["url"], "brief": c.get("meta_description", "")}
                for c in builder.controversies
            ],
            breadcrumbs=builder.breadcrumbs(
                ("Impara", "/impara/"),
                ("Controversie", "/impara/controversie/"),
            ),
        )
        builder.write_page(builder.out_dir / "impara" / "controversie", index)
        builder.track_sitemap("/impara/controversie/", priority=0.6, changefreq="weekly")
