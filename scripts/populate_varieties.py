#!/usr/bin/env python3
"""Enrich variety JSON files with deep sections, leads, FAQ, explore_next, fonti."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAR_DIR = ROOT / "content" / "varieta"

ENRICHMENT: dict[str, dict] = {
    "bancha": {
        "lead": "Il bancha non chiede attenzione da sommelier: è il verde della frigo in bottiglia, del pomeriggio pigro, della foglia matura che sa di fieno e cielo aperto.",
        "cultivar": "Yabukita e cultivar locali",
        "deep_title": "Lavorazione e quotidianità",
        "deep_text": "Raccolto tardivo o da foglie più grandi, fissato al vapore e essiccato con meno enfasi sul pregio estetico del sencha. In Giappone convive con il matcha cerimoniale senza contraddizione: pane quotidiano e occasione speciale nella stessa cultura.",
        "faq_extra": ("È adatto ai bambini?", "Bassa caffeina e morbidezza lo rendono tra i verdi più accessibili; attenzione solo a temperature non eccessive."),
        "errors_extra": ["Snobismo verso il bancha come tè «povero»"],
        "explore_next": [
            ("Kukicha", "/varieta/kukicha/", "ancora più leggero"),
            ("Glossario bancha", "/glossario/bancha/", "definizione"),
            ("Colazione", "/italia/momenti/colazione/", "momento italiano"),
        ],
        "fonti": ["onuma, consumo quotidiano", "pellegrino, verdi giapponesi", "rosen, lavorazione bancha"],
    },
    "sencha": {
        "lead": "Ago verdi, profumo di erba tagliata al mattino: il sencha è il battito cardiaco del tè giapponese.",
        "cultivar": "Yabukita (dominante in Giappone)",
        "deep_title": "Dal sole alla tazza",
        "deep_text": "Foglie esposte al sole, fissate al vapore in pochi secondi, arrotolate in aghi. Ogni regione — Shizuoka, Uji, Kyushu — modula marinezza e amaro. Lo shincha è il suo primo raccolto primaverile, più vivido e effimero.",
        "faq_extra": ("Sencha e gyokuro: differenza?", "Stessa pianta: il gyokuro è ombreggiato prima del raccolto; il sencha cresce al sole ed è più vegetale e accessibile."),
        "errors_extra": ["Usare la stessa temperatura del gyokuro (troppo fredda, tazza piatta)"],
        "explore_next": [
            ("Gyokuro", "/varieta/gyokuro/", "passo successivo umami"),
            ("Glossario sencha", "/glossario/sencha/", "termine"),
            ("Percorso bancha→matcha", "/gioca/percorsi/dal-bancha-al-matcha/", "tappa 2"),
        ],
        "fonti": ["pellegrino, pp. 123–125", "sommelier, scheda sencha", "rosen, lavorazione sencha"],
    },
    "gyokuro": {
        "lead": "Il gyokuro non si beve di fretta. È ombra, seta e brodo vegetale: un verde che chiede acqua tiepida e un minuto di silenzio.",
        "cultivar": "Yabukita, Okumidori (ombreggiati)",
        "deep_title": "Ombreggiatura",
        "deep_text": "Tre settimane sotto reti prima del raccolto: la pianta produce più clorofilla e L-teanina, meno catechine amare. Da foglie ombreggiate non arrotolate nasce il tencha, base del matcha.",
        "faq_extra": ("Quante infusioni?", "Due o tre con tempi leggermente crescenti; dosaggio generoso (4 g / 100 ml)."),
        "errors_extra": ["Trattarlo come sencha (temperatura e dosaggio sbagliati)"],
        "explore_next": [
            ("Matcha", "/varieta/matcha/", "stessa filiera ombra"),
            ("Umami", "/glossario/umami/", "gusto chiave"),
            ("Pausa", "/italia/momenti/pausa/", "momento consigliato"),
        ],
        "fonti": ["sommelier, scheda gyokuro", "pellegrino, verdi giapponesi", "onuma, quotidianità vs Chado"],
    },
    "matcha": {
        "lead": "Polvere verde brillante, schiuma fine: nel matcha bevi la foglia intera, non un infusionato. È gesto, colore, corpo denso.",
        "cultivar": "Tencha ombreggiato macinato",
        "deep_title": "Tencha e cerimonia",
        "deep_text": "Foglie ombreggiate, venature rimosse, macinate in pietra. Usucha per la cerimonia quotidiana, koicha per incontri formali. Il matcha da cucina e da latte non sostituisce il grado cerimoniale.",
        "faq_extra": ("Matcha in pasticceria italiana?", "Valido come ingrediente se la polvere è di qualità; diverso dal matcha zuccherato da supermercato."),
        "errors_extra": ["Frullare con latte freddo senza setacciare (grumi)", "Confondere culinary grade e cerimoniale"],
        "explore_next": [
            ("Chasen", "/glossario/chasen/", "strumento"),
            ("Chanoyu", "/glossario/chanoyu/", "rito"),
            ("Cucina", "/impara/cucina/", "ricette"),
        ],
        "fonti": ["rosen, lavorazione matcha", "onuma, matcha e cucina", "pellegrino, matcha"],
    },
    "genmaicha": {
        "lead": "Riso tostato e foglia verde insieme: il genmaicha profuma di padella e comfort, come pane caldo in una giornata uggiosa.",
        "cultivar": "Bancha o sencha + riso mochi tostato",
        "deep_title": "Blend e storia",
        "deep_text": "Nato come tè economico che allungava la foglia con cereale; oggi è scelta voluta per profilo nocciola e bassa caffeina. Il riso non è decorazione: modella corpo e dolcezza.",
        "faq_extra": ("Si sente il riso in bocca?", "Sì: note tostate e cereali convivono con il verde, senza coprirlo del tutto."),
        "errors_extra": ["Infusione troppo lunga (amaro dal riso bruciato in tazza)"],
        "explore_next": [
            ("Bancha", "/varieta/bancha/", "base comune"),
            ("Inverno", "/italia/stagioni/inverno/", "stagione ideale"),
            ("Glossario genmaicha", "/glossario/genmaicha/", "definizione"),
        ],
        "fonti": ["onuma, ricette", "pellegrino, varietà", "rosen, cucina"],
    },
    "hojicha": {
        "lead": "Foglie ambrate, profumo di nocciola tostata: l'hojicha è il verde che la sera non ti sveglia.",
        "cultivar": "Bancha o kukicha tostati",
        "deep_title": "Tostatura",
        "deep_text": "Passaggio al calore trasforma colore e chimica: caffeina ridotta, note caramellate. In Giappone si beve anche freddo in estate. Non è tè nero: parte sempre da verde.",
        "faq_extra": ("Hojicha e sonno?", "Bassa caffeina; adatto dopo cena, ma la sensibilità personale conta."),
        "errors_extra": ["Confonderlo con tè nero", "Acqua bollente prolungata (amarezza tostata)"],
        "explore_next": [
            ("Dopo cena", "/italia/momenti/dopo-cena/", "momento IT"),
            ("Kukicha", "/varieta/kukicha/", "alternativa leggera"),
            ("Caffeina", "/impara/caffeina/", "contenuti"),
        ],
        "fonti": ["pellegrino, verdi giapponesi", "rosen, lavorazione"],
    },
    "kukicha": {
        "lead": "Steli e fogli in miniatura: il kukicha è dolce, leggero, onesto — il tè che non pretende di essere pregiato per farsi amare.",
        "cultivar": "Steli e fogli di sencha o gyokuro",
        "deep_title": "Economia della pianta",
        "deep_text": "Usa parti spesso scartate nella selezione premium. Bassa caffeina, prezzo accessibile, sapore pulito. Ideale per introdurre palati italiani al verde senza amaro.",
        "faq_extra": ("Si vede la differenza col sencha?", "Sì: pezzi di ramo, infusione più chiara, meno marinezza."),
        "errors_extra": ["Dosaggio da sencha premium (troppo concentrato)"],
        "explore_next": [
            ("Bancha", "/varieta/bancha/", "alternativa"),
            ("Glossario kukicha", "/glossario/kukicha/", "termine"),
            ("Prima infusione", "/impara/preparazione/", "basilari"),
        ],
        "fonti": ["pellegrino, verdi giapponesi"],
    },
    "dragon-well": {
        "lead": "Foglie piattate a piastra, liquore verde-giallo: il Long Jing sa di nocciola fresca e fagiolini appena scottati.",
        "cultivar": "Longjing #43 e cultivar di West Lake",
        "deep_title": "Pan-firing a Hangzhou",
        "deep_text": "Fissazione in wok, pressatura a mano, forma piatta iconica. Il terroir di Zhejiang imprime dolcezza e burro vegetale. Primavera è stagione d'eccellenza.",
        "faq_extra": ("Dragon Well e Long Jing?", "Stesso tè: nome cinese Long Jing, traduzione Dragon Well."),
        "errors_extra": ["Acqua troppo calda che appiattisce il profilo", "Infusione in teiera piccola senza spazio per foglia piatta"],
        "explore_next": [
            ("Bi Luo Chun", "/varieta/bi-luo-chun/", "altra primavera cinese"),
            ("Glossario Long Jing", "/glossario/longjing/", "termine"),
            ("Primavera", "/italia/stagioni/primavera/", "stagione"),
        ],
        "fonti": ["sommelier, Lung Ching", "pellegrino, Long Jing"],
    },
    "gunpowder": {
        "lead": "Perle di foglia che rotolano in tazza: il gunpowder è robusto, legnoso, indulgente — il verde che ha attraversato i mari.",
        "cultivar": "Zhucha, cultivar locali",
        "deep_title": "Zhu Cha",
        "deep_text": "Rolling compatto per conservazione e export. Regge temperature leggermente più alte del sencha delicato. Infusioni ripetute in teiera grande.",
        "faq_extra": ("Perché «gunpowder»?", "Nome occidentale per la forma a pallottola; in Cina è zhu cha, tè perla."),
        "errors_extra": ["Trattarlo come bi luo chun delicato"],
        "explore_next": [
            ("Wok", "/glossario/wok/", "lavorazione"),
            ("Autunno", "/italia/stagioni/autunno/", "stagione"),
            ("Storia", "/impara/storia-cultura/", "commercio"),
        ],
        "fonti": ["pellegrino, verdi cinesi", "rosen, storia export"],
    },
    "bi-luo-chun": {
        "lead": "Spirali verdi come conchiglie minuscole: il bi luo chun profuma di frutta bianca e fiori di primavera.",
        "cultivar": "Cultivar di Dongting, Jiangsu",
        "deep_title": "Raccolto primaverile",
        "deep_text": "Foglie a spirale raccolte presto, spesso in vigneti con pesche (tradizione locale). Profilo floreale delicato: gaiwan e acqua a 75 °C, non ebollizione.",
        "faq_extra": ("Perché spirali?", "Rolling artistico che protegge aromi volatili e rallenta infusione."),
        "errors_extra": ["Troppa foglia in tazza (amaro floreale)", "Acqua dell'ebollitore"],
        "explore_next": [
            ("Dragon Well", "/varieta/dragon-well/", "confronto cinese"),
            ("Gaiwan", "/glossario/gaiwan/", "strumento"),
            ("Degustazione", "/impara/degustazione/", "metodo"),
        ],
        "fonti": ["pellegrino, Bi Lo Chun", "sommelier, degustazione"],
    },
    "darjeeling-verde": {
        "lead": "Muschio di sentiero dopo pioggia, nebbia in quota: il Darjeeling verde non assomiglia al muscat del Darjeeling nero.",
        "cultivar": "Cultivar dell'Himalaya (AV2, ecc.)",
        "deep_title": "Verde di montagna",
        "deep_text": "Raro rispetto al nero della stessa regione. Lavorazione che preserva freschezza vegetale e mineralità. Per palati abituati a vini bianchi strutturati.",
        "faq_extra": ("È lo stesso Darjeeling che conosco?", "Stessa regione, altra lavorazione: profilo completamente diverso."),
        "errors_extra": ["Aspettarsi muscat tipico del nero", "Infusione troppo breve per foglia intrecciata"],
        "explore_next": [
            ("Degustazione", "/impara/degustazione/", "scheda sensoriale"),
            ("Storia India", "/impara/storia-cultura/", "contesto"),
            ("Glossario Darjeeling", "/glossario/darjeeling/", "termine"),
        ],
        "fonti": ["pellegrino, contesto indiano", "sommelier, Nilgiri verde"],
    },
    "cold-brew-gyokuro": {
        "lead": "Ore in frigo, umami dolce senza amaro: il cold brew gyokuro è estate in un bicchiere, lento e trasparente.",
        "cultivar": "Gyokuro ombreggiato",
        "deep_title": "Estrazione fredda",
        "deep_text": "5 g per 500 ml, 4–8 ore a 4 °C. Estrae aminoacidi e zuccheri con poche catechine amare. Alternativa italiana alle bibite zuccherate estive.",
        "faq_extra": ("Posso freddare un gyokuro caldo?", "Profilo diverso: il cold brew dall'inizio è più dolce e pulito."),
        "errors_extra": ["Ore insufficienti (acqua insipida)", "Usare foglia non fresca"],
        "explore_next": [
            ("Gyokuro", "/varieta/gyokuro/", "stessa foglia calda"),
            ("Estate", "/italia/stagioni/estate/", "contesto IT"),
            ("Aperitivo", "/italia/momenti/aperitivo/", "momento"),
        ],
        "fonti": ["pellegrino, preparazione", "onuma, estate"],
    },
}


def p(text: str) -> dict:
    return {"type": "paragraph", "spans": [{"type": "text", "value": text}]}


def h2(text: str) -> dict:
    return {"type": "heading", "level": 2, "spans": [{"type": "text", "value": text}]}


def enrich_variety(doc: dict, data: dict) -> dict:
    slug = doc["slug"]
    blocks = doc["body"]["blocks"]

    # Lead paragraph first
    lead = p(data["lead"])
    if blocks and blocks[0].get("type") == "paragraph":
        blocks[0] = lead
    else:
        blocks.insert(0, lead)

    # taxonomy cultivar
    if data.get("cultivar"):
        doc["taxonomy"]["cultivar"] = data["cultivar"]

    # errors: ensure 3+
    for b in blocks:
        if b.get("type") == "errors":
            existing = set(b["items"])
            for e in data.get("errors_extra", []):
                if e not in existing:
                    b["items"].append(e)

    # faq: add second item
    for b in blocks:
        if b.get("type") == "faq":
            q, a = data["faq_extra"]
            if not any(it["question"] == q for it in b["items"]):
                b["items"].append(
                    {"question": q, "answer_spans": [{"type": "text", "value": a}]}
                )

    # deep section + fonti
    deep = {
        "type": "level_section",
        "level": "deep",
        "blocks": [
            h2(data["deep_title"]),
            p(data["deep_text"]),
            h2("Fonti"),
            {
                "type": "list",
                "ordered": False,
                "items": [{"spans": [{"type": "text", "value": f}]} for f in data["fonti"]],
            },
        ],
    }
    # Insert before related_links if present, else append
    idx = next((i for i, b in enumerate(blocks) if b.get("type") == "related_links"), len(blocks))
    blocks.insert(idx, deep)

    # explore_next
    doc["navigation"]["explore_next"] = [
        {"name": n, "url": u, "reason": r} for n, u, r in data["explore_next"]
    ]

    return doc


def main() -> None:
    for slug, data in ENRICHMENT.items():
        path = VAR_DIR / f"{slug}.json"
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc = enrich_variety(doc, data)
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Enriched {slug}")
    print(f"Done: {len(ENRICHMENT)} varieties")


if __name__ == "__main__":
    main()
