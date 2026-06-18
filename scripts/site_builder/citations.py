"""Canonical bibliography entries aligned with books/knowledge-base.json."""

from __future__ import annotations

BOOKS: dict[str, dict[str, str]] = {
    "rosen": {
        "author": "Rosen, Diana",
        "title": "Il libro del tè verde",
    },
    "sommelier": {
        "author": "Bisogno, Victoria; Pettigrew, Jane",
        "title": "Manuale del sommelier del tè",
    },
    "pellegrino": {
        "author": "Pellegrino, Davide",
        "title": "Manuale per la preparazione del tè",
    },
    "onuma": {
        "author": "Onuma, Izumi Forasté",
        "title": "El secreto japones del tè verde",
    },
    "hara": {
        "author": "Hara, Yukihiko (a cura di)",
        "title": "Health Benefits of Green Tea",
    },
}


def bib_item(
    book_id: str,
    tema: str,
    sotto_tema: str,
    pages: str | None,
) -> dict:
    """Structured bibliography entry for a KB source."""
    book = BOOKS[book_id]
    return {
        "author": book["author"],
        "title": book["title"],
        "tema": tema,
        "sotto_tema": sotto_tema,
        "pages": pages,
    }


def bib_kb_prospettiva(prosp_id: str, questione: str) -> dict:
    """Entry for a contrasting perspective in the knowledge base."""
    return {
        "author": "The Verde",
        "title": "Knowledge base sul tè verde",
        "tema": prosp_id,
        "sotto_tema": f"Prospettiva contrastante: {questione}",
        "pages": None,
        "kb_ref": "books/knowledge-base.json",
    }


def bibliography_block(items: list[dict]) -> dict:
    return {"type": "bibliography", "items": items}
