"""Render structured content blocks to semantic HTML."""

from __future__ import annotations

from html import escape
from typing import Any


def render_spans(spans: list[dict]) -> str:
    out: list[str] = []
    for span in spans:
        stype = span.get("type", "text")
        value = escape(span.get("value", ""))
        if stype == "strong":
            out.append(f"<strong>{value}</strong>")
        elif stype == "em":
            out.append(f"<em>{value}</em>")
        elif stype == "link":
            href = escape(span.get("href", ""), quote=True)
            out.append(f'<a href="{href}">{value}</a>')
        else:
            out.append(value)
    return "".join(out)


def render_block(block: dict) -> str:
    btype = block.get("type")

    if btype == "heading":
        level = min(max(int(block.get("level", 2)), 1), 3)
        tag = f"h{level}"
        return f"<{tag}>{render_spans(block.get('spans', []))}</{tag}>"

    if btype == "paragraph":
        return f"<p>{render_spans(block.get('spans', []))}</p>"

    if btype == "list":
        tag = "ol" if block.get("ordered") else "ul"
        items = []
        for item in block.get("items", []):
            items.append(f"<li>{render_spans(item.get('spans', []))}</li>")
        return f"<{tag}>{''.join(items)}</{tag}>"

    if btype == "equipment":
        items = "".join(f"<li>{escape(i)}</li>" for i in block.get("items", []))
        return f"<h2>Attrezzatura</h2><ul>{items}</ul>"

    if btype == "errors":
        items = "".join(f"<li>{escape(i)}</li>" for i in block.get("items", []))
        return f"<h2>Errori comuni</h2><ul>{items}</ul>"

    if btype == "pairings":
        items = "".join(f"<li>{escape(i)}</li>" for i in block.get("items", []))
        return f"<h2>Abbinamenti</h2><ul>{items}</ul>"

    if btype == "callout":
        variant = block.get("variant", "tip")
        inner = render_spans(block.get("spans", []))
        if variant == "italia":
            return (
                '<div class="tv-italy-box"><h2 class="tv-italy-box__title">In Italia</h2>'
                f"<p>{inner}</p></div>"
            )
        cls = f"tv-callout tv-callout--{escape(variant)}"
        return f'<aside class="{cls}"><p>{inner}</p></aside>'

    if btype == "steps":
        return _render_steps(block.get("items", []))

    if btype == "faq":
        return _render_faqs(block.get("items", []))

    if btype == "related_links":
        return _render_related(block.get("items", []))

    if btype == "positions":
        items = []
        for pos in block.get("items", []):
            fonte = escape(pos.get("fonte", ""))
            tesi = escape(pos.get("tesi", ""))
            items.append(
                f'<blockquote class="tv-position" cite="{fonte}">'
                f'<p class="tv-position__tesi">{tesi}</p>'
                f'<footer class="tv-position__fonte">— {fonte}</footer></blockquote>'
            )
        return f'<div class="tv-positions">{"".join(items)}</div>'

    if btype == "level_section":
        level = block.get("level", "intro")
        title = "Per iniziare" if level == "intro" else "Approfondimento"
        inner = render_blocks(block.get("blocks", []))
        return f"<h2>{title}</h2>{inner}"

    if btype in ("sensory_profile", "brew_params"):
        return ""

    return ""


def _render_steps(items: list[dict]) -> str:
    if not items:
        return ""
    lis = []
    for step in items:
        time_html = (
            f'<span class="tv-step-list__time">{escape(step.get("duration", ""))}</span>'
            if step.get("duration")
            else ""
        )
        lis.append(
            f'<li class="tv-step-list__item">'
            f'<span class="tv-step-list__action">{escape(step.get("text", ""))}</span>'
            f"{time_html}</li>"
        )
    return (
        '<h2 id="i-passaggi">I passaggi</h2>'
        f'<ol class="tv-step-list">{"".join(lis)}</ol>'
    )


def _render_faqs(items: list[dict]) -> str:
    if not items:
        return ""
    parts = []
    for faq in items:
        q = escape(faq.get("question", ""))
        a = render_spans(faq.get("answer_spans", []))
        parts.append(
            f'<details class="tv-faq__item">'
            f'<summary class="tv-faq__question">{q}</summary>'
            f'<p class="tv-faq__answer">{a}</p></details>'
        )
    return (
        '<h2 id="domande-frequenti">Domande frequenti</h2>'
        f'<div class="tv-faq">{"".join(parts)}</div>'
    )


def _render_related(items: list[dict]) -> str:
    if not items:
        return ""
    lis = []
    for r in items:
        reason = f" — {escape(r['reason'])}" if r.get("reason") else ""
        url = escape(r.get("url", ""), quote=True)
        name = escape(r.get("name", ""))
        lis.append(f'<li><a href="{url}"><strong>{name}</strong></a>{reason}</li>')
    return (
        '<h2 id="varieta-simili">Varietà simili</h2>'
        f'<ul class="tv-related__list">{"".join(lis)}</ul>'
    )


def render_blocks(blocks: list[dict], *, page_type: str | None = None) -> str:
    if page_type == "variety":
        return render_variety_body(blocks)
    return "".join(render_block(b) for b in blocks)


def render_variety_body(blocks: list[dict]) -> str:
    """Layout a zone: lead, #prepara, #approfondisci."""
    skip_types = {"sensory_profile", "brew_params", "heading"}
    lead = ""
    prepara_parts: list[str] = []
    approfondisci_parts: list[str] = []
    leftover: list[str] = []

    for block in blocks:
        btype = block.get("type")
        if btype in skip_types:
            continue
        if btype == "heading" and block.get("level") == 1:
            continue
        html = render_block(block)
        if not html:
            continue

        if btype == "paragraph" and not lead:
            lead = f'<p class="tv-variety-lead">{render_spans(block.get("spans", []))}</p>'
        elif btype in ("equipment", "errors", "steps"):
            prepara_parts.append(html)
        elif btype in ("callout", "pairings", "faq", "related_links"):
            if block.get("variant") == "italia" or btype == "callout":
                approfondisci_parts.append(html)
            elif btype == "pairings":
                approfondisci_parts.append(html)
            elif btype in ("faq", "related_links"):
                approfondisci_parts.append(html)
            else:
                approfondisci_parts.append(html)
        else:
            leftover.append(html)

    out = lead + "".join(leftover)
    if prepara_parts:
        out += (
            f'<section id="prepara" class="tv-zone">'
            f'{"".join(prepara_parts)}</section>'
        )
    if approfondisci_parts:
        out += (
            f'<section id="approfondisci" class="tv-zone">'
            f'{"".join(approfondisci_parts)}</section>'
        )
    return out.strip()


def has_level_sections(blocks: list[dict]) -> bool:
    for block in blocks:
        if block.get("type") == "level_section" and block.get("level") == "deep":
            return True
        if block.get("type") == "level_section":
            if has_level_sections(block.get("blocks", [])):
                return True
    return False


def find_blocks_by_type(blocks: list[dict], btype: str) -> list[dict]:
    found: list[dict] = []
    for block in blocks:
        if block.get("type") == btype:
            found.append(block)
        if block.get("type") == "level_section":
            found.extend(find_blocks_by_type(block.get("blocks", []), btype))
    return found
