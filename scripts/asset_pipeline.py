"""Minify and fingerprint static assets for production builds."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

CSS_BUNDLE = ("tokens.css", "base.css", "components.css")
CRITICAL_CSS_BUNDLE = ("critical-tokens.css", "critical-shell.css", "critical-content.css")

# Bundled to cut HTTP requests on hot pages (order preserved).
JS_PAGE_BUNDLES: dict[str, tuple[str, ...]] = {
    "core": ("nav",),
    "deferred": ("prefetch", "explore-tracking"),
    "article-page": ("level-toggle", "share"),
    "diario-page": ("supabase-config", "diario", "badges"),
    "percorsi": ("badges", "paths"),
    "variety-page": ("scroll-spy", "share"),
    "controversy-page": ("poll", "share"),
    "home-page": ("share",),
    "glossary-page": ("share",),
    "hub-page": ("level-toggle", "share"),
    "catalog-page": ("share",),
    "quiz-page": ("quiz", "share"),
}

# Built only when referenced; omit dead scripts from dist.
JS_SKIP = frozenset({"season"})


def short_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()[:10]


def build_critical_css(assets_dir: Path) -> str:
    bundle = "\n".join(
        (assets_dir / "css" / name).read_text(encoding="utf-8") for name in CRITICAL_CSS_BUNDLE
    )
    return minify_css(bundle)


def asset_source_signature(assets_dir: Path) -> str:
    """Hash of CSS bundle inputs + JS sources (excluding skipped)."""
    chunks: list[bytes] = []
    css_names = list(dict.fromkeys(CSS_BUNDLE + CRITICAL_CSS_BUNDLE))
    for name in css_names:
        chunks.append((assets_dir / "css" / name).read_bytes())
    bundled = {stem for stems in JS_PAGE_BUNDLES.values() for stem in stems}
    for js_path in sorted((assets_dir / "js").glob("*.js")):
        stem = js_path.stem
        if stem in JS_SKIP:
            continue
        chunks.append(js_path.read_bytes())
    chunks.append(json.dumps(JS_PAGE_BUNDLES, sort_keys=True).encode("utf-8"))
    return short_hash(b"".join(chunks))


def minify_css(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([{};:,>+~])\s*", r"\1", text)
    return text.strip()


def minify_js(text: str) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.rstrip()
        if not stripped:
            continue
        in_string = False
        quote = ""
        out = []
        i = 0
        while i < len(stripped):
            ch = stripped[i]
            if in_string:
                out.append(ch)
                if ch == "\\" and i + 1 < len(stripped):
                    out.append(stripped[i + 1])
                    i += 2
                    continue
                if ch == quote:
                    in_string = False
                i += 1
                continue
            if ch in ("'", '"', "`"):
                in_string = True
                quote = ch
                out.append(ch)
                i += 1
                continue
            if ch == "/" and i + 1 < len(stripped) and stripped[i + 1] == "/":
                break
            out.append(ch)
            i += 1
        lines.append("".join(out).rstrip())
    return "\n".join(lines).strip() + "\n"


def minify_html(html: str) -> str:
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    html = re.sub(r">\s+<", "><", html)
    return html.strip() + "\n"


def dumps_compact(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def _purge_hashed_assets(directory: Path, base_name: str, ext: str) -> None:
    if not directory.exists():
        return
    for path in directory.glob(f"{base_name}.*{ext}"):
        path.unlink(missing_ok=True)


def _write_hashed_file(directory: Path, base_name: str, ext: str, content: str) -> str:
    _purge_hashed_assets(directory, base_name, ext)
    content_hash = short_hash(content.encode("utf-8"))
    out_name = f"{base_name}.{content_hash}{ext}"
    (directory / out_name).write_text(content, encoding="utf-8")
    return f"/assets/{directory.name}/{out_name}"


def build_assets(assets_dir: Path, out_dir: Path) -> tuple[str, dict[str, str], str]:
    """Write hashed CSS/JS to out_dir/assets. Returns (css_url, js_url_map, critical_css)."""
    css_dir = out_dir / "assets" / "css"
    js_dir = out_dir / "assets" / "js"
    css_dir.mkdir(parents=True, exist_ok=True)
    js_dir.mkdir(parents=True, exist_ok=True)

    bundle = "\n".join((assets_dir / "css" / name).read_text(encoding="utf-8") for name in CSS_BUNDLE)
    css_url = _write_hashed_file(css_dir, "site", ".css", minify_css(bundle))
    critical_css = build_critical_css(assets_dir)

    bundled_stems = {stem for stems in JS_PAGE_BUNDLES.values() for stem in stems}
    js_urls: dict[str, str] = {}

    for bundle_name, stems in JS_PAGE_BUNDLES.items():
        combined = "\n".join(
            (assets_dir / "js" / f"{stem}.js").read_text(encoding="utf-8") for stem in stems
        )
        js_urls[bundle_name] = _write_hashed_file(js_dir, bundle_name, ".js", minify_js(combined))

    for js_path in sorted((assets_dir / "js").glob("*.js")):
        stem = js_path.stem
        if stem in JS_SKIP or stem in bundled_stems:
            continue
        minified = minify_js(js_path.read_text(encoding="utf-8"))
        js_urls[stem] = _write_hashed_file(js_dir, stem, ".js", minified)

    return css_url, js_urls, critical_css


def save_asset_manifest(
    cache_path: Path,
    signature: str,
    css_url: str,
    js_urls: dict[str, str],
    critical_css: str = "",
) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        dumps_compact(
            {"signature": signature, "css_url": css_url, "js_urls": js_urls, "critical_css": critical_css}
        ),
        encoding="utf-8",
    )


def load_asset_manifest(cache_path: Path) -> dict | None:
    if not cache_path.exists():
        return None
    try:
        return json.loads(cache_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
