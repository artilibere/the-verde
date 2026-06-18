# -*- coding: utf-8 -*-
"""SiteBuilder — orchestrates JSON content to static HTML."""

from __future__ import annotations

import shutil
import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from asset_pipeline import (  # noqa: E402
    asset_source_signature,
    build_assets,
    dumps_compact,
    load_asset_manifest,
    minify_html,
    save_asset_manifest,
)
from site_builder.blocks import has_level_sections, render_blocks
from site_builder.builders import controversy as controversy_builder
from site_builder.builders import glossary as glossary_builder
from site_builder.builders import hub as hub_builder
from site_builder.builders import variety as variety_builder
from site_builder.document import document_to_meta, variety_breadcrumb_title
from site_builder.enrichers._seo_core import build_llms_txt, build_robots_txt, build_sitemap_xml
from site_builder.enrichers.navigation import PATH_ORDER, explore_next, path_nav
from site_builder.page_document import document_to_page
from site_builder.renderer import TemplateRenderer
from site_builder.loader import discover_documents, infer_type_from_path, load_document, load_json

CACHE_DIR = ROOT / ".cache"
ASSET_MANIFEST = CACHE_DIR / "asset-manifest.json"


def write_page(out_dir: Path, html: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(minify_html(html), encoding="utf-8")


class SiteBuilder:
    def __init__(
        self,
        content_dir: Path,
        out_dir: Path,
        templates_dir: Path,
        assets_dir: Path,
        *,
        validate: bool = True,
    ):
        self.content_dir = content_dir
        self.out_dir = out_dir
        self.assets_dir = assets_dir
        self.templates_dir = templates_dir
        self.validate = validate
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
        self.site_name = self.sitemap.get("site_name", "The Verde")
        self.renderer = TemplateRenderer(templates_dir, self.site_name, self.base_url, self.nav)
        self.varieties: list[dict] = []
        self.glossary: list[dict] = []
        self.guides: list[dict] = []
        self.hubs: list[dict] = []
        self.controversies: list[dict] = []
        self.all_pages: list[dict] = []
        self.sitemap_urls: list[dict] = []
        self.css_url = "/assets/css/site.css"
        self.js_urls: dict[str, str] = {}
        self._docs_by_path: dict[Path, dict] = {}

    def write_page(self, out_dir: Path, html: str) -> None:
        write_page(out_dir, html)

    def load_content(self) -> None:
        from site_builder.loader import validate_document

        for path in discover_documents(self.content_dir):
            doc = load_document(path, self.content_dir)
            if self.validate:
                errors = validate_document(self.content_dir, doc)
                if errors:
                    raise ValueError(f"{path}: " + "; ".join(errors))
            self._docs_by_path[path] = doc

    def doc_at(self, *parts: str) -> dict | None:
        path = self.content_dir.joinpath(*parts)
        json_path = path.with_suffix(".json")
        if json_path in self._docs_by_path:
            return self._docs_by_path[json_path]
        if path.suffix == ".json" and path in self._docs_by_path:
            return self._docs_by_path[path]
        return None

    def docs_in(self, subdir: str, *, doc_type: str | None = None) -> list[tuple[Path, dict]]:
        base = self.content_dir / subdir
        out = []
        for path, doc in self._docs_by_path.items():
            try:
                path.relative_to(base)
            except ValueError:
                continue
            if doc_type and doc.get("type") != doc_type:
                continue
            out.append((path, doc))
        return sorted(out, key=lambda x: x[0].name)

    def render(self, template: str, **ctx) -> str:
        return self.renderer.render(template, **ctx)

    def track_sitemap(self, url: str, *, changefreq: str = "monthly", priority: float = 0.5) -> None:
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
        (self.out_dir / "llms.txt").write_text(
            build_llms_txt(self.base_url, self.site_name), encoding="utf-8"
        )

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

    def _render_doc(
        self,
        doc: dict,
        url: str,
        *,
        page_type: str,
        template: str,
        breadcrumbs: list[dict],
        extra: dict | None = None,
    ) -> str:
        meta = document_to_meta(doc, url=url)
        page = document_to_page(
            doc,
            url=url,
            base_url=self.base_url,
            page_type=page_type,
            meta=meta,
            breadcrumbs=breadcrumbs,
        )
        ctx = {
            "page_type": page_type,
            "page": page,
            "meta": meta,
            "content_html": self.renderer.render_legacy_body(doc, page_type=page_type),
            "breadcrumbs": breadcrumbs,
            "_doc": doc,
        }
        if extra:
            ctx.update(extra)
        return self.render(template, **ctx)

    def build_varieties(self) -> None:
        variety_builder.collect_varieties(self)
        variety_builder.build_catalog_and_pages(self)

    def build_guides(self) -> None:
        items = self.docs_in("guide", doc_type="article")
        for _path, doc in items:
            slug = doc["slug"]
            url = f"/guide/{slug}/"
            meta = document_to_meta(doc, url=url)
            self.guides.append(meta)
            page = self._render_doc(
                doc,
                url,
                page_type="article",
                template="article.html",
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
                items=[
                    {"title": g["title"], "url": g["url"], "brief": g.get("meta_description", "")}
                    for g in self.guides
                ],
                breadcrumbs=self.breadcrumbs(("Guide", "/guide/")),
            )
            write_page(self.out_dir / "guide", index)
            self.track_sitemap("/guide/", priority=0.7, changefreq="weekly")

    def build_impara(self) -> None:
        if not self.controversies:
            self.build_impara_controversies_first()
        hub_builder.build_impara(self)
        controversy_builder.build_pages(self)

    def build_italia(self) -> None:
        hub_builder.build_italia(self)
        doc = self.doc_at("italia", "abbinamenti.json")
        if doc:
            url = "/italia/abbinamenti/"
            page = self._render_doc(
                doc,
                url,
                page_type="article",
                template="article.html",
                breadcrumbs=self.breadcrumbs(("In Italia", "/italia/"), ("Abbinamenti", url)),
            )
            write_page(self.out_dir / "italia" / "abbinamenti", page)
            self.track_sitemap(url, priority=0.6, changefreq="monthly")

    def build_glossario(self) -> None:
        glossary_builder.build(self)

    def build_gioca(self) -> None:
        percorsi = []
        for _path, doc in self.docs_in("gioca/percorsi", doc_type="article"):
            slug = doc["slug"]
            url = f"/gioca/percorsi/{slug}/"
            meta = document_to_meta(doc, url=url)
            blocks = doc.get("body", {}).get("blocks", [])
            html = render_blocks(blocks)
            meta.update({"url": url, "content_html": html})
            percorsi.append(meta)
            page = self._render_doc(
                doc,
                url,
                page_type="article",
                template="article.html",
                breadcrumbs=self.breadcrumbs(
                    ("Gioca", "/gioca/"),
                    ("Percorsi", "/gioca/percorsi/"),
                    (meta["title"], url),
                ),
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
                breadcrumbs=self.breadcrumbs(
                    ("Gioca", "/gioca/"),
                    ("Quiz", "/gioca/quiz/"),
                    (q["title"], quiz_url),
                ),
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
                items=[
                    {"title": p["title"], "url": p["url"], "brief": p.get("meta_description", "")}
                    for p in percorsi
                ],
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
                items=[
                    {"title": q["title"], "url": f"/gioca/quiz/{q['slug']}/", "brief": q.get("description", "")}
                    for q in quiz_items
                ],
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
        doc = self.doc_at("pagine", "home.json")
        meta = document_to_meta(doc, url="/") if doc else {}
        blocks = doc.get("body", {}).get("blocks", []) if doc else []
        season = self._current_season()
        infusion = self._infusion_of_day(season)
        page = self.render(
            "home.html",
            page_type="home",
            url="/",
            seo_title=meta.get("title", self.site_name),
            meta_description=meta.get("meta_description") or meta.get("description", ""),
            meta=meta,
            content_html=render_blocks(blocks) if blocks else "",
            varieties=self.varieties[:4],
            guides=self.guides[:3],
            season=season,
            infusion=infusion,
            paths=self.paths_config.get("paths", []) if isinstance(self.paths_config, dict) else [],
            _doc=doc,
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
            doc = self.doc_at("pagine", f"{name}.json")
            if doc:
                url = f"/{name}/"
                meta = document_to_meta(doc, url=url)
                page = self._render_doc(
                    doc,
                    url,
                    page_type="legal",
                    template="article.html",
                    breadcrumbs=self.breadcrumbs((meta.get("title", name.title()), url)),
                )
                write_page(self.out_dir / name, page)
                self.track_sitemap(url, priority=0.2, changefreq="yearly")

    def build_rss(self) -> None:
        items = self.guides[:20]
        rss = ['<?xml version="1.0" encoding="UTF-8"?>']
        rss.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
        rss.append("<channel>")
        rss.append("<title>The Verde  Guide</title>")
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
        self.renderer.configure_site(
            hreflang=self.hreflang,
            locale=self.locale,
            og_image=self.og_image,
            social=self.social,
            css_url=self.css_url,
            js_urls=self.js_urls,
        )
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

    def _cached_asset_files_present(self, cached: dict) -> bool:
        for url in [cached["css_url"], *cached["js_urls"].values()]:
            if not (self.out_dir / url.lstrip("/")).is_file():
                return False
        return True

    def build(self) -> None:
        self.load_content()
        sig = asset_source_signature(self.assets_dir)
        cached = load_asset_manifest(ASSET_MANIFEST)
        assets_unchanged = bool(cached and cached.get("signature") == sig)
        self._clean_output(preserve_assets=assets_unchanged)
        if assets_unchanged and cached and not self._cached_asset_files_present(cached):
            assets_unchanged = False
        if assets_unchanged and cached:
            self.css_url = cached["css_url"]
            self.js_urls = cached["js_urls"]
            self.prepare_assets(rebuild=False)
        else:
            self.prepare_assets(rebuild=True)
        self.build_impara_controversies_first()
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

    def build_impara_controversies_first(self) -> None:
        """Pre-load controversies for explore_next on varieties."""
        controversy_builder.collect(self)
