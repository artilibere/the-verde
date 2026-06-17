"""Transform variety page HTML: remove duplicates, wrap zones, semantic markup."""

from __future__ import annotations

import re

REMOVE_SECTIONS = (
    "Profilo sensoriale",
    "I passaggi",
    "Domande frequenti",
    "Varietà simili",
)

PREPARA_SECTIONS = ("Attrezzatura", "Errori comuni")
APPROFONDISCI_SECTIONS = ("In Italia", "Abbinamenti")


def _h2_pattern(title: str) -> re.Pattern[str]:
    return re.compile(
        rf"<h2[^>]*>{re.escape(title)}</h2>.*?(?=<h2[^>]*>|$)",
        re.DOTALL | re.IGNORECASE,
    )


def _remove_section(html: str, title: str) -> str:
    return _h2_pattern(title).sub("", html, count=1)


def _wrap_zone(html: str, zone_id: str, inner: str) -> str:
    if not inner.strip():
        return html
    block = f'<section id="{zone_id}" class="tv-zone">{inner}</section>'
    return html + block if not html.strip() else html.rstrip() + block


def _render_steps(steps: list[dict]) -> str:
    if not steps:
        return ""
    items = []
    for step in steps:
        time_html = (
            f'<span class="tv-step-list__time">{step["time"]}</span>' if step.get("time") else ""
        )
        items.append(
            f'<li class="tv-step-list__item">'
            f'<span class="tv-step-list__action">{step["action"]}</span>{time_html}</li>'
        )
    return (
        '<h2 id="i-passaggi">I passaggi</h2>'
        f'<ol class="tv-step-list">{"".join(items)}</ol>'
    )


def _render_faqs(faqs: list[dict]) -> str:
    if not faqs:
        return ""
    items = []
    for faq in faqs:
        items.append(
            '<details class="tv-faq__item">'
            f'<summary class="tv-faq__question">{faq["question"]}</summary>'
            f'<p class="tv-faq__answer">{faq["answer"]}</p>'
            "</details>"
        )
    return (
        '<h2 id="domande-frequenti">Domande frequenti</h2>'
        f'<div class="tv-faq">{"".join(items)}</div>'
    )


def _render_related(related: list[dict]) -> str:
    if not related:
        return ""
    items = []
    for r in related:
        reason = f" — {r['reason']}" if r.get("reason") else ""
        items.append(
            f'<li><a href="{r["url"]}"><strong>{r["name"]}</strong></a>{reason}</li>'
        )
    return (
        '<h2 id="varieta-simili">Varietà simili</h2>'
        f'<ul class="tv-related__list">{"".join(items)}</ul>'
    )


def enrich_variety_html(
    html: str,
    steps: list[dict] | None = None,
    faqs: list[dict] | None = None,
    related: list[dict] | None = None,
) -> str:
    """Strip sections rendered elsewhere; wrap prepara / approfondisci zones."""
    html = re.sub(r"<h1[^>]*>.*?</h1>\s*", "", html, count=1, flags=re.DOTALL)
    for title in REMOVE_SECTIONS:
        html = _remove_section(html, title)

    sections: dict[str, str] = {}
    parts = re.split(r"(<h2[^>]*>[^<]+</h2>)", html, flags=re.IGNORECASE)
    lead = parts[0].strip() if parts else ""
    i = 1
    while i < len(parts) - 1:
        heading_tag = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        title_m = re.search(r">([^<]+)<", heading_tag)
        title = title_m.group(1).strip() if title_m else ""
        key = title.lower()
        sections[key] = heading_tag + body
        i += 2

    prepara_inner = ""
    for name in PREPARA_SECTIONS:
        prepara_inner += sections.pop(name.lower(), "")
    if steps:
        prepara_inner += _render_steps(steps)

    approfondisci_inner = ""
    italy = sections.pop("in italia", "")
    if italy:
        italy_body = re.sub(r"<h2[^>]*>In Italia</h2>\s*", "", italy, flags=re.I)
        approfondisci_inner += (
            '<div class="tv-italy-box"><h2 class="tv-italy-box__title">In Italia</h2>'
            f"{italy_body}</div>"
        )
    abbinamenti = sections.pop("abbinamenti", "")
    if abbinamenti:
        approfondisci_inner += abbinamenti
    if faqs:
        approfondisci_inner += _render_faqs(faqs)
    if related:
        approfondisci_inner += _render_related(related)

    leftover = "".join(sections.values())

    out = ""
    if lead:
        out += f'<p class="tv-variety-lead">{re.sub(r"</?p>", "", lead).strip()}</p>'
    if leftover.strip():
        out += leftover
    out = _wrap_zone(out, "prepara", prepara_inner)
    out = _wrap_zone(out, "approfondisci", approfondisci_inner)
    return out.strip()
