"""Shared PageDocument rendering for section builders."""

from __future__ import annotations

from site_builder.document import document_to_meta
from site_builder.page_document import document_to_page


def render_page_document(
    builder,
    doc: dict,
    url: str,
    *,
    page_type: str,
    template: str,
    breadcrumbs: list[dict],
    meta: dict | None = None,
    hub_extras: dict | None = None,
    extra: dict | None = None,
) -> str:
    meta = meta or document_to_meta(doc, url=url)
    page = document_to_page(
        doc,
        url=url,
        base_url=builder.base_url,
        page_type=page_type,
        meta=meta,
        breadcrumbs=breadcrumbs,
        hub_extras=hub_extras,
    )
    ctx = {
        "page_type": page_type,
        "page": page,
        "meta": meta,
        "title": meta.get("title", ""),
        "lead": meta.get("meta_description", ""),
        "url": url,
        "breadcrumbs": breadcrumbs,
        "_doc": doc,
    }
    if extra:
        ctx.update(extra)
    return builder.render(template, **ctx)
