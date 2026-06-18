"""Navigation enricher tests."""

from __future__ import annotations

from site_builder.enrichers.navigation import MAX_EXPLORE, explore_next, path_nav


def test_path_nav_order():
    nav = path_nav("sencha", lambda s: s)
    assert nav is not None
    assert nav["prev"]["slug"] == "bancha"
    assert nav["next"]["slug"] == "shincha"


def test_explore_next_related_varieties():
    varieties = [
        {"slug": "sencha", "title": "Sencha", "url": "/varieta/sencha/", "brief": ""},
        {"slug": "gyokuro", "title": "Gyokuro", "url": "/varieta/gyokuro/", "brief": "u"},
    ]
    links = explore_next(
        "sencha",
        {"related_slugs": ["gyokuro"]},
        varieties=varieties,
        controversies=[],
        relazioni={},
    )
    assert len(links) >= 1
    assert links[0]["url"] == "/varieta/gyokuro/"


def test_explore_next_respects_max():
    varieties = [
        {"slug": f"v{i}", "title": f"V{i}", "url": f"/varieta/v{i}/", "brief": ""}
        for i in range(10)
    ]
    links = explore_next(
        "sencha",
        {"related_slugs": [f"v{i}" for i in range(10)]},
        varieties=varieties,
        controversies=[],
        relazioni={},
    )
    assert len(links) <= MAX_EXPLORE


def test_explore_next_explicit_override():
    override = [{"type": "custom", "title": "Custom", "url": "/custom/", "brief": ""}]
    links = explore_next(
        "x",
        {"navigation": {"explore_next": override}},
        varieties=[],
        controversies=[],
        relazioni={},
    )
    assert links == override
