"""Block renderer unit tests."""

from __future__ import annotations

from site_builder.blocks import render_block, render_blocks, render_spans, render_variety_body

def test_render_spans_link():
    html = render_spans(
        [
            {"type": "text", "value": "Vedi "},
            {"type": "link", "value": "sencha", "href": "/varieta/sencha/"},
        ]
    )
    assert '<a href="/varieta/sencha/">sencha</a>' in html


def test_render_heading_level():
    html = render_block(
        {"type": "heading", "level": 2, "spans": [{"type": "text", "value": "Titolo"}]}
    )
    assert html == "<h2>Titolo</h2>"


def test_render_faq_semantic():
    html = render_block(
        {
            "type": "faq",
            "items": [
                {
                    "question": "Domanda?",
                    "answer_spans": [{"type": "text", "value": "Risposta."}],
                }
            ],
        }
    )
    assert "<details" in html
    assert "<summary" in html
    assert "Domanda?" in html


def test_render_variety_zones():
    blocks = [
        {"type": "paragraph", "spans": [{"type": "text", "value": "Lead varietà."}]},
        {"type": "equipment", "items": ["Kyusu"]},
        {"type": "steps", "items": [{"text": "Infusiona", "duration": "1 min"}]},
        {
            "type": "callout",
            "variant": "italia",
            "spans": [{"type": "text", "value": "In Italia..."}],
        },
    ]
    html = render_variety_body(blocks)
    assert 'id="prepara"' in html
    assert 'id="approfondisci"' in html
    assert "tv-variety-lead" in html


def test_render_bibliography_formal():
    html = render_block(
        {
            "type": "bibliography",
            "items": [
                {
                    "author": "Hara, Yukihiko (a cura di)",
                    "title": "Health Benefits of Green Tea",
                    "tema": "hara-anticancer",
                    "sotto_tema": "Trial clinici",
                    "pages": "113",
                }
            ],
        }
    )
    assert "tv-bibliography" in html
    assert "Bibliografia" in html
    assert "Hara, Yukihiko" in html
    assert "<cite" in html
    assert "Tema" not in html
    assert "hara-anticancer" not in html


def test_render_bibliography_skips_kb_entry():
    html = render_block(
        {
            "type": "bibliography",
            "items": [
                {
                    "author": "Rosen, Diana",
                    "title": "Il libro del tè verde",
                    "tema": "rosen-salute",
                    "sotto_tema": "Salute",
                    "pages": "2714",
                },
                {
                    "author": "The Verde",
                    "title": "Knowledge base sul tè verde",
                    "tema": "qualita-sensoriale-vs-chimica",
                    "sotto_tema": "Prospettiva contrastante",
                    "pages": None,
                    "kb_ref": "books/knowledge-base.json",
                },
            ],
        }
    )
    assert "knowledge-base.json" not in html
    assert "Rosen, Diana" in html


def test_article_blocks_no_zones():
    blocks = [
        {"type": "paragraph", "spans": [{"type": "text", "value": "Paragrafo."}]},
    ]
    html = render_blocks(blocks)
    assert "prepara" not in html
    assert "<p>Paragrafo.</p>" in html
