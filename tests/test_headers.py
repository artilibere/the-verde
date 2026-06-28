"""Cloudflare Pages _headers contract tests."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_headers_asset_cache_rules_follow_html_rules():
    text = (ROOT / "_headers").read_text(encoding="utf-8")
    assets_idx = text.index("/assets/*")
    security_idx = text.index("/*")
    assert assets_idx > security_idx
    assert "max-age=31536000, immutable" in text
    security_block = text.split("/*", 1)[1].split("\n\n", 1)[0]
    assert "Cache-Control" not in security_block
