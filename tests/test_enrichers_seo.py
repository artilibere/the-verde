"""SEO and schema.org enricher tests."""

from __future__ import annotations

from site_builder.document import collect_faq_items
from site_builder.enrichers._seo_core import (
    build_llms_txt,
    dumps_json_ld,
    faq_schema,
    item_list_schema,
    learning_resource_schema,
    quiz_faq_items,
    variety_schema,
    webpage_schema,
)
from site_builder.enrichers.schema_org import howto_schema, supplementary_schemas
from site_builder.enrichers.seo_context import _collect_hub_list_items, apply_seo, build_schema_blocks


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


def test_hub_item_list_schema_from_ctx():
    items = _collect_hub_list_items(
        {
            "items": [
                {"title": "Sencha", "url": "/varieta/sencha/"},
                {"title": "Gyokuro", "url": "/varieta/gyokuro/"},
            ]
        }
    )
    schema = item_list_schema(
        "https://the-verde.it",
        name="Impara",
        url="/impara/",
        items=items,
    )
    assert schema["@type"] == "ItemList"
    assert len(schema["itemListElement"]) == 2


def test_build_schema_blocks_hub_has_item_list():
    class _Builder:
        base_url = "https://the-verde.it"
        site_name = "The Verde"
        hreflang = "it"
        locale = "it-IT"
        og_image = "/assets/images/og-default.png"
        social = {}

    blocks = build_schema_blocks(
        {
            "page_type": "hub",
            "items": [
                {"title": "Storia", "url": "/impara/storia-cultura/"},
                {"title": "Salute", "url": "/impara/salute/"},
            ],
        },
        _Builder(),
        {},
        "/impara/",
        "Impara",
        "Otto pilastri di conoscenza sul tè verde.",
    )
    assert any('"@type":"ItemList"' in block or '"@type": "ItemList"' in block for block in blocks)


def test_quiz_faq_items_skips_personality_quiz():
    quiz = {
        "questions": [
            {"q": "Q1?", "options": ["A", "B"], "correct": 0, "explain": "Perché A."},
            {"q": "Q2?", "options": ["X", "Y"], "scores": {"x": 1}},
        ]
    }
    items = quiz_faq_items(quiz)
    assert len(items) == 1
    assert items[0]["question"] == "Q1?"
    assert "Perché A." in items[0]["answer"]


def test_variety_schema_brew_properties():
    schema = variety_schema(
        "https://the-verde.it",
        title="Sencha",
        description="Tè verde giapponese.",
        url="/varieta/sencha/",
        origin_slug="giappone",
        origin_label="Giappone",
        brew_temp=70,
        brew_grams=4,
        brew_seconds=60,
    )
    props = schema.get("additionalProperty") or []
    names = {p["name"] for p in props}
    assert "Temperatura acqua" in names
    assert "Dosaggio" in names


def test_learning_resource_schema_for_path():
    lr = learning_resource_schema(
        "https://the-verde.it",
        title="Primavera in tazza",
        description="Percorso guidato.",
        url="/gioca/percorsi/primavera-in-tazza/",
        steps=[
            {"title": "Shincha", "type": "varieta", "slug": "shincha"},
            {"title": "Quiz", "type": "quiz", "url": "/gioca/quiz/calendario-primavera/"},
        ],
    )
    assert lr is not None
    assert lr["@type"] == "LearningResource"
    assert len(lr["hasPart"]) == 2


def test_build_llms_txt_includes_gioca_sections():
    text = build_llms_txt(
        "https://the-verde.it",
        "The Verde",
        paths=[{"slug": "primavera-in-tazza", "title": "Primavera in tazza", "description": "Raccolti."}],
        quizzes=[{"slug": "verde-vero", "title": "Verde vero", "description": "Tè o tisana?"}],
    )
    assert "Gioca — percorsi guidati" in text
    assert "Gioca — quiz" in text
    assert "Entità chiave (disambiguazione)" in text
    assert "/gioca/quiz/verde-vero/" in text


def test_build_schema_blocks_quiz_has_faq():
    class _Builder:
        base_url = "https://the-verde.it"
        site_name = "The Verde"
        hreflang = "it"
        locale = "it-IT"
        og_image = "/assets/images/og-default.png"
        social = {}

    quiz = {
        "slug": "verde-vero",
        "title": "Verde vero",
        "questions": [
            {"q": "Camomilla è tè verde?", "options": ["Sì", "No"], "correct": 1, "explain": "È una tisana."},
        ],
    }
    blocks = build_schema_blocks(
        {"page_type": "quiz", "quiz": quiz},
        _Builder(),
        {},
        "/gioca/quiz/verde-vero/",
        "Verde vero",
        "Quiz sul tè verde.",
    )
    assert any("FAQPage" in block for block in blocks)


def test_apply_seo_truncates_long_title_with_brand_suffix():
    class _Builder:
        base_url = "https://the-verde.it"
        site_name = "The Verde"
        hreflang = "it"
        locale = "it-IT"
        og_image = ""
        social = {}

    ctx = {
        "seo_title": "Huang Shan Mao Feng — lanugine delle Montagne Gialle",
        "seo_description": "Descrizione valida abbastanza lunga per superare la soglia minima SEO del sito editoriale.",
        "page_type": "variety",
    }
    apply_seo(ctx, _Builder())
    rendered = f"{ctx['seo_title']} | The Verde"
    assert len(rendered) <= 60
    assert ctx["seo_title"].endswith("…")

