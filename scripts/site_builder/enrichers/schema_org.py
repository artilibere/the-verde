"""Auto-generate supplementary schema.org from document blocks."""

from __future__ import annotations

from site_builder.blocks import find_blocks_by_type
from site_builder.enrichers._seo_core import ITALY_AUDIENCE


def howto_schema(
    base_url: str,
    *,
    title: str,
    url: str,
    steps: list[dict],
) -> dict | None:
    if not steps:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": title,
        "url": f"{base_url}{url}",
        "inLanguage": "it-IT",
        "audience": ITALY_AUDIENCE,
        "step": [
            {
                "@type": "HowToStep",
                "position": i + 1,
                "name": step.get("action", step.get("text", "")),
                "text": step.get("action", step.get("text", "")),
            }
            for i, step in enumerate(steps)
        ],
    }


def supplementary_schemas(
    base_url: str,
    *,
    doc: dict,
    meta: dict,
    url: str,
) -> list[dict]:
    """Extra JSON-LD from blocks when not in seo.schema_org."""
    seo = doc.get("seo") or {}
    if seo.get("schema_org"):
        custom = seo["schema_org"]
        return custom if isinstance(custom, list) else [custom]

    blocks = doc.get("body", {}).get("blocks", [])
    extras: list[dict] = []

    if doc.get("type") == "variety":
        step_items = []
        for block in find_blocks_by_type(blocks, "steps"):
            for item in block.get("items", []):
                step_items.append({"action": item.get("text", ""), "text": item.get("text", "")})
        howto = howto_schema(
            base_url,
            title=meta.get("title", ""),
            url=url,
            steps=step_items or meta.get("steps", []),
        )
        if howto:
            extras.append(howto)

    return extras
