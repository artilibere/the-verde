"""Full build integration tests."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from site_builder.builder import SiteBuilder

from conftest import ASSETS_DIR, CONTENT_DIR, ROOT, TEMPLATES_DIR


@pytest.fixture
def build_out(tmp_path):
    out = tmp_path / "dist"
    builder = SiteBuilder(CONTENT_DIR, out, TEMPLATES_DIR, ASSETS_DIR, validate=True)
    builder.build()
    return out


def test_build_completes(build_out):
    assert build_out.exists()
    assert (build_out / "index.html").exists()


def test_build_page_count(build_out):
    html_files = list(build_out.rglob("index.html"))
    assert len(html_files) >= 69


def test_varieta_catalog_json(build_out):
    catalog = build_out / "assets" / "js" / "config" / "varieties.json"
    assert catalog.exists()
    assert "varieties" in catalog.read_text(encoding="utf-8")


def test_sitemap_and_robots(build_out):
    assert (build_out / "sitemap.xml").exists()
    assert (build_out / "robots.txt").exists()
    assert (build_out / "llms.txt").exists()
    robots = (build_out / "robots.txt").read_text(encoding="utf-8")
    assert "Sitemap:" in robots
    llms = (build_out / "llms.txt").read_text(encoding="utf-8")
    assert "Glossario" in llms


def test_validate_only():
    builder = SiteBuilder(CONTENT_DIR, ROOT / "dist", TEMPLATES_DIR, ASSETS_DIR)
    builder.load_content()
