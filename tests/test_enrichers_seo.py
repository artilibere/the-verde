"""SEO and schema.org enricher tests."""

from __future__ import annotations

from site_builder.enrichers._seo_core import dumps_json_ld, faq_schema, webpage_schema
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
