#!/usr/bin/env python3
"""Populate impara hub and controversie JSON with rich editorial content."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from site_builder.citations import bib_item, bib_kb_prospettiva, bibliography_block
IMPARA = ROOT / "content" / "impara"
CONTRO = IMPARA / "controversie"


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


def callout_italia(text: str) -> dict:
    return {"type": "callout", "variant": "italia", "spans": [{"type": "text", "value": text}]}


def fonti(items: list[str]) -> list[dict]:
    """Legacy bullet list — prefer bibliography_block() for new content."""
    return [h2("Fonti"), ul(items)]


def fonti_bibliography(items: list[dict]) -> list[dict]:
    return [bibliography_block(items)]


def intro_deep(intro_paras: list[str], deep_blocks: list[dict]) -> list[dict]:
    return [
        {"type": "level_section", "level": "intro", "blocks": [p(x) for x in intro_paras]},
        {"type": "level_section", "level": "deep", "blocks": deep_blocks},
    ]


def hub_doc(
    slug: str,
    title: str,
    description: str,
    keywords: list[str],
    blocks: list[dict],
    tema_kb: str,
    controversie: list[str],
    explore_next: list[tuple[str, str, str]],
) -> dict:
    return {
        "schema_version": "1.0",
        "type": "hub",
        "slug": slug,
        "meta": {
            "title": title,
            "description": description,
            "keywords": keywords + ["tè verde", "Camellia sinensis"],
            "canonical_path": f"/impara/{slug}/",
        },
        "seo": {"robots": "index,follow", "og_type": "article"},
        "navigation": {
            "related_slugs": [],
            "temi_kb": [tema_kb],
            "controversie": controversie,
            "explore_next": [{"name": n, "url": u, "reason": r} for n, u, r in explore_next],
        },
        "taxonomy": {},
        "body": {"blocks": blocks},
    }


def controversy_doc(
    slug: str,
    title: str,
    description: str,
    positions: list[tuple[str, str]],
    intro_paras: list[str],
    cuore_paras: list[str],
    deep_blocks: list[dict],
    explore_next: list[tuple[str, str, str]],
) -> dict:
    blocks = [
        {
            "type": "positions",
            "items": [{"fonte": f, "tesi": t} for f, t in positions],
        },
        {"type": "level_section", "level": "intro", "blocks": [p(x) for x in intro_paras]},
        h2("Il cuore della questione"),
        *[p(x) for x in cuore_paras],
        {"type": "level_section", "level": "deep", "blocks": deep_blocks},
    ]
    return {
        "schema_version": "1.0",
        "type": "controversy",
        "slug": slug,
        "meta": {
            "title": title,
            "description": description,
            "keywords": [slug.replace("-", " "), "tè verde", "controversia"],
            "canonical_path": f"/impara/controversie/{slug}/",
        },
        "seo": {"robots": "index,follow", "og_type": "article"},
        "navigation": {
            "related_slugs": [],
            "temi_kb": [],
            "controversie": [],
            "explore_next": [{"name": n, "url": u, "reason": r} for n, u, r in explore_next],
        },
        "taxonomy": {},
        "body": {"blocks": blocks},
    }


HUBS: dict[str, dict] = {
    "storia-cultura": hub_doc(
        "storia-cultura",
        "Storia e cultura del tè verde",
        "Dalle leggende cinesi al tè verde sulla tavola italiana: come una foglia ha attraversato continenti.",
        ["storia tè verde", "cultura del tè", "origini"],
        intro_deep(
            [
                "Il tè verde non nasce in un supermercato: nasce in colline umide, in monasteri, in porti dove mercanti scambiavano merci preziose. Capirne la storia ti aiuta a bere con più consapevolezza — e a non confondere tradizione con marketing.",
                "Qui trovi il filo che collega Shen Nong e i monaci buddhisti al matcha nelle pasticcerie italiane di oggi. Non è un elenco di date: è la mappa culturale del verde.",
            ],
            [
                h2("Dalle origini alla diffusione"),
                p("In Cina la leggenda attribuisce la scoperta a Shen Nong; in Giappone il monaco Eisai portò semi e testi che legarono il tè alla meditazione zen. Il verde restò a lungo la forma dominante prima che l'ossidazione generasse oolong e neri."),
                p("Via Venezia e le rotte commerciali il tè entrò in Europa come bene di lusso. In Italia non ha mai soppiantato il caffè, ma oggi — tea shop, ristorazione giapponese, interesse per il benessere — il verde trova spazio come complemento, non come sostituto ideologico."),
                ul(
                    [
                        "Cina: culla del tè, pan-firing e gong fu cha",
                        "Giappone: vapore, sencha quotidiano, matcha cerimoniale",
                        "India e Sri Lanka: verdi di montagna meno noti ma affascinanti",
                        "Italia: adozione recente, spesso filtrata da moda wellness",
                    ]
                ),
                callout_italia(
                    "In Italia il tè verde arriva spesso tramite pasticceria (matcha) o erboristeria (tisane confuse con vero tè). Conoscere la storia distingue Camellia sinensis da camomilla e valorizza le tradizioni d'origine."
                ),
                links(
                    [
                        ("Dragon Well", "/varieta/dragon-well/", "tè cinese iconico"),
                        ("Matcha", "/varieta/matcha/", "filiera giapponese"),
                        ("Gong fu cha", "/glossario/gong-fu-cha/", "rito cinese"),
                        ("Controversia Cina vs Giappone", "/impara/controversie/cerimonia-cina-vs-giappone/", "due rituali"),
                    ]
                ),
                faq_block(
                    [
                        (
                            "Il tè verde è sempre stato «salutare» nella storia?",
                            "La medicina tradizionale cinese lo valorizzò presto; la scienza moderna misura catechine con altri strumenti. La storia parla di uso culturale e medicinale; non di capsule miracolose.",
                        ),
                        (
                            "Perché in Italia siamo legati al caffè e non al tè?",
                            "Storia economica e sociale: il caffè divenne rito urbano nel Settecento. Il tè restò di nicchia fino al boom wellness degli anni Duemila.",
                        ),
                    ]
                ),
                *fonti(["rosen, tema rosen-storia", "pellegrino, tradizioni mondiali", "onuma, cultura quotidiana"]),
            ],
        ),
        "storia_cultura",
        ["cerimonia-cina-vs-giappone", "consumo-quotidiano-vs-rituale"],
        [
            ("Gunpowder", "/varieta/gunpowder/", "storia export"),
            ("Darjeeling verde", "/varieta/darjeeling-verde/", "India"),
            ("Guide matcha Italia", "/guide/matcha-italia/", "contesto locale"),
        ],
    ),
    "lavorazione": hub_doc(
        "lavorazione",
        "Lavorazione e qualità",
        "Come una foglia diventa verde: vapore, padella, ombra e la chimica che resta in tazza.",
        ["lavorazione tè verde", "steaming", "qualità foglia"],
        intro_deep(
            [
                "La stessa pianta — Camellia sinensis — può diventare verde brillante o tè nero scuro. La differenza non è la botanica: è cosa succede alle foglie subito dopo il raccolto.",
                "Capire la lavorazione ti spiega perché il gyokuro costa più del bancha, perché il Dragon Well sa di nocciola e perché una foglia stantia non si recupera con acqua calda.",
            ],
            [
                h2("Fermare il tempo sulla foglia"),
                p("Il cuore del tè verde è la fixation: bloccare l'ossidazione con calore. In Giappone domina il vapore (steaming); in Cina spesso la padella (pan-firing). Poi arrivano rolling, essiccazione, selezione."),
                p("L'ombreggiatura — gyokuro, tencha — è una scelta agronomica prima ancora che di cucina: meno sole, più aminoacidi, più umami, meno amaro grezzo."),
                ul(
                    [
                        "Steaming (Giappone): sencha, gyokuro, bancha — verde intenso, note marine",
                        "Pan-firing (Cina): Long Jing, bi luo chun — nocciola, fagiolino",
                        "Tostatura: hojicha — colore ambrato, caffeina ridotta",
                        "Macinatura: tencha → matcha — foglia intera in polvere",
                    ]
                ),
                links(
                    [
                        ("Gyokuro", "/varieta/gyokuro/", "ombreggiato"),
                        ("Vapore", "/glossario/vapore/", "steaming"),
                        ("Wok", "/glossario/wok/", "padella cinese"),
                        ("Qualità sensoriale vs chimica", "/impara/controversie/qualita-sensoriale-vs-chimica/", "dibattito"),
                    ]
                ),
                faq_block(
                    [
                        (
                            "Tè verde in bustina: stessa lavorazione?",
                            "Spesso polvere o frammenti di bassa qualità, essiccazione industriale. Non rappresenta il verde specialty.",
                        ),
                        (
                            "La freschezza conta?",
                            "Sì. Catechine e aromi volatili degradano con il tempo; il verde di primavera (shincha) è atteso proprio per vivacità.",
                        ),
                    ]
                ),
                *fonti(["rosen, tema rosen-lavorazione", "pellegrino, lavorazione", "sommelier, produzione"]),
            ],
        ),
        "lavorazione_qualità",
        ["qualita-sensoriale-vs-chimica"],
        [
            ("Bi Luo Chun", "/varieta/bi-luo-chun/", "spirali primaverili"),
            ("Hojicha", "/varieta/hojicha/", "tostatura"),
            ("Lavorazione hub", "/impara/lavorazione/", "questa pagina"),
        ],
    ),
    "preparazione": hub_doc(
        "preparazione",
        "Preparazione e servizio",
        "Temperatura, grammi, secondi: trasformare la foglia in una tazza che mantiene la promessa del titolo.",
        ["preparazione tè verde", "temperatura", "infusione"],
        intro_deep(
            [
                "Hai comprato un sencha pregiato e lo hai scottato con acqua bollente? La preparazione non è pedanteria da manuale: è il modo in cui rispetti il lavoro di chi ha coltivato e lavorato la foglia.",
                "Qui impari i parametri che contano — gradi, grammi, secondi — e gli strumenti che aiutano senza trasformarti in collezionista compulsivo.",
            ],
            [
                h2("I tre numeri che salvano la tazza"),
                p("Temperatura dell'acqua, rapporto foglia/acqua, tempo di infusione. Cambiando uno solo modifichi amaro, corpo, caffeina estratta. Il sencha chiede 70–80 °C; il gyokuro ancora meno; il gunpowder regge un po' più di calore."),
                p("In Italia l'acqua del rubinetto spesso è dura: un filtro può migliorare sencha e gyokuro. La teiera dedicata — kyusu per il Giappone, gaiwan per il gong fu — non è snobismo: evita sapori residui."),
                ul(
                    [
                        "Sencha: ~3 g / 100 ml, 75 °C, 60 s",
                        "Gyokuro: ~4 g / 100 ml, 50–60 °C, 90 s",
                        "Dragon Well: ~3 g / 100 ml, 80 °C, 2 min",
                        "Matcha: 2 g / 70 ml, frusta chasen, non infusione",
                    ]
                ),
                callout_italia(
                    "L'errore italiano più comune è l'acqua dell'ebollitore versata su qualsiasi verde. Se hai sempre trovato il tè «amaro e insaporevole», prova bancha o genmaicha con 80 °C prima di abbandonare il verde."
                ),
                links(
                    [
                        ("Kyusu", "/glossario/kyusu/", "teiera giapponese"),
                        ("Gaiwan", "/glossario/gaiwan/", "coppa cinese"),
                        ("Quiz errori", "/gioca/quiz/riconosci-errore/", "verifica"),
                        ("Cold brew", "/varieta/cold-brew-gyokuro/", "estrazione fredda"),
                    ]
                ),
                faq_block(
                    [
                        (
                            "Devo pesare la foglia?",
                            "Per imparare sì; poi l'occhio basta. Un cucchiaino raso di sencha è circa 3 g — ma la bilancia insegna in una settimana.",
                        ),
                        (
                            "Posso reinfundere?",
                            "Molti verdi reggono 2–3 infusioni brevi; il profilo cambia a ogni versata. È parte del piacere del gong fu e del sencha in kyusu.",
                        ),
                    ]
                ),
                *fonti(["pellegrino, via del tè", "sommelier, servizio", "onuma, preparazione quotidiana"]),
            ],
        ),
        "preparazione_servizio",
        ["cerimonia-cina-vs-giappone", "consumo-quotidiano-vs-rituale"],
        [
            ("Sencha", "/varieta/sencha/", "scheda pratica"),
            ("Percorso dal bancha al matcha", "/gioca/percorsi/dal-bancha-al-matcha/", "apprendimento"),
        ],
    ),
    "degustazione": hub_doc(
        "degustazione",
        "Degustazione sensoriale",
        "Occhio, naso, palato: leggere il tè verde come si legge un vino — senza snobismo, con precisione.",
        ["degustazione tè", "profilo sensoriale", "gusto"],
        intro_deep(
            [
                "Degustare il tè verde non significa trovare mille aggettivi poetici: significa osservare la foglia, annusare il liquore caldo, sentire amaro e dolcezza equilibrati, notare cosa resta dopo il sorso.",
                "Se conosci già vino o olio extravergine, hai metà strada fatta. Qui trovi il lessico per capire cosa promette una scheda varietà e cosa stai bevendo davvero.",
            ],
            [
                h2("I quattro passi"),
                p("Aspetto della foglia e del liquore: colore, limpidezza, consistenza. Aroma in tazza: vegetale, tostato, floreale, marine. Gusto: attacco, corpo, amaro, umami. Retrogusto: quanto dura e come evolve."),
                p("L'umami nel gyokuro non è un termine da chef stellati: è la stessa rotondità che riconosci in un brodo o nel parmigiano — un ponte per il palato italiano, non un esotismo forzato."),
                ul(
                    [
                        "Vegetale fresco → sencha, shincha",
                        "Umami denso → gyokuro, matcha",
                        "Nocciola e fagiolino → Dragon Well",
                        "Tostato e nocciola → hojicha, genmaicha",
                        "Mineralità → darjeeling verde",
                    ]
                ),
                links(
                    [
                        ("Percorso palato italiano", "/gioca/percorsi/palato-italiano/", "esercizio guidato"),
                        ("Umami", "/glossario/umami/", "quinto gusto"),
                        ("Astringenza", "/glossario/astringenza/", "sensazione chiave"),
                        ("Gyokuro", "/varieta/gyokuro/", "esempio umami"),
                    ]
                ),
                faq_block(
                    [
                        (
                            "Serve una scheda da sommelier?",
                            "Aiuta in formazione; a casa bastano quattro domande: cosa vedo, cosa odoro, cosa gusto, cosa resta.",
                        ),
                        (
                            "Il prezzo garantisce qualità?",
                            "Non sempre. Occhio e naso rivelano foglia stantia o lavorazione scadente anche su packaging elegante.",
                        ),
                    ]
                ),
                *fonti(["sommelier, degustazione", "pellegrino, schede varietà", "onuma, riconoscere qualità"]),
            ],
        ),
        "degustazione_sensoriale",
        ["qualita-sensoriale-vs-chimica"],
        [
            ("Bi Luo Chun", "/varieta/bi-luo-chun/", "floreale"),
            ("Dragon Well", "/varieta/dragon-well/", "nocciola"),
            ("Darjeeling verde", "/varieta/darjeeling-verde/", "mineralità"),
        ],
    ),
    "salute": hub_doc(
        "salute",
        "Salute e catechine",
        "Cosa sappiamo davvero sul tè verde e il benessere — senza detox, senza promesse da integratore.",
        ["salute tè verde", "catechine", "EGCG"],
        intro_deep(
            [
                "Il tè verde contiene polifenoli — soprattutto catechine — con potenziale antiossidante documentato in laboratorio. Ma tra una molecola in provetta e la tua tazza del mattino c'è un mondo di differenze.",
                "Questa pagina non ti vende cure: ti aiuta a distinguere evidenza, tradizione e marketing italiano post-2000.",
            ],
            [
                h2("Cosa è ragionevole aspettarsi"),
                p("Consumo regolare di tè verde può far parte di uno stile di vita attento; non sostituisce terapie mediche né una dieta equilibrata. Il matcha, bevendo la foglia intera, concentra più catechine di un sencha filtrato — ma non è una pillola magica."),
                p("Gli studi clinici usano spesso estratti standardizzati di EGCG; le dosi in tazza sono più basse e modulate da temperatura, tempo e qualità della foglia."),
                ul(
                    [
                        "Evidenza solida: potenziale antiossidante delle catechine",
                        "Dibattito aperto: dosi efficaci per prevenzione specifica",
                        "Da evitare: «detox», «brucia grassi», «cura tumori» in etichetta",
                        "Matcha e sencha quotidiano: più catechine di bancha leggero",
                    ]
                ),
                callout_italia(
                    "In Italia erboristerie e social promettono spesso miracoli. Diffida di chi confonde tisane e tè verde, o vende integratori EGCG come sostituto del piacere in tazza."
                ),
                links(
                    [
                        ("Controversia scienza vs tradizione", "/impara/controversie/salute-scienza-vs-tradizione/", "dibattito KB"),
                        ("Bevanda vs integratore", "/impara/controversie/bevanda-vs-integratore/", "capsule o tazza"),
                        ("Catechine", "/glossario/catechine/", "molecole chiave"),
                        ("Matcha", "/varieta/matcha/", "foglia intera"),
                    ]
                ),
                faq_block(
                    [
                        (
                            "Quante tazze al giorno?",
                            "Tradizione giapponese: 3–5; scienza non fissa un numero universale. Ascolta corpo e medico se hai condizioni specifiche.",
                        ),
                        (
                            "Il tè verde dimagrisce?",
                            "Non da solo. Eventuali effetti sul metabolismo sono modesti e non compensano abitudini alimentari.",
                        ),
                    ]
                ),
                *fonti_bibliography(
                    [
                        bib_item("hara", "hara-panoramica", "Efficacia del tè nella salute umana", "71"),
                        bib_item("hara", "hara-anticancer", "Catechine in prevenzione e terapia del cancro", "102–104"),
                        bib_item("rosen", "rosen-salute", "Polifenoli, EGCG e antiossidanti", "2714–2838"),
                        bib_item("pellegrino", "pellegrino-salute", "Oncologia, diabete e dimagrimento", "2938–2964"),
                    ]
                ),
            ],
        ),
        "salute_catechine",
        ["salute-scienza-vs-tradizione", "bevanda-vs-integratore"],
        [
            ("Quiz miti", "/gioca/quiz/mito-verita/", "verifica"),
            ("EGCG", "/glossario/egcg/", "catechina studiata"),
        ],
    ),
    "cerimonia": hub_doc(
        "cerimonia",
        "Cerimonia e spiritualità",
        "Dal gong fu cha al chanoyu: quando il tè diventa rito — e quando basta una pausa consapevole.",
        ["cerimonia del tè", "chanoyu", "gong fu cha"],
        intro_deep(
            [
                "Cerimonia non significa per forza kimono e giardino di muschio. Significa che acqua e foglia ricevono attenzione piena — in Cina come convivialità, in Giappone come via estetica.",
                "Puoi attingere a queste tradizioni senza recitarle: un kyusu scaldato, tre respiri prima del primo sorso, già è un gesto diverso dal bustino scartato al volo.",
            ],
            [
                h2("Due tradizioni, due registri"),
                p("Il gong fu cha cinese è ospitalità e abilità: piccole tazze, infusioni ripetute, gaiwan o yixing. Il chanoyu giapponese codifica spazio (roji), strumenti (chawan, chasen) e matcha in usucha o koicha."),
                p("In Giappone convivono bancha in bottiglia e Chado formale — non c'è contraddizione. Il quotidiano e il sacro attraversano la stessa bevanda."),
                links(
                    [
                        ("Chanoyu", "/glossario/chanoyu/", "via del tè"),
                        ("Gong fu cha", "/glossario/gong-fu-cha/", "arte cinese"),
                        ("Percorso rituale è quotidiano", "/gioca/percorsi/rituale-quotidiano/", "gioco"),
                        ("Matcha", "/varieta/matcha/", "cuore cerimoniale"),
                    ]
                ),
                faq_block(
                    [
                        (
                            "Posso praticare chanoyu in Italia?",
                            "Ci sono scuole e gruppi; anche senza sala formale puoi imparare usucha con matcha e chasen di qualità.",
                        ),
                        (
                            "Il rituale è religioso?",
                            "Ha radici zen; oggi molti lo vivono come estetica e presenza, non come dogma.",
                        ),
                    ]
                ),
                *fonti(["onuma, cerimonia", "pellegrino, chanoyu", "sommelier, cerimonie"]),
            ],
        ),
        "cerimonia_spiritualita",
        ["cerimonia-cina-vs-giappone", "consumo-quotidiano-vs-rituale"],
        [
            ("Chasen", "/glossario/chasen/", "frusta matcha"),
            ("Impara preparazione", "/impara/preparazione/", "tecnica base"),
        ],
    ),
    "caffeina": hub_doc(
        "caffeina",
        "Caffeina e tannini",
        "Stimola o calma? Dipende dalla foglia, dal tempo in tazza e dall'orologio.",
        ["caffeina tè verde", "L-teanina", "tannini"],
        intro_deep(
            [
                "Il tè verde contiene caffeina — a volte più di quanto credi, soprattutto in matcha e gyokuro. Eppure molti lo descrivono come «più dolce» del caffè: entrano in gioco tannini e L-teanina.",
                "Qui impari a scegliere la varietà giusta per la mattina, la pausa o la sera senza sorprese.",
            ],
            [
                h2("Modulare energia e calma"),
                p("I tannini legano parte della caffeina e rallentano l'assorbimento. La L-teanina, abbondante nei verdi ombreggiati, è associata a vigilanza più stabile. Non è magia: è chimica in tazza."),
                p("Gyokuro e matcha prima di dormire? Sconsigliati per la maggior parte. Hojicha o kukicha la sera: sì. Sencha a metà pomeriggio: equilibrio per molti palati italiani abituati all'espresso."),
                ul(
                    [
                        "Alta caffeina: matcha, gyokuro",
                        "Media: sencha, dragon well",
                        "Bassa: bancha, kukicha, hojicha",
                        "Infusione lunga = più caffeina (e più amaro)",
                    ]
                ),
                links(
                    [
                        ("Controversia stimolazione", "/impara/controversie/caffeina-stimolazione/", "posizioni KB"),
                        ("L-teanina", "/glossario/l-teanina/", "aminoacido"),
                        ("Quiz l'ora giusta", "/gioca/quiz/ora-giusta/", "esercizio"),
                        ("Hojicha", "/varieta/hojicha/", "sera"),
                    ]
                ),
                faq_block(
                    [
                        (
                            "Tè verde decaffeinato?",
                            "Esiste, ma perde parte del profilo; spesso meglio hojicha naturale per la sera.",
                        ),
                        (
                            "Stomaco vuoto?",
                            "Tannini su stomaco sensibile possono irritare: inizia con bancha o genmaicha, non gyokuro a digiuno.",
                        ),
                    ]
                ),
                *fonti(["pellegrino, salute", "sommelier, proprietà", "onuma, mg caffeina"]),
            ],
        ),
        "caffeina_tannini",
        ["caffeina-stimolazione"],
        [
            ("Bancha", "/varieta/bancha/", "bassa caffeina"),
            ("Matcha", "/varieta/matcha/", "alta caffeina"),
        ],
    ),
    "cucina": hub_doc(
        "cucina",
        "Cucina e usi pratici",
        "Matcha in pasticceria, hojicha nel dessert, foglie usate: il tè verde esce dalla tazza.",
        ["matcha cucina", "ricette tè verde", "cucina"],
        intro_deep(
            [
                "Il matcha non è solo cerimonia: è polvere di colore, umami e catechine che invade gelati, tiramisù, pannacotte. In Giappone Onuma propone cheesecake e torte; in Italia il verde è diventato ingrediente da pasticceria — con risultati disomogenei.",
                "Fuori dalla moda, il tè verde in cucina ha senso quando la qualità della polvere regge: culinary grade sì, polvere zuccherata da latte no.",
            ],
            [
                h2("Ingredienti e riusi"),
                p("Matcha per dolci e saltato (tempura verde, rub su pesce). Hojicha per note tostate in crema e cioccolato. Foglie usate di gyokuro o sencha ancora profumate — compost o cosmetica casalinga secondo Rosen."),
                p("Il matcha da cucina richiede comunque foglie ombreggiate ben lavorate; il prezzo basso spesso significa amaro e colore spento."),
                callout_italia(
                    "Il matcha latte verde dei bar non è riferimento gastronomico: zucchero e latte mascherano polveri mediocri. Per cucinare, compra matcha da pasticceria di provenienza chiara."
                ),
                links(
                    [
                        ("Matcha", "/varieta/matcha/", "ingrediente base"),
                        ("Genmaicha", "/varieta/genmaicha/", "comfort"),
                        ("Bevanda vs integratore", "/impara/controversie/bevanda-vs-integratore/", "dose in cucina"),
                        ("Guide matcha Italia", "/guide/matcha-italia/", "contesto"),
                    ]
                ),
                faq_block(
                    [
                        (
                            "Matcha da supermercato per dolci?",
                            "Funziona per colore; per sapore serve grado culinary o superiore, conservato al buio.",
                        ),
                        (
                            "Tè verde in savory italiano?",
                            "Matcha su risotto o pesce chiede dosi minime; hojicha più facile con cioccolato e noci.",
                        ),
                    ]
                ),
                *fonti(["onuma, ricette matcha", "rosen, cucina e bellezza", "pellegrino, matcha"]),
            ],
        ),
        "cucina_usi_pratici",
        ["bevanda-vs-integratore"],
        [
            ("Hojicha", "/varieta/hojicha/", "tostato in dessert"),
            ("Italia abbinamenti", "/italia/abbinamenti/", "gastronomia"),
        ],
    ),
}

CONTROVERSIES: dict[str, dict] = {
    "salute-scienza-vs-tradizione": controversy_doc(
        "salute-scienza-vs-tradizione",
        "Quanto è davvero dimostrato che il tè verde faccia bene?",
        "Tradizione millenaria, studi epidemiologici e trial clinici: cosa possiamo dire con onestà.",
        [
            (
                "hara",
                "Servono meccanismi molecolari, trial clinici randomizzati e misurazione della biodisponibilità delle catechine per affermare effetti terapeutici specifici. La letteratura è promettente ma non sempre trasferibile in «tre tazze al giorno».",
            ),
            (
                "rosen",
                "Secoli di medicina tradizionale cinese e studi epidemiologici in Giappone (Shizuoka) supportano benefici su cuore, invecchiamento e prevenzione. Il tè è terapia in tazza anche prima dei paper.",
            ),
            (
                "onuma",
                "La saggezza popolare giapponese — Eisai, la nonna che beve matcha — e l'esperienza quotidiana confermano virtù salutari prima ancora che la chimica le nomini.",
            ),
            (
                "pellegrino",
                "Il tè verde va inserito nella prevenzione e nello stile di vita sano, con moderazione e qualità. Non sostituisce mai diagnosi e terapie del medico curante.",
            ),
        ],
        [
            "Ogni settimana un titolo promette che il tè verde «cura» qualcosa. Le catechine esistono, gli antiossidanti pure — ma la strada dalla foglia al claim in etichetta è tortuosa.",
            "Questa controversia non chiede di scegliere tra scienza e tradizione: chiede di capire cosa ciascuna può promettere senza ingannare chi beve.",
        ],
        [
            "La medicina tradizionale cinese ha classificato il tè come allievo della salute molto prima degli analizzatori. Oggi Hara e collaboratori misurano EGCG in microgrammi e confrontano gruppi in trial. Entrambi guardano la stessa foglia con linguaggi diversi.",
            "In Italia il rischio è il taglio wellness: estratti in capsula, tisane verdi che non sono Camellia sinensis, promesse detox post festività. La risposta equilibrata: bevi tè verde di qualità per piacere e abitudine; eventuali benefici sono un plus documentato con cautela.",
        ],
        [
            h2("Dove convergono le fonti"),
            p("Tutte concordano che il tè verde non è acqua colorata: contiene molecole bioattive. Tutte sconsigliano di trattarlo come farmaco sostitutivo."),
            h2("Dove divergono"),
            p("Hara chiede rigore clinico prima di claim forti; Rosen e Onuma accettano evidenza storica e popolazione. Pellegrino media: prevenzione sì, terapia no."),
            h2("In pratica"),
            p("Bevi per gusto e ritualità; non per colpa. Se usi integratori EGCG, parlane con il medico — dosi alte possono interagire con farmaci."),
            faq_block(
                [
                    (
                        "Il tè previene il cancro?",
                        "Studi osservazionali suggeriscono correlazioni; non sostituiscono screening e cure mediche.",
                    ),
                    (
                        "Chi ha ragione?",
                        "Nessun vincitore assoluto: cautela scientifica e tradizione convivono.",
                    ),
                ]
            ),
            links(
                [
                    ("Salute e catechine", "/impara/salute/", "hub tema"),
                    ("Catechine", "/glossario/catechine/", "molecole"),
                    ("Quiz miti", "/gioca/quiz/mito-verita/", "verifica"),
                ]
            ),
            *fonti_bibliography(
                [
                    bib_item("hara", "hara-panoramica", "Biodisponibilità dei polifenoli", "89"),
                    bib_item("hara", "hara-anticancer", "Catechine in prevenzione e terapia del cancro", "102–104"),
                    bib_item("rosen", "rosen-salute", "Polifenoli, EGCG e antiossidanti", "2714–2838"),
                    bib_item("onuma", "onuma-storia", "Eisai: «il tè è l'elisir della salute»", "196"),
                    bib_item("pellegrino", "pellegrino-salute", "Il tè verde va inserito nella prevenzione", "2907–2964"),
                    bib_kb_prospettiva(
                        "salute-scienza-vs-tradizione",
                        "Quanto è dimostrato che il tè verde faccia bene?",
                    ),
                ]
            ),
        ],
        [("Bevanda vs integratore", "/impara/controversie/bevanda-vs-integratore/", "correlata")],
    ),
    "bevanda-vs-integratore": controversy_doc(
        "bevanda-vs-integratore",
        "Meglio in tazza o in capsula?",
        "EGCG in polvere o matcha frustato: due modi di assumere catechine, due esperienze.",
        [
            (
                "rosen",
                "Gli integratori offrono dosi concentrate di catechine senza caffeina, utili a chi non tollera stimoli. Ma privano del piacere rituale, del colore in tazza, della varietà sensoriale. La bevanda resta la forma completa.",
            ),
            (
                "pellegrino",
                "Il matcha, bevendo la foglia intera sospesa in acqua, concentra antiossidanti più di qualsiasi infusione filtrata — senza uscire dal mondo del tè vero.",
            ),
            (
                "hara",
                "I trial clinici sulla salute usano spesso estratti standardizzati di EGCG, non tazze di sencha. La biodisponibilità e il dosaggio misurabile favoriscono la capsula in laboratorio — non necessariamente in cucina.",
            ),
        ],
        [
            "In farmacia trovi estratti di tè verde; in teiera trovi umami, aroma, gesto. Non è lo stesso prodotto anche se la parola «catechine» compare in entrambi.",
            "La domanda non è solo «cosa fa più bene» ma «cosa stai cercando»: dose precisa, assenza di caffeina, o esperienza culturale e sensoriale?",
        ],
        [
            "Gli integratori nascono quando la ricerca ha bisogno di standardizzare l'EGCG. La tazza nasce quando una cultura ha deciso che bere foglie è modo di stare al mondo. In Italia entrambi convivono: matcha latte zuccherato da un lato, capsule detox dall'altro — e al centro poco tè vero di qualità.",
            "Il matcha cerimoniale o da cucina è ponte: bevi la foglia intera senza industrializzare in capsula. Rosen lo considera ideale; Hara lo studierebbe ancora in trial separati.",
        ],
        [
            h2("Sintesi"),
            p("Bevanda integra corpo, mente e cultura; estratto integra protocolli e dosi. Per la maggior parte dei bevitori italiani curiosi, la tazza resta il punto di partenza — integratori solo su consiglio professionale."),
            p("Se scegli la capsula per comodità, accetta di perdere aroma, ritualità e la varietà infinita delle lavorazioni. Se scegli la tazza, accetta che la dose di EGCG non sarà quella di un trial clinico — e che forse va bene così."),
            links(
                [
                    ("Matcha", "/varieta/matcha/", "foglia intera"),
                    ("Salute", "/impara/salute/", "hub"),
                    ("Cucina", "/impara/cucina/", "matcha fuori tazza"),
                ]
            ),
            *fonti(["rosen, integratori", "hara, trial EGCG", "pellegrino, matcha"]),
        ],
        [("Scienza vs tradizione", "/impara/controversie/salute-scienza-vs-tradizione/", "correlata")],
    ),
    "cerimonia-cina-vs-giappone": controversy_doc(
        "cerimonia-cina-vs-giappone",
        "Gong fu cha o chanoyu: due anime del rituale",
        "Convivialità cinese e codice giapponese: confronto senza scegliere un vincitore.",
        [
            (
                "sommelier",
                "Il gong fu cha è conviviale e informale: ospite al centro, abilità tecnica del preparatore, sette passi classici ma adattabili. Oolong e verdi in infusioni multiple; conversazione e tazze piccole.",
            ),
            (
                "pellegrino",
                "Il chanoyu è evento sociale formale: koicha denso e usucha leggero, percorso nel roji, umiltà verso l'ospite, fusione con ikebana, ceramica e architettura del chashitsu.",
            ),
            (
                "onuma",
                "La cerimonia giapponese incarna bellezza e semplicità adottabili anche in Occidente — non come spettacolo esotico ma come esercizio di presenza.",
            ),
        ],
        [
            "Cina e Giappone non condividono un unico «rito del tè». Condividono l'idea che acqua e foglia meritino attenzione — poi divergono.",
            "In Italia spesso tutto viene etichettato «cerimoniale» in confezione regalo. Capire gong fu e chanoyu ti salva da marketing vuoto.",
        ],
        [
            "Il gong fu cha nasce come ospitalità: offri il meglio che hai, reinfondi, conversi. Il chanoyu nasce come disciplina estetica zen: ogni movimento ha nome, il silenzio è parte del menu.",
            "Nessuno è «superiore»: il gong fu è più accessibile a una cena tra amici; il chanoyu richiede studio e spazio. Puoi ispirarti a entrambi senza appropriazione superficiale.",
        ],
        [
            h2("Cosa portare a casa"),
            p("Dal gong fu: piccole tazze, infusioni brevi, attenzione all'ospite. Dal chanoyu: lentezza, pulizia del gesto, matcha preparato con cura."),
            p("In Italia non serve replicare un roji: serve smettere di chiamare «cerimoniale» ogni confezione regalo. Impara un gesto alla volta."),
            links(
                [
                    ("Gong fu cha", "/glossario/gong-fu-cha/", "definizione"),
                    ("Chanoyu", "/glossario/chanoyu/", "definizione"),
                    ("Cerimonia hub", "/impara/cerimonia/", "approfondimento"),
                ]
            ),
            *fonti(["sommelier, cerimonie", "pellegrino, chanoyu", "onuma, cerimonia"]),
        ],
        [("Consumo vs rituale", "/impara/controversie/consumo-quotidiano-vs-rituale/", "correlata")],
    ),
    "qualita-sensoriale-vs-chimica": controversy_doc(
        "qualita-sensoriale-vs-chimica",
        "Cosa definisce un buon tè verde?",
        "Palato, occhio e laboratorio: tre modi di misurare la stessa foglia.",
        [
            (
                "sommelier",
                "Scheda sensoriale professionale: assenza di difetti, equilibrio tra corpo e astringenza, note varietali tipiche del cultivar e del terroir. Il prezzo non basta.",
            ),
            (
                "onuma",
                "Aroma di erba fresca, brillantezza della foglia, sapore equilibrato senza domanda di laboratorio. Anche al supermercato si impara a scartare polveri spente.",
            ),
            (
                "hara",
                "Contenuto di catechine, cultivar e processo produttivo giapponese determinano il profilo «salutare». La chimica non è nemica del gusto ma lo misura diversamente.",
            ),
            (
                "rosen",
                "La bellezza della foglia essiccata e il piacere in tazza sono criteri legittimi. Un tè può emozionare senza scheda analitica.",
            ),
        ],
        [
            "Compri un gyokuro per l'umami o per le catechine? Spesso per entrambi, senza saperlo. Ma quando qualità scende, palato e laboratorio possono non coincidere.",
            "Questa controversia riguarda chi produce, chi vende e chi beve: cosa intendiamo quando diciamo «buono».",
        ],
        [
            "Un verde eccellente al gusto tende a essere anche fresco e ben lavorato — quindi ricco di molecole interessanti. Ma un integratore di EGCG non ti regala il profilo sensoriale del gyokuro.",
            "In Italia il consumatore incontra spesso solo prezzo e packaging: imparare a degustare è difesa contro fregature.",
        ],
        [
            h2("Convergenza pratica"),
            p("Foglia intera, colore vivido, aroma pulito, assenza di muffa o tostatura rancida: palato e occhio filtrano già molto. Il laboratorio serve produttori e ricerca, non obbligatoriamente la tua cucina."),
            p("Quando paghi un gyokuro premium, paghi anche lavorazione e freschezza che tendono a coincidere con un profilo ricco — anche se non hai uno spettrometro in cucina."),
            links(
                [
                    ("Degustazione", "/impara/degustazione/", "metodo"),
                    ("Gyokuro", "/varieta/gyokuro/", "esempio premium"),
                    ("Lavorazione", "/impara/lavorazione/", "dalla foglia"),
                ]
            ),
            *fonti(["sommelier, degustazione", "hara, catechine", "rosen, estetica foglia"]),
        ],
        [("Salute scienza vs tradizione", "/impara/controversie/salute-scienza-vs-tradizione/", "correlata")],
    ),
    "caffeina-stimolazione": controversy_doc(
        "caffeina-stimolazione",
        "Il tè verde stimola o rilassa?",
        "Caffeina, L-teanina e varietà scelta: la risposta è «dipende» — ecco da cosa.",
        [
            (
                "pellegrino",
                "Stimola senza eccitare: la caffeina è legata ai tannini, rilascio più lento del caffè; la L-teanina modula verso calma vigile. Effetto più lungo e meno nervoso per molti bevitori.",
            ),
            (
                "sommelier",
                "La L-teanina è associata ad onde alfa e concentrazione con calma corporea — spiega perché il tè non equivale a un espresso per il sistema nervoso.",
            ),
            (
                "onuma",
                "Gyokuro prima dello sport può aiutare; prima di dormire no. La varietà conta più dell'etichetta generica «tè verde».",
            ),
        ],
        [
            "In Italia ti dicono «il tè verde fa bene e calma». Poi bevi matcha alle tre del mattino e non capisci perché non dormi. La caffeina c'è; cambia forma e dose.",
            "Non esiste un unico effetto: esiste una tazza, un momento, una foglia.",
        ],
        [
            "Il caffè italiano concentra caffeina in pochi millilitri e la libera in fretta. Il tè la lega a polifenoli e aminoacidi: curva diversa. Ma gyokuro e matcha possono superare sencha per mg in tazza.",
            "Scegli hojicha dopo cena, sencha a metà pomeriggio, evita matcha se sei sensibile. Non è regola universale: ascolta il corpo.",
        ],
        [
            h2("Guida rapida"),
            ul(
                [
                    "Mattina energia: matcha, gyokuro con cautela",
                    "Pausa lavoro: sencha, dragon well",
                    "Sera: hojicha, kukicha, bancha",
                    "Infusione lunga: più caffeina e più amaro",
                ]
            ),
            p("Il caffè espresso resta la bussola italiana per molti: il tè non deve sostituirlo, ma offre un'altra curva di energia quando vuoi meno picco e più durata."),
            links(
                [
                    ("Caffeina hub", "/impara/caffeina/", "tema"),
                    ("Quiz ora giusta", "/gioca/quiz/ora-giusta/", "esercizio"),
                    ("L-teanina", "/glossario/l-teanina/", "modulazione"),
                ]
            ),
            *fonti(["pellegrino, salute", "sommelier, proprieta", "onuma, varieta"]),
        ],
        [("Salute", "/impara/salute/", "contesto")],
    ),
    "consumo-quotidiano-vs-rituale": controversy_doc(
        "consumo-quotidiano-vs-rituale",
        "Tè verde: abitudine quotidiana o esperienza speciale?",
        "Bancha in bottiglia e chanoyu nella stessa cultura: perché non è contraddizione.",
        [
            (
                "onuma",
                "In Giappone il tè accompagna colazione, ristorante, pause — presenza costante, non solo cerimonia del weekend.",
            ),
            (
                "rosen",
                "Il piacere quotidiano del tè con riso o con visitatori convive con la cerimonia formale cha-no-yu. Due registri, stessa pianta.",
            ),
            (
                "pellegrino",
                "In Giappone coesistono bancha in bottiglia al distributore e culto formale del Chado nella sala cerimoniale: due registri, stessa cultura, nessuna gerarchia morale tra «alto» e «basso».",
            ),
        ],
        [
            "In Occidente il tè «cerimoniale» viene venduto come lusso; il quotidiano come bustina dimenticata. In Giappone la scala è più ricca.",
            "In Italia possiamo imparare: un gesto lento il sabato e un sencha veloce il lunedì — nessuno dei due è «meno autentico».",
        ],
        [
            "Il rischio italiano è l'alternativa ideologica: o tutto wellness lento, o tutto moda matcha. La tradizione giapponese è più semplice: il tè è bevanda, ospitalità, estetica — a seconda dell'ora.",
            "Non devi scegliere tra rito e praticità: puoi scalare il chanoyu a una kyusu scaldata e tre attimi di silenzio.",
        ],
        [
            h2("Proposta concreta"),
            p("Quotidiano: sencha o bancha in tazza grande, parametri semplici. Speciale: matcha con chasen la domenica, o percorso guidato sul sito."),
            p("Il gesto lento non è incompatibile con la vita veloce: è una scelta di pochi minuti, non di un'ora intera — anche in cucina italiana tra un caffè e l'altro."),
            links(
                [
                    ("Percorso rituale", "/gioca/percorsi/rituale-quotidiano/", "gioco"),
                    ("Bancha", "/varieta/bancha/", "quotidiano"),
                    ("Cerimonia hub", "/impara/cerimonia/", "rito"),
                ]
            ),
            *fonti(["onuma, quotidianita", "rosen, poesia", "pellegrino, Giappone"]),
        ],
        [("Gong fu vs chanoyu", "/impara/controversie/cerimonia-cina-vs-giappone/", "correlata")],
    ),
}


def main() -> None:
    for slug, doc in HUBS.items():
        path = IMPARA / f"{slug}.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Hub: {slug}")
    for slug, doc in CONTROVERSIES.items():
        path = CONTRO / f"{slug}.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Controversy: {slug}")
    print("Done.")


if __name__ == "__main__":
    main()
