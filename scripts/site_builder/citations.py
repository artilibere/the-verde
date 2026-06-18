"""Canonical bibliography entries aligned with books/knowledge-base.json."""

from __future__ import annotations

import re
from typing import Any

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

def fonte_autore(fonte_id: str) -> str:
    """Display name for a KB book id in prospettive / citazioni."""
    book = BOOKS.get(fonte_id.strip().lower())
    if book:
        return book["author"]
    return fonte_id.replace("-", " ").strip().title()


def enrich_position_items(items: list[dict]) -> list[dict]:
    """Add autore label while keeping fonte id for polls and cite."""
    return [
        {**pos, "autore": fonte_autore(pos.get("fonte", ""))}
        for pos in items
    ]


# tema_id → (book_id, sotto_tema, pages)
TEMA_REF: dict[str, tuple[str, str, str | None]] = {
    "rosen-poesia": ("rosen", "Poesia e filosofia del tè verde", "97–189"),
    "rosen-storia": ("rosen", "Storia e tradizioni del tè verde", "47–51"),
    "rosen-lavorazione": ("rosen", "Lavorazione e varietà", "1575–1592"),
    "rosen-preparazione": ("rosen", "Acquisto, conservazione e preparazione", "2300–2448"),
    "rosen-salute": ("rosen", "Salute e benessere", "2714–2838"),
    "rosen-bellezza-cucina": ("rosen", "Bellezza e cucina", "57–58"),
    "sommelier-storia": ("sommelier", "Storia e cultura del tè", "190–200"),
    "sommelier-produzione-verde": ("sommelier", "Produzione del tè verde", None),
    "sommelier-degustazione": ("sommelier", "Analisi sensoriale e varietà", None),
    "sommelier-proprieta": ("sommelier", "Proprietà chimiche e salute", None),
    "sommelier-cerimonie": ("sommelier", "Cerimonie e galateo", "4358"),
    "pellegrino-pianta": ("pellegrino", "Coltivazione e lavorazione", "15–33"),
    "pellegrino-lavorazione": ("pellegrino", "Coltivazione e lavorazione", "20–27"),
    "pellegrino-via-del-te": ("pellegrino", "La via del tè: acqua, teiere e preparazione", "45–69"),
    "pellegrino-tradizioni": ("pellegrino", "Tradizioni mondiali del tè verde", "85–93"),
    "pellegrino-salute": ("pellegrino", "Il tè verde e la salute", "2811–3058"),
    "pellegrino-varietà": ("pellegrino", "Varietà di tè verde", "76–128"),
    "onuma-vincolo": ("onuma", "Legame personale e familiare con il tè verde", "108–172"),
    "onuma-storia": ("onuma", "Storia del tè verde in Giappone", "179–198"),
    "onuma-cerimonia": ("onuma", "Cerimonia e protocollo del tè verde", "15–22"),
    "onuma-salute-pratica": ("onuma", "Proprietà e consumo consapevole", "1202–1348"),
    "onuma-matcha-cucina": ("onuma", "Matcha, pelle e riuso", "23–24"),
    "hara-panoramica": ("hara", "Prospettiva scientifica globale", "71–89"),
    "hara-anticancer": ("hara", "Effetti anticancerogeni", "102–113"),
    "hara-metabolismo": ("hara", "Obesità, metabolismo e cuore", "118–131"),
    "hara-altri-effetti": ("hara", "Immunità, fegato, cervello e oral health", "136–171"),
}

# Legacy free-text citation → (book_id, tema, sotto_tema, pages)
LEGACY_CITATIONS: dict[str, tuple[str, str, str, str | None]] = {
    "hara, temi salute": ("hara", "hara-panoramica", "Prospettiva scientifica globale", "71–89"),
    "hara, trial EGCG": ("hara", "hara-anticancer", "Trial clinici e sviluppo farmaci", "113"),
    "hara, catechine": ("hara", "hara-panoramica", "Biodisponibilità dei polifenoli", "89"),
    "hara, catechine e foglia intera": ("hara", "hara-panoramica", "Caratteristiche del tè verde giapponese", "74"),
    "rosen, integratori": ("rosen", "rosen-salute", "Integratori vs bevanda", "2807–2819"),
    "rosen, cucina e bellezza": ("rosen", "rosen-bellezza-cucina", "Ricette con tè verde in cucina", "57–58"),
    "rosen, cucina": ("rosen", "rosen-bellezza-cucina", "Ricette con tè verde in cucina", "57–58"),
    "rosen, lavorazione bancha": ("rosen", "rosen-lavorazione", "Lavorazione di Bancha e Sencha", "1592"),
    "rosen, lavorazione sencha": ("rosen", "rosen-lavorazione", "Lavorazione di Bancha e Sencha", "1592"),
    "rosen, lavorazione matcha": ("rosen", "rosen-lavorazione", "Lavorazione del Matcha", "1585"),
    "rosen, lavorazione": ("rosen", "rosen-lavorazione", "Lavorazione e varietà", "1575–1592"),
    "rosen, storia export": ("rosen", "rosen-storia", "Tè verde in India e Sri Lanka", "50–171"),
    "rosen, stagionalità": ("rosen", "rosen-lavorazione", "Lavorazione e varietà", "1575–1592"),
    "rosen, estetica foglia": ("rosen", "rosen-poesia", "La foglia come oggetto estetico", "146–151"),
    "rosen, teiere Yixing": ("rosen", "rosen-preparazione", "Teiere Yixing e cura degli utensili", "2300–2351"),
    "rosen, poesia": ("rosen", "rosen-poesia", "Poesia e filosofia del tè verde", "97–189"),
    "rosen, storia e diffusione del tè": ("rosen", "rosen-storia", "Storia e tradizioni del tè verde", "47–51"),
    "rosen, usi pratici e estetica della foglia": ("rosen", "rosen-poesia", "La foglia come oggetto estetico", "146–151"),
    "rosen, pp. 47–51": ("rosen", "rosen-storia", "Scoperta e miti (Shen Nong, Bodhidharma)", "47–51"),
    "pellegrino, chanoyu": ("pellegrino", "pellegrino-tradizioni", "Chanoyu giapponese: koicha e usucha", "91–93"),
    "pellegrino, matcha": ("pellegrino", "pellegrino-varietà", "Tè verde e cucina (Matcha, kombucha)", "76–81"),
    "pellegrino, preparazione": ("pellegrino", "pellegrino-via-del-te", "Tè freddo e conservazione foglie", "69"),
    "pellegrino, via del tè": ("pellegrino", "pellegrino-via-del-te", "La via del tè: acqua, teiere e preparazione", "45–69"),
    "pellegrino, salute": ("pellegrino", "pellegrino-salute", "Il tè verde e la salute", "2811–3058"),
    "pellegrino, prevenzione": ("pellegrino", "pellegrino-salute", "Sistema cardiovascolare e colesterolo", "2907–2924"),
    "pellegrino, lavorazione": ("pellegrino", "pellegrino-pianta", "Fermentazione o ossidazione?", "20–27"),
    "pellegrino, varietà": ("pellegrino", "pellegrino-varietà", "Varietà di tè verde", "112–128"),
    "pellegrino, schede varietà": ("pellegrino", "pellegrino-varietà", "Schede tecniche varietali", "112–128"),
    "pellegrino, verdi giapponesi": ("pellegrino", "pellegrino-varietà", "Verdi giapponesi (Sencha, Matcha, Gyokuro, Bancha…)", "123–128"),
    "pellegrino, verdi giapponesi e matcha": ("pellegrino", "pellegrino-varietà", "Verdi giapponesi (Sencha, Matcha, Gyokuro, Bancha…)", "123–128"),
    "pellegrino, verdi cinesi": ("pellegrino", "pellegrino-varietà", "Verdi cinesi (Long Jing, Bi Lo Chun, Gunpowder…)", "112–122"),
    "pellegrino, cinesi": ("pellegrino", "pellegrino-varietà", "Verdi cinesi (Long Jing, Bi Lo Chun, Gunpowder…)", "112–122"),
    "pellegrino, Long Jing": ("pellegrino", "pellegrino-varietà", "Verdi cinesi (Long Jing, Bi Lo Chun, Gunpowder…)", "112–122"),
    "pellegrino, Bi Lo Chun": ("pellegrino", "pellegrino-varietà", "Verdi cinesi (Long Jing, Bi Lo Chun, Gunpowder…)", "112–122"),
    "pellegrino, tradizioni": ("pellegrino", "pellegrino-tradizioni", "Tradizioni mondiali del tè verde", "85–93"),
    "pellegrino, tradizioni mondiali": ("pellegrino", "pellegrino-tradizioni", "Tradizioni mondiali del tè verde", "85–2727"),
    "pellegrino, teiere": ("pellegrino", "pellegrino-via-del-te", "Teiere Yixing e manutenzione", "50–62"),
    "pellegrino, servizio": ("pellegrino", "pellegrino-via-del-te", "La via del tè: acqua, teiere e preparazione", "45–69"),
    "pellegrino, contesto indiano": ("pellegrino", "pellegrino-pianta", "Zone di coltivazione mondiali", "33"),
    "pellegrino, cultura del tè in Occidente": ("pellegrino", "pellegrino-tradizioni", "Tradizioni mondiali del tè verde", "85–2727"),
    "pellegrino, Giappone": ("pellegrino", "pellegrino-tradizioni", "Chanoyu giapponese: koicha e usucha", "91–93"),
    "pellegrino, pp. 45–52": ("pellegrino", "pellegrino-pianta", "La pianta del tè e la raccolta", "15–17"),
    "pellegrino, pp. 123–125": ("pellegrino", "pellegrino-varietà", "Verdi giapponesi (Sencha, Matcha, Gyokuro, Bancha…)", "123–128"),
    "sommelier, degustazione": ("sommelier", "sommelier-degustazione", "Analisi sensoriale e varietà", None),
    "sommelier, scheda sencha": ("sommelier", "sommelier-degustazione", "Scheda sensoriale Sencha", None),
    "sommelier, scheda gyokuro": ("sommelier", "sommelier-degustazione", "Scheda sensoriale Gyokuro", None),
    "sommelier, cerimonie": ("sommelier", "sommelier-cerimonie", "Cerimonie e galateo", "4358"),
    "sommelier, gong fu": ("sommelier", "sommelier-cerimonie", "Cerimonie del tè", None),
    "sommelier, servizio": ("sommelier", "sommelier-degustazione", "Servizio e degustazione", None),
    "sommelier, produzione": ("sommelier", "sommelier-produzione-verde", "Produzione del tè verde", None),
    "sommelier, proprietà": ("sommelier", "sommelier-proprieta", "Proprietà chimiche e salute", None),
    "sommelier, proprieta": ("sommelier", "sommelier-proprieta", "Proprietà chimiche e salute", None),
    "sommelier, Lung Ching": ("sommelier", "sommelier-degustazione", "Scheda sensoriale Lung Ching (Dragon Well)", None),
    "sommelier, Nilgiri": ("sommelier", "sommelier-degustazione", "Scheda sensoriale Nilgiri verde", None),
    "sommelier, Nilgiri verde": ("sommelier", "sommelier-degustazione", "Scheda sensoriale Nilgiri verde", None),
    "sommelier, commercio e rituali": ("sommelier", "sommelier-storia", "Storia e cultura del tè", "190–200"),
    "onuma, cerimonia": ("onuma", "onuma-cerimonia", "Cerimonia e protocollo del tè verde", "15–22"),
    "onuma, consumo quotidiano": ("onuma", "onuma-vincolo", "Rituale quotidiano in famiglia", "108–131"),
    "onuma, quotidianità": ("onuma", "onuma-vincolo", "Rituale quotidiano in famiglia", "108–131"),
    "onuma, quotidianita": ("onuma", "onuma-vincolo", "Rituale quotidiano in famiglia", "108–131"),
    "onuma, quotidianità vs Chado": ("onuma", "onuma-vincolo", "Rituale quotidiano in famiglia", "108–131"),
    "onuma, estate": ("onuma", "onuma-salute-pratica", "Tè prima dello sport, prima di dormire, a digiuno", "1202–1241"),
    "onuma, ricette": ("onuma", "onuma-matcha-cucina", "Ricette con matcha", "24"),
    "onuma, ricette matcha": ("onuma", "onuma-matcha-cucina", "Ricette con matcha", "24"),
    "onuma, matcha": ("onuma", "onuma-matcha-cucina", "Matcha, pelle e riuso", "23–24"),
    "onuma, matcha e cucina": ("onuma", "onuma-matcha-cucina", "Matcha, pelle e riuso", "23–24"),
    "onuma, matcha in cucina e quotidianità": ("onuma", "onuma-matcha-cucina", "Matcha, pelle e riuso", "23–24"),
    "onuma, mg caffeina": ("onuma", "onuma-salute-pratica", "Contenuto caffeina per varietà", "1267–1275"),
    "onuma, varieta": ("onuma", "onuma-salute-pratica", "Contenuto caffeina per varietà", "1267–1275"),
    "onuma, riconoscere qualità": ("onuma", "onuma-salute-pratica", "Come riconoscere un buon tè verde", "1312–1348"),
    "onuma, preparazione quotidiana": ("onuma", "onuma-cerimonia", "Cerimonia e protocollo del tè verde", "15–22"),
    "onuma, cultura quotidiana": ("onuma", "onuma-vincolo", "Rituale quotidiano in famiglia", "108–131"),
    "onuma, adozione contemporanea": ("onuma", "onuma-vincolo", "Takeko's Tea: dal ricordo al progetto imprenditoriale", "165–172"),
}

_TEMA_RE = re.compile(r"^(\w+),\s*tema\s+([\w-]+)$", re.I)
_PAGES_RE = re.compile(r"^(\w+),\s*pp\.\s*(.+)$", re.I)
_TRECCANI_RE = re.compile(r"^Treccani\s*—\s*(.+)$", re.I)


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


def bib_treccani(voce: str) -> dict:
    return {
        "author": "Treccani",
        "title": "Enciclopedia on line",
        "tema": "treccani",
        "sotto_tema": f"voce «{voce.strip()}»",
        "pages": None,
        "kb_ref": "https://www.treccani.it",
    }


def bibliography_block(items: list[dict]) -> dict:
    return {"type": "bibliography", "items": items}


def is_kb_bibliography_entry(item: dict) -> bool:
    """True for internal KB entries — excluded from public bibliography."""
    if item.get("kb_ref") == "books/knowledge-base.json":
        return True
    return (
        item.get("author") == "The Verde"
        and item.get("title") == "Knowledge base sul tè verde"
    )


def legacy_to_bib_entry(
    text: str,
    *,
    slug: str | None = None,
    doc_type: str | None = None,
) -> dict | None:
    """Convert a legacy Fonti bullet to a structured bibliography entry."""
    raw = text.strip()
    if not raw:
        return None

    if raw in LEGACY_CITATIONS:
        book_id, tema, sotto, pages = LEGACY_CITATIONS[raw]
        if book_id == "_kb":
            return None
        return bib_item(book_id, tema, sotto, pages)

    m = _TEMA_RE.match(raw)
    if m:
        book_id, tema = m.group(1), m.group(2)
        if tema in TEMA_REF:
            _, sotto, pages = TEMA_REF[tema]
            return bib_item(book_id, tema, sotto, pages)
        return bib_item(book_id, tema, tema.replace("-", " "), None)

    m = _PAGES_RE.match(raw)
    if m:
        book_id, pages = m.group(1), m.group(2).strip()
        tema_guess = {
            "pellegrino": "pellegrino-varietà",
            "rosen": "rosen-storia",
        }.get(book_id, f"{book_id}-panoramica")
        if tema_guess in TEMA_REF:
            _, sotto, _ = TEMA_REF[tema_guess]
            return bib_item(book_id, tema_guess, sotto, pages)
        return bib_item(book_id, tema_guess, f"Riferimento pagine {pages}", pages)

    m = _TRECCANI_RE.match(raw)
    if m:
        return bib_treccani(m.group(1))

    # Skip non-citation prose accidentally listed under Fonti
    if len(raw) > 120 or raw.count(".") > 2:
        return None

    return None


def _is_fonti_heading(block: dict) -> bool:
    if block.get("type") != "heading":
        return False
    spans = block.get("spans", [])
    if not spans:
        return False
    return spans[0].get("value", "").strip().lower() == "fonti"


def _list_item_texts(list_block: dict) -> list[str]:
    texts: list[str] = []
    for item in list_block.get("items", []):
        parts = [s.get("value", "") for s in item.get("spans", []) if s.get("type") == "text"]
        joined = "".join(parts).strip()
        if joined:
            texts.append(joined)
    return texts


def transform_fonti_blocks(
    blocks: list[dict],
    *,
    slug: str | None = None,
    doc_type: str | None = None,
) -> list[dict]:
    """Replace Fonti heading+list pairs with bibliography blocks."""
    out: list[dict] = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block.get("type") == "level_section":
            out.append(
                {
                    **block,
                    "blocks": transform_fonti_blocks(
                        block.get("blocks", []),
                        slug=slug,
                        doc_type=doc_type,
                    ),
                }
            )
            i += 1
            continue

        if (
            _is_fonti_heading(block)
            and i + 1 < len(blocks)
            and blocks[i + 1].get("type") == "list"
        ):
            texts = _list_item_texts(blocks[i + 1])
            items: list[dict] = []
            seen: set[str] = set()
            for text in texts:
                entry = legacy_to_bib_entry(text, slug=slug, doc_type=doc_type)
                if entry is None:
                    continue
                key = f"{entry['author']}|{entry['tema']}|{entry['sotto_tema']}"
                if key in seen:
                    continue
                seen.add(key)
                items.append(entry)

            if items:
                out.append(bibliography_block(items))
            i += 2
            continue

        if block.get("type") == "bibliography":
            items = [
                item
                for item in block.get("items", [])
                if not is_kb_bibliography_entry(item)
            ]
            if items:
                out.append({**block, "items": items})
            i += 1
            continue

        out.append(block)
        i += 1

    return out


def migrate_document(doc: dict) -> dict:
    slug = doc.get("slug")
    doc_type = doc.get("type")
    body = doc.get("body", {})
    blocks = body.get("blocks", [])
    if not blocks:
        return doc
    new_blocks = sanitize_bibliography_blocks(
        transform_fonti_blocks(blocks, slug=slug, doc_type=doc_type)
    )
    if new_blocks != blocks:
        doc = {**doc, "body": {**body, "blocks": new_blocks}}
    return doc


def sanitize_bibliography_blocks(blocks: list[dict]) -> list[dict]:
    """Drop internal KB entries from bibliography blocks."""
    out: list[dict] = []
    for block in blocks:
        if block.get("type") == "level_section":
            out.append(
                {
                    **block,
                    "blocks": sanitize_bibliography_blocks(block.get("blocks", [])),
                }
            )
        elif block.get("type") == "bibliography":
            items = [
                item
                for item in block.get("items", [])
                if not is_kb_bibliography_entry(item)
            ]
            if items:
                out.append({**block, "items": items})
        else:
            out.append(block)
    return out
