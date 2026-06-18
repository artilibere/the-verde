"""Glossary term pages and index."""

from __future__ import annotations

from site_builder.builders._render import render_page_document
from site_builder.document import document_to_meta
from site_builder.enrichers.navigation import explore_next


def build(builder) -> None:
    for _path, doc in builder.docs_in("glossario", doc_type="glossary"):
        slug = doc["slug"]
        url = f"/glossario/{slug}/"
        meta = document_to_meta(doc, url=url)
        meta["explore_next"] = explore_next(
            slug,
            meta,
            varieties=builder.varieties,
            controversies=builder.controversies,
            relazioni=builder.relazioni if isinstance(builder.relazioni, dict) else {},
            hubs=builder.hubs,
            glossary=[],
        )
        builder.glossary.append(meta)

        html = render_page_document(
            builder,
            doc,
            url,
            page_type="glossary",
            template="glossary.html",
            meta=meta,
            breadcrumbs=builder.breadcrumbs(("Glossario", "/glossario/"), (meta["title"], url)),
        )
        builder.write_page(builder.out_dir / "glossario" / slug, html)
        builder.all_pages.append({"title": meta["title"], "url": url, "type": "glossario"})
        builder.track_sitemap(url, priority=0.5, changefreq="yearly")

    if builder.glossary:
        index = builder.render(
            "hub.html",
            page_type="hub",
            title="Glossario",
            lead="Termini del mondo del tè verde, con glossa in italiano.",
            url="/glossario/",
            items=sorted(
                [
                    {"title": g["title"], "url": g["url"], "brief": g.get("meta_description", "")}
                    for g in builder.glossary
                ],
                key=lambda x: x["title"],
            ),
            breadcrumbs=builder.breadcrumbs(("Glossario", "/glossario/")),
        )
        builder.write_page(builder.out_dir / "glossario", index)
        builder.track_sitemap("/glossario/", priority=0.6, changefreq="weekly")
