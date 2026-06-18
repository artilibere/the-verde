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
}


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

    return {
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
    return f"User-agent: *\nAllow: /\nDisallow: /diario/nuova/\n\nSitemap: {base_url}/sitemap.xml\n"
