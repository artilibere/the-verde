#!/usr/bin/env python3
"""Populate guide articles with rich editorial content (the-verde-expert voice)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "content" / "guide"


def p(text: str) -> dict:
    return {"type": "paragraph", "spans": [{"type": "text", "value": text}]}


def h2(text: str) -> dict:
    return {"type": "heading", "level": 2, "spans": [{"type": "text", "value": text}]}


def li(text: str) -> dict:
    return {"spans": [{"type": "text", "value": text}]}


def ul(items: list[str], ordered: bool = False) -> dict:
    return {"type": "list", "ordered": ordered, "items": [li(x) for x in items]}


def links(items: list[tuple[str, str, str]]) -> dict:
    return {
        "type": "related_links",
        "items": [{"name": n, "url": u, "reason": r} for n, u, r in items],
    }


def faq_block(items: list[tuple[str, str]]) -> dict:
    return {
        "type": "faq",
        "items": [
            {"question": q, "answer_spans": [{"type": "text", "value": a}]} for q, a in items
        ],
    }


def fonti(items: list[str]) -> list[dict]:
    return [h2("Fonti"), ul(items)]


def guide_doc(
    slug: str,
    title: str,
    description: str,
    keywords: list[str],
    published: str,
    intro_paras: list[str],
    deep_blocks: list[dict],
    tema_kb: list[str],
    explore_next: list[tuple[str, str, str]],
    extra_root_blocks: list[dict] | None = None,
) -> dict:
    blocks: list[dict] = [
        {"type": "level_section", "level": "intro", "blocks": [p(x) for x in intro_paras]},
        {"type": "level_section", "level": "deep", "blocks": deep_blocks},
    ]
    if extra_root_blocks:
        blocks.extend(extra_root_blocks)
    return {
        "schema_version": "1.0",
        "type": "article",
        "slug": slug,
        "meta": {
            "title": title,
            "description": description,
            "keywords": keywords + ["tè verde", "Camellia sinensis"],
            "canonical_path": f"/guide/{slug}/",
            "published": published,
        },
        "seo": {"robots": "index,follow", "og_type": "article"},
        "navigation": {
            "related_slugs": [],
            "temi_kb": tema_kb,
            "controversie": [],
            "explore_next": [{"name": n, "url": u, "reason": r} for n, u, r in explore_next],
        },
        "taxonomy": {},
        "body": {"blocks": blocks},
    }


GUIDES: dict[str, dict] = {
    "matcha-italia": guide_doc(
        "matcha-italia",
        "Perché il matcha non è una moda passeggera in Italia",
        "Dal boom pasticceria al matcha cerimoniale: come il verde in polvere ha trovato radici nel gusto italiano.",
        ["matcha Italia", "matcha pasticceria", "matcha cerimoniale", "trend tè verde"],
        "2026-03-15",
        [
            "Il matcha è arrivato nelle vetrine italiane come ingrediente — verde intenso in un tiramisù, in un gelato, in un latte zuccherato — molto prima che molti italiani sapessero cosa fosse una chasen o una ciotola di tencha.",
            "Questa guida spiega perché quel verde non è solo un colore di tendenza: è l'estremo di una filiera giapponese (ombra, macinazione, foglia intera) che la cucina italiana ha adottato per estetica e sapore, aprendo porte a un tè più consapevole.",
        ],
        [
            h2("Dalla vetrina alla tazza"),
            p(
                "In Giappone il matcha nasce come bevanda da cerimonia e come compagno quotidiano in versione usucha o koicha. In Italia lo hai incontrato probabilmente al contrario: prima il dolce, poi — se sei curioso — la polvere amara frullata con acqua calda."
            ),
            p(
                "Non è un errore culturale da correggere con snobismo: è un percorso di adozione. La pasticceria italiana ha sempre assorbito ingredienti stranieri (cacao, vaniglia, agrumi canditi) e li ha resi suoi. Il matcha segue la stessa logica, con un vantaggio: ti introduce alla Camellia sinensis come foglia intera, non come infusione filtrata."
            ),
            h2("Tre matcha, tre storie"),
            ul(
                [
                    "Matcha da supermercato o da bar: spesso zuccherato, colorante, poco tencha vero — marketing «cerimoniale» senza sostanza",
                    "Matcha da cucina: polvere più rustica, ottima per torte, panna, gelato; non pretendere umami da koicha",
                    "Matcha cerimoniale: tencha ombreggiato macinato a pietra, brillante, vegetale, amaro-equilibrato — si beve, non solo si spolvera",
                ]
            ),
            p(
                "Onuma e Rosen documentano entrambi il matcha in cucina e in cosmetica; Pellegrino lo colloca nella famiglia dei verdi giapponesi con regole di preparazione precise. La lezione per l'Italia: non esiste un solo «matcha», come non esiste un solo «vino»."
            ),
            h2("Perché non è una moda passeggera"),
            p(
                "Le mode alimentari italiane durano un estate e spariscono. Il matcha resta perché risolve problemi reali del mercato: colore naturale senza additivi, nota vegetale in pasticceria premium, alternativa al caffè con curva di energia diversa, ponte verso la ristorazione giapponese e coreana ormai radicata nelle grandi città."
            ),
            p(
                "Il bubble tea ha amplificato la domanda; i tea shop specialty hanno educato una fascia di pubblico alla polvere di qualità. Anche quando il latte matcha cala nei social, resta una platea che ha imparato a distinguere polvere spenta e tencha fresco — e chiede di più."
            ),
            p(
                "In Italia il rischio non è che il matcha scompaia: è che resti confinato al dolce zuccherato. La sfida educativa è mostrare che la stessa pianta può essere usucha in tazza, matcha su panettone semplice, o koicha in silenzio — senza contraddizione."
            ),
            h2("Come iniziare con intelligenza"),
            ul(
                [
                    "Compra polvere con origine e data di macinatura indicata; evita confezioni senza produttore",
                    "Prova prima usucha (2 g, 70 ml, 80 °C) prima di usare tutto in crema pasticcera",
                    "Abbina a dolci italiani poco zuccherati: panettone semplice, marron glacé, agrumi canditi",
                    "Non confondere l-theanina e caffeina concentrate con «detox» — il matcha stimola, in dosi diverse dal caffè",
                ]
            ),
            *fonti(
                [
                    "pellegrino, verdi giapponesi e matcha",
                    "onuma, matcha in cucina e quotidianità",
                    "rosen, usi pratici e estetica della foglia",
                    "hara, catechine e foglia intera",
                    "Treccani — voce «tè» (storia del consumo in Europa)",
                ]
            ),
        ],
        ["cucina_usi_pratici", "cerimonia_spiritualita"],
        [
            ("Scheda matcha", "/varieta/matcha/", "filiera completa"),
            ("Cucina e usi", "/impara/cucina/", "ricette e abbinamenti"),
            ("Bevanda o integratore?", "/impara/controversie/bevanda-vs-integratore/", "controversia"),
        ],
        [
            links(
                [
                    ("Tencha", "/glossario/tencha/", "materia prima"),
                    ("Chasen", "/glossario/chasen/", "strumento"),
                    ("Chanoyu", "/glossario/chanoyu/", "rito"),
                    ("Percorso dal bancha al matcha", "/gioca/percorsi/dal-bancha-al-matcha/", "apprendimento"),
                ]
            ),
            faq_block(
                [
                    (
                        "Il matcha del bar è «falso»?",
                        "Spesso è zuccherato e di grado basso: non è falso tè, ma non è cerimoniale. Va bene come dessert; per capire il matcha serve polvere pura in tazza.",
                    ),
                    (
                        "Posso usare lo stesso matcha per torta e cerimonia?",
                        "Puoi, ma il cerimoniale in forno è uno spreco economico e il da cucina in tazza può essere grossolano e amaro. Meglio due qualità se ti appassioni.",
                    ),
                    (
                        "Il matcha sostituisce il caffè?",
                        "Non deve sostituirlo: offre energia più lunga e meno picco per molti bevitori. In Italia convive con l'espresso come opzione di metà pomeriggio o merenda consapevole.",
                    ),
                ]
            ),
        ],
    ),
    "te-italia-storia": guide_doc(
        "te-italia-storia",
        "Il tè verde in Italia: una storia di nicchia",
        "Da Venezia al boom wellness: come il verde è entrato nelle case italiane senza sfidare il caffè.",
        ["tè verde Italia", "storia del tè", "cultura italiana", "specialty tea"],
        "2026-04-01",
        [
            "Se chiedi un tè al bar di quartiere, spesso ti guardano come se avessi ordinato un'insalata alle otto di mattina. Il caffè è il ritmo del Paese; il tè verde è cresciuto ai margini — poi, nelle grandi città, con forza sorprendente.",
            "Questa guida racconta come il verde è arrivato in Italia, perché è rimasto di nicchia rispetto al caffè, e cosa sta cambiando oggi tra tea shop, ristorazione asiatica e curiosità per il single origin.",
        ],
        [
            h2("Venezia e le prime rotte"),
            p(
                "Il tè entra in Europa con le rotte commerciali che toccano Venezia e Genova tra XVI e XVIII secolo. Per secoli resta bevanda di élite, medicina esotica, dono diplomatico — non abitudine popolare come il caffè che conquisterà i caffè italiani dal Settecento in poi."
            ),
            p(
                "Rosen e i manuali di storia del tè ricordano che la diffusione globale passa da monaci, mercanti e colonie: l'Italia riceve il prodotto, ma non costruisce intorno ad esso un rito urbano paragonabile all'espresso."
            ),
            h2("Caffè al centro, tè ai margini"),
            p(
                "Nel Novecento italiano il tè in bustina — spesso nero, Earl Grey, influenze britanniche — compare a colazione o nel pomeriggio domenicale. Il verde resta raro, confuso con le tisane dell'erboristeria, associato a «regime» o a estetica giapponese per pochi appassionati."
            ),
            p(
                "Il caffè occupa la pausa lavoro, il dopo pranzo, il incontro veloce al bancone. Il tè non ha mai disputato quello spazio: ha cercato altri — casa, yoga studio, ristorante giapponese, scaffale bio — senza pretendere di essere «il nuovo caffè»."
            ),
            h2("Il boom wellness e la confusione"),
            p(
                "Dagli anni Duemila il tè verde diventa sinonimo di detox, dimagrimento, antiossidanti sui packaging delle bustine scadenti. La KB è chiara: le catechine esistono, ma miracoli e integratori sono un'altra storia. In Italia questo boom ha fatto due cose opposte: ha popularizzato la parola «tè verde» e ha alimentato delusione quando l'erba amara in acqua bollente non curava nulla."
            ),
            p(
                "Chi è rimasto ha scoperto che il problema non era il tè, ma la qualità e la preparazione. È la stessa traiettoria del vino italiano dopo anni di tavola rossa: si sale di gradino quando il palato chiede di più."
            ),
            h2("Oggi: nicchia che cresce"),
            ul(
                [
                    "Tea shop specialty a Milano, Roma, Torino, Bologna, Firenze — consulenza e degustazione",
                    "Ristorazione giapponese e coreana che normalizza gyokuro, sencha, matcha in tazza",
                    "Pasticceria: matcha in gelato e dolci come ponte verso il verde «vero»",
                    "Autori e formatori italiani (es. Davide Pellegrino) che traducono tradizioni orientali senza snaturarle",
                    "E-commerce e single origin: tracciabilità come nel vino e nell'olio EVO",
                ]
            ),
            p(
                "Il Nord vede più pasticceria matcha e coworking con teiere; il Centro turismo culturale e ristorazione; Sud e isole meno shop fisici ma più ordini online. Non è uniforme — e non deve esserlo: il tè verde in Italia cresce per curiosità, non per decreto."
            ),
            h2("Cosa significa per te"),
            p(
                "Non devi scegliere tra caffè e tè come tra due squadre. Il verde italiano maturo è complementare: sencha nella pausa delle dieci, hojicha dopo cena domenicale, matcha in pasticceria quando vuoi colore senza artificio. La nicchia è ampia abbastanza per chi vuole imparare — piccola abbastanza da restare scelta, non obbligo wellness."
            ),
            *fonti(
                [
                    "rosen, storia e diffusione del tè",
                    "pellegrino, cultura del tè in Occidente",
                    "sommelier, commercio e rituali",
                    "onuma, adozione contemporanea",
                    "Treccani — voce «tè»",
                ]
            ),
        ],
        ["storia_cultura"],
        [
            ("Storia e cultura", "/impara/storia-cultura/", "hub tematico"),
            ("Matcha in Italia", "/guide/matcha-italia/", "capitolo successivo"),
            ("Dragon Well", "/varieta/dragon-well/", "verde cinese storico"),
        ],
        [
            links(
                [
                    ("Gunpowder", "/varieta/gunpowder/", "verde mediterraneo"),
                    ("Italia hub", "/italia/", "contesto locale"),
                    ("Percorso palato italiano", "/gioca/percorsi/palato-italiano/", "esercizio"),
                ]
            ),
            faq_block(
                [
                    (
                        "Perché in Italia si beve più caffè che tè?",
                        "Storia sociale e economica: il caffè ha legato bar, lavoro e incontro pubblico per due secoli. Il tè non ha avuto lo stesso investimento culturale — non è questione di qualità intrinseca.",
                    ),
                    (
                        "Il tè verde «detox» funziona?",
                        "Il tè può far parte di abitudini sane; non detoxifica organi né sostituisce medico o dieta equilibrata. Diffida di chi vende miracoli in bustina.",
                    ),
                    (
                        "Da dove iniziare oggi in Italia?",
                        "Un tea shop che fa assaggi, o una scheda varietà accessibile (bancha, genmaicha, sencha). Evita la prima bustina discount come giudizio sul mondo intero.",
                    ),
                ]
            ),
        ],
    ),
}


def main() -> None:
    for slug, doc in GUIDES.items():
        path = GUIDE / f"{slug}.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Guide: {slug}")
    print("Done.")


if __name__ == "__main__":
    main()
