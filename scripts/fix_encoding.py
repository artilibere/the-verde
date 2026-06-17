#!/usr/bin/env python3
"""Restore Italian accents in prose; preserve URL slugs and /varieta/ paths."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", "dist", "pagefind", ".venv", "__pycache__", "books"}
SKIP_FILES = {"scripts/build.py", "assets/js/diario.js", "assets/js/paths.js", "assets/js/share.js"}
EXTENSIONS = {".md", ".html", ".json", ".py", ".js", ".mdc"}

MOJIBAKE = [
    ("tÃ¨", "tè"),
    ("tï¿½", "tè"),
    ("Varietï¿½", "Varietà"),
    ("Variet\uFFFD", "Varietà"),
    ("t\uFFFD", "tè"),
    ("verit\uFFFD", "verità"),
    ("Forast\uFFFD", "Forasté"),
]

REPLACEMENTS = [
    ("te verde", "tè verde"),
    ("Te verde", "Tè verde"),
    # NOTE: keep this conservative; don't touch "ristorante giapponese"
    (" te giapponese", " tè giapponese"),
    ("del te ", "del tè "),
    ("del te.", "del tè."),
    ("del te,", "del tè,"),
    (" il te ", " il tè "),
    (" il te.", " il tè."),
    (" il te,", " il tè,"),
    (" il te che", " il tè che"),
    ("t verde", "tè verde"),
    (" l acqua", " l'acqua"),
    (" l errore", " l'errore"),
    (" L ora", " L'ora"),
    ("L ora", "L'ora"),
    (" d inverno", " d'inverno"),
    (" all aperitivo", " all'aperitivo"),
    (" d Oriente", " d'Oriente"),
    (" foglia e il", " foglia è il"),
    (" l hojicha", " l'hojicha"),
    (" L ombreggiatura", " L'ombreggiatura"),
    ("L ombreggiatura", "L'ombreggiatura"),
    ("pero,", "però,"),
    ("pero ", "però "),
    ("pero.", "però."),
    ("puo ", "può "),
    ("puo.", "può."),
    ("piu ", "più "),
    ("piu.", "più."),
    ("piu,", "più,"),
    ("caffe ", "caffè "),
    ("caffe.", "caffè."),
    ("caffe,", "caffè,"),
    ("caffe:", "caffè:"),
    ("caffe;", "caffè;"),
    ("caffe domina", "caffè domina"),
    ("citta", "città"),
    (" ne le ", " né le "),
    (" ne le", " né le"),
    ("quotidianita", "quotidianità"),
    ("qualita", "qualità"),
    ("grassosita", "grassosità"),
    ("acidita", "acidità"),
    ("onesta ", "onestà "),
    ("onesta.", "onestà."),
    ("Perche ", "Perché "),
    (" cosi ", " così "),
    ("dell Himalaya", "dell'Himalaya"),
    ("dell amaro", "dell'amaro"),
    ("personalita", "personalità"),
    ("Mineralita", "Mineralità"),
    ("non e l unico", "non è l'unico"),
    ("non e una", "non è una"),
    ("Il matcha e arrivato", "Il matcha è arrivato"),
    (", e diventato", ", è diventato"),
    ("il kukicha e economico", "il kukicha è economico"),
    ("Quale te ", "Quale tè "),
    ("Quando bevi te", "Quando bevi tè"),
    ("Orologio del te", "Orologio del tè"),
    ("Pensatore del te", "Pensatore del tè"),
    ("Arte cinese del te", "Arte cinese del tè"),
    ("E un te ", "È un tè "),
    ("te affumicato", "tè affumicato"),
    ("tutte e 6 le", "tutte le 6"),
    ("Verita", "Verità"),
    ("Mito o verita", "Mito o verità"),
    ("Varieta di", "Varietà di"),
    ("Varieta ", "Varietà "),
    ("varieta e", "varietà e"),
    ("varieta,", "varietà,"),
    ("varieta.", "varietà."),
    ("varieta?", "varietà?"),
    ("varieta ", "varietà "),
    (" di variet ", " di varietà "),
    (" di variet:", " di varietà:"),
    (" di variet.", " di varietà."),
    ("ci che ", "ciò che "),
    ("ci che.", "ciò che."),
]

# Copula «e» → «è» (soggetti noti)
COPULA_E = re.compile(
    r"\b(il sencha|il gyokuro|il matcha|il bancha|il kukicha|il tè|la cerimonia)\s+e\s+"
    r"(spesso|il battito|il più|arrivato|economico|diventato)\b",
    re.IGNORECASE,
)

PROTECTED_LINE = re.compile(
    r"(/varieta/|^\s*slug\s*:|^\s*\"slug\"\s*:|href\s*=\s*[\"']/varieta|"
    r"varieta/\{|f\"/varieta|type\"\s*:\s*\"varieta\"|name=\"varieta\"|"
    r"/ \"varieta\"|\"varieta\"|varieta_temi|_temi\"|"
    r"\?varieta=|\?varieta\"|^\s*stile\s*:|^\s*origine\s*:)",
    re.I,
)


TEMP_C = re.compile(r"(\d{2,3})\s+C\b")


def fix_line(line: str) -> str:
    for old, new in MOJIBAKE:
        line = line.replace(old, new)
    if re.match(r"^\s*slug\s*:", line, re.I):
        return line
    allow_varieta = not PROTECTED_LINE.search(line)
    for old, new in REPLACEMENTS:
        if not allow_varieta and "varieta" in old.lower():
            continue
        line = line.replace(old, new)
    if allow_varieta:
        line = re.sub(r"(?<![/\-a-zA-Z0-9])varieta(?![/\-a-zA-Z0-9:\"'=])", "varietà", line)
        line = COPULA_E.sub(r"\1 è \2", line)
    line = TEMP_C.sub(r"\1 °C", line)
    return line


def read_text(path: Path) -> str | None:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def fix_file(path: Path) -> bool:
    original = read_text(path)
    if original is None:
        print(f"skip (non-UTF-8): {path.relative_to(ROOT)}")
        return False
    fixed = "\n".join(fix_line(ln) for ln in original.splitlines())
    if original.endswith("\n") and not fixed.endswith("\n"):
        fixed += "\n"
    if fixed != original:
        path.write_text(fixed, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = []
    for path in sorted(ROOT.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix not in EXTENSIONS:
            continue
        if path.name == "fix_encoding.py":
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES:
            continue
        if path.name == "build.py" and "scripts" in path.parts:
            continue
        if fix_file(path):
            changed.append(path.relative_to(ROOT))
    for rel in changed:
        print(f"fixed: {rel}")
    print(f"Done — {len(changed)} file(s) updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
