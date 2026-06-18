#!/usr/bin/env python3
"""One-shot migration: Markdown content → structured JSON documents."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import frontmatter
import markdown

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_builder.loader import infer_type_from_path, validate_document

MD_EXTENSIONS = ["extra", "smarty"]


def slugify_keyword(text: str) -> str:
    text = text.lower().strip()
    for old, new in [("\u00e0", "a"), ("\u00e8", "e"), ("\u00e9", "e"), ("\u00ec", "i"), ("\u00f2", "o"), ("\u00f9", "u")]:
        text = text.replace(old, new)
    return text


def text_to_spans(text: str) -> list[dict]:
    text = text.strip()
    if not text:
        return [{"type": "text", "value": ""}]
    spans: list[dict] = []
    pattern = re.compile(r"\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)]+)\)")
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            spans.append({"type": "text", "value": text[pos : m.start()]})
        if m.group(1):
            spans.append({"type": "strong", "value": m.group(1)})
        else:
            spans.append({"type": "link", "value": m.group(2), "href": m.group(3)})
        pos = m.end()
    if pos < len(text):
        spans.append({"type": "text", "value": text[pos:]})
    return spans or [{"type": "text", "value": text}]


def html_to_text(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html).strip()


def parse_md_sections(content: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current = "_lead"
    sections[current] = ""
    for line in content.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = ""
        else:
            sections[current] = sections.get(current, "") + line + "\n"
    return sections


def md_list_items(section: str) -> list[str]:
    items = []
    for line in section.splitlines():
        line = line.strip()
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif re.match(r"^\d+\.\s", line):
            items.append(re.sub(r"^\d+\.\s*", "", line).strip())
    return items


def parse_sensory_section(section: str) -> dict | None:
    profile = {}
    for label in ("Aspetto", "Aroma", "Gusto", "Retrogusto"):
        m = re.search(rf"\*\*{label}:\*\*\s*(.+)", section)
        if m:
            profile[label.lower()] = m.group(1).strip()
    return profile if profile else None


def parse_steps_section(section: str) -> list[dict]:
    steps = []
    for item in md_list_items(section):
        if " - " in item:
            text, duration = item.split(" - ", 1)
            steps.append({"text": text.strip(), "duration": duration.strip()})
        else:
            steps.append({"text": item, "duration": ""})
    return steps


def parse_faq_section(section: str) -> list[dict]:
    faqs = []
    parts = re.split(r"^###\s+", section, flags=re.MULTILINE)
    for part in parts[1:]:
        lines = part.strip().split("\n", 1)
        if len(lines) == 2:
            faqs.append(
                {
                    "question": lines[0].strip(),
                    "answer_spans": text_to_spans(lines[1].strip()),
                }
            )
    return faqs


def parse_related_section(section: str) -> list[dict]:
    related = []
    for item in md_list_items(section):
        m = re.search(r"\*\*([^*]+)\*\*\s*\(([^)]+)\)", item)
        if m:
            url = m.group(2).strip()
            if not url.startswith("/"):
                url = f"/varieta/{url.strip('/')}/"
            reason_m = re.search(r"[-\u2014]\s*(.+)$", item)
            related.append(
                {
                    "name": m.group(1).strip(),
                    "url": url,
                    "reason": reason_m.group(1).strip() if reason_m else "",
                }
            )
    return related


def url_for_path(path: Path, content_dir: Path, slug: str) -> str:
    rel = path.relative_to(content_dir)
    parts = rel.parts
    if parts[0] == "varieta":
        return f"/varieta/{slug}/"
    if parts[0] == "guide":
        return f"/guide/{slug}/"
    if parts[0] == "glossario":
        return f"/glossario/{slug}/"
    if parts[0] == "impara" and len(parts) > 2 and parts[1] == "controversie":
        return f"/impara/controversie/{slug}/"
    if parts[0] == "impara":
        return f"/impara/{slug}/"
    if parts[0] == "italia":
        if path.name == "index.md":
            return "/italia/"
        if len(parts) > 2 and parts[1] == "momenti":
            return f"/italia/momenti/{slug}/"
        if len(parts) > 2 and parts[1] == "stagioni":
            return f"/italia/stagioni/{slug}/"
        if slug == "abbinamenti":
            return "/italia/abbinamenti/"
    if parts[0] == "gioca" and len(parts) > 2 and parts[1] == "percorsi":
        return f"/gioca/percorsi/{slug}/"
    if parts[0] == "pagine":
        if slug == "home":
            return "/"
        return f"/{slug}/"
    return f"/{slug}/"


def keywords_from_meta(fm: dict, title: str) -> list[str]:
    kws = list(fm.get("keywords", []))
    if not kws:
        kws = ["tè verde", "Camellia sinensis"]
        if fm.get("stile"):
            kws.append(str(fm["stile"]))
        if fm.get("origine"):
            kws.append(str(fm["origine"]))
        first = title.split("—")[0].strip() if "—" in title else title.split(" - ")[0].strip()
        if first:
            kws.insert(0, first.lower())
    return kws[:8]


def convert_variety(path: Path, fm: dict, sections: dict) -> dict:
    slug = fm.get("slug", path.stem)
    blocks: list[dict] = []

    lead = sections.get("_lead", "").strip()
    if lead:
        paras = [p.strip() for p in lead.split("\n\n") if p.strip()]
        for para in paras:
            if para.startswith("# "):
                continue
            blocks.append({"type": "paragraph", "spans": text_to_spans(para)})

    sensory = parse_sensory_section(sections.get("profilo sensoriale", ""))
    if sensory:
        blocks.append({"type": "sensory_profile", **sensory})

    brew = {
        "type": "brew_params",
        "temp": fm.get("brew_temp", 75),
        "grams": fm.get("brew_grams", 3),
        "seconds": fm.get("brew_seconds", 60),
        "infusions": str(fm.get("brew_infusions", "2-3")),
    }
    blocks.append(brew)

    equip = md_list_items(sections.get("attrezzatura", ""))
    if equip:
        blocks.append({"type": "equipment", "items": equip})

    steps = parse_steps_section(sections.get("i passaggi", "") or sections.get("preparazione", ""))
    if steps:
        blocks.append({"type": "steps", "items": steps})

    errors = md_list_items(sections.get("errori comuni", ""))
    if errors:
        blocks.append({"type": "errors", "items": errors})

    italia = sections.get("in italia", "").strip()
    if italia:
        blocks.append({"type": "callout", "variant": "italia", "spans": text_to_spans(html_to_text(italia))})

    pairings = md_list_items(sections.get("abbinamenti", ""))
    if pairings:
        blocks.append({"type": "pairings", "items": pairings})

    faqs = parse_faq_section(sections.get("domande frequenti", ""))
    if faqs:
        blocks.append({"type": "faq", "items": faqs})

    related = parse_related_section(sections.get("varietà simili", ""))
    if related:
        blocks.append({"type": "related_links", "items": related})

    title = fm.get("title", slug)
    description = fm.get("meta_description") or title
    nav: dict = {
        "related_slugs": fm.get("related_slugs", []),
        "temi_kb": fm.get("temi_kb", []),
        "controversie": fm.get("controversie", []),
        "momenti": fm.get("momenti", []),
        "stagioni": fm.get("stagioni", []),
        "explore_next": [],
    }
    if fm.get("percorso_tappa"):
        nav["percorso_tappa"] = fm["percorso_tappa"]
    if fm.get("badge_sblocco"):
        nav["badge_sblocco"] = fm["badge_sblocco"]

    return {
        "schema_version": "1.0",
        "type": "variety",
        "slug": slug,
        "meta": {
            "title": title,
            "description": description,
            "keywords": keywords_from_meta(fm, title),
            "canonical_path": f"/varieta/{slug}/",
        },
        "seo": {"robots": "index,follow", "og_type": "article"},
        "navigation": nav,
        "taxonomy": {
            "origine": fm.get("origine", ""),
            "stile": fm.get("stile", ""),
            "caffeina": fm.get("caffeina", ""),
            "stagione": fm.get("stagione", ""),
            "cultivar": fm.get("cultivar", ""),
            "sort_order": fm.get("sort_order"),
            "brew": {
                "temp": fm.get("brew_temp", 75),
                "grams": fm.get("brew_grams", 3),
                "seconds": fm.get("brew_seconds", 60),
                "infusions": str(fm.get("brew_infusions", "2-3")),
            },
        },
        "body": {"blocks": blocks},
    }


def convert_generic(
    path: Path, fm: dict, sections: dict, doc_type: str, content_dir: Path
) -> dict:
    slug = fm.get("slug", path.stem)
    if path.name == "index.md" and path.parent.name == "italia":
        slug = "index"
    blocks: list[dict] = []

    if doc_type == "controversy" and fm.get("posizioni"):
        blocks.append({"type": "positions", "items": fm["posizioni"]})

    for key, section in sections.items():
        if key == "_lead":
            for para in [p.strip() for p in section.split("\n\n") if p.strip() and not p.startswith("#")]:
                if para.startswith("# "):
                    blocks.append(
                        {
                            "type": "heading",
                            "level": 1,
                            "spans": text_to_spans(para.lstrip("# ").strip()),
                        }
                    )
                else:
                    blocks.append({"type": "paragraph", "spans": text_to_spans(para)})
        elif key in ("per iniziare", "approfondimento", "in sintesi"):
            level = "intro" if key == "per iniziare" else "deep"
            inner: list[dict] = []
            for para in [p.strip() for p in section.split("\n\n") if p.strip()]:
                inner.append({"type": "paragraph", "spans": text_to_spans(para)})
            blocks.append({"type": "level_section", "level": level, "blocks": inner})
        elif key == "posizioni":
            continue
        else:
            blocks.append(
                {
                    "type": "heading",
                    "level": 2,
                    "spans": text_to_spans(key.title()),
                }
            )
            items = md_list_items(section)
            if items:
                blocks.append(
                    {
                        "type": "list",
                        "ordered": bool(re.search(r"^\d+\.", section, re.M)),
                        "items": [{"spans": text_to_spans(i)} for i in items],
                    }
                )
            else:
                for para in [p.strip() for p in section.split("\n\n") if p.strip()]:
                    blocks.append({"type": "paragraph", "spans": text_to_spans(para)})

    title = fm.get("title", slug)
    canonical = url_for_path(path, content_dir, slug)
    description = fm.get("meta_description") or fm.get("description") or title
    published = fm.get("published")
    if published is not None and not isinstance(published, str):
        published = str(published)

    meta: dict = {
        "title": title,
        "description": description,
        "keywords": keywords_from_meta(fm, title),
        "canonical_path": canonical,
    }
    if published:
        meta["published"] = published

    nav: dict = {
        "related_slugs": fm.get("related_slugs", []),
        "temi_kb": fm.get("temi_kb", []),
        "controversie": fm.get("controversie", []),
        "explore_next": [],
    }
    if fm.get("percorso_tappa"):
        nav["percorso_tappa"] = fm["percorso_tappa"]
    if fm.get("badge_sblocco"):
        nav["badge_sblocco"] = fm["badge_sblocco"]

    return {
        "schema_version": "1.0",
        "type": doc_type,
        "slug": slug,
        "meta": meta,
        "seo": {"robots": "index,follow", "og_type": "article"},
        "navigation": nav,
        "taxonomy": {},
        "body": {"blocks": blocks},
    }


def convert_file(path: Path, content_dir: Path) -> dict:
    post = frontmatter.load(path)
    fm = dict(post.metadata)
    sections = parse_md_sections(post.content)
    doc_type = infer_type_from_path(path.with_suffix(".json"), content_dir)

    if doc_type == "variety":
        return convert_variety(path, fm, sections)
    return convert_generic(path, fm, sections, doc_type, content_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate Markdown to JSON content")
    parser.add_argument("--content", type=Path, default=ROOT / "content")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    content_dir = args.content

    errors = []
    converted = 0
    for md_path in sorted(content_dir.rglob("*.md")):
        if "_config" in md_path.parts:
            continue
        try:
            doc = convert_file(md_path, content_dir)
            out_path = md_path.with_suffix(".json")
            doc_errors = validate_document(content_dir, doc)
            if doc_errors:
                errors.extend(f"{md_path}: {e}" for e in doc_errors)
                continue
            if not args.dry_run:
                out_path.write_text(
                    json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            converted += 1
            print(f"OK {md_path.relative_to(content_dir)} → {out_path.name}")
        except Exception as exc:
            errors.append(f"{md_path}: {exc}")

    if errors:
        print("\nErrors:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    print(f"\nConverted {converted} files")


if __name__ == "__main__":
    main()
