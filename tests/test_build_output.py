"""HTML output contract tests (a11y + SEO)."""

from __future__ import annotations

from pathlib import Path

import json
from bs4 import BeautifulSoup
import pytest

from site_builder.builder import SiteBuilder

from conftest import ASSETS_DIR, CONTENT_DIR, TEMPLATES_DIR


@pytest.fixture(scope="module")
def built_dist(tmp_path_factory):
    out = tmp_path_factory.mktemp("dist")
    builder = SiteBuilder(CONTENT_DIR, out, TEMPLATES_DIR, ASSETS_DIR)
    builder.build()
    return out


def _soup(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def test_sencha_canonical_and_meta(built_dist):
    page = _soup(built_dist / "varieta" / "sencha" / "index.html")
    canonical = page.find("link", rel="canonical")
    assert canonical is not None
    assert canonical["href"].endswith("/varieta/sencha/")
    desc = page.find("meta", attrs={"name": "description"})
    assert desc is not None
    assert desc.get("content")


def test_sencha_single_h1(built_dist):
    page = _soup(built_dist / "varieta" / "sencha" / "index.html")
    assert len(page.find_all("h1")) == 1


def test_sencha_main_landmark(built_dist):
    page = _soup(built_dist / "varieta" / "sencha" / "index.html")
    assert page.find("main") is not None


def test_sencha_json_ld(built_dist):
    page = _soup(built_dist / "varieta" / "sencha" / "index.html")
    scripts = page.find_all("script", type="application/ld+json")
    assert len(scripts) >= 1
    combined = " ".join(s.string or "" for s in scripts)
    assert "@graph" in combined
    assert "Article" in combined or "FAQPage" in combined


def test_home_has_website_schema(built_dist):
    page = _soup(built_dist / "index.html")
    scripts = page.find_all("script", type="application/ld+json")
    combined = " ".join(s.string or "" for s in scripts)
    assert "WebSite" in combined


def test_home_meta_from_json(built_dist):
    home = json.loads((CONTENT_DIR / "pagine" / "home.json").read_text(encoding="utf-8"))
    page = _soup(built_dist / "index.html")
    title = page.find("title")
    desc = page.find("meta", attrs={"name": "description"})
    assert title is not None
    assert home["meta"]["title"] in title.get_text()
    assert desc is not None
    assert desc["content"] == home["meta"]["description"]
    og_image = page.find("meta", property="og:image")
    assert og_image is not None
    assert og_image["content"].endswith("/assets/images/og-default.png")


def test_home_body_geo_visible(built_dist):
    page = _soup(built_dist / "index.html")
    hero = page.select_one(".tv-hero__intro")
    assert hero is not None
    h1 = hero.find("h1")
    assert h1 is not None
    assert "Camellia sinensis" in hero.get_text()
    assert len(page.find_all("h1")) == 1


def test_llms_txt_linked_in_head(built_dist):
    page = _soup(built_dist / "index.html")
    head_link = page.find("link", href="/llms.txt")
    assert head_link is not None
    assert head_link.get("rel") == ["alternate"]


def test_sencha_has_card_feed(built_dist):
    page = _soup(built_dist / "varieta" / "sencha" / "index.html")
    assert page.find(class_="tv-feed") is not None
    assert len(page.find_all(class_="tv-card")) >= 3


def test_glossary_umami_has_card_feed(built_dist):
    page = _soup(built_dist / "glossario" / "umami" / "index.html")
    assert page.find(class_="tv-feed") is not None
    assert page.find(id="faq") is not None


def test_controversy_has_card_feed(built_dist):
    page = _soup(built_dist / "impara" / "controversie" / "caffeina-stimolazione" / "index.html")
    assert page.find(class_="tv-feed") is not None
    assert page.find(id="positions") is not None
    assert page.find(class_="tv-poll") is not None


def test_impara_hub_has_card_feed(built_dist):
    page = _soup(built_dist / "impara" / "preparazione" / "index.html")
    assert page.find(class_="tv-feed") is not None
    assert len(page.find_all(class_="tv-card")) >= 2
