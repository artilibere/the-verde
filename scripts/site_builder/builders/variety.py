"""Variety catalog and detail pages."""

from __future__ import annotations

from site_builder.document import document_to_meta, variety_breadcrumb_title
from site_builder.enrichers.navigation import PATH_ORDER, explore_next, path_nav
from site_builder.page_document import document_to_page


def collect_varieties(builder) -> None:
    items = builder.docs_in("varieta", doc_type="variety")
    if not items:
        return

    for _path, doc in items:
        slug = doc["slug"]
        url = f"/varieta/{slug}/"
        meta = document_to_meta(doc, url=url)
        variety = {**meta, "path_nav": path_nav(slug, builder.variety_title), "explore_next": []}
        builder.varieties.append(variety)

    builder.varieties.sort(
        key=lambda v: (
            PATH_ORDER.index(v["slug"]) if v["slug"] in PATH_ORDER else 99,
            v.get("origine", ""),
            v["title"],
        )
    )

    relazioni = builder.relazioni if isinstance(builder.relazioni, dict) else {}
    for v in builder.varieties:
        v["explore_next"] = explore_next(
            v["slug"],
            v,
            varieties=builder.varieties,
            controversies=builder.controversies,
            relazioni=relazioni,
            hubs=builder.hubs,
            glossary=builder.glossary,
        )


def build_catalog_and_pages(builder) -> None:
    from asset_pipeline import dumps_compact

    items = builder.docs_in("varieta", doc_type="variety")
    if not items:
        return

    index_json = {
        "varieties": [
            {
                "slug": v["slug"],
                "title": v["title"],
                "brief": (v.get("brief") or "")[:80],
                "origine": v.get("origine_slug", ""),
                "stile": v.get("stile_slug", ""),
                "caffeina": v.get("caffeina_slug", ""),
                "stagione": v.get("stagione_slug", ""),
                "url": v["url"],
            }
            for v in builder.varieties
        ],
    }
    config_out = builder.out_dir / "assets" / "js" / "config"
    config_out.mkdir(parents=True, exist_ok=True)
    (config_out / "varieties.json").write_text(dumps_compact(index_json), encoding="utf-8")

    for _path, doc in items:
        slug = doc["slug"]
        url = f"/varieta/{slug}/"
        v = next(x for x in builder.varieties if x["slug"] == slug)
        crumbs = builder.breadcrumbs(
            ("Varietà", "/varieta/"),
            (variety_breadcrumb_title(v["title"]), url),
        )
        page = document_to_page(
            doc,
            url=url,
            base_url=builder.base_url,
            page_type="variety",
            meta=v,
            breadcrumbs=crumbs,
        )
        html = builder.renderer.render(
            "variety.html",
            page_type="variety",
            page=page,
            meta=v,
            breadcrumbs=crumbs,
            _doc=doc,
        )
        builder.write_page(builder.out_dir / "varieta" / slug, html)
        builder.all_pages.append({"title": v["title"], "url": url, "type": "varieta"})
        builder.track_sitemap(url, priority=0.8, changefreq="monthly")

    catalog = builder.renderer.render(
        "catalog.html",
        page_type="catalog",
        title="Varietà di tè verde",
        meta_description="Catalogo enciclopedico di varietà di tè verde: origine, stile, preparazione e contesto italiano.",
        url="/varieta/",
        varieties=builder.varieties,
        breadcrumbs=builder.breadcrumbs(("Varietà", "/varieta/")),
    )
    builder.write_page(builder.out_dir / "varieta", catalog)
    builder.track_sitemap("/varieta/", priority=0.9, changefreq="weekly")
