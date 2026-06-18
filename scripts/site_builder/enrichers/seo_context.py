"""Apply SEO context and schema blocks to template render context."""

from __future__ import annotations

from site_builder.enrichers._seo_core import (
    article_schema,
    breadcrumb_schema,
    defined_term_schema,
    dumps_json_ld,
    faq_schema,
    item_list_schema,
    italia_article_schema,
    organization_schema,
    variety_schema,
    webpage_schema,
    website_schema,
)
from site_builder.enrichers.schema_org import supplementary_schemas
from site_builder.document import collect_faq_items


def apply_seo(ctx: dict, builder) -> None:
    meta = ctx.get("meta") or {}
    url = ctx.get("seo_url") or ctx.get("url") or meta.get("url")
    title = ctx.get("seo_title") or ctx.get("title") or meta.get("title") or builder.site_name
    description = (
        ctx.get("seo_description")
        or ctx.get("meta_description")
        or meta.get("meta_description")
        or meta.get("description")
        or ctx.get("lead")
        or "Cultura del tè verde (Camellia sinensis) per chi vive in Italia."
    )
    ctx.setdefault("seo_url", url)
    ctx.setdefault("seo_title", title)
    ctx.setdefault("seo_description", description)
    ctx.setdefault("seo_robots", "noindex,follow" if ctx.get("noindex") else "index,follow")
    page_type = ctx.get("page_type", "")
    if page_type == "search":
        ctx["seo_robots"] = "noindex,follow"

    keywords = meta.get("keywords") or []
    if keywords:
        ctx["seo_keywords"] = ", ".join(keywords)

    ctx.setdefault("seo_hreflang", builder.hreflang)
    ctx.setdefault("seo_locale", builder.locale)
    if builder.og_image:
        social_image = builder.social.get("og_image_social") or builder.og_image
        ctx.setdefault("og_image", f"{builder.base_url}{social_image}")
        ctx.setdefault("og_image_width", builder.social.get("og_image_width", 1200))
        ctx.setdefault("og_image_height", builder.social.get("og_image_height", 630))
        ctx.setdefault(
            "og_image_alt",
            builder.social.get("og_image_alt", f"{builder.site_name} — tè verde in Italia"),
        )
        ctx.setdefault("twitter_image", ctx["og_image"])
        if builder.social.get("og_image_type"):
            ctx.setdefault("og_image_type", builder.social["og_image_type"])
    ctx.setdefault("twitter_card", builder.social.get("twitter_card", "summary_large_image"))
    ctx.setdefault("theme_color", builder.social.get("theme_color", "#3e5c4e"))
    if meta.get("published"):
        ctx["article_published"] = meta["published"]
    if len(description) > 160:
        ctx["seo_description"] = description[:157].rstrip() + "…"
    ctx.setdefault(
        "og_type",
        "article"
        if page_type in ("article", "guide", "variety", "glossary", "controversy")
        else "website",
    )
    ctx["schema_blocks"] = build_schema_blocks(ctx, builder, meta, url, title, description)


def build_schema_blocks(
    ctx: dict, builder, meta: dict, url: str | None, title: str, description: str
) -> list[str]:
    blocks: list[str] = []
    page_type = ctx.get("page_type", "")
    base_url = builder.base_url
    doc = ctx.get("_doc") or {}

    if page_type == "home":
        blocks.append(dumps_json_ld(website_schema(base_url, builder.site_name)))
        blocks.append(
            dumps_json_ld(
                organization_schema(
                    base_url,
                    builder.site_name,
                    same_as=builder.social.get("same_as") or None,
                )
            )
        )

    crumbs = ctx.get("breadcrumbs")
    if crumbs and len(crumbs) > 1:
        blocks.append(dumps_json_ld(breadcrumb_schema(base_url, crumbs)))

    if page_type in ("article", "controversy") and url:
        if url.startswith("/italia/"):
            blocks.append(
                dumps_json_ld(
                    italia_article_schema(
                        base_url, title=title, description=description, url=url
                    )
                )
            )
        else:
            blocks.append(
                dumps_json_ld(
                    article_schema(base_url, title=title, description=description, url=url)
                )
            )
        faq_items = collect_faq_items(doc=doc, page=ctx.get("page"))
        faq = faq_schema(faq_items or meta.get("faqs", []))
        if faq:
            blocks.append(dumps_json_ld(faq))
    elif page_type == "variety" and url:
        blocks.append(
            dumps_json_ld(
                variety_schema(
                    base_url,
                    title=title,
                    description=description,
                    url=url,
                    origin_slug=meta.get("origine_slug", ""),
                    origin_label=meta.get("origine", ""),
                )
            )
        )
        faq_items = collect_faq_items(doc=doc, page=ctx.get("page"))
        faq = faq_schema(faq_items or meta.get("faqs", []))
        if faq:
            blocks.append(dumps_json_ld(faq))
    elif page_type == "hub" and url and url.startswith("/italia/"):
        blocks.append(
            dumps_json_ld(
                italia_article_schema(base_url, title=title, description=description, url=url)
            )
        )
    elif page_type == "glossary" and url:
        blocks.append(
            dumps_json_ld(
                defined_term_schema(
                    base_url, name=title, description=description, url=url
                )
            )
        )
        faq_items = collect_faq_items(doc=doc, page=ctx.get("page"))
        faq = faq_schema(faq_items or meta.get("faqs", []))
        if faq:
            blocks.append(dumps_json_ld(faq))
    elif page_type == "catalog" and url:
        blocks.append(
            dumps_json_ld(
                webpage_schema(
                    base_url, title=title, description=description, url=url, italy_context=True
                )
            )
        )
        varieties = ctx.get("varieties") or []
        if varieties:
            blocks.append(
                dumps_json_ld(
                    item_list_schema(base_url, name=title, url=url, items=varieties)
                )
            )
    elif page_type in ("gioca", "diario", "community", "quiz") and url:
        blocks.append(
            dumps_json_ld(
                webpage_schema(
                    base_url, title=title, description=description, url=url, italy_context=True
                )
            )
        )
    elif page_type == "hub" and url and not url.startswith("/italia/"):
        blocks.append(
            dumps_json_ld(
                webpage_schema(
                    base_url, title=title, description=description, url=url, italy_context=True
                )
            )
        )

    if doc:
        for extra in supplementary_schemas(base_url, doc=doc, meta=meta, url=url or ""):
            blocks.append(dumps_json_ld(extra))

    return blocks
