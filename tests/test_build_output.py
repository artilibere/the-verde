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
    hero = page.select_one(".tv-card--hero-entry")
    assert hero is not None
    h1 = hero.find("h1")
    assert h1 is not None
    details = page.select_one(".tv-card--collapsible .tv-prose")
    assert details is not None
    assert "Camellia sinensis" in details.get_text()
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
    fonte = page.find(class_="tv-position__fonte")
    assert fonte is not None
    text = fonte.get_text()
    assert "sommelier" not in text.lower()
    assert "rosen" not in text.lower()
    assert "pellegrino" not in text.lower() or "Davide" in text


def test_impara_hub_has_card_feed(built_dist):
    page = _soup(built_dist / "impara" / "preparazione" / "index.html")
    assert page.find(class_="tv-feed") is not None
    assert len(page.find_all(class_="tv-card")) >= 2


def test_home_loads_core_and_share_bundle(built_dist):
    page = _soup(built_dist / "index.html")
    scripts = [
        s["src"]
        for s in page.find_all("script", src=True)
        if s["src"].startswith("/assets/js/")
    ]
    assert len(scripts) == 2
    assert any("core." in src for src in scripts)
    assert any("home-page." in src for src in scripts)
    assert page.find(id="condividi") is not None


def test_variety_loads_core_and_variety_bundle(built_dist):
    page = _soup(built_dist / "varieta" / "sencha" / "index.html")
    scripts = [
        s["src"]
        for s in page.find_all("script", src=True)
        if s["src"].startswith("/assets/js/")
    ]
    assert len(scripts) == 2
    assert any("core." in src for src in scripts)
    assert any("variety-page." in src for src in scripts)


def test_variety_prefetches_path_nav_next(built_dist):
    page = _soup(built_dist / "varieta" / "sencha" / "index.html")
    prefetches = page.find_all("link", rel="prefetch")
    hrefs = {link.get("href") for link in prefetches}
    assert hrefs == {"/varieta/shincha/"}
    assert page.find("a", attrs={"data-tv-prefetch": "high"}) is not None


def test_async_stylesheet_with_critical_inline(built_dist):
    page = _soup(built_dist / "index.html")
    head = page.find("head")
    assert head.find("style") is not None
    async_css = head.find("link", rel="preload", attrs={"as": "style"})
    assert async_css is not None
    assert async_css.get("onload")
    blocking = [
        link
        for link in head.find_all("link", rel="stylesheet")
        if link.find_parent("noscript") is None
    ]
    assert blocking == []
    assert head.find("noscript").find("link", rel="stylesheet") is not None


def test_core_bundle_is_nav_only(built_dist):
    core_files = list((built_dist / "assets" / "js").glob("core.*.js"))
    assert core_files, "core bundle missing"
    text = core_files[0].read_text(encoding="utf-8")
    assert "tv-header__menu-btn" in text or "tv-header__nav--open" in text
    assert "prefetchPath" not in text
    assert "tv_internal_link" not in text


def test_deferred_bundle_has_prefetch_and_tracking(built_dist):
    deferred_files = list((built_dist / "assets" / "js").glob("deferred.*.js"))
    assert deferred_files, "deferred bundle missing"
    text = deferred_files[0].read_text(encoding="utf-8")
    assert "prefetchPath" in text or 'rel="prefetch"' in text
    assert "tv_internal_link" in text


def test_deferred_loader_in_base(built_dist):
    html = (built_dist / "index.html").read_text(encoding="utf-8")
    assert "tv-deferred-js" in html
    assert "requestIdleCallback" in html or "setTimeout(cb, 1)" in html


def test_bottom_nav_marks_prefetch_high(built_dist):
    page = _soup(built_dist / "varieta" / "sencha" / "index.html")
    nav = page.find("nav", class_="tv-bottom-nav")
    assert nav is not None
    assert nav.find("a", href="/impara/", attrs={"data-tv-prefetch": "high"}) is not None

    html = (built_dist / "index.html").read_text(encoding="utf-8")
    assert "loadGtm" in html or "googletagmanager.com/gtm.js" in html
    assert "setTimeout(loadGtm" in html
    assert html.index("<meta charset") < html.index("loadGtm")
    assert 'rel="preconnect" href="https://www.googletagmanager.com"' not in html


def test_icons_inlined_without_external_sprite_request(built_dist):
    html = (built_dist / "index.html").read_text(encoding="utf-8")
    assert 'href="#tv-icon-leaf"' in html
    assert "/assets/icons/tv-icons.svg#tv-icon-" not in html
    assert 'id="tv-icon-leaf"' in html


def test_home_schema_single_json_ld_block(built_dist):
    page = _soup(built_dist / "index.html")
    scripts = page.find_all("script", type="application/ld+json")
    assert len(scripts) == 1
    assert '"@graph"' in scripts[0].string


def test_skip_link_targets_main(built_dist):
    page = _soup(built_dist / "index.html")
    skip = page.find("a", class_="tv-skip-link")
    main = page.find("main", id="main")
    assert skip is not None
    assert skip["href"] == "#main"
    assert main is not None


def test_impara_hub_level_toggle_aria(built_dist):
    page = _soup(built_dist / "impara" / "preparazione" / "index.html")
    toggle = page.find("button", attrs={"data-level-toggle": True})
    assert toggle is not None
    assert toggle.get("aria-expanded") == "false"
    assert toggle.get("aria-label")


def test_bottom_nav_active_has_aria_current(built_dist):
    page = _soup(built_dist / "italia" / "index.html")
    current = page.select_one('.tv-bottom-nav__item[aria-current="page"]')
    assert current is not None
    assert current.get("href", current.get("href")) == "/italia/" or current["href"].endswith("/italia/")


def test_controversy_poll_radiogroup(built_dist):
    page = _soup(built_dist / "impara" / "controversie" / "caffeina-stimolazione" / "index.html")
    form = page.find("form", id="controversy-poll")
    assert form is not None
    assert form.get("role") == "radiogroup"
    assert form.get("aria-labelledby") == "poll-heading"


def test_glossary_faq_card_landmark(built_dist):
    page = _soup(built_dist / "glossario" / "umami" / "index.html")
    faq_card = page.find(id="faq")
    assert faq_card is not None
    assert faq_card.get("aria-labelledby") == "card-title-faq"
    assert page.find(id="card-title-faq") is not None
