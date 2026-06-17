#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

if [[ ! -f .venv/.deps_ok ]] || [[ requirements.txt -nt .venv/.deps_ok ]]; then
  pip install -q -r requirements.txt
  touch .venv/.deps_ok
fi

python3 scripts/build.py --content content --out dist
npx --yes pagefind --site dist --output-path dist/pagefind
npx --yes wrangler pages deploy dist --project-name=the-verde --branch=main "$@"
