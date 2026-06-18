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
    if hub_extras:
        hub_list: list[dict] = list(hub_extras.get("items") or [])
        for section in hub_extras.get("sections") or []:
            hub_list.extend(section.get("items") or [])
        for controversy in hub_extras.get("controversies") or []:
            hub_list.append(
                {
                    "title": controversy.get("title", ""),
                    "url": controversy.get("url", ""),
                }
            )
        if hub_list:
            ctx["hub_list_items"] = hub_list
        if hub_extras.get("sections"):
            ctx["sections"] = hub_extras["sections"]
    return builder.render(template, **ctx)
