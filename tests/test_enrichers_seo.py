"""SEO and schema.org enricher tests."""

from __future__ import annotations

from site_builder.document import collect_faq_items
from site_builder.enrichers._seo_core import build_llms_txt, dumps_json_ld, faq_schema, webpage_schema
from site_builder.enrichers.schema_org import howto_schema, supplementary_schemas


def test_webpage_schema_has_context():
    schema = webpage_schema(
        "https://the-verde.it",
        title="Test",
        description="Desc",
        url="/test/",
    )
    assert schema["@context"] == "https://schema.org"
    assert schema["@type"] == "WebPage"
    assert schema["inLanguage"] == "it-IT"


def test_faq_schema_from_meta():
    faq = faq_schema([{"question": "Q?", "answer": "A."}])
    assert faq is not None
    assert faq["@type"] == "FAQPage"
    assert len(faq["mainEntity"]) == 1


def test_howto_schema_from_steps():
    howto = howto_schema(
        "https://the-verde.it",
        title="Sencha",
        url="/varieta/sencha/",
        steps=[{"action": "Infusiona", "text": "Infusiona"}],
    )
    assert howto is not None
    assert howto["@type"] == "HowTo"


def test_supplementary_schemas_variety():
    doc = {
        "type": "variety",
        "seo": {},
        "body": {
            "blocks": [
                {
                    "type": "steps",
                    "items": [{"text": "Scalda acqua", "duration": "2 min"}],
                }
            ]
        },
    }
    extras = supplementary_schemas(
        "https://the-verde.it",
        doc=doc,
        meta={"title": "Sencha"},
        url="/varieta/sencha/",
    )
    assert any(e["@type"] == "HowTo" for e in extras)


def test_dumps_json_ld_compact():
    raw = dumps_json_ld({"@context": "https://schema.org", "@type": "Thing"})
    assert '"@context"' in raw
    assert " " not in raw or raw.count(" ") < 3


def test_collect_faq_items_from_blocks():
    doc = {
        "body": {
            "blocks": [
                {
                    "type": "faq",
                    "items": [
                        {
                            "question": "Cos'è il sencha?",
                            "answer_spans": [{"type": "text", "value": "Tè verde giapponese al sole."}],
                        }
                    ],
                }
            ]
        }
    }
    items = collect_faq_items(doc=doc)
    assert len(items) == 1
    assert items[0]["question"] == "Cos'è il sencha?"


def test_build_llms_txt_contains_hubs():
    text = build_llms_txt("https://the-verde.it", "The Verde")
    assert "Camellia sinensis" in text
    assert "/glossario/" in text
    assert "/varieta/" in text
    assert "Domande tipiche" in text
    assert "/feed.xml" in text


def test_build_llms_txt_with_inventory():
    text = build_llms_txt(
        "https://the-verde.it",
        "The Verde",
        varieties=[{"title": "Sencha", "url": "/varieta/sencha/", "description": "Tè verde giapponese."}],
        glossary=[{"title": "Umami", "url": "/glossario/umami/", "description": "Quinto gusto."}],
    )
    assert "[Sencha]" in text
    assert "[Umami]" in text
    assert "Varietà (schede complete)" in text

