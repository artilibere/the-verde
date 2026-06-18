"""Jinja2 template renderer for PageDocument and legacy context."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from site_builder.blocks import has_level_sections, render_blocks
from site_builder.enrichers.seo_context import apply_seo


class TemplateRenderer:
    def __init__(self, templates_dir: Path, site_name: str, base_url: str, nav: list):
        self.site_name = site_name
        self.base_url = base_url
        self.nav = nav
        self.css_url = "/assets/css/site.css"
        self.js_urls: dict[str, str] = {}
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.env.globals["asset_css"] = lambda: self.css_url
        self.env.globals["asset_js"] = lambda name: self.js_urls.get(name, f"/assets/js/{name}.js")
        self._hreflang = "it"
        self._locale = "it-IT"
        self._og_image = ""
        self._social: dict = {}

    def configure_site(
        self,
        *,
        hreflang: str,
        locale: str,
        og_image: str,
        social: dict,
        css_url: str,
        js_urls: dict[str, str],
    ) -> None:
        self._hreflang = hreflang
        self._locale = locale
        self._og_image = og_image
        self._social = social
        self.css_url = css_url
        self.js_urls = js_urls

    def render(self, template: str, **ctx) -> str:
        ctx.setdefault("site_name", self.site_name)
        ctx.setdefault("nav", self.nav)
        ctx.setdefault("base_url", self.base_url)
        ctx.setdefault("year", date.today().year)

        builder_proxy = _BuilderProxy(
            site_name=self.site_name,
            base_url=self.base_url,
            hreflang=self._hreflang,
            locale=self._locale,
            og_image=self._og_image,
            social=self._social,
        )
        apply_seo(ctx, builder_proxy)

        page = ctx.get("page")
        if page and page.get("schema"):
            # PageDocument @graph replaces apply_seo schema_blocks for typed pages.
            ctx["schema_graph_json"] = json.dumps(page["schema"], ensure_ascii=False)
            ctx["schema_blocks"] = [
                json.dumps(page["schema"], ensure_ascii=False, separators=(",", ":"))
            ]

        doc = ctx.get("_doc")
        content_html = ctx.get("content_html", "")
        if doc and "has_levels" not in ctx:
            blocks = doc.get("body", {}).get("blocks", [])
            ctx["has_levels"] = has_level_sections(blocks)
        elif page and "has_levels" not in ctx:
            ctx["has_levels"] = any(c.get("id") == "deep" for c in page.get("cards", []))
        elif content_html and "has_levels" not in ctx:
            ctx["has_levels"] = "Approfondimento" in content_html

        return self.env.get_template(template).render(**ctx)

    def render_legacy_body(self, doc: dict, *, page_type: str | None = None) -> str:
        blocks = doc.get("body", {}).get("blocks", [])
        ptype = "variety" if doc.get("type") == "variety" else page_type
        return render_blocks(blocks, page_type=ptype if doc.get("type") == "variety" else None)


class _BuilderProxy:
    """Minimal proxy so apply_seo can read site config from renderer."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
