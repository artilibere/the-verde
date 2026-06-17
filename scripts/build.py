#!/usr/bin/env python3
"""Build static site for the-verde.it from Markdown content."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import date
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
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
    section = extract_section(html, "Variet\u00e0 simili")
    related = []
    if not section:
        return related
    for m in re.finditer(r"<li>(.*?)</li>", section, re.DOTALL):
        raw = m.group(1)
        link = re.search(r'href="([^"]+)"', raw)
        name = re.search(r"<strong>([^<]+)</strong>", raw)
        plain = re.sub(r"<[^>]+>", "", raw)
        reason_m = re.search(r"[-\u2014]\s*(.+)$", plain)
        if link and name:
            related.append({
                "url": link.group(1),
                "name": name.group(1),
                "reason": reason_m.group(1).strip() if reason_m else "",
            })
    return related


def wrap_variety_sections(html: str) -> str:
    if "<h2>Profilo sensoriale</h2>" in html:
        html = html.replace(
            "<h2>Profilo sensoriale</h2>",
            '<section id="scopri" class="tv-zone"><h2>Profilo sensoriale</h2>',
            1,
        )
    for heading, zone in [("Attrezzatura", "prepara"), ("In Italia", "approfondisci")]:
        marker = f"<h2>{heading}</h2>"
        if marker in html:
            html = html.replace(marker, f'<section id="{zone}" class="tv-zone">{marker}', 1)
    return html


def write_page(out_dir: Path, html: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")

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
        self.nav = self.sitemap.get("nav", [])
        self.varieties: list[dict] = []
        self.glossary: list[dict] = []
        self.guides: list[dict] = []
        self.hubs: list[dict] = []
        self.controversies: list[dict] = []
        self.all_pages: list[dict] = []

    def render(self, template: str, **ctx) -> str:
        ctx.setdefault("site_name", "The Verde")
        ctx.setdefault("nav", self.nav)
        ctx.setdefault("base_url", self.base_url)
        ctx.setdefault("year", date.today().year)
        return self.env.get_template(template).render(**ctx)

    def breadcrumbs(self, *crumbs: tuple[str, str]) -> list[dict]:
        items = [{"name": "Home", "url": "/"}]
        for name, url in crumbs:
            items.append({"name": name, "url": url})
        return items

    def path_nav(self, slug: str) -> dict | None:
        if slug not in PATH_ORDER:
            return None
        idx = PATH_ORDER.index(slug)
        nav = {"current": slug, "index": idx + 1, "total": len(PATH_ORDER)}
        if idx > 0:
            prev_slug = PATH_ORDER[idx - 1]
            nav["prev"] = {"slug": prev_slug, "url": f"/varieta/{prev_slug}/"}
        if idx < len(PATH_ORDER) - 1:
            next_slug = PATH_ORDER[idx + 1]
            nav["next"] = {"slug": next_slug, "url": f"/varieta/{next_slug}/"}
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
                    "brief": v.get("brief", ""),
                    "origine": v.get("origine_slug", ""),
                    "stile": v.get("stile_slug", ""),
                    "caffeina": v.get("caffeina_slug", ""),
                    "stagione": v.get("stagione_slug", ""),
                    "brew_temp": v.get("brew_temp"),
                    "brew_grams": v.get("brew_grams"),
                    "url": v["url"],
                    "sort_order": PATH_ORDER.index(v["slug"]) if v["slug"] in PATH_ORDER else 99,
                }
                for v in self.varieties
            ],
            "path_order": PATH_ORDER,
        }
        var_out = self.out_dir / "varieta"
        var_out.mkdir(parents=True, exist_ok=True)
        (var_out / "index.json").write_text(json.dumps(index_json, ensure_ascii=False, indent=2), encoding="utf-8")

        for v in self.varieties:
            _, html_body, _ = parse_md(var_dir / f"{v['slug']}.md")
            html_body = wrap_variety_sections(html_body)
            page = self.render(
                "variety.html",
                page_type="variety",
                meta=v,
                content_html=html_body,
                breadcrumbs=self.breadcrumbs(("Variet�", "/varieta/"), (v["title"].split("—")[0] if "—" in v["title"] else v["title"].split("-")[0].strip(), v["url"])),
            )
            write_page(self.out_dir / "varieta" / v["slug"], page)
            self.all_pages.append({"title": v["title"], "url": v["url"], "type": "varieta"})

        catalog = self.render(
            "catalog.html",
            page_type="catalog",
            title="Variet� di t� verde",
            meta_description="Catalogo enciclopedico di variet di t� verde: origine, stile, preparazione e contesto italiano.",
            url="/varieta/",
            varieties=self.varieties,
            breadcrumbs=self.breadcrumbs(("Variet�", "/varieta/")),
        )
        write_page(self.out_dir / "varieta", catalog)

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

        if self.guides:
            index = self.render(
                "hub.html",
                page_type="hub",
                title="Guide editoriali",
                lead="Articoli narrativi sul t� verde: cultura, storia e contesto italiano.",
                url="/guide/",
                items=[{"title": g["title"], "url": g["url"], "brief": g.get("meta_description", "")} for g in self.guides],
                breadcrumbs=self.breadcrumbs(("Guide", "/guide/")),
            )
            write_page(self.out_dir / "guide", index)

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

            idx = self.render(
                "hub.html",
                page_type="hub",
                title="Controversie",
                lead="Questioni aperte sul t� verde: prospettive contrastanti dalle fonti.",
                url="/impara/controversie/",
                items=[{"title": c["title"], "url": c["url"], "brief": c.get("meta_description", "")} for c in self.controversies],
                breadcrumbs=self.breadcrumbs(("Impara", "/impara/"), ("Controversie", "/impara/controversie/")),
            )
            write_page(self.out_dir / "impara" / "controversie", idx)

        index = self.render(
            "hub.html",
            page_type="hub",
            title="Impara",
            lead="Otto pilastri di conoscenza sul t� verde, dalla storia alla scienza.",
            url="/impara/",
            items=[{"title": t["nome"], "url": t["url"], "brief": ""} for t in temi],
            breadcrumbs=self.breadcrumbs(("Impara", "/impara/")),
        )
        write_page(self.out_dir / "impara", index)

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

        if self.glossary:
            index = self.render(
                "hub.html",
                page_type="hub",
                title="Glossario",
                lead="Termini del mondo del t� verde, con glossa in italiano.",
                url="/glossario/",
                items=sorted([{"title": g["title"], "url": g["url"], "brief": g.get("meta_description", "")} for g in self.glossary], key=lambda x: x["title"]),
                breadcrumbs=self.breadcrumbs(("Glossario", "/glossario/")),
            )
            write_page(self.out_dir / "glossario", index)

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

        quiz_items = self.quizzes.get("quizzes", []) if isinstance(self.quizzes, dict) else []
        for q in quiz_items:
            page = self.render(
                "quiz.html",
                page_type="quiz",
                quiz=q,
                breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/"), ("Quiz", "/gioca/quiz/"), (q["title"], f"/gioca/quiz/{q['slug']}/")),
            )
            write_page(self.out_dir / "gioca" / "quiz" / q["slug"], page)

        hub = self.render(
            "gioca.html",
            page_type="gioca",
            title="Gioca e impara",
            percorsi=percorsi,
            quizzes=quiz_items,
            badges=self.badges.get("badges", []) if isinstance(self.badges, dict) else [],
            breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/")),
        )
        write_page(self.out_dir / "gioca", hub)

        if percorsi:
            idx = self.render(
                "hub.html",
                page_type="hub",
                title="Percorsi guidati",
                lead="Quattro itinerari per esplorare il t� verde passo dopo passo.",
                url="/gioca/percorsi/",
                items=[{"title": p["title"], "url": p["url"], "brief": p.get("meta_description", "")} for p in percorsi],
                breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/"), ("Percorsi", "/gioca/percorsi/")),
            )
            write_page(self.out_dir / "gioca" / "percorsi", idx)

        if quiz_items:
            idx = self.render(
                "hub.html",
                page_type="hub",
                title="Quiz",
                lead="Metti alla prova ci che hai imparato.",
                url="/gioca/quiz/",
                items=[{"title": q["title"], "url": f"/gioca/quiz/{q['slug']}/", "brief": q.get("description", "")} for q in quiz_items],
                breadcrumbs=self.breadcrumbs(("Gioca", "/gioca/"), ("Quiz", "/gioca/quiz/")),
            )
            write_page(self.out_dir / "gioca" / "quiz", idx)

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

    def build_diario(self) -> None:
        page = self.render(
            "diario.html",
            page_type="diario",
            title="Diario del tè",
            varieties=self.varieties,
            breadcrumbs=self.breadcrumbs(("Diario", "/diario/")),
        )
        write_page(self.out_dir / "diario", page)
        nuova = self.render(
            "diario.html",
            page_type="diario",
            title="Nuova infusione",
            varieties=self.varieties,
            form_mode="new",
            breadcrumbs=self.breadcrumbs(("Diario", "/diario/"), ("Nuova infusione", "/diario/nuova/")),
        )
        write_page(self.out_dir / "diario" / "nuova", nuova)

    def build_community(self) -> None:
        page = self.render(
            "community.html",
            page_type="community",
            title="Community",
            breadcrumbs=self.breadcrumbs(("Community", "/community/")),
        )
        write_page(self.out_dir / "community", page)

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

    def build_rss(self) -> None:
        items = self.guides[:20]
        rss = ['<?xml version="1.0" encoding="UTF-8"?>']
        rss.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
        rss.append("<channel>")
        rss.append(f"<title>The Verde  Guide</title>")
        rss.append(f"<link>{self.base_url}/guide/</link>")
        rss.append("<description>Guide editoriali sul t� verde</description>")
        rss.append(f'<atom:link href="{self.base_url}/feed.xml" rel="self" type="application/rss+xml"/>')
        for g in items:
            rss.append("<item>")
            rss.append(f"<title>{g['title']}</title>")
            rss.append(f"<link>{self.base_url}{g['url']}</link>")
            rss.append(f"<description>{g.get('meta_description', '')}</description>")
            rss.append(f"<pubDate>{g.get('published', date.today().isoformat())}</pubDate>")
            rss.append("</item>")
        rss.append("</channel></rss>")
        (self.out_dir / "feed.xml").write_text("\n".join(rss), encoding="utf-8")

    def copy_assets(self) -> None:
        assets_out = self.out_dir / "assets"
        if self.assets_dir.exists():
            if assets_out.exists():
                shutil.rmtree(assets_out)
            shutil.copytree(self.assets_dir, assets_out)
        for name in ("_headers", "_redirects"):
            src = ROOT / name
            if src.exists():
                shutil.copy(src, self.out_dir / name)

        config_out = self.out_dir / "assets" / "js" / "config"
        config_out.mkdir(parents=True, exist_ok=True)
        (config_out / "quizzes.json").write_text(json.dumps(self.quizzes, ensure_ascii=False, indent=2), encoding="utf-8")
        (config_out / "badges.json").write_text(json.dumps(self.badges, ensure_ascii=False, indent=2), encoding="utf-8")
        (config_out / "paths.json").write_text(json.dumps(self.paths_config, ensure_ascii=False, indent=2), encoding="utf-8")
        (config_out / "seasons.json").write_text(json.dumps(self.seasons, ensure_ascii=False, indent=2), encoding="utf-8")

    def build(self) -> None:
        if self.out_dir.exists():
            shutil.rmtree(self.out_dir)
        self.out_dir.mkdir(parents=True)
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
        self.copy_assets()
        print(f"Built {len(self.all_pages)} pages ? {self.out_dir}")


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
