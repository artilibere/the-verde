#!/usr/bin/env python3
"""Populate glossary JSON files with rich content from curated data."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSS_DIR = ROOT / "content" / "glossario"


def p(text: str) -> dict:
    return {"type": "paragraph", "spans": [{"type": "text", "value": text}]}


def h2(text: str) -> dict:
    return {"type": "heading", "level": 2, "spans": [{"type": "text", "value": text}]}


def li(text: str) -> dict:
    return {"spans": [{"type": "text", "value": text}]}


def ul(items: list[str]) -> dict:
    return {"type": "list", "ordered": False, "items": [li(x) for x in items]}


def links(items: list[tuple[str, str, str]]) -> dict:
    return {
        "type": "related_links",
        "items": [{"name": n, "url": u, "reason": r} for n, u, r in items],
    }


def faq(q: str, a: str) -> dict:
    return {
        "type": "faq",
        "items": [{"question": q, "answer_spans": [{"type": "text", "value": a}]}],
    }


def fonti(items: list[str]) -> list[dict]:
    return [h2("Fonti"), ul(items)]


def build_glossary(
    slug: str,
    title: str,
    description: str,
    keywords: list[str],
    intro: str,
    deep_blocks: list[dict],
    temi_kb: list[str],
    explore_next: list[tuple[str, str, str]],
    related_slugs: list[str] | None = None,
) -> dict:
    return {
        "schema_version": "1.0",
        "type": "glossary",
        "slug": slug,
        "meta": {
            "title": title,
            "description": description,
            "keywords": keywords + ["tè verde", "Camellia sinensis"],
            "canonical_path": f"/glossario/{slug}/",
        },
        "seo": {"robots": "index,follow", "og_type": "article"},
        "navigation": {
            "related_slugs": related_slugs or [],
            "temi_kb": temi_kb,
            "controversie": [],
            "explore_next": [
                {"name": n, "url": u, "reason": r} for n, u, r in explore_next
            ],
        },
        "taxonomy": {},
        "body": {
            "blocks": [
                {"type": "level_section", "level": "intro", "blocks": [p(intro)]},
                {"type": "level_section", "level": "deep", "blocks": deep_blocks},
            ]
        },
    }


# Curated glossary content (KB-aligned + Treccani where noted in Fonti)
ENTRIES: dict[str, dict] = {}


def _entry(
    slug,
    title,
    description,
    keywords,
    intro,
    context_title,
    body_paras,
    bullets,
    rl,
    fq,
    fonti_list,
    temi_kb,
    explore_next,
    related_slugs=None,
):
    deep = [h2(context_title)]
    deep.extend(p(x) for x in body_paras)
    deep.append(ul(bullets))
    deep.append(links(rl))
    deep.append(faq(fq[0], fq[1]))
    deep.extend(fonti(fonti_list))
    ENTRIES[slug] = build_glossary(
        slug, title, description, keywords, intro, deep, temi_kb, explore_next, related_slugs
    )


# --- Botanica e chimica ---
_entry(
    "camellia-sinensis",
    "Camellia sinensis",
    "L'unica pianta che produce il vero tè: foglie lavorate, non tisane.",
    ["Camellia sinensis", "pianta del tè"],
    "Quando parli di tè verde, parli sempre di una sola pianta: la Camellia sinensis. Non è un'erba generica né una miscela aromatica: è un arbusto dalle foglie che, se non ossidate, diventano il verde che conosci in tazza.",
    "Botanica e origini",
    [
        "Appartenente alla famiglia delle Teaceae, la Camellia sinensis cresce in colline umide e climi temperati. Due varietà principali — sinensis e assamica — e innumerevoli cultivar danno origine a sencha, dragon well, gyokuro e tutto il resto.",
        "Il nome unisce l'omaggio al botanico Georg Josef Kamel e il latino sinensis, «cinese», perché le prime descrizioni scientifiche partirono da lì. Ma la pianta vive oggi dal Giappone all'India, dal Kenya allo Sri Lanka.",
    ],
    [
        "Solo le foglie (e in casi come il matcha, anche il consumo dell'intera foglia) contano per il tè vero",
        "Tisane come camomilla o menta non sono Camellia sinensis",
        "Stessa pianta, lavorazioni diverse: verde, oolong, nero, bianco",
    ],
    [
        ("Sencha", "/varieta/sencha/", "esempio di verde giapponese"),
        ("Catechine", "/glossario/catechine/", "polifenoli nella foglia"),
        ("Storia e cultura", "/impara/storia-cultura/", "diffusione mondiale"),
    ],
    ("Il tè verde è una pianta diversa dal tè nero?", "No: stessa Camellia sinensis. La differenza è nella lavorazione — il verde ferma l'ossidazione presto."),
    ["pellegrino, pp. 45–52", "rosen, pp. 47–51", "Treccani — Camellia"],
    ["storia_cultura", "lavorazione_qualità"],
    [
        ("Lavorazione", "/impara/lavorazione/", "dalla foglia al verde"),
        ("Sencha", "/varieta/sencha/", "varietà quotidiana"),
    ],
)

_entry(
    "catechine",
    "Catechine",
    "Polifenoli antiossidanti del tè verde, responsabili di gran parte del profilo salutare.",
    ["catechine", "polifenoli", "antiossidanti"],
    "Le catechine sono molecole che la foglia di tè accumula per difendersi dal sole. Nel tè verde restano abbondanti perché la lavorazione interrompe l'ossidazione prima che si trasformino in altri composti.",
    "Nel tè verde",
    [
        "Il gruppo più studiato include l'EGCG — epigallocatechina gallato — ma ce ne sono altre, ognuna con un ruolo nel gusto e nella ricerca sulla salute.",
        "Temperatura e tempo di infusione ne modulano l'estrazione: acqua troppo calda può rendere la tazza amara senza necessariamente «fare più bene».",
    ],
    [
        "Concentrate nel verde non ossidato rispetto al nero",
        "Legate all'amaro e all'astringenza in tazza",
        "Oggetto di trial clinici con cautela (hara)",
    ],
    [
        ("EGCG", "/glossario/egcg/", "catechina più studiata"),
        ("Salute", "/impara/salute/", "evidenze e limiti"),
        ("Matcha", "/varieta/matcha/", "foglia intera = più catechine"),
    ],
    ("Bevendo tè verde assumo sempre molte catechine?", "Dipende da varietà, freschezza, temperatura e tempo. Il matcha, bevendo la polvere, ne concentra di più rispetto a un infusionato filtrato."),
    ["hara, tema hara-anticancer", "rosen, tema rosen-salute", "Treccani — antiossidante"],
    ["salute_catechine"],
    [
        ("Salute: scienza vs tradizione", "/impara/controversie/salute-scienza-vs-tradizione/", "dibattito aperto"),
        ("Matcha", "/varieta/matcha/", "concentrazione in tazza"),
    ],
)

_entry(
    "egcg",
    "EGCG",
    "Epigallocatechina gallato: la catechina più abbondante e più studiata nel tè verde.",
    ["EGCG", "epigallocatechina gallato"],
    "Se le catechine sono il coro, l'EGCG è la voce che la scienza ascolta più spesso. È la catechina dominante nel tè verde e compare in molti studi su antiossidanti e metabolismo.",
    "Scienza e tazza",
    [
        "In laboratorio l'EGCG mostra attività antiossidante marcata; i trial sull'uomo usano spesso estratti standardizzati, non sempre una tazza quotidiana di sencha.",
        "Non confondere milligrammi in vitro con l'esperienza del bere: piacere, ritualità e consumo regolare contano quanto una molecola isolata.",
    ],
    [
        "Più abbondante in verdi freschi e ben conservati",
        "Sensibile a ossidazione e a infusioni troppo lunghe",
        "Integratori ≠ tazza: biodisponibilità diversa",
    ],
    [
        ("Catechine", "/glossario/catechine/", "famiglia chimica"),
        ("Bevanda vs integratore", "/impara/controversie/bevanda-vs-integratore/", "prospettiva KB"),
        ("Gyokuro", "/varieta/gyokuro/", "verde ricco se fresco"),
    ],
    ("L'EGCG dimostra che il tè cura?", "No da solo. Supporta ricerca preventiva; non sostituisce terapie mediche."),
    ["hara, tema hara-anticancer", "hara, tema hara-metabolismo", "Treccani — epigallocatechina"],
    ["salute_catechine"],
    [("Salute", "/impara/salute/", "quadro completo")],
)

_entry(
    "l-teanina",
    "L-teanina",
    "Aminoacido del tè che modula caffeina e calma, soprattutto nei verdi ombreggiati.",
    ["L-teanina", "teanina"],
    "La L-teanina è l'amico silenzioso della caffeina nel tè. Non la annulla: la accompagna, ammorbidendo l'eccitazione e favorendo una vigilanza più stabile.",
    "Effetto in tazza",
    [
        "Si accumula nelle foglie ombreggiate — gyokuro, tencha per matcha — perché la pianta, al buio, produce più aminoacidi e meno catechine amare.",
        "È uno dei motivi per cui il tè «stimola senza eccitare» rispetto al caffè, almeno per molti bevitori.",
    ],
    [
        "Più presente in gyokuro e matcha di qualità",
        "Associata a onde alfa e concentrazione (sommelier, pellegrino)",
        "Non è un sedativo: è equilibrio",
    ],
    [
        ("Caffeina e stimolazione", "/impara/controversie/caffeina-stimolazione/", "dibattito KB"),
        ("Gyokuro", "/varieta/gyokuro/", "ombra e aminoacidi"),
        ("Caffeina", "/impara/caffeina/", "modulazione"),
    ],
    ("La L-teanina elimina la caffeina?", "No. La modula: meno picco nervoso, effetto più prolungato e dolce."),
    ["pellegrino, tema pellegrino-salute", "sommelier, tema sommelier-proprieta", "Treccani — teanina"],
    ["caffeina_tannini", "salute_catechine"],
    [("Gyokuro", "/varieta/gyokuro/", "alta L-teanina")],
)

_entry(
    "astringenza",
    "Astringenza",
    "Sensazione di ruvidità e contrazione sulla lingua, legata a tannini e catechine.",
    ["astringenza", "tannini", "degustazione"],
    "L'astringenza non è amaro: è quella sensazione che stringe il palato, come un vino giovane o una mela verde. Nel tè verde arriva soprattutto da tannini e catechine estratti troppo a lungo o troppo caldi.",
    "Percezione e preparazione",
    [
        "Un filo di astringenza può dare struttura alla tazza; in eccesso segnala errore di infusione o foglia di bassa qualità.",
        "I verdi giapponesi delicati — gyokuro, sencha di prima qualità — la rivelano se scotti l'acqua o insisti nei secondi.",
    ],
    [
        "Diversa dall'amaro, anche se spesso convivono",
        "Modulabile con temperatura, dosaggio e tempo",
        "Stomaco vuoto: i tannini irritano più facilmente",
    ],
    [
        ("Degustazione", "/impara/degustazione/", "lessico del gusto"),
        ("Sencha", "/varieta/sencha/", "sensibile al calore"),
        ("Preparazione", "/impara/preparazione/", "parametri"),
    ],
    ("L'astringenza è un difetto?", "Non sempre. È un difetto se domina e nasconde aroma e dolcezza; può essere equilibrio in un verde strutturato."),
    ["sommelier, tema sommelier-degustazione", "pellegrino, tema pellegrino-via-del-te"],
    ["degustazione_sensoriale", "preparazione_servizio"],
    [("Sencha", "/varieta/sencha/", "esempio pratico")],
)

_entry(
    "umami",
    "Umami",
    "Quinto gusto, sapidità brodosa percepita nei verdi giapponesi di alta gamma.",
    ["umami", "quinto gusto", "sapidità"],
    "Quinto gusto in tazza: l'umami è burro vegetale, brodo leggero, mare lontano. Non è sale — è rotondità che riempie il palato, soprattutto nel gyokuro e nel matcha di qualità.",
    "Dal glutammato alla foglia ombreggiata",
    [
        "Il termine giapponese umami indica una piacevole sapidità; nel tè verde emerge quando aminoacidi e lavorazione preservano dolcezza e riducono l'amaro grezzo.",
        "Se conosci il parmigiano o una colatura di alici, hai già un ponte sensoriale — senza forzare paragoni che snaturano il tè.",
    ],
    [
        "Segnale di qualità nei verdi ombreggiati",
        "Si perde con acqua bollente e foglie stantie",
        "Lessico utile per degustare come un sommelier",
    ],
    [
        ("Gyokuro", "/varieta/gyokuro/", "umami denso"),
        ("Matcha", "/varieta/matcha/", "corpo pieno"),
        ("Degustazione", "/impara/degustazione/", "scheda sensoriale"),
    ],
    ("L'umami è solo giapponese?", "Il concetto è giapponese; la sensazione compare anche in altri verdi ben fatti, ma è iconica nel gyokuro."),
    ["onuma, tema onuma-salute-pratica", "sommelier, tema sommelier-degustazione", "Treccani — umami"],
    ["degustazione_sensoriale"],
    [("Gyokuro", "/varieta/gyokuro/", "riferimento")],
)

_entry(
    "vapore",
    "Vapore (steaming)",
    "Fissazione al vapore: metodo giapponese che preserva il verde brillante del tè.",
    ["vapore", "steaming", "lavorazione"],
    "Il vapore è il gesto che ferma la foglia al verde. In Giappone, pochi secondi di steam dopo il raccolto bloccano l'ossidazione e fissano l'aroma erbaceo che distingue sencha e gyokuro dalla panificazione cinese.",
    "Lavorazione",
    [
        "Dopo il vapore seguono rolling e essiccazione: la foglia si arrotola, si asciuga, si stabilizza. Ogni fase modula umami, amaro e persistenza.",
        "Il metodo cinese preferisce spesso la padella calda; non è meglio o peggio — è un'altra grammatica del gusto.",
    ],
    [
        "Tipico del Giappone (sencha, gyokuro, bancha)",
        "Preserva colore verde e note vegetali",
        "Alternativa cinese: pan-firing nel wok",
    ],
    [
        ("Lavorazione", "/impara/lavorazione/", "dalla pianta alla tazza"),
        ("Sencha", "/varieta/sencha/", "verde al vapore"),
        ("Wok", "/glossario/wok/", "metodo cinese"),
    ],
    ("Tutto il tè verde è al vapore?", "No. Molti verdi cinesi usano padella; il vapore è dominante in Giappone."),
    ["rosen, tema rosen-lavorazione", "pellegrino, tema pellegrino-lavorazione", "sommelier, tema sommelier-produzione"],
    ["lavorazione_qualità"],
    [("Sencha", "/varieta/sencha/", "esempio")],
)

# Continue with variety terms and ritual terms - I'll add them in the same file
# Due to length, I'll add remaining entries in batches via search_replace or extend the script

# Variety glossary terms
_variety_entries = [
    ("sencha", "Sencha", "Il tè verde quotidiano del Giappone: foglie al sole, aroma di erba fresca.",
     "Il sencha è quello che beve il Giappone a colazione, al lavoro, con gli amici. Foglie esposte al sole, fissate al vapore, arrotolate in aghi sottili.",
     "Lavorazione e gusto", ["Raccolto principale del verde giapponese", "Profilo vegetale, marinezza, amaro controllato", "75 °C circa, non acqua bollente"],
     [("Scheda sencha", "/varieta/sencha/", "preparazione"), ("Gyokuro", "/glossario/gyokuro/", "confronto ombra"), ("Vapore", "/glossario/vapore/", "steaming")],
     ("Sencha e gyokuro sono la stessa pianta?", "Sì, stessa Camellia sinensis. Il gyokuro è ombreggiato prima del raccolto; il sencha cresce al sole."),
     ["pellegrino, pp. 123–125", "rosen, tema rosen-lavorazione"], ["preparazione_servizio", "degustazione_sensoriale"],
     [("Sencha", "/varieta/sencha/", "scheda completa"), ("Bancha", "/glossario/bancha/", "più leggero")]),
    ("gyokuro", "Gyokuro", "Tè ombreggiato: umami denso, infusione tiepida, gesto lento.",
     "Il gyokuro nasce all'ombra. Tre settimane senza sole diretto e la foglia cambia: più L-teanina, meno amaro, un verde profondo che chiede acqua tiepida e attenzione.",
     "Ombreggiatura", ["Massimo rappresentante dell'umami giapponese", "50–60 °C, dosaggio generoso", "Base culturale del tencha e del matcha cerimoniale"],
     [("Scheda gyokuro", "/varieta/gyokuro/", "parametri"), ("Tencha", "/glossario/tencha/", "senza arrotolamento"), ("Umami", "/glossario/umami/", "gusto")],
     ("Perché costa di più?", "L'ombreggiatura riduce la resa e richiede manodopera; paghi qualità e lavorazione."),
     ["sommelier, scheda gyokuro", "pellegrino, verdi giapponesi"], ["lavorazione_qualità", "degustazione_sensoriale"],
     [("Gyokuro", "/varieta/gyokuro/", "scheda")]),
    ("matcha", "Matcha", "Polvere di tencha: bevi la foglia intera, sospesa in acqua.",
     "Il matcha non si infusa e non si scarta: si scia, si frusta, si beve tutto. È tencha macinata, ombreggiata, senza le venature dell'arrotolamento del sencha.",
     "Cerimonia e cucina", ["Usucha leggera e koicha densa in chanoyu", "Matcha da cucina ≠ cerimoniale", "Frusta chasen, non forchetta"],
     [("Scheda matcha", "/varieta/matcha/", "preparazione"), ("Tencha", "/glossario/tencha/", "materia prima"), ("Chasen", "/glossario/chasen/", "frusta")],
     ("Tutto il matcha verde in polvere è uguale?", "No. Grado cerimoniale, da cucina e polveri zuccherate per latte sono mondi diversi."),
     ["rosen, tema rosen-lavorazione", "onuma, tema onuma-matcha-cucina"], ["cerimonia_spiritualita", "cucina_usi_pratici"],
     [("Matcha", "/varieta/matcha/", "scheda")]),
    ("bancha", "Bancha", "Foglia matura o tardiva: quotidiano, leggero, bassa caffeina.",
     "Il bancha è il tè della frigo in bottiglia e della tavola familiare. Foglie più mature, sapore più rustico, caffeina contenuta: perfetto per chi inizia o per la sera.",
     "Quotidianità", ["Non è tè «di serie B»: è tradizione autentica", "Spesso usato per genmaicha", "80 °C, infusioni brevi"],
     [("Scheda bancha", "/varieta/bancha/", "scheda"), ("Genmaicha", "/glossario/genmaicha/", "blend"), ("Kukicha", "/glossario/kukicha/", "rametti")],
     ("Bancha è tè scadente?", "No. È una categoria voluta, con storia e uso quotidiano in Giappone."),
     ["rosen, lavorazione bancha", "onuma, consumo quotidiano"], ["preparazione_servizio", "caffeina_tannini"],
     [("Bancha", "/varieta/bancha/", "scheda")]),
    ("hojicha", "Hojicha", "Tè verde tostato: nocciola, bassa caffeina, sera rassicurante.",
     "L'hojicha profuma di pane tostato. Foglie o rametti passati al calore: il verde diventa ambrato, la caffeina cala, il gesto serale si fa semplice.",
     "Tostatura", ["Ideale dopo cena", "Note di nocciola e caramello leggero", "90 °C, tempi brevi"],
     [("Scheda hojicha", "/varieta/hojicha/", "scheda"), ("Bancha", "/glossario/bancha/", "materia possibile"), ("Caffeina", "/impara/caffeina/", "contenuto")],
     ("L'hojicha è tè nero?", "No. Parte da verde; la tostatura cambia colore e profilo, non la botanica."),
     ["pellegrino, verdi giapponesi", "rosen, tema rosen-lavorazione"], ["lavorazione_qualità", "caffeina_tannini"],
     [("Hojicha", "/varieta/hojicha/", "scheda")]),
    ("genmaicha", "Genmaicha", "Bancha o sencha con riso tostato: comfort cereale in tazza.",
     "Il genmaicha sa di riso in padella e foglia verde insieme. È il tè del comfort: caldo, familiare, gentile con lo stomaco.",
     "Blend giapponese", ["Riso tostato + verde", "Bassa caffeina", "Ottimo per neofiti"],
     [("Scheda genmaicha", "/varieta/genmaicha/", "scheda"), ("Bancha", "/glossario/bancha/", "base comune"), ("Cucina", "/impara/cucina/", "usi")],
     ("Il riso è solo decorazione?", "No. Modella sapore e corpo; è parte integrante del blend."),
     ["onuma, ricette", "pellegrino, varietà"], ["cucina_usi_pratici"],
     [("Genmaicha", "/varieta/genmaicha/", "scheda")]),
    ("kukicha", "Kukicha", "Tè di rametti e fogli: dolce, leggero, economico.",
     "Il kukicha usa parti spesso scartate altrove — steli e fogli — e ne fa un tè dolce e accessibile. Bassa caffeina, quotidianità senza pretese.",
     "Economia della pianta", ["Ago o pezzi di ramo", "Infusione a 80 °C", "Adatto a tutto il giorno"],
     [("Scheda kukicha", "/varieta/kukicha/", "scheda"), ("Bancha", "/glossario/bancha/", "alternativa leggera"), ("Hojicha", "/glossario/hojicha/", "sera")],
     ("Kukicha è inferiore al sencha?", "È diverso: meno pregiato nel mercato premium, ma autentico e piacevole."),
     ["pellegrino, verdi giapponesi"], ["caffeina_tannini", "preparazione_servizio"],
     [("Kukicha", "/varieta/kukicha/", "scheda")]),
    ("tencha", "Tencha", "Foglie ombreggiate non arrotolate: base del matcha.",
     "Il tencha è il gyokuro senza twist: ombreggiato, essiccato, destinato al macinino. Da lui nasce il matcha; non si beve infuso come il sencha.",
     "Verso il matcha", ["Ombreggiatura come gyokuro", "Macinato = matcha", "Vene e nervature rimosse prima della polvere"],
     [("Matcha", "/glossario/matcha/", "prodotto finito"), ("Gyokuro", "/glossario/gyokuro/", "parente"), ("Scheda matcha", "/varieta/matcha/", "uso")],
     ("Si può infusare il tencha?", "Raramente al dettaglio; è materia prima per matcha."),
     ["rosen, lavorazione matcha", "pellegrino, matcha"], ["lavorazione_qualità"],
     [("Matcha", "/varieta/matcha/", "scheda")]),
    ("shincha", "Shincha", "Primo raccolto primaverile del sencha: freschezza effimera.",
     "Lo shincha è la primavera in tazza: raccolto precoce, foglie tenere, aroma vivido che non aspetta. In Giappone è atteso come un evento stagionale.",
     "Stagionalità", ["Sencha di primissimo raccolto", "Bevuto fresco, entro mesi", "Prezzo premium per breve disponibilità"],
     [("Sencha", "/glossario/sencha/", "famiglia"), ("Primavera", "/italia/stagioni/primavera/", "contesto IT"), ("Lavorazione", "/impara/lavorazione/", "raccolto")],
     ("Shincha e sencha sono diversi?", "Lo shincha è sencha di prima fioritura; stessa lavorazione, foglia più giovane."),
     ["rosen, stagionalità", "onuma, quotidianità"], ["storia_cultura", "lavorazione_qualità"],
     [("Sencha", "/varieta/sencha/", "scheda")]),
    ("gunpowder", "Gunpowder (Zhu Cha)", "Foglie arrotolate a perla: verde cinese robusto e viaggiatore.",
     "Il gunpowder sembra munizioni di foglia: perle scure che si aprono in tazza. È il verde che ha attraversato i mari — resistente, intenso, forgiving se sbagli un po' la temperatura.",
     "Cina", ["Pan-firing o vapore + rolling compatto", "85 °C, infusioni ripetute", "Note legnose e leggermente affumicate"],
     [("Scheda gunpowder", "/varieta/gunpowder/", "parametri"), ("Wok", "/glossario/wok/", "lavorazione"), ("Dragon Well", "/glossario/longjing/", "altro cinese")],
     ("Perché si chiama gunpowder?", "Per la forma a pallottola che ricorda la polvere da sparo — nome occidentale, non cinese."),
     ["pellegrino, verdi cinesi", "sommelier, produzione"], ["storia_cultura", "preparazione_servizio"],
     [("Gunpowder", "/varieta/gunpowder/", "scheda")]),
    ("longjing", "Long Jing (Dragon Well)", "Tè piatto di Zhejiang: nocciola, fagiolini, primavera cinese.",
     "Il Long Jing — Dragon Well — è leggenda cinese: foglie pressate a piastra, profilo di nocciola e verdura dolce. Si beve guardando il liquore verde giallo, non di fretta.",
     "Tè famoso", ["Pan-frying in wok", "80 °C, due-tre minuti", "Terroir di West Lake (Hangzhou)"],
     [("Dragon Well", "/varieta/dragon-well/", "scheda sito"), ("Wok", "/glossario/wok/", "padella"), ("Bi Luo Chun", "/varieta/bi-luo-chun/", "altro primaverile")],
     ("Dragon Well e Long Jing sono lo stesso?", "Sì: Long Jing è il nome cinese, Dragon Well la traduzione."),
     ["sommelier, Lung Ching", "pellegrino, Long Jing"], ["storia_cultura", "degustazione_sensoriale"],
     [("Dragon Well", "/varieta/dragon-well/", "scheda")]),
    ("darjeeling", "Darjeeling verde", "Raro verde dell'Himalaya: muschio, montagna, mineralità.",
     "Il Darjeeling verde non è il muscat del Darjeeling nero. È un'altra voce: verde di alta quota, umido, mineralità che ricorda sentieri dopo la pioggia.",
     "India", ["Coltivazione in altitudine", "Infusione lunga, 80 °C", "Per palati abituati a vini bianchi minerali"],
     [("Scheda Darjeeling verde", "/varieta/darjeeling-verde/", "scheda"), ("Degustazione", "/impara/degustazione/", "metodo"), ("Storia", "/impara/storia-cultura/", "India")],
     ("Darjeeling verde = Darjeeling nero?", "Stessa regione, lavorazione diversa: profilo completamente diverso."),
     ["pellegrino, contesto indiano", "sommelier, Nilgiri"], ["storia_cultura", "degustazione_sensoriale"],
     [("Darjeeling verde", "/varieta/darjeeling-verde/", "scheda")]),
    ("cold-brew", "Cold brew", "Infusione a freddo: dolcezza, zero amaro, estate lenta.",
     "Il cold brew non è tè freddo zuccherato da supermercato. È pazienza: foglia in acqua fredda per ore, estrazione gentile, umami che emerge senza astringenza.",
     "Estrazione fredda", ["4–8 ore in frigo per gyokuro", "Bassa caffeina relativa", "Ideale per estate italiana"],
     [("Cold brew gyokuro", "/varieta/cold-brew-gyokuro/", "scheda"), ("Gyokuro", "/glossario/gyokuro/", "foglia adatta"), ("Estate", "/italia/stagioni/estate/", "contesto")],
     ("Cold brew con acqua bollente raffreddata?", "No: è estrazione a freddo dall'inizio; profilo diverso."),
     ["pellegrino, preparazione", "onuma, estate"], ["preparazione_servizio", "caffeina_tannini"],
     [("Cold brew gyokuro", "/varieta/cold-brew-gyokuro/", "scheda")]),
]

for slug, title, desc, intro, ctx, bullets, rl, fq, fonti_list, temi, explore in _variety_entries:
    body = [
        f"Nel tè verde, {title} non è un'etichetta generica: ha storia, lavorazione e un profilo in tazza che lo distingue dalle altre voci del catalogo.",
        f"Capire {title} ti aiuta a scegliere temperatura, momento della giornata e abbinamenti — senza trattare tutti i verdi come la stessa bevanda.",
    ]
    _entry(slug, title, desc, [slug.replace("-", " ")], intro, ctx, body, bullets, rl, fq, fonti_list, temi, explore)

# Ritual / tools entries
_ritual_entries = [
    ("chasen", "Chasen", "Frusta di bambù per matcha: schiuma, gesto, cerimonia.",
     "Il chasen è un bouquet di bambù tagliato a petali. Senza di lui il matcha resta polvere morta in fondo alla ciotola; con lui nasce schiuma e corpo.",
     "Utensile", ["80–120 petali di bambù", "Movimento a M, non frullatore", "Va asciugato e conservato con cura"],
     [("Matcha", "/glossario/matcha/", "bevanda"), ("Chawan", "/glossario/chawan/", "ciotola"), ("Chanoyu", "/glossario/chanoyu/", "rito")],
     ("Posso usare la frusta da cucina?", "Sconsigliato: il chasen incorpora aria senza graffiare."),
     ["onuma, cerimonia", "pellegrino, matcha"], ["cerimonia_spiritualita", "preparazione_servizio"],
     [("Matcha", "/varieta/matcha/", "preparazione")]),
    ("chawan", "Chawan", "Ciotola da tè per matcha: forma, ceramica, mani.",
     "Il chawan è più di un recipiente: è il palmo che accoglie il matcha, il bordo da cui sorseggi in cerimonia, la ceramica che dialoga con stagioni e ospiti.",
     "Ceramica", ["Forme estive e invernali in chanoyu", "Senza manico", "Riscaldare prima del versamento"],
     [("Matcha", "/glossario/matcha/", "contenuto"), ("Chasen", "/glossario/chasen/", "frusta"), ("Cerimonia", "/impara/cerimonia/", "contesto")],
     ("Qualsiasi ciotola va bene?", "Per cerimonia no; per casa sì, se larga e stabile per la frusta."),
     ["sommelier, cerimonie", "onuma, cerimonia"], ["cerimonia_spiritualita"],
     [("Cerimonia", "/impara/cerimonia/", "approfondimento")]),
    ("kyusu", "Kyusu", "Teiera giapponese con manico laterale: sencha quotidiano.",
     "La kyusu è la mano che versa sencha: manico di lato, filtro interno, collo corto. Ti invita a servire tazze piccole, ripetute, concentrazione sul gesto.",
     "Servizio", ["Terracotta o ceramica", "Ideale per sencha e gyokuro", "Non detergenti aggressivi"],
     [("Sencha", "/varieta/sencha/", "uso"), ("Gyokuro", "/varieta/gyokuro/", "dosaggio alto"), ("Preparazione", "/impara/preparazione/", "tecnica")],
     ("Kyusu solo per verde?", "Principalmente sì; dedicare una teiera a un tipo di tè."),
     ["pellegrino, teiere", "sommelier, servizio"], ["preparazione_servizio"],
     [("Sencha", "/varieta/sencha/", "scheda")]),
    ("yunomi", "Yunomi", "Tazza giapponese senza manico per tè quotidiano.",
     "Lo yunomi è la tazza della pausa: senza manico, da tenere a due mani, spesso più alto che largo. Non è cerimoniale come il chawan, ma non è anonimo.",
     "Tazza", ["Per sencha, bancha, hojicha", "Mostra colore del liquore", "Piccole porzioni, più infusioni"],
     [("Sencha", "/varieta/sencha/", "bevanda"), ("Kyusu", "/glossario/kyusu/", "versamento"), ("Degustazione", "/impara/degustazione/", "colore")],
     ("Yunomi e tazza da tè inglese?", "Forme diverse; lo yunomi è per piccole quantità ripetute."),
     ["onuma, quotidianità", "pellegrino, servizio"], ["preparazione_servizio"],
     [("Degustazione", "/impara/degustazione/", "metodo")]),
    ("yixing", "Yixing", "Teiera di terracotta porosa cinese: una teiera, un tè.",
     "Lo yixing assorbe olio del tè nel tempo. Per questo si dedica a un solo tipo — spesso un oolong o un verde — e diventa più buono con gli anni.",
     "Tradizione cinese", ["Argilla di Yixing", "Non lavare con sapone", "Gong fu cha"],
     [("Gong fu cha", "/glossario/gong-fu-cha/", "rito"), ("Gaiwan", "/glossario/gaiwan/", "alternativa"), ("Preparazione", "/impara/preparazione/", "stile")],
     ("Yixing per matcha?", "No: il matcha usa chawan; lo yixing è per infusioni di foglia."),
     ["rosen, teiere Yixing", "pellegrino, tradizioni"], ["preparazione_servizio", "cerimonia_spiritualita"],
     [("Gong fu cha", "/glossario/gong-fu-cha/", "contesto")]),
    ("gaiwan", "Gaiwan", "Coppa con coperchio e sottocoppa: versatilità del gong fu.",
     "Il gaiwan è tre pezzi che fanno uno: infusione, filtro, versamento. Con esso controlli tempo e concentrazione — cuore del gong fu cha.",
     "Gong fu", ["Porcellana o vetro per degustare", "Ideale per bi luo chun e oolong leggeri", "Infusioni multiple brevi"],
     [("Gong fu cha", "/glossario/gong-fu-cha/", "metodo"), ("Bi Luo Chun", "/varieta/bi-luo-chun/", "varietà"), ("Dragon Well", "/varieta/dragon-well/", "varietà")],
     ("Serve esperienza?", "Un po'; ma è uno degli strumenti più didattici per capire il tè."),
     ["sommelier, gong fu", "pellegrino, cinesi"], ["preparazione_servizio"],
     [("Preparazione", "/impara/preparazione/", "guida")]),
    ("wok", "Wok (padella)", "Padella cinese per fissare il verde: Dragon Well e bi luo chun.",
     "Il wok non è solo cucina: nella lavorazione del tè è la padella rovente che ferma l'enzima dell'ossidazione e imprime note di nocciola e fagiolino.",
     "Pan-firing", ["Tipico verdi cinesi", "Alternativa al vapore giapponese", "Richiede maestria del produttore"],
     [("Dragon Well", "/varieta/dragon-well/", "esempio"), ("Vapore", "/glossario/vapore/", "confronto"), ("Lavorazione", "/impara/lavorazione/", "processi")],
     ("Wok e vapore: quale migliore?", "Né migliore né peggiore: tradizioni e profili diversi."),
     ["pellegrino, verdi cinesi", "rosen, lavorazione"], ["lavorazione_qualità"],
     [("Lavorazione", "/impara/lavorazione/", "approfondimento")]),
    ("gong-fu-cha", "Gong fu cha", "Arte cinese del tè: infusioni brevi, ospitalità, abilità.",
     "Il gong fu cha non è spettacolo: è ospitalità concentrata. Piccole tazze, molte infusioni, attenzione all'acqua e al tempo — conviviale più che monacale.",
     "Rito cinese", ["Sette passi classici ma adattabili", "Yixing o gaiwan", "Anche per alcuni verdi"],
     [("Cerimonia Cina vs Giappone", "/impara/controversie/cerimonia-cina-vs-giappone/", "confronto KB"), ("Gaiwan", "/glossario/gaiwan/", "strumento"), ("Preparazione", "/impara/preparazione/", "tecnica")],
     ("Gong fu solo per oolong?", "Nato per oolong; oggi anche verdi e bianchi in stile gong fu."),
     ["sommelier, cerimonie", "pellegrino, tradizioni"], ["cerimonia_spiritualita"],
     [("Cerimonia", "/impara/cerimonia/", "hub")]),
    ("chanoyu", "Chanoyu", "Via del tè giapponese: estetica, ospite, presenza.",
     "Il chanoyu — spesso chiamato cerimonia del tè — è lentezza codificata. Non è solo bere matcha: è giardino, pietra, fiore, umiltà.",
     "Chado", ["Usucha e koicha", "Roji, il giardino d'ingresso", "Sen no Rikyu e semplicità"],
     [("Matcha", "/glossario/matcha/", "bevanda"), ("Roji", "/glossario/roji/", "giardino"), ("Usucha e koicha", "/glossario/usucha/", "stili")],
     ("Chanoyu è per tutti?", "La forma completa richiede studio; il gesto consapevole è accessibile a casa."),
     ["onuma, cerimonia", "pellegrino, chanoyu"], ["cerimonia_spiritualita"],
     [("Cerimonia", "/impara/cerimonia/", "approfondimento")]),
    ("roji", "Roji", "Giardino del tè: transizione dal mondo al chanoyu.",
     "Il roji è il sentiero umido che ti prepara alla tazza. Non è decorazione: è il primo sorso dell'esperienza, fuori dal tempo quotidiano.",
     "Spazio cerimoniale", ["Passaggio simbolico", "Pietre, muschio, acqua", "Pace prima del chashitsu"],
     [("Chanoyu", "/glossario/chanoyu/", "rito"), ("Cerimonia", "/impara/cerimonia/", "contesto"), ("Consumo quotidiano vs rituale", "/impara/controversie/consumo-quotidiano-vs-rituale/", "KB")],
     ("Esiste un roji in Italia?", "Raramente fedele; puoi creare un angolo di transizione anche su un balcone."),
     ["pellegrino, chanoyu", "onuma, cerimonia"], ["cerimonia_spiritualita"],
     [("Cerimonia", "/impara/cerimonia/", "hub")]),
    ("usucha", "Usucha", "Matcha leggero: schiuma fine, consistenza fluida.",
     "L'usucha è il matcha della maggior parte delle cerimonie quotidiane: più acqua, meno polvere, schiuma setosa che si beve in un sorso prolungato.",
     "Stile matcha", ["Più polvere diluita del koicha", "Frullatura energica con chasen", "Per ospiti e pratica regolare"],
     [("Koicha", "/glossario/koicha/", "stile denso"), ("Matcha", "/glossario/matcha/", "polvere"), ("Chasen", "/glossario/chasen/", "strumento")],
     ("Usucha è matcha «light» da bar?", "No: è tradizione cerimoniale, non latte zuccherato."),
     ["onuma, matcha", "sommelier, cerimonie"], ["cerimonia_spiritualita"],
     [("Matcha", "/varieta/matcha/", "scheda")]),
    ("koicha", "Koicha", "Matcha denso: pasta liquida, cerimonia alta.",
     "Il koicha è matcha quasi senza acqua: corpo denso, amaro nobile, gesto lento. Si condivide una sola ciotola tra ospiti in cerimonie formali.",
     "Stile matcha", ["Doppia dose di polvere", "Mescolatura lenta", "Matcha di altissima qualità richiesto"],
     [("Usucha", "/glossario/usucha/", "confronto"), ("Matcha", "/glossario/matcha/", "materia"), ("Chanoyu", "/glossario/chanoyu/", "contesto")],
     ("Koicha per principianti?", "Meglio iniziare con usucha; il koicha è esperienza avanzata."),
     ["pellegrino, chanoyu", "onuma, cerimonia"], ["cerimonia_spiritualita"],
     [("Matcha", "/varieta/matcha/", "scheda")]),
]

for slug, title, desc, intro, ctx, bullets, rl, fq, fonti_list, temi, explore in _ritual_entries:
    body = [
        f"{title} collega gesto e cultura: non è solo oggetto o parola, ma parte di un modo di bere il verde con attenzione.",
        "In Italia puoi incontrarlo nei tea shop, nei corsi di preparazione o nelle schede varietà: riconoscerlo ti orienta tra utensili e rituali diversi.",
    ]
    _entry(slug, title, desc, [slug.replace("-", " ")], intro, ctx, body, bullets, rl, fq, fonti_list, temi, explore)


def main() -> None:
    GLOSS_DIR.mkdir(parents=True, exist_ok=True)
    for slug, doc in ENTRIES.items():
        path = GLOSS_DIR / f"{slug}.json"
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {path.name}")
    print(f"Total: {len(ENTRIES)} glossary entries")


if __name__ == "__main__":
    main()
