"""SEO helpers: sitemap, robots, JSON-LD structured data."""

from __future__ import annotations

import json
from xml.sax.saxutils import escape as xml_escape

ITALY_PLACE = {"@type": "Country", "name": "Italy"}
ITALY_AUDIENCE = {
    "@type": "Audience",
    "audienceType": "Appassionati di tè verde in Italia",
    "geographicArea": ITALY_PLACE,
}

ORIGIN_COUNTRIES: dict[str, dict] = {
    "giappone": {"@type": "Country", "name": "Japan"},
    "cina": {"@type": "Country", "name": "China"},
    "india": {"@type": "Country", "name": "India"},
    "taiwan": {"@type": "Country", "name": "Taiwan"},
    "corea": {"@type": "Country", "name": "South Korea"},
}


def _brew_properties(
    *,
    temp: float | int | None = None,
    grams: float | int | None = None,
    seconds: float | int | None = None,
    infusions: str | None = None,
) -> list[dict]:
    props: list[dict] = []
    if temp is not None:
        props.append(
            {
                "@type": "PropertyValue",
                "name": "Temperatura acqua",
                "value": f"{temp} °C",
            }
        )
    if grams is not None:
        props.append(
            {
                "@type": "PropertyValue",
                "name": "Dosaggio",
                "value": f"{grams} g per 150 ml",
            }
        )
    if seconds is not None and seconds > 0:
        props.append(
            {
                "@type": "PropertyValue",
                "name": "Tempo infusione",
                "value": f"{seconds} secondi",
            }
        )
    if infusions:
        props.append(
            {
                "@type": "PropertyValue",
                "name": "Infusioni",
                "value": str(infusions),
            }
        )
    return props


def dumps_json_ld(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def webpage_schema(
    base_url: str,
    *,
    title: str,
    description: str,
    url: str,
    italy_context: bool = True,
) -> dict:
    schema: dict = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": f"{base_url}{url}",
        "inLanguage": "it-IT",
    }
    if italy_context:
        schema["audience"] = ITALY_AUDIENCE
        schema["spatialCoverage"] = ITALY_PLACE
    return schema


def item_list_schema(
    base_url: str,
    *,
    name: str,
    url: str,
    items: list[dict],
) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "url": f"{base_url}{url}",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": item["title"],
                "url": f"{base_url}{item['url']}",
            }
            for i, item in enumerate(items)
        ],
    }


def website_schema(base_url: str, site_name: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_name,
        "url": base_url,
        "inLanguage": "it-IT",
        "audience": ITALY_AUDIENCE,
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{base_url}/cerca/?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }


def organization_schema(base_url: str, site_name: str, same_as: list[str] | None = None) -> dict:
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": site_name,
        "url": base_url,
        "description": "Cultura del tè verde (Camellia sinensis) per chi vive in Italia.",
        "areaServed": ITALY_PLACE,
        "knowsLanguage": ["it"],
    }
    if same_as:
        schema["sameAs"] = same_as
    return schema


def breadcrumb_schema(base_url: str, crumbs: list[dict]) -> dict:
    items = []
    for i, crumb in enumerate(crumbs, start=1):
        url = crumb.get("url") or ""
        if url and not url.startswith("http"):
            url = f"{base_url}{url}"
        items.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": crumb.get("name", ""),
                "item": url or None,
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def article_schema(base_url: str, *, title: str, description: str, url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": f"{base_url}{url}",
        "inLanguage": "it-IT",
        "audience": ITALY_AUDIENCE,
        "publisher": {"@type": "Organization", "name": "The Verde", "url": base_url},
    }


def italia_article_schema(base_url: str, *, title: str, description: str, url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": f"{base_url}{url}",
        "inLanguage": "it-IT",
        "about": ITALY_PLACE,
        "spatialCoverage": ITALY_PLACE,
        "audience": ITALY_AUDIENCE,
        "publisher": {"@type": "Organization", "name": "The Verde", "url": base_url},
    }


def variety_schema(
    base_url: str,
    *,
    title: str,
    description: str,
    url: str,
    origin_slug: str = "",
    origin_label: str = "",
    brew_temp: float | int | None = None,
    brew_grams: float | int | None = None,
    brew_seconds: float | int | None = None,
    brew_infusions: str | None = None,
) -> dict:
    about: dict = {
        "@type": "Thing",
        "name": title.split("—")[0].strip() if "—" in title else title,
    }
    country = ORIGIN_COUNTRIES.get(origin_slug)
    if country:
        about["countryOfOrigin"] = country
    elif origin_label:
        about["description"] = f"Origine: {origin_label}"

    schema: dict = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": f"{base_url}{url}",
        "inLanguage": "it-IT",
        "about": about,
        "spatialCoverage": ITALY_PLACE,
        "audience": ITALY_AUDIENCE,
        "publisher": {"@type": "Organization", "name": "The Verde", "url": base_url},
    }
    brew_props = _brew_properties(
        temp=brew_temp,
        grams=brew_grams,
        seconds=brew_seconds,
        infusions=brew_infusions,
    )
    if brew_props:
        schema["additionalProperty"] = brew_props
    return schema


def quiz_faq_items(quiz: dict) -> list[dict]:
    """Extract FAQ pairs from quiz config for GEO (skips personality quizzes)."""
    items: list[dict] = []
    for q in quiz.get("questions") or []:
        if "correct" not in q or "explain" not in q:
            continue
        options = q.get("options") or []
        correct_idx = q.get("correct")
        if not isinstance(correct_idx, int) or correct_idx < 0 or correct_idx >= len(options):
            continue
        answer = f"{options[correct_idx]}. {q['explain']}"
        items.append({"question": q.get("q", ""), "answer": answer})
    return items


def learning_resource_schema(
    base_url: str,
    *,
    title: str,
    description: str,
    url: str,
    steps: list[dict],
) -> dict | None:
    if not steps:
        return None
    parts: list[dict] = []
    for step in steps:
        part: dict = {
            "@type": "LearningResource",
            "name": step.get("title") or step.get("slug", ""),
            "learningResourceType": step.get("type", "step"),
        }
        step_url = step.get("url")
        if step_url:
            part["url"] = _llms_abs(base_url, step_url)
        elif step.get("type") == "varieta":
            part["url"] = _llms_abs(base_url, f"/varieta/{step.get('slug', '')}/")
        parts.append(part)
    return {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": title,
        "description": description,
        "url": _llms_abs(base_url, url),
        "inLanguage": "it-IT",
        "audience": ITALY_AUDIENCE,
        "learningResourceType": "guided learning path",
        "teaches": "Tè verde (Camellia sinensis)",
        "hasPart": parts,
    }


def faq_schema(faqs: list[dict]) -> dict | None:
    if not faqs:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "inLanguage": "it-IT",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q["question"],
                "acceptedAnswer": {"@type": "Answer", "text": q["answer"]},
            }
            for q in faqs
        ],
    }


def defined_term_schema(base_url: str, *, name: str, description: str, url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": name,
        "description": description,
        "url": f"{base_url}{url}",
        "inLanguage": "it-IT",
        "inDefinedTermSet": f"{base_url}/glossario/",
    }


def build_sitemap_xml(entries: list[dict], *, hreflang: str = "it") -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for entry in entries:
        loc = xml_escape(entry["loc"])
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        if entry.get("lastmod"):
            lines.append(f"    <lastmod>{entry['lastmod']}</lastmod>")
        if entry.get("changefreq"):
            lines.append(f"    <changefreq>{entry['changefreq']}</changefreq>")
        if entry.get("priority") is not None:
            lines.append(f"    <priority>{entry['priority']:.1f}</priority>")
        lines.append(
            f'    <xhtml:link rel="alternate" hreflang="{hreflang}" href="{loc}"/>'
        )
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>')
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build_robots_txt(base_url: str) -> str:
    return (
        f"User-agent: *\n"
        f"Allow: /\n"
        f"Disallow: /diario/nuova/\n\n"
        f"Sitemap: {base_url}/sitemap.xml\n"
        f"# GEO: {base_url}/llms.txt\n"
    )


def _llms_abs(base_url: str, path: str) -> str:
    if path.startswith("http"):
        return path
    return f"{base_url.rstrip('/')}{path if path.startswith('/') else f'/{path}'}"


def _llms_brief(text: str, *, max_len: int = 110) -> str:
    text = " ".join((text or "").split())
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 1].rsplit(" ", 1)[0]
    return f"{cut}…"


def _llms_list(
    items: list[dict],
    *,
    base_url: str,
    title_key: str = "title",
    url_key: str = "url",
    brief_key: str = "description",
) -> str:
    lines: list[str] = []
    for item in items:
        title = item.get(title_key) or item.get("slug", "")
        url = item.get(url_key) or "/"
        brief = _llms_brief(item.get(brief_key) or item.get("brief") or "")
        if brief:
            lines.append(f"- [{title}]({_llms_abs(base_url, url)}): {brief}")
        else:
            lines.append(f"- [{title}]({_llms_abs(base_url, url)})")
    return "\n".join(lines)


def build_llms_txt(
    base_url: str,
    site_name: str,
    *,
    varieties: list[dict] | None = None,
    glossary: list[dict] | None = None,
    impara_topics: list[dict] | None = None,
    controversies: list[dict] | None = None,
    guides: list[dict] | None = None,
    italia_pages: list[dict] | None = None,
    paths: list[dict] | None = None,
    quizzes: list[dict] | None = None,
) -> str:
    """Machine-readable site summary for generative engines (llms.txt)."""
    varieties = varieties or []
    glossary = glossary or []
    impara_topics = impara_topics or []
    controversies = controversies or []
    guides = guides or []
    italia_pages = italia_pages or []
    paths = paths or []
    quizzes = quizzes or []

    query_map = [
        ("Cos'è il tè verde (Camellia sinensis)", "/glossario/camellia-sinensis/"),
        ("Come preparare il sencha", "/varieta/sencha/"),
        ("Differenza gyokuro e sencha", "/varieta/gyokuro/"),
        ("Cos'è lo shincha", "/varieta/shincha/"),
        ("Kabusecha: tra sencha e gyokuro", "/varieta/kabusecha/"),
        ("Quanta caffeina nel tè verde", "/impara/caffeina/"),
        ("Nilgiri verde vs Darjeeling verde", "/varieta/nilgiri-verde/"),
        ("Jeoncha tè verde coreano", "/varieta/jeoncha/"),
        ("Huang Shan Mao Feng preparazione", "/varieta/huangshan-maofeng/"),
        ("Matcha in Italia: cultura e uso", "/guide/matcha-italia/"),
        ("Tè verde e salute: cosa è dimostrato", "/impara/controversie/salute-scienza-vs-tradizione/"),
        ("Abbinamenti tè verde e cucina italiana", "/italia/abbinamenti/"),
        ("Cerimonia del tè: Cina vs Giappone", "/impara/controversie/cerimonia-cina-vs-giappone/"),
        ("Cos'è l'umami nel tè", "/glossario/umami/"),
        ("Tè verde o tisana: differenza", "/gioca/quiz/verde-vero/"),
        ("Temperatura acqua per ogni varietà", "/gioca/quiz/quale-temperatura/"),
        ("Primavera: shincha e raccolti", "/gioca/percorsi/primavera-in-tazza/"),
    ]
    query_lines = "\n".join(
        f"- {question} → {_llms_abs(base_url, path)}" for question, path in query_map
    )

    sections: list[str] = [
        f"# {site_name}",
        "",
        "> Cultura del tè verde (Camellia sinensis) per chi vive in Italia — non tisane, non hype detox.",
        "",
        f"{site_name} è un sito editoriale in italiano dedicato esclusivamente al tè verde "
        "(*Camellia sinensis*). Ogni pagina espone meta title, description, canonical, "
        "JSON-LD schema.org (Article, DefinedTerm, FAQPage, HowTo) e contestualizzazione per l'Italia.",
        "",
        "## Hub principali",
        "",
        f"- [Home]({_llms_abs(base_url, '/')}): punto di ingresso e navigazione tematica",
        f"- [Varietà]({_llms_abs(base_url, '/varieta/')}): schede sensoriali, parametri infusione, contesto italiano",
        f"- [Impara]({_llms_abs(base_url, '/impara/')}): storia, salute, cerimonia, preparazione, lavorazione",
        f"- [Glossario]({_llms_abs(base_url, '/glossario/')}): termini definiti (schema DefinedTerm)",
        f"- [In Italia]({_llms_abs(base_url, '/italia/')}): abbinamenti, stagioni, momenti della giornata",
        f"- [Guide]({_llms_abs(base_url, '/guide/')}): articoli long-form editoriali",
        f"- [Gioca]({_llms_abs(base_url, '/gioca/')}): percorsi guidati e quiz",
        f"- [Diario]({_llms_abs(base_url, '/diario/')}): registro personale infusioni (area utente, noindex)",
    ]

    if varieties:
        sections += ["", "## Varietà (schede complete)", "", _llms_list(varieties, base_url=base_url)]
    if glossary:
        sections += ["", "## Glossario (termini definiti)", "", _llms_list(glossary, base_url=base_url)]
    if impara_topics:
        sections += ["", "## Impara — temi", "", _llms_list(impara_topics, base_url=base_url)]
    if controversies:
        sections += [
            "",
            "## Controversie (prospettive multiple, E-E-A-T)",
            "",
            _llms_list(controversies, base_url=base_url),
        ]
    if guides:
        sections += ["", "## Guide", "", _llms_list(guides, base_url=base_url)]
    if italia_pages:
        sections += ["", "## In Italia", "", _llms_list(italia_pages, base_url=base_url)]
    if paths:
        path_items = [
            {
                "title": p.get("title", p.get("slug", "")),
                "url": f"/gioca/percorsi/{p.get('slug', '')}/",
                "description": p.get("description", ""),
            }
            for p in paths
        ]
        sections += ["", "## Gioca — percorsi guidati", "", _llms_list(path_items, base_url=base_url)]
    if quizzes:
        quiz_items = [
            {
                "title": q.get("title", q.get("slug", "")),
                "url": f"/gioca/quiz/{q.get('slug', '')}/",
                "description": q.get("description", ""),
            }
            for q in quizzes
        ]
        sections += ["", "## Gioca — quiz", "", _llms_list(quiz_items, base_url=base_url)]

    sections += [
        "",
        "## Entità chiave (disambiguazione)",
        "",
        "- **Tè verde** = foglia di *Camellia sinensis*, non ossidata — distinto da tisane (camomilla, menta, rooibos)",
        "- **Matcha** = tencha ombreggiato macinato; si beve la foglia intera in polvere",
        "- **Shincha** = primo raccolto primaverile giapponese (sencha giovane)",
        "- **Gyokuro / kabusecha / tencha** = scala di ombreggiatura giapponese",
        "- Fonti editoriali: manuali Pellegrino, Sommelier del tè, Rosen, Onuma, Hara (citati in bibliografia pagine)",
        "",
        "## Domande tipiche (dove trovare risposte)",
        "",
        query_lines,
        "",
        "## Formato e citazione",
        "",
        "- Lingua: italiano (it-IT); audience: appassionati di tè verde in Italia",
        "- Distingue sempre tè verde (Camellia sinensis) da tisane e infusi erboristici",
        "- Le varietà includono profilo sensoriale, parametri infusione (temperatura, dosaggio, tempi) e HowTo",
        "- Le controversie presentano prospettive multiple con fonti bibliografiche (E-E-A-T)",
        "- Per citare: usa title + URL canonico; preferisci estratti da FAQ, steps o definizioni glossario",
        "",
        "## Escluso dall'indice",
        "",
        f"- Ricerca interna: {_llms_abs(base_url, '/cerca/')} (noindex)",
        f"- Nuova infusione diario: {_llms_abs(base_url, '/diario/nuova/')} (noindex)",
        "",
        "## Discovery",
        "",
        f"- Sitemap: {_llms_abs(base_url, '/sitemap.xml')}",
        f"- RSS: {_llms_abs(base_url, '/feed.xml')}",
        f"- Robots: {_llms_abs(base_url, '/robots.txt')}",
        "",
        "## Legale",
        "",
        f"- [Privacy]({_llms_abs(base_url, '/privacy/')})",
        f"- [Termini]({_llms_abs(base_url, '/termini/')})",
        "",
    ]
    return "\n".join(sections)

