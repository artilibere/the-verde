"""Pytest configuration for the-verde.it build tests."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

CONTENT_DIR = ROOT / "content"
DIST_DIR = ROOT / "dist"
TEMPLATES_DIR = ROOT / "templates"
ASSETS_DIR = ROOT / "assets"
