#!/usr/bin/env python3
"""Migrate legacy Fonti sections to structured bibliography blocks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_builder.citations import migrate_document  # noqa: E402

CONTENT = ROOT / "content"
SKIP_DIRS = {"_schemas", "_config"}


def iter_content_json() -> list[Path]:
    paths: list[Path] = []
    for path in sorted(CONTENT.rglob("*.json")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        paths.append(path)
    return paths


def main() -> int:
    changed = 0
    for path in iter_content_json():
        doc = json.loads(path.read_text(encoding="utf-8"))
        if "body" not in doc:
            continue
        before = json.dumps(doc["body"], ensure_ascii=False, sort_keys=True)
        updated = migrate_document(doc)
        after = json.dumps(updated["body"], ensure_ascii=False, sort_keys=True)
        if before != after:
            path.write_text(
                json.dumps(updated, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"migrated: {path.relative_to(ROOT)}")
            changed += 1
    print(f"Done — {changed} file(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
