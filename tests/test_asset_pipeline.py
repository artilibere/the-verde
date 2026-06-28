"""Asset pipeline unit tests."""

from __future__ import annotations

from asset_pipeline import JS_PAGE_BUNDLES, minify_js


def test_minify_js_strips_line_comments_outside_strings():
    raw = "const url = 'https://example.com'; // keep query\n// remove\nconst x = 1;"
    out = minify_js(raw)
    assert "https://example.com" in out
    assert "remove" not in out
    assert "const x = 1;" in out


def test_core_bundle_includes_nav_and_level_toggle():
    assert JS_PAGE_BUNDLES["core"] == ("nav", "level-toggle")


def test_deferred_bundle_includes_prefetch_and_tracking():
    assert JS_PAGE_BUNDLES["deferred"] == ("prefetch", "explore-tracking")


def test_article_page_bundle_includes_share():
    assert JS_PAGE_BUNDLES["article-page"] == ("share",)


def test_minify_html_strips_comments():
    from asset_pipeline import minify_html

    html = "<div><!-- comment --><p>ok</p></div>"
    assert "<!--" not in minify_html(html)
    assert "<p>ok</p>" in minify_html(html)


def test_variety_and_controversy_page_bundles():
    assert JS_PAGE_BUNDLES["variety-page"] == ("scroll-spy", "share")
    assert JS_PAGE_BUNDLES["controversy-page"] == ("poll", "share")


def test_referral_page_bundles_include_share():
    assert JS_PAGE_BUNDLES["home-page"] == ("share",)
    assert JS_PAGE_BUNDLES["quiz-page"] == ("quiz", "share")
    assert JS_PAGE_BUNDLES["catalog-page"] == ("share",)
