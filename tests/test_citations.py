"""Bibliography migration and legacy citation parsing."""

from __future__ import annotations

from site_builder.citations import fonte_autore, legacy_to_bib_entry, migrate_document


def test_fonte_autore_maps_book_id():
    assert fonte_autore("sommelier") == "Bisogno, Victoria; Pettigrew, Jane"
    assert fonte_autore("rosen") == "Rosen, Diana"


def test_legacy_tema_pattern():
    entry = legacy_to_bib_entry("rosen, tema rosen-salute")
    assert entry is not None
    assert entry["author"] == "Rosen, Diana"
    assert entry["tema"] == "rosen-salute"
    assert entry["pages"] == "2714–2838"


def test_legacy_treccani():
    entry = legacy_to_bib_entry("Treccani — umami")
    assert entry is not None
    assert entry["author"] == "Treccani"
    assert "umami" in entry["sotto_tema"]


def test_migrate_fonti_heading_to_bibliography():
    doc = {
        "slug": "esempio",
        "type": "glossary",
        "body": {
            "blocks": [
                {
                    "type": "level_section",
                    "level": "deep",
                    "blocks": [
                        {
                            "type": "heading",
                            "level": 2,
                            "spans": [{"type": "text", "value": "Fonti"}],
                        },
                        {
                            "type": "list",
                            "ordered": False,
                            "items": [
                                {
                                    "spans": [
                                        {"type": "text", "value": "pellegrino, chanoyu"}
                                    ]
                                }
                            ],
                        },
                    ],
                }
            ]
        },
    }
    out = migrate_document(doc)
    deep = out["body"]["blocks"][0]["blocks"]
    assert len(deep) == 1
    assert deep[0]["type"] == "bibliography"
    assert deep[0]["items"][0]["tema"] == "pellegrino-tradizioni"
