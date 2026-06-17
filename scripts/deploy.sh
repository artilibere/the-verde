#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
pip install -q -r requirements.txt
python3 scripts/build.py --content content --out dist
npx --yes pagefind --site dist --output-path dist/pagefind
npx --yes wrangler pages deploy dist --project-name=the-verde --branch=main "$@"
