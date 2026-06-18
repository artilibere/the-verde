#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build static site for the-verde.it from JSON content."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_builder.builder import SiteBuilder

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the-verde.it static site")
    parser.add_argument("--content", type=Path, default=ROOT / "content")
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    parser.add_argument("--templates", type=Path, default=ROOT / "templates")
    parser.add_argument("--assets", type=Path, default=ROOT / "assets")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate JSON content, do not build",
    )
    args = parser.parse_args()

    builder = SiteBuilder(
        args.content,
        args.out,
        args.templates,
        args.assets,
        validate=True,
    )
    if args.validate_only:
        builder.load_content()
        print("All content documents valid.")
        return

    builder.build()


if __name__ == "__main__":
    main()
