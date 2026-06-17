# -*- coding: utf-8 -*-
"""Build static site for the-verde.it from Markdown content."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asset_pipeline import (
    asset_source_signature,
    build_assets,
    dumps_compact,
    load_asset_manifest,
    minify_html,
    save_asset_manifest,
)
from html_enrich import enrich_variety_html
from seo import (
    article_schema,
    breadcrumb_schema,
    build_robots_txt,
    build_sitemap_xml,
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
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / ".cache"
ASSET_MANIFEST = CACHE_DIR / "asset-manifest.json"
PATH_ORDER = ["bancha", "sencha", "gyokuro", "matcha"]
MD_EXTENSIONS = ["extra", "smarty", "toc"]


def slugify(text: str) -> str:
    text = text.lower().strip()
    for old, new in [("\u00e0", "a"), ("\u00e8", "e"), ("\u00e9", "e"), ("\u00ec", "i"), ("\u00f2", "o"), ("\u00f9", "u")]:
        text = text.replace(old, new)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def load_json(path: Path) -> dict | list:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def parse_md(path: Path) -> tuple[dict, str, frontmatter.Post]:
    post = frontmatter.load(path)
    meta = dict(post.metadata)
    meta.setdefault("slug", path.stem)
    html = markdown.markdown(post.content, extensions=MD_EXTENSIONS)
    return meta, html, post


def extract_section(html: str, heading: str) -> str | None:
    pattern = rf"<h2[^>]*>{re.escape(heading)}</h2>(.*?)(?=<h2|$)"
    m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else None


def parse_faq(html: str) -> list[dict]:
    faqs = []
    section = extract_section(html, "Domande frequenti")
    if not section:
        return faqs
    parts = re.split(r"<h3[^>]*>", section)
    for part in parts[1:]:
        m = re.match(r"(.*?)</h3>\s*(.*)", part, re.DOTALL)
        if m:
            q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            a = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            if q and a:
                faqs.append({"question": q, "answer": a})
    return faqs


def parse_sensory(html: str) -> dict:
    section = extract_section(html, "Profilo sensoriale")
    profile = {}
    if not section:
        return profile
    for label in ("Aspetto", "Aroma", "Gusto", "Retrogusto"):
        m = re.search(rf"<strong>{label}:</strong>\s*([^<]+)", section)
        if m:
            profile[label.lower()] = m.group(1).strip()
    return profile


def parse_steps(html: str) -> list[dict]:
    section = extract_section(html, "I passaggi") or extract_section(html, "Preparazione")
    steps = []
    if not section:
        return steps
    for m in re.finditer(r"<li>(.*?)</li>", section, re.DOTALL):
        raw = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if " - " in raw:
            action, time = raw.split(" - ", 1)
            steps.append({"action": action.strip(), "time": time.strip()})
        else:
            steps.append({"action": raw, "time": ""})
    return steps


def parse_related_varieties(html: str) -> list[dict]:
    section = extract_section(html, "Varietà simili")
    related = []
    if not section:
        return related
    for m in re.finditer(r"<li>(.*?)</li>", section, re.DOTALL):
        raw = m.group(1)
        link = re.search(r'href="([^"]+)"', raw)
        name = re.search(r"<strong>([^<]+)</strong>", raw)
        plain = re.sub(r"<[^>]+>", "", raw)
        reason_m = re.search(r"[-\u2014]\s*(.+)$", plain)
        url = link.group(1) if link else ""
        if not url:
            # Markdown often renders as plain text: "Gyokuro (/varieta/gyokuro/) — motivo"
            url_m = re.search(r"(\(/varieta/[^)]+\))", plain)
            if url_m:
                url = url_m.group(1).strip("()")
            else:
                url_m = re.search(r"(/varieta/[a-z0-9\-]+/)", plain)
                url = url_m.group(1) if url_m else ""
        if name and url:
            related.append(
                {
                    "url": url,
                    "name": name.group(1),
                    "reason": reason_m.group(1).strip() if reason_m else "",
                }
            )
    return related


def variety_breadcrumb_title(title: str) -> str:
    for sep in (" — ", " - "):
        if sep in title:
            return title.split(sep, 1)[0].strip()
    return title.strip()


def write_page(out_dir: Path, html: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(minify_html(html), encoding="utf-8")

class SiteBuilder:
    def __init__(self, content_dir: Path, out_dir: Path, templates_dir: Path, assets_dir: Path):
        self.content_dir = content_dir
        self.out_dir = out_dir
        self.assets_dir = assets_dir
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.sitemap = load_json(content_dir / "_config" / "sitemap.json")
        self.relazioni = load_json(content_dir / "relazioni.json")
        self.badges = load_json(content_dir / "_config" / "badges.json")
        self.quizzes = load_json(content_dir / "_config" / "quizzes.json")
        self.paths_config = load_json(content_dir / "_config" / "paths.json")
        self.seasons = load_json(content_dir / "_config" / "seasons.json")
        self.base_url = self.sitemap.get("base_url", "https://the-verde.it")
        self.hreflang = self.sitemap.get("hreflang", "it")
        self.locale = self.sitemap.get("locale", "it-IT")
        self.og_image = self.sitemap.get("og_image", "")
        self.social = self.sitemap.get("social", {})
        self.nav = self.sitemap.get("nav", [])
        self.varieties: list[dict] = []
        self.glossary: list[dict] = []
        self.guides: list[dict] = []
        self.hubs: list[dict] = []
        self.controversies: list[dict] = []
        self.all_pages: list[dict] = []
        self.sitemap_urls: list[dict] = []
        self.site_name = self.sitemap.get("site_name", "The Verde")
        self.css_url = "/assets/css/site.css"
        self.js_urls: dict[str, str] = {}
        self.env.globals["asset_css"] = lambda: self.css_url
        self.env.globals["asset_js"] = lambda name: self.js_urls.get(name, f"/assets/js/{name}.js")

    def render(self, template: str, **ctx) -> str:
        ctx.setdefault("site_name", self.site_name)
        ctx.setdefault("nav", self.nav)
        ctx.setdefault("base_url", self.base_url)
        ctx.setdefault("year", date.today().year)
        self._apply_seo(ctx)
        content_html = ctx.get("content_html", "")
        if content_html and "has_levels" not in ctx:
            ctx["has_levels"] = bool(
                re.search(r"<h2[^>]*>.*?Approfondimento", content_html, re.I | re.DOTALL)
            )
        return self.env.get_template(template).render(**ctx)

    def track_sitemap(
        self,
        url: str,
        *,
        changefreq: str = "monthly",
        priority: float = 0.5,
    ) -> None:
        if not url.endswith("/"):
            url = f"{url}/"
        self.sitemap_urls.append(
            {
                "loc": f"{self.base_url}{url}",
                "lastmod": date.today().isoformat(),
                "changefreq": changefreq,
                "priority": priority,
            }
        )

    def _apply_seo(self, ctx: dict) -> None:
        meta = ctx.get("meta") or {}
        url = ctx.get("seo_url") or ctx.get("url") or meta.get("url")
        title = ctx.get("seo_title") or ctx.get("title") or meta.get("title") or self.site_name
        description = (
            ctx.get("seo_description")
            or ctx.get("meta_description")
            or meta.get("meta_description")
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
        ctx.setdefault("seo_hreflang", self.hreflang)
        ctx.setdefault("seo_locale", self.locale)
        if self.og_image:
            ctx.setdefault("og_image", f"{self.base_url}{self.og_image}")
            ctx.setdefault("og_image_width", self.social.get("og_image_width", 1200))
            ctx.setdefault("og_image_height", self.social.get("og_image_height", 630))
            ctx.setdefault(
                "og_image_alt",
                self.social.get("og_image_alt", f"{self.site_name} — tè verde in Italia"),
            )
        ctx.setdefault("twitter_card", self.social.get("twitter_card", "summary_large_image"))
        ctx.setdefault("theme_color", self.social.get("theme_color", "#3e5c4e"))
        if meta.get("published"):
            ctx["article_published"] = meta["published"]
        if len(description) > 160:
            description = description[:157].rstrip() + "…"
            ctx["seo_description"] = description
        ctx.setdefault("og_type", "article" if page_type in ("article", "guide", "variety", "glossary", "controversy") else "website")
        ctx["schema_blocks"] = self._schema_blocks(ctx, meta, url, title, description)

    def _schema_blocks(
        self, ctx: dict, meta: dict, url: str | None, title: str, description: str
    ) -> list[str]:
        blocks: list[str] = []
        page_type = ctx.get("page_type", "")

        if page_type == "home":
            blocks.append(dumps_json_ld(website_schema(self.base_url, self.site_name)))
            blocks.append(
                dumps_json_ld(
                    organization_schema(
                        self.base_url,
                        self.site_name,
                        same_as=self.social.get("same_as") or None,
                    )
                )
            )

        crumbs = ctx.get("breadcrumbs")
        if crumbs and len(crumbs) > 1:
            blocks.append(dumps_json_ld(breadcrumb_schema(self.base_url, crumbs)))

        if page_type in ("article", "controversy") and url:
            if url.startswith("/italia/"):
                blocks.append(
                    dumps_json_ld(
                        italia_article_schema(
                            self.base_url, title=title, description=description, url=url
                        )
                    )
                )
            else:
                blocks.append(
                    dumps_json_ld(
                        article_schema(self.base_url, title=title, description=description, url=url)
                    )
                )
        elif page_type == "variety" and url:
            blocks.append(
                dumps_json_ld(
                    variety_schema(
                        self.base_url,
                        title=title,
                        description=description,
                        url=url,
                        origin_slug=meta.get("origine_slug", ""),
                        origin_label=meta.get("origine", ""),
                    )
                )
            )
            faq = faq_schema(meta.get("faqs", []))
            if faq:
                blocks.append(dumps_json_ld(faq))
        elif page_type == "hub" and url and url.startswith("/italia/"):
            blocks.append(
                dumps_json_ld(
                    italia_article_schema(
                        self.base_url, title=title, description=description, url=url
                    )
                )
            )
        elif page_type == "glossary" and url:
            blocks.append(
                dumps_json_ld(
                    defined_term_schema(
                        self.base_url,
                        name=title,
                        description=description,
                        url=url,
                    )
                )
            )
        elif page_type == "catalog" and url:
            blocks.append(
                dumps_json_ld(
                    webpage_schema(
                        self.base_url,
                        title=title,
                        description=description,
                        url=url,
                        italy_context=True,
                    )
                )
            )
            varieties = ctx.get("varieties") or []
            if varieties:
                blocks.append(
                    dumps_json_ld(
                        item_list_schema(
                            self.base_url,
                            name=title,
                            url=url,
                            items=varieties,
                        )
                    )
                )
        elif page_type in ("gioca", "diario", "community", "quiz") and url:
            blocks.append(
                dumps_json_ld(
                    webpage_schema(
                        self.base_url,
                        title=title,
                        description=description,
                        url=url,
                        italy_context=True,
                    )
                )
            )
        elif page_type == "hub" and url and not url.startswith("/italia/"):
            blocks.append(
                dumps_json_ld(
                    webpage_schema(
                        self.base_url,
                        title=title,
                        description=description,
                        url=url,
                        italy_context=True,
                    )
                )
            )

        return blocks

    def build_sitemap(self) -> None:
        seen = set()
        entries = []
        for entry in self.sitemap_urls:
            if entry["loc"] in seen:
                continue
            seen.add(entry["loc"])
            entries.append(entry)
        entries.sort(key=lambda e: e["loc"])
        (self.out_dir / "sitemap.xml").write_text(
            build_sitemap_xml(entries, hreflang=self.hreflang), encoding="utf-8"
        )
        (self.out_dir / "robots.txt").write_text(build_robots_txt(self.base_url), encoding="utf-8")

    def breadcrumbs(self, *crumbs: tuple[str, str]) -> list[dict]:
        items = [{"name": "Home", "url": "/"}]
        for name, url in crumbs:
            items.append({"name": name, "url": url})
        return items

    def variety_title(self, slug: str) -> str:
        v = next((x for x in self.varieties if x["slug"] == slug), None)
        if v:
            return variety_breadcrumb_title(v["title"])
        return slug.replace("-", " ").title()

    def path_nav(self, slug: str) -> dict | None:
        if slug not in PATH_ORDER:
            return None
        idx = PATH_ORDER.index(slug)
        nav = {"current": slug, "index": idx + 1, "total": len(PATH_ORDER)}
        if idx > 0:
            prev_slug = PATH_ORDER[idx - 1]
            nav["prev"] = {
                "slug": prev_slug,
                "title": self.variety_title(prev_slug),
                "url": f"/varieta/{prev_slug}/",
            }
        if idx < len(PATH_ORDER) - 1:
            next_slug = PATH_ORDER[idx + 1]
            nav["next"] = {
                "slug": next_slug,
                "title": self.variety_title(next_slug),
                "url": f"/varieta/{next_slug}/",
            }
        return nav

    def explore_next(self, slug: str, meta: dict) -> list[dict]:
        links = []
        for rs in meta.get("related_slugs", []):
            v = next((x for x in self.varieties if x["slug"] == rs), None)
            if v:
                links.append({"type": "varieta", "title": v["title"], "url": v["url"], "brief": v.get("brief", "")})
        temi = meta.get("temi_kb", [])
        if temi and self.relazioni:
            tema_map = {t["id"]: t for t in self.relazioni.get("temi", [])}
            for tid in temi[:2]:
                if tid in tema_map:
                    t = tema_map[tid]
                    links.append({"type": "tema", "title": t["nome"], "url": t["url"], "brief": ""})
        for cid in meta.get("controversie", [])[:1]:
            c = next((x for x in self.controversies if x["slug"] == cid), None)
            if c:
                links.append({"type": "controversia", "title": c["title"], "url": c["url"], "brief": c.get("brief", "")})
        return links[:4]

    def build_varieties(self) -> None:
        var_dir = self.content_dir / "varieta"
        if not var_dir.exists():
            return
        for path in sorted(var_dir.glob("*.md")):
            meta, html, post = parse_md(path)
            slug = meta["slug"]
            url = f"/varieta/{slug}/"
            meta["url"] = url
            brief_m = re.search(r"<p>(.*?)</p>", html)
            brief = meta.get("brief") or (re.sub(r"<[^>]+>", "", brief_m.group(1))[:160] if brief_m else "")
            variety = {
                **meta,
                "slug": slug,
                "url": url,
                "brief": brief,
                "origine_slug": slugify(meta.get("origine", "")),
                "stile_slug": slugify(meta.get("stile", "")),
                "caffeina_slug": slugify(meta.get("caffeina", "")),
                "stagione_slug": slugify(meta.get("stagione", "")),
                "sensory": parse_sensory(html),
                "steps": parse_steps(html),
                "faqs": parse_faq(html),
                "related_varieties": parse_related_varieties(html),
                "path_nav": self.path_nav(slug),
                "explore_next": [],
            }
            variety["explore_next"] = self.explore_next(slug, meta)
            self.varieties.append(variety)

        self.varieties.sort(key=lambda v: (
            PATH_ORDER.index(v["slug"]) if v["slug"] in PATH_ORDER else 99,
            v.get("origine", ""),
            v["title"],
        ))

        for v in self.varieties:
            v["explore_next"] = self.explore_next(v["slug"], v)

        index_json = {
            "varieties": [
                {
                    "slug": v["slug"],
                    "title": v["title"],
                    "brief": (v.get("brief") or "")[:120],
                    "origine": v.get("origine_slug", ""),
                    "stile": v.get("stile_slug", ""),
                    "caffeina": v.get("caffeina_slug", ""),
                    "stagione": v.get("stagione_slug", ""),
                    "url": v["url"],
                }
                for v in self.varieties
            ],
        }
        var_out = self.out_dir / "varieta"
        var_out.mkdir(parents=True, exist_ok=True)
        (var_out / "index.json").write_text(dumps_compact(index_json), encoding="utf-8")

        for v in self.varieties:
            _, html_body, _ = parse_md(var_dir / f"{v['slug']}.md")
            html_body = enrich_variety_html(
                html_body,
                v.get("steps"),
                v.get("faqs"),
                v.get("related_varieties"),
            )
            page = self.render(
                "variety.html",
                page_type="variety",
                meta=v,
                content_html=html_body,
                breadcrumbs=self.breadcrumbs(
                    ("Varietà", "/varieta/"),
                    (variety_breadcrumb_title(v["title"]), v["url"]),
                ),
            )
            write_page(self.out_dir / "varieta" / v["slug"], page)
            self.all_pages.append({"title": v["title"], "url": v["url"], "type": "varieta"})
            self.track_sitemap(v["url"], priority=0.8, changefreq="monthly")

        catalog = self.render(
            "catalog.html",
            page_type="catalog",
            title="Varietà di tè verde",
            meta_description="Catalogo enciclopedico di varietà di tè verde: origine, stile, preparazione e contesto italiano.",
            url="/varieta/",
            varieties=self.varieties,
            breadcrumbs=self.breadcrumbs(("Varietà", "/varieta/")),
        )
        write_page(self.out_dir / "varieta", catalog)
        self.track_sitemap("/varieta/", priority=0.9, changefreq="weekly")

    def build_guides(self) -> None:
        guide_dir = self.content_dir / "guide"
        if not guide_dir.exists():
            return
        for path in sorted(guide_dir.glob("*.md")):
            meta, html, _ = parse_md(path)
            slug = meta["slug"]
            url = f"/guide/{slug}/"
            meta.update({"url": url, "slug": slug})
            self.guides.append(meta)
            page = self.render(
                "article.html",
                page_type="article",
                meta=meta,
                content_html=html,
                breadcrumbs=self.breadcrumbs(("Guide", "/guide/"), (meta["title"], url)),
            )
            write_page(self.out_dir / "guide" / slug, page)
            self.all_pages.append({"title": meta["title"], "url": url, "type": "guide"})
            self.track_sitemap(url, priority=0.7, changefreq="monthly")

        if self.guides:
            index = self.render(
                "hub.html",
                page_type="hub",
                title="Guide editoriali",
                lead="Articoli narrativi sul tè verde: cultura, storia e contesto italiano.",
                url="/guide/",
                items=[{"title": g["title"], "url": g["url"], "brief": g.get("meta_description", "")} for g in self.guides],
                breadcrumbs=self.breadcrumbs(("Guide", "/guide/")),
            )
            write_page(self.out_dir / "guide", index)
            self.track_sitemap("/guide/", priority=0.7, changefreq="weekly")

    def build_impara(self) -> None:
        impara_dir = self.content_dir / "impara"
        if not impara_dir.exists():
            return
        temi = self.relazioni.get("temi", [])
        contro_dir = impara_dir / "controversie"
        if contro_dir.exists():
            for path in sorted(contro_dir.glob("*.md")):
                meta, html, _ = parse_md(path)
                slug = meta["slug"]
                url = f"/impara/controversie/{slug}/"
                meta.update({"url": url, "slug": slug})
                self.controversies.append(meta)
        for path in sorted(impara_dir.glob("*.md")):
            meta, html, _ = parse_md(path)
            slug = meta["slug"]
            url = f"/impara/{slug}/"
            meta.update({"url": url, "slug": slug})
            tema = next((t for t in temi if slug in t.get("url", "")), None)
            linked_varieties = [v for v in self.varieties if tema and tema["id"] in v.get("temi_kb", [])]
            if not linked_varieties and tema:
                vt = self.relazioni.get("varieta_temi", {})
                for vs, ts in vt.items():
                    if tema["id"] in ts:
                        lv = next((v for v in self.varieties if v["slug"] == vs), None)
                        if lv:
                            linked_varieties.append(lv)
            linked_controversies = []
            if tema:
                for c in self.controversies:
                    if c["slug"] in tema.get("controversie", []):
                        linked_controversies.append(c)
            self.hubs.append(meta)
            page = self.render(
                "hub.html",
                page_type="hub",
                title=meta["title"],
                lead=meta.get("meta_description", ""),
                url=url,
                content_html=html,
                items=[{"title": v["title"], "url": v["url"], "brief": v.get("brief", "")} for v in linked_varieties[:6]],
                controversies=linked_controversies,
                relazioni=[r for r in self.relazioni.get("relazioni", []) if tema and (r["da"] == tema["id"] or r["a"] == tema["id"])],
                breadcrumbs=self.breadcrumbs(("Impara", "/impara/"), (meta["title"], url)),
            )
            write_page(self.out_dir / "impara" / slug, page)
            self.all_pages.append({"title": meta["title"], "url": url, "type": "impara"})
            self.track_sitemap(url, priority=0.7, changefreq="monthly")

        if self.controversies:
            for meta in self.controversies:
                slug = meta["slug"]
                url = meta["url"]
                _, html, _ = parse_md(contro_dir / f"{slug}.md")
                page = self.render(
                    "controversy.html",
                    page_type="controversy",
                    meta=meta,
                    content_html=html,
                    breadcrumbs=self.breadcrumbs(
                        ("Impara", "/impara/"),
                        ("Controversie", "/impara/controversie/"),
                        (meta["title"], url),
                    ),
                )
                write_page(self.out_dir / "impara" / "controversie" / slug, page)
                self.all_pages.append({"title": meta["title"], "url": url, "type": "controversia"})
                self.track_sitemap(url, priority=0.6, changefreq="monthly")

            idx = self.render(
                "hub.html",
                page_type="hub",
                title="Controversie",
                lead="Questioni aperte sul tè verde: prospettive contrastanti dalle fonti.",
                url="/impara/controversie/",
                items=[{"title": c["title"], "url": c["url"], "brief": c.get("meta_description", "")} for c in self.controversies],
                breadcrumbs=self.breadcrumbs(("Impara", "/impara/"), ("Controversie", "/impara/controversie/")),
            )
            write_page(self.out_dir / "impara" / "controversie", idx)
            self.track_sitemap("/impara/controversie/", priority=0.6, changefreq="weekly")

        index = self.render(
            "hub.html",
            page_type="hub",
            title="Impara",
            lead="Otto pilastri di conoscenza sul tè verde, dalla storia alla scienza.",
            url="/impara/",
            items=[{"title": t["nome"], "url": t["url"], "brief": ""} for t in temi],
            breadcrumbs=self.breadcrumbs(("Impara", "/impara/")),
        )
        write_page(self.out_dir / "impara", index)
        self.track_sitemap("/impara/", priority=0.8, changefreq="weekly")

    def build_italia(self) -> None:
        italia_dir = self.content_dir / "italia"
        if not italia_dir.exists():
            return
        hub_path = italia_dir / "index.md"
        if hub_path.exists():
            meta, html, _ = parse_md(hub_path)
            page = self.render(
                "hub.html",
                page_type="hub",
                title=meta.get("title", "In Italia"),
                lead=meta.get("meta_description", ""),
                url="/italia/",
                content_html=html,
                breadcrumbs=self.breadcrumbs(("In Italia", "/italia/")),
            )
            write_page(self.out_dir / "italia", page)
            self.track_sitemap("/italia/", priority=0.7, changefreq="weekly")

        for sub, prefix in [("momenti", "/italia/momenti/"), ("stagioni", "/italia/stagioni/")]:
            sub_dir = italia_dir / sub
            if not sub_dir.exists():
                continue
            for path in sorted(sub_dir.glob("*.md")):
                meta, html, _ = parse_md(path)
                slug = meta["slug"]
                url = f"{prefix}{slug}/"
                meta.update({"url": url, "slug": slug})
                linked = [v for v in self.varieties if slug in v.get("momenti", []) or slug in v.get("stagioni", [])]
                page = self.render(
                    "hub.html",
                    page_type="hub",
                    title=meta["title"],
                    lead=meta.get("meta_description", ""),
                    url=url,
                    content_html=html,
                    items=[{"title": v["title"], "url": v["url"], "brief": v.get("brief", "")} for v in linked],
                    breadcrumbs=self.breadcrumbs(("In Italia", "/italia/"), (meta["title"], url)),
                )
                write_page(self.out_dir / "italia" / sub / slug, page)
                self.all_pages.append({"title": meta["title"], "url": url, "type": "italia"})
                self.track_sitemap(url, priority=0.6, changefreq="monthly")

        abbinamenti = italia_dir / "abbinamenti.md"
        if abbinamenti.exists():
            meta, html, _ = parse_md(abbinamenti)
            page = self.render(
                "article.html",
                page_type="article",
                meta={**meta, "url": "/italia/abbinamenti/", "slug": "abbinamenti"},
                content_html=html,
                breadcrumbs=self.breadcrumbs(("In Italia", "/italia/"), ("Abbinamenti", "/italia/abbinamenti/")),
            )
            write_page(self.out_dir / "italia" / "abbinamenti", page)
            self.track_sitemap("/italia/abbinamenti/", priority=0.6, changefreq="monthly")

    def build_glossario(self) -> None:
        gloss_dir = self.content_dir / "glossario"
        if not gloss_dir.exists():
            return
        for path in sorted(gloss_dir.glob("*.md")):
            meta, html, _ = parse_md(path)
            slug = meta["slug"]
            url = f"/glossario/{slug}/"
            meta.update({"url": url, "slug": slug})
            self.glossary.append(meta)
            page = self.render(
                "glossary.html",
                page_type="glossary",
                meta=meta,
                content_html=html,
                breadcrumbs=self.breadcrumbs(("Glossario", "/glossario/"), (meta["title"], url)),
            )
            write_page(self.out_dir / "glossario" / slug, page)
            self.all_pages.append({"title": meta["title"], "url": url, "type": "glossario"})
            self.track_sitemap(url, priority=0.5, changefreq="yearly")

        if self.glossary:
            index = self.render(
                "hub.html",
                page_type="hub",
                title="Glossario",
                lead="Termini del mondo del tè verde, con glossa in italiano.",
                url="/glossario/",
                items=sorted([{"title": g["title"], "url": g["url"], "brief": g.get("meta_description", "")} for g in self.glossary], key=lambda x: x["title"]),
                breadcrumbs=self.breadcrumbs(("Glossario", "/glossario/")),
            )
            write_page(self.out_dir / "glossario", index)
            self.track_sitemap("/glossario/", priority=0.6, changefreq="weekly")

    def build_gioca(self) -> None:
        gioca_dir = self.content_dir / "gioca"
        percorsi = []
        if (gioca_dir / "percorsi").exists():
            for path in sorted((gioca_dir / "percorsi").glob("*.md")):
                meta, html, _ = parse_md(path)
                slug = meta["slug"]
                url = f"/gioca/percorsi/{slug}/"
                meta.update({"url": url, "slug": slug, "content_html": html})
                percorsi.append(meta)
                page = self.render(
                    "article.html",
                    page_type="article",
                    meta=meta,
                    content_html=html,
                    breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/"), ("Percorsi", "/gioca/percorsi/"), (meta["title"], url)),
                )
                write_page(self.out_dir / "gioca" / "percorsi" / slug, page)
                self.track_sitemap(url, priority=0.6, changefreq="monthly")

        quiz_items = self.quizzes.get("quizzes", []) if isinstance(self.quizzes, dict) else []
        for q in quiz_items:
            quiz_url = f"/gioca/quiz/{q['slug']}/"
            page = self.render(
                "quiz.html",
                page_type="quiz",
                quiz=q,
                url=quiz_url,
                seo_title=q["title"],
                seo_description=q.get("description", "Quiz sul tè verde per chi vive in Italia."),
                breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/"), ("Quiz", "/gioca/quiz/"), (q["title"], quiz_url)),
            )
            write_page(self.out_dir / "gioca" / "quiz" / q["slug"], page)
            self.track_sitemap(f"/gioca/quiz/{q['slug']}/", priority=0.4, changefreq="yearly")

        hub = self.render(
            "gioca.html",
            page_type="gioca",
            title="Gioca e impara",
            url="/gioca/",
            meta_description="Percorsi guidati, quiz e badge per esplorare il tè verde con calma.",
            percorsi=percorsi,
            quizzes=quiz_items,
            badges=self.badges.get("badges", []) if isinstance(self.badges, dict) else [],
            breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/")),
        )
        write_page(self.out_dir / "gioca", hub)
        self.track_sitemap("/gioca/", priority=0.6, changefreq="weekly")

        if percorsi:
            idx = self.render(
                "hub.html",
                page_type="hub",
                title="Percorsi guidati",
                lead="Quattro itinerari per esplorare il tè verde passo dopo passo.",
                url="/gioca/percorsi/",
                items=[{"title": p["title"], "url": p["url"], "brief": p.get("meta_description", "")} for p in percorsi],
                breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/"), ("Percorsi", "/gioca/percorsi/")),
            )
            write_page(self.out_dir / "gioca" / "percorsi", idx)
            self.track_sitemap("/gioca/percorsi/", priority=0.6, changefreq="weekly")

        if quiz_items:
            idx = self.render(
                "hub.html",
                page_type="hub",
                title="Quiz",
                lead="Metti alla prova ciò che hai imparato.",
                url="/gioca/quiz/",
                items=[{"title": q["title"], "url": f"/gioca/quiz/{q['slug']}/", "brief": q.get("description", "")} for q in quiz_items],
                breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/"), ("Quiz", "/gioca/quiz/")),
            )
            write_page(self.out_dir / "gioca" / "quiz", idx)
            self.track_sitemap("/gioca/quiz/", priority=0.5, changefreq="weekly")

        badges_page = self.render(
            "hub.html",
            page_type="hub",
            title="I tuoi badge",
            lead="Collezione di traguardi pedagogici. I badge si sbloccano navigando, quiz e diario.",
            url="/gioca/badge/",
            items=[],
            badges=self.badges.get("badges", []) if isinstance(self.badges, dict) else [],
            breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/"), ("Badge", "/gioca/badge/")),
        )
        write_page(self.out_dir / "gioca" / "badge", badges_page)
        self.track_sitemap("/gioca/badge/", priority=0.3, changefreq="yearly")

    def build_diario(self) -> None:
        page = self.render(
            "diario.html",
            page_type="diario",
            title="Diario del tè",
            url="/diario/",
            meta_description="Registra le tue infusioni: varietà, temperatura e note sensoriali.",
            varieties=self.varieties,
            breadcrumbs=self.breadcrumbs(("Diario", "/diario/")),
        )
        write_page(self.out_dir / "diario", page)
        self.track_sitemap("/diario/", priority=0.4, changefreq="monthly")
        nuova = self.render(
            "diario.html",
            page_type="diario",
            title="Nuova infusione",
            varieties=self.varieties,
            form_mode="new",
            noindex=True,
            breadcrumbs=self.breadcrumbs(("Diario", "/diario/"), ("Nuova infusione", "/diario/nuova/")),
        )
        write_page(self.out_dir / "diario" / "nuova", nuova)

    def build_community(self) -> None:
        page = self.render(
            "community.html",
            page_type="community",
            title="Community",
            url="/community/",
            meta_description="Discussioni sul tè verde in Italia — commenti e scambio tra appassionati.",
            breadcrumbs=self.breadcrumbs(("Community", "/community/")),
        )
        write_page(self.out_dir / "community", page)
        self.track_sitemap("/community/", priority=0.4, changefreq="monthly")

    def build_search(self) -> None:
        page = self.render(
            "search.html",
            page_type="search",
            title="Cerca",
            breadcrumbs=self.breadcrumbs(("Cerca", "/cerca/")),
        )
        write_page(self.out_dir / "cerca", page)

    def build_home(self) -> None:
        home_path = self.content_dir / "pagine" / "home.md"
        meta, html, _ = parse_md(home_path) if home_path.exists() else ({}, "", None)
        season = self._current_season()
        infusion = self._infusion_of_day(season)
        page = self.render(
            "home.html",
            page_type="home",
            url="/",
            seo_title="The Verde — Il tè verde, con radici e gusto",
            meta_description="Cultura del tè verde (Camellia sinensis) per chi vive in Italia: varietà, preparazione, abbinamenti e guide editoriali.",
            meta=meta,
            content_html=html,
            varieties=self.varieties[:4],
            guides=self.guides[:3],
            season=season,
            infusion=infusion,
            paths=self.paths_config.get("paths", []) if isinstance(self.paths_config, dict) else [],
        )
        write_page(self.out_dir, page)
        self.all_pages.append({"title": "Home", "url": "/", "type": "home"})
        self.track_sitemap("/", priority=1.0, changefreq="weekly")

    def _current_season(self) -> dict:
        seasons = self.seasons.get("seasons", []) if isinstance(self.seasons, dict) else []
        month = date.today().month
        for s in seasons:
            if month in s.get("months", []):
                return s
        return seasons[0] if seasons else {"name": "Primavera", "slug": "primavera"}

    def _infusion_of_day(self, season: dict) -> dict:
        varieties = [v for v in self.varieties if v.get("stagione_slug") == season.get("slug", "")]
        if not varieties:
            varieties = self.varieties
        if not varieties:
            return {}
        idx = date.today().toordinal() % len(varieties)
        v = varieties[idx]
        return {"title": v["title"], "url": v["url"], "brief": v.get("brief", ""), "season": season.get("name", "")}

    def build_legal(self) -> None:
        for name in ("privacy", "termini"):
            path = self.content_dir / "pagine" / f"{name}.md"
            if path.exists():
                meta, html, _ = parse_md(path)
                page = self.render(
                    "article.html",
                    page_type="legal",
                    meta={**meta, "url": f"/{name}/", "slug": name},
                    content_html=html,
                    breadcrumbs=self.breadcrumbs((meta.get("title", name.title()), f"/{name}/")),
                )
                write_page(self.out_dir / name, page)
                self.track_sitemap(f"/{name}/", priority=0.2, changefreq="yearly")

    def build_rss(self) -> None:
        items = self.guides[:20]
        rss = ['<?xml version="1.0" encoding="UTF-8"?>']
        rss.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
        rss.append("<channel>")
        rss.append(f"<title>The Verde  Guide</title>")
        rss.append(f"<link>{self.base_url}/guide/</link>")
        rss.append("<description>Guide editoriali sul tè verde</description>")
        rss.append(f'<atom:link href="{self.base_url}/feed.xml" rel="self" type="application/rss+xml"/>')
        for g in items:
            rss.append("<item>")
            rss.append(f"<title>{xml_escape(g['title'])}</title>")
            rss.append(f"<link>{self.base_url}{g['url']}</link>")
            rss.append(f"<description>{xml_escape(g.get('meta_description', ''))}</description>")
            rss.append(f"<pubDate>{g.get('published', date.today().isoformat())}</pubDate>")
            rss.append("</item>")
        rss.append("</channel></rss>")
        (self.out_dir / "feed.xml").write_text("\n".join(rss), encoding="utf-8")

    def prepare_assets(self, rebuild: bool = True) -> None:
        if rebuild:
            self.css_url, self.js_urls = build_assets(self.assets_dir, self.out_dir)
            sig = asset_source_signature(self.assets_dir)
            save_asset_manifest(ASSET_MANIFEST, sig, self.css_url, self.js_urls)
        config_out = self.out_dir / "assets" / "js" / "config"
        config_out.mkdir(parents=True, exist_ok=True)
        (config_out / "quizzes.json").write_text(dumps_compact(self.quizzes), encoding="utf-8")
        (config_out / "badges.json").write_text(dumps_compact(self.badges), encoding="utf-8")
        (config_out / "paths.json").write_text(dumps_compact(self.paths_config), encoding="utf-8")
        (config_out / "seasons.json").write_text(dumps_compact(self.seasons), encoding="utf-8")
        images_src = self.assets_dir / "images"
        if images_src.exists():
            images_out = self.out_dir / "assets" / "images"
            images_out.mkdir(parents=True, exist_ok=True)
            for img in images_src.iterdir():
                if img.is_file():
                    shutil.copy(img, images_out / img.name)
        for name in ("_headers", "_redirects"):
            src = ROOT / name
            if src.exists():
                shutil.copy(src, self.out_dir / name)

    def _clean_output(self, preserve_assets: bool) -> None:
        if not self.out_dir.exists():
            self.out_dir.mkdir(parents=True)
            return
        assets_dir = self.out_dir / "assets"
        if preserve_assets and not assets_dir.exists():
            preserve_assets = False
        if preserve_assets:
            for item in self.out_dir.iterdir():
                if item.name == "assets":
                    continue
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            assets_dir.mkdir(parents=True, exist_ok=True)
        else:
            shutil.rmtree(self.out_dir)
            self.out_dir.mkdir(parents=True)

    def build(self) -> None:
        sig = asset_source_signature(self.assets_dir)
        cached = load_asset_manifest(ASSET_MANIFEST)
        assets_unchanged = bool(cached and cached.get("signature") == sig)
        self._clean_output(preserve_assets=assets_unchanged)
        if assets_unchanged and cached:
            self.css_url = cached["css_url"]
            self.js_urls = cached["js_urls"]
            self.prepare_assets(rebuild=False)
        else:
            self.prepare_assets(rebuild=True)
        self.build_varieties()
        self.build_guides()
        self.build_impara()
        self.build_italia()
        self.build_glossario()
        self.build_gioca()
        self.build_diario()
        self.build_community()
        self.build_search()
        self.build_home()
        self.build_legal()
        self.build_rss()
        self.build_sitemap()
        print(f"Built {len(self.all_pages)} pages → {self.out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the-verde.it static site")
    parser.add_argument("--content", type=Path, default=ROOT / "content")
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    parser.add_argument("--templates", type=Path, default=ROOT / "templates")
    parser.add_argument("--assets", type=Path, default=ROOT / "assets")
    args = parser.parse_args()
    builder = SiteBuilder(args.content, args.out, args.templates, args.assets)
    builder.build()


if __name__ == "__main__":
    main()
