#!/usr/bin/env python3
"""Generate 11 new variety JSON files (Tier A + B from source audit)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VAR_DIR = ROOT / "content" / "varieta"

VARIETIES: list[dict[str, Any]] = [
    {
        "slug": "jeoncha",
        "title": "Jeoncha — verde coreano di primavera",
        "description": "Jeoncha (Korean Green) è tè verde coreano raccolto a mano tra aprile e maggio: aroma vegetale, liquore vellutato. Scheda e preparazione.",
        "keywords": ["jeoncha", "korean green", "tè verde coreano", "Camellia sinensis", "Corea"],
        "origine": "Corea",
        "stile": "jeoncha",
        "caffeina": "Media",
        "stagione": "Primavera",
        "cultivar": "Cultivar coreana (raccolto Gogu–Ipha)",
        "sort_order": 13,
        "brew": {"temp": 78, "grams": 2.5, "seconds": 150, "infusions": "1"},
        "lead": "Piccole foglie tenere, vapore e tostatura leggera: il jeoncha unisce la marinezza giapponese alla morbidezza vellutata di alcuni verdi cinesi.",
        "sensory": {
            "aspetto": "Verde intenso, leggermente arricciato",
            "aroma": "Erbaceo, prato fiorito",
            "gusto": "Rotondo, vellutato",
            "retrogusto": "Persistente, delicato",
        },
        "equipment": ["Kyusu in porcellana o ceramica", "Acqua 75–80 °C"],
        "steps": [
            {"text": "2–3 g per 150 ml, acqua a 75–80 °C", "duration": "2 min"},
            {"text": "Infusione singola 2–3 minuti", "duration": "3 min"},
            {"text": "Versa tutto il liquore in una volta", "duration": "30 sec"},
        ],
        "errors": [
            "Acqua bollente (amaro vegetale)",
            "Infusione troppo lunga",
            "Confonderlo con sencha giapponese (dosaggio diverso)",
        ],
        "callout": "In Corea il jeoncha accompagna riso e pesce: in Italia prova la prima infusione dopo un sushi leggero o un pranzo di mare senza condimenti pesanti.",
        "pairings": ["Pesce crudo e riso", "Verdure al vapore"],
        "faq": [
            ("Jeoncha e Korean Green sono la stessa cosa?", "Sì: jeoncha è il nome coreano; in Occidente spesso compare come Korean Green."),
            ("Perché ricorda il sencha?", "Stabilizzazione al vapore e tostatura leggera avvicinano il profilo ai verdi giapponesi, con corpo più morbido in bocca."),
        ],
        "deep_title": "Raccolto primaverile coreano",
        "deep_text": "Raccolto a mano tra aprile e maggio, nei periodi Gogu e Ipha del calendario lunare. Foglie tenere leggermente arricciate, stabilizzate al vapore e tostate con parsimonia. Liquore giallo dorato, profumo di prato fiorito simile ai sencha primaverili giapponesi, sapore rotondo e vellutato.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Korean Green", "pages": "113"},
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-tradizioni", "sotto_tema": "Tè verde coreano (Jeoncha)", "pages": "2698–2727"},
        ],
        "related_slugs": ["sencha", "gyokuro"],
        "temi_kb": ["lavorazione_qualità", "storia_cultura"],
        "momenti": ["pausa"],
        "stagioni_nav": ["primavera"],
        "related_links": [
            ("Sencha", "/varieta/sencha/", "verde giapponese affine"),
            ("Primavera", "/italia/stagioni/primavera/", "stagione del raccolto"),
        ],
        "explore_next": [
            ("Sencha", "/varieta/sencha/", "confronto giapponese"),
            ("Gyokuro", "/varieta/gyokuro/", "più ombra e umami"),
            ("Glossario sencha", "/glossario/sencha/", "termine collegato"),
            ("Storia e cultura", "/impara/storia-cultura/", "contesto orientale"),
        ],
    },
    {
        "slug": "huangshan-maofeng",
        "title": "Huang Shan Mao Feng — lanugine delle Montagne Gialle",
        "description": "Huang Shan Mao Feng è tè verde dell'Anhui: germogli lanuginosi, profilo floreale e di castagna. Parametri di infusione e abbinamenti.",
        "keywords": ["huang shan mao feng", "mao feng", "tè verde cinese", "Anhui", "Camellia sinensis"],
        "origine": "Cina",
        "stile": "huangshan-maofeng",
        "caffeina": "Media",
        "stagione": "Primavera",
        "cultivar": "Cultivar dell'Huang Shan, Anhui",
        "sort_order": 14,
        "brew": {"temp": 75, "grams": 3, "seconds": 210, "infusions": "3-4"},
        "lead": "Lanugine bianca su foglie lunghe e brillanti: lo Huang Shan Mao Feng profuma di fiori e frutta in guscio, con dolcezza discreta in tazza.",
        "sensory": {
            "aspetto": "Verde brillante, lanugine bianca impalpabile",
            "aroma": "Floreale, frutta in guscio",
            "gusto": "Fresco, delicato",
            "retrogusto": "Leggermente dolce",
        },
        "equipment": ["Gaiwan o teiera in porcellana", "Acqua 75–80 °C"],
        "steps": [
            {"text": "Stile occidentale: 3 g in 150 ml a 75 °C per 3–4 min", "duration": "4 min"},
            {"text": "Stile orientale: 5 g in 150 ml a 80 °C per 30–40 sec", "duration": "40 sec"},
            {"text": "Ripeti 3–4 infusioni brevi", "duration": "2 min"},
        ],
        "errors": [
            "Acqua troppo calda che appiattisce i fiori",
            "Troppa foglia in tazza piccola",
            "Infusione unica troppo lunga in stile orientale",
        ],
        "callout": "Tra Anhui e Jiangsu: se ami il bi luo chun, lo Huang Shan Mao Feng è il passo successivo verso note di castagna e nebbia montana — perfetto in pausa pomeridiana primaverile.",
        "pairings": ["Frutta secca e castagne", "Verdure tenere primaverili"],
        "faq": [
            ("Cosa significa Mao Feng?", "Punte pelose: indica germogli ricoperti da sottile lanugine bianca, segno di raccolta precoce."),
            ("Occidentale o orientale?", "Entrambi funzionano: infusione singola più semplile; gaiwan multipla esalta la progressione aromatica."),
        ],
        "deep_title": "Montagne Gialle dell'Anhui",
        "deep_text": "Originario dell'altopiano Huang Shan, esportato dal tardo Ottocento. Raccolta delle due prime foglioline e del germoglio. Foglie verde brillante con lanugine, liquore giallo-verde dal profilo floreale e di castagna. Uno dei verdi cinesi più rinomati al mondo.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Huang Shan Mao Feng", "pages": "114"},
        ],
        "related_slugs": ["bi-luo-chun", "dragon-well", "tai-ping-hou-kui"],
        "temi_kb": ["lavorazione_qualità", "degustazione_sensoriale"],
        "momenti": ["pausa"],
        "stagioni_nav": ["primavera"],
        "related_links": [
            ("Bi Luo Chun", "/varieta/bi-luo-chun/", "altra primavera cinese"),
            ("Tai Ping Hou Kui", "/varieta/tai-ping-hou-kui/", "stesso Anhui"),
        ],
        "explore_next": [
            ("Dragon Well", "/varieta/dragon-well/", "verde in padella"),
            ("Gaiwan", "/glossario/gaiwan/", "strumento ideale"),
            ("Degustazione", "/impara/degustazione/", "leggi il profilo"),
            ("Primavera", "/italia/stagioni/primavera/", "stagione"),
        ],
    },
    {
        "slug": "tai-ping-hou-kui",
        "title": "Tai Ping Hou Kui — foglie piatte di Anhui",
        "description": "Tai Ping Hou Kui è tè verde raro dell'Anhui: foglie pressate lunghe, profilo floreale di orchidea. Scheda sensoriale e preparazione.",
        "keywords": ["tai ping hou kui", "hou kui", "tè verde cinese", "Anhui", "Camellia sinensis"],
        "origine": "Cina",
        "stile": "tai-ping-hou-kui",
        "caffeina": "Media",
        "stagione": "Primavera",
        "cultivar": "Shi-da (Anhui, alta quota)",
        "sort_order": 15,
        "brew": {"temp": 75, "grams": 3, "seconds": 240, "infusions": "3-4"},
        "lead": "Foglie lunghissime, piatte, con impronta a scacchiera: il Tai Ping Hou Kui è raro, elegante, profumo di orchidea su liquore verde chiaro.",
        "sensory": {
            "aspetto": "Verde pallido, foglie tese e appiattite",
            "aroma": "Floreale, orchidea",
            "gusto": "Delicato, fresco",
            "retrogusto": "Pulito, persistente",
        },
        "equipment": ["Teiera o gaiwan in porcellana o vetro", "Acqua 75 °C"],
        "steps": [
            {"text": "3 g in 150 ml a 75 °C per 4 minuti (stile occidentale)", "duration": "4 min"},
            {"text": "Oppure 5 g in 150 ml, 30–40 sec (stile orientale)", "duration": "40 sec"},
            {"text": "3–4 infusioni successive brevi", "duration": "2 min"},
        ],
        "errors": [
            "Spezzare le foglie lunghe (perdi la presentazione)",
            "Acqua bollente",
            "Dosaggio eccessivo per un tè così delicato",
        ],
        "callout": "Per le grandi occasioni — Pellegrino lo suggerisce al mattino o nel pomeriggio. In Italia, un Hou Kui merita una tazza senza distrazioni, come un grande vino bianco strutturato.",
        "pairings": ["Piatti di pesce leggeri", "Verdure al vapore"],
        "faq": [
            ("Perché «Hou Kui»?", "Leggenda del «primo tè delle scimmie»: hou significa scimmia, kui il primo — per l'area inaccessibile di raccolta."),
            ("Perché le venature rossastre?", "Effetto della pressatura in lavorazione; in infusione è normale e distintivo."),
        ],
        "deep_title": "Cultivar Shi-da in alta quota",
        "deep_text": "Coltivato ad alta altitudine nella contea di Tai Ping, Anhui. Si raccolgono a mano solo le due foglie apicali con germoglio, con alto scarto in lavorazione. Foglie pressate assumono forma inconfondibile; liquore verde chiaro, profumo floreale di orchidea.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Tai Ping Hou Kui", "pages": "115"},
        ],
        "related_slugs": ["huangshan-maofeng", "bi-luo-chun"],
        "temi_kb": ["lavorazione_qualità", "storia_cultura"],
        "momenti": ["pausa"],
        "stagioni_nav": ["primavera"],
        "related_links": [
            ("Huang Shan Mao Feng", "/varieta/huangshan-maofeng/", "stesso Anhui"),
            ("Bi Luo Chun", "/varieta/bi-luo-chun/", "primavera cinese"),
        ],
        "explore_next": [
            ("Huang Shan Mao Feng", "/varieta/huangshan-maofeng/", "confronto Anhui"),
            ("Gaiwan", "/glossario/gaiwan/", "infusioni multiple"),
            ("Degustazione", "/impara/degustazione/", "scheda sensoriale"),
            ("Primavera", "/italia/stagioni/primavera/", "stagione"),
        ],
    },
    {
        "slug": "xin-yang-mao-jian",
        "title": "Xin Yang Mao Jian — mao jian dell'Henan",
        "description": "Xin Yang Mao Jian è tè verde cinese dell'Henan: germogli lanuginosi, freschezza erbacea intensa. Preparazione e profilo in tazza.",
        "keywords": ["xin yang mao jian", "mao jian", "tè verde cinese", "Henan", "Camellia sinensis"],
        "origine": "Cina",
        "stile": "xin-yang-mao-jian",
        "caffeina": "Media",
        "stagione": "Primavera",
        "cultivar": "Cultivar di Xin Yang, Henan",
        "sort_order": 16,
        "brew": {"temp": 70, "grams": 2.5, "seconds": 210, "infusions": "3"},
        "lead": "Germogli lanuginosi e foglie sottili: lo Xin Yang Mao Jian unisce erbaceità viva a retrogusto rinfrescante — tè da riservare alle occasioni speciali.",
        "sensory": {
            "aspetto": "Verde scuro, piccole foglie arrotolate",
            "aroma": "Erbaceo, castagna lessa",
            "gusto": "Intenso, fresco",
            "retrogusto": "Persistente, rinfrescante",
        },
        "equipment": ["Teiera in porcellana o vetro", "Acqua 70–80 °C"],
        "steps": [
            {"text": "2–3 g in 150 ml a 70 °C per 3–4 min", "duration": "4 min"},
            {"text": "Stile orientale: 5 g, 30–40 sec a 70–80 °C", "duration": "40 sec"},
            {"text": "Fino a 3 infusioni successive", "duration": "2 min"},
        ],
        "errors": [
            "Temperatura oltre 80 °C (amaro erbaceo)",
            "Infusione troppo breve in stile occidentale",
            "Acquistare qualità scadente senza lanugine visibile",
        ],
        "callout": "Non sempre in vetrina nei tea shop italiani: quando lo trovi, trattalo come un grande bianco strutturato — poche tazze, massima attenzione.",
        "pairings": ["Verdure primaverili", "Piatti leggeri non speziati"],
        "faq": [
            ("Cosa significa Mao Jian?", "Punte pelose: prima foglia con germoglio, coperti da lanugine."),
            ("Perché 70 °C?", "Pellegrino suggerisce temperatura più bassa per preservare freschezza erbacea e note floreali."),
        ],
        "deep_title": "Henan e raccolta selettiva",
        "deep_text": "Prodotto nella regione di Xin Yang, provincia di Henan, tra i verdi cinesi più stimati. Gusto soave e freschezza erbacea; raccolta della prima foglia con germoglio. Foglie verde scuro, liquore verde-giallo intenso con retrogusto rinfrescante.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Xin Yang Mao Jian", "pages": "118"},
        ],
        "related_slugs": ["huangshan-maofeng", "bi-luo-chun"],
        "temi_kb": ["lavorazione_qualità", "degustazione_sensoriale"],
        "momenti": ["pausa"],
        "stagioni_nav": ["primavera"],
        "related_links": [
            ("Huang Shan Mao Feng", "/varieta/huangshan-maofeng/", "altro mao"),
            ("Bi Luo Chun", "/varieta/bi-luo-chun/", "primavera delicata"),
        ],
        "explore_next": [
            ("Huang Shan Mao Feng", "/varieta/huangshan-maofeng/", "confronto premium"),
            ("Gaiwan", "/glossario/gaiwan/", "infusioni brevi"),
            ("Degustazione", "/impara/degustazione/", "metodo"),
            ("Primavera", "/italia/stagioni/primavera/", "stagione"),
        ],
    },
    {
        "slug": "snow-bud",
        "title": "Snow Bud — germoglio di neve del Fujian",
        "description": "Snow Bud (Xue Ya) è tè verde del Fujian oltre i 1000 m: cultivar Da Bai, lanugine argentea, profilo dolce e di castagna arrosto.",
        "keywords": ["snow bud", "xue ya", "tè verde cinese", "Fujian", "Camellia sinensis"],
        "origine": "Cina",
        "stile": "snow-bud",
        "caffeina": "Bassa",
        "stagione": "Primavera",
        "cultivar": "Da Bai (Fujian, >1000 m)",
        "sort_order": 17,
        "brew": {"temp": 78, "grams": 2.5, "seconds": 150, "infusions": "1"},
        "lead": "Germogli argentati come neve appena caduta: lo Snow Bud unisce la cultivar del tè bianco a una lavorazione verde — morbido, dolce, di castagna arrosto.",
        "sensory": {
            "aspetto": "Verde chiaro, germogli con lanugine bianca",
            "aroma": "Erbaceo, floreale delicato",
            "gusto": "Morbido, leggermente dolce",
            "retrogusto": "Castagna arrosto, persistente",
        },
        "equipment": ["Gaiwan in porcellana o vetro", "Acqua 75–80 °C"],
        "steps": [
            {"text": "2–3 g in 150 ml a 75–80 °C", "duration": "2 min"},
            {"text": "Infusione singola 2–3 minuti", "duration": "3 min"},
            {"text": "Non riinfondere: germogli esauriti rapidamente", "duration": "30 sec"},
        ],
        "errors": [
            "Acqua bollente che brucia i germogli",
            "Dosaggio eccessivo (amaro floreale)",
            "Confonderlo con bai mu dan (è lavorato come verde)",
        ],
        "callout": "Abbina cibi salati leggeri e verdure crude — in primavera italiana, un'insalata di rucola e finocchio senza aceto forte lascia emergere la dolcezza del liquore.",
        "pairings": ["Verdure crude", "Cibi salati leggeri"],
        "faq": [
            ("Perché «germoglio di neve»?", "Xue Ya in cinese: i germogli apicali coperti di lanugine bianca ricordano la neve."),
            ("È un tè bianco?", "No: usa cultivar Da Bai tipica del bianco, ma la lavorazione segue il verde."),
        ],
        "deep_title": "Da Bai in alta quota",
        "deep_text": "Prodotto oltre i 1000 metri nel Fujian. Raccolta primaverile accurata di foglie e germogli apicali lanuginosi. Liquore giallo paglierino, note fruttate e castagna arrosto. Particolare incrocio tra tradizione bianca e lavorazione verde.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Snow Bud (Xue Ya)", "pages": "119"},
        ],
        "related_slugs": ["bi-luo-chun", "dragon-well"],
        "temi_kb": ["lavorazione_qualità", "degustazione_sensoriale"],
        "momenti": ["pausa"],
        "stagioni_nav": ["primavera"],
        "related_links": [
            ("Bi Luo Chun", "/varieta/bi-luo-chun/", "primavera delicata"),
            ("Dragon Well", "/varieta/dragon-well/", "verde cinese"),
        ],
        "explore_next": [
            ("Bi Luo Chun", "/varieta/bi-luo-chun/", "primavera cinese"),
            ("Primavera", "/italia/stagioni/primavera/", "stagione"),
            ("Degustazione", "/impara/degustazione/", "profilo"),
            ("Gaiwan", "/glossario/gaiwan/", "strumento"),
        ],
    },
    {
        "slug": "chun-mee",
        "title": "Chun Mee — sopracciglia preziose",
        "description": "Chun Mee è tè verde cinese dal gusto deciso: foglie a sopracciglio, profilo erbaceo simile al gunpowder. Preparazione e abbinamenti.",
        "keywords": ["chun mee", "chun mei", "tè verde cinese", "Camellia sinensis", "export"],
        "origine": "Cina",
        "stile": "chun-mee",
        "caffeina": "Media",
        "stagione": "Primavera",
        "cultivar": "Cultivar multi-provincia (Chun Mee)",
        "sort_order": 18,
        "brew": {"temp": 83, "grams": 2.5, "seconds": 150, "infusions": "1-2"},
        "lead": "Foglie arrotolate a sopracciglio, verde intenso: il Chun Mee è popolare, robusto, onesto — il verde cinese che ha attraversato mercati e tè alla menta.",
        "sensory": {
            "aspetto": "Verde intenso, curve a sopracciglio (~1 cm)",
            "aroma": "Erbaceo intenso",
            "gusto": "Forte, simile al gunpowder",
            "retrogusto": "Persistente, leggermente aspro",
        },
        "equipment": ["Teiera in ceramica o porcellana", "Acqua 80–85 °C"],
        "steps": [
            {"text": "Sciacqua le foglie con acqua calda per pochi secondi", "duration": "10 sec"},
            {"text": "2–3 g in 150 ml a 80–85 °C per 2–3 min", "duration": "3 min"},
            {"text": "Versa tutto; adatto anche freddo o con menta", "duration": "30 sec"},
        ],
        "errors": [
            "Saltare lo sciacquo con qualità economiche (asprezza)",
            "Infusione troppo lunga",
            "Confonderlo con gunpowder (forma diversa, profilo affine)",
        ],
        "callout": "Base storica del tè alla menta marocchino: in estate italiana, prova freddo con menta fresca — più pulito del gunpowder se la qualità è buona (gradi alti come 41022).",
        "pairings": ["Menta e dolce leggero", "Piatti speziati moderati"],
        "faq": [
            ("Cosa significa Chun Mee?", "Preziose sopracciglia: la forma arrotolata ricorda un sopracciglio."),
            ("Come scegliere la qualità?", "I gradi numerici indicano qualità: evita i più bassi (8147); Moonpalace e simili sono più floreali e puliti."),
        ],
        "deep_title": "Export e tè alla menta",
        "deep_text": "Prodotto in diverse province cinesi, molto popolare all'estero. Foglie arrotolate a sopracciglio; profilo simile al gunpowder ma forma diversa. Qualità scadenti lasciano sensazione di polvere in bocca; le pregiate (41022, Moonpalace) offrono gusto forte e profumo fiorito.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Chun Mee", "pages": "120"},
            {"author": "Rosen, Diana", "title": "Il libro del tè verde", "tema": "rosen-lavorazione", "sotto_tema": "Chunmee", "pages": "875–882"},
        ],
        "related_slugs": ["gunpowder", "dragon-well"],
        "temi_kb": ["storia_cultura", "preparazione_servizio"],
        "momenti": ["pausa", "aperitivo"],
        "stagioni_nav": ["estate"],
        "related_links": [
            ("Gunpowder", "/varieta/gunpowder/", "verde robusto affine"),
            ("Storia", "/impara/storia-cultura/", "commercio del tè"),
        ],
        "explore_next": [
            ("Gunpowder", "/varieta/gunpowder/", "confronto robusto"),
            ("Estate", "/italia/stagioni/estate/", "freddo e menta"),
            ("Preparazione", "/impara/preparazione/", "sciacquo foglie"),
            ("Aperitivo", "/italia/momenti/aperitivo/", "momento"),
        ],
    },
    {
        "slug": "liu-an-guapian",
        "title": "Lu An Gua Pian — semi di melone dell'Anhui",
        "description": "Lu An Gua Pian è tè verde dell'Anhui senza germoglio: foglie mature a forma di seme di melone, profilo corposo e dolce.",
        "keywords": ["lu an gua pian", "gua pian", "tè verde cinese", "Anhui", "Camellia sinensis"],
        "origine": "Cina",
        "stile": "liu-an-guapian",
        "caffeina": "Media",
        "stagione": "Primavera",
        "cultivar": "Cultivar di Lu An, Anhui (foglie mature)",
        "sort_order": 19,
        "brew": {"temp": 78, "grams": 3, "seconds": 180, "infusions": "4-5"},
        "lead": "Foglie grandi senza germoglio, lavorate in wok con scopetta di paglia: il Lu An Gua Pian ha forma di seme di melone e sapore corposo, miele e frutta secca tostata.",
        "sensory": {
            "aspetto": "Verde scuro, lungo, leggermente arricciato",
            "aroma": "Erbaceo, frutta secca tostata",
            "gusto": "Corposo, leggermente dolce",
            "retrogusto": "Prolungato, miele",
        },
        "equipment": ["Gaiwan in porcellana o vetro", "Acqua 75–80 °C"],
        "steps": [
            {"text": "3 g in 150 ml a 75–80 °C per 3 min (occidentale)", "duration": "3 min"},
            {"text": "5 g in 150 ml, 30 sec (orientale)", "duration": "30 sec"},
            {"text": "4–5 infusioni successive da 30 sec", "duration": "2 min"},
        ],
        "errors": [
            "Trattarlo come tè a germoglio (dosaggio da bi luo chun)",
            "Acqua bollente",
            "Infusione unica troppo breve per foglie mature",
        ],
        "callout": "Pellegrino suggerisce prosciutto e melone: abbinamento italiano naturale — salato dolce che esalta la dolcezza vegetale del liquore.",
        "pairings": ["Prosciutto e melone", "Verdure a foglia"],
        "faq": [
            ("Perché «semi di melone»?", "Gua Pian: le foglie mature lavorate assomigliano a semi di melone, non usano il germoglio."),
            ("Perché la lavorazione è così laboriosa?", "Stabilizzazione in wok con scopetta di paglia, poi riscaldamento in cesta ~60 volte: tè di grande artigianalità."),
        ],
        "deep_title": "Senza germoglio, solo foglia",
        "deep_text": "Prodotto nella contea di Lu An, Anhui. A differenza di molti verdi pregiati usa foglie più grandi e tenere, non il germoglio. Lavorazione in wok con scopetta di paglia e cicli brevi di riscaldamento ripetuti. Liquore giallo-verde corposo, note di frutta secca tostata e miele.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Lu An Gua Pian", "pages": "122"},
        ],
        "related_slugs": ["dragon-well", "huangshan-maofeng"],
        "temi_kb": ["lavorazione_qualità", "cucina_usi_pratici"],
        "momenti": ["pausa"],
        "stagioni_nav": ["primavera", "estate"],
        "related_links": [
            ("Dragon Well", "/varieta/dragon-well/", "wok cinese"),
            ("Abbinamenti", "/italia/abbinamenti/", "prosciutto e melone"),
        ],
        "explore_next": [
            ("Dragon Well", "/varieta/dragon-well/", "altro wok"),
            ("Abbinamenti", "/italia/abbinamenti/", "cibo e tè"),
            ("Wok", "/glossario/wok/", "lavorazione"),
            ("Huang Shan Mao Feng", "/varieta/huangshan-maofeng/", "Anhui"),
        ],
    },
    {
        "slug": "nilgiri-verde",
        "title": "Nilgiri verde — monti azzurri del Sud India",
        "description": "Nilgiri verde è tè dell'altopiano indiano meridionale: profilo vegetale e agrumato, raccolta tutto l'anno. Scheda sensoriale e infusione.",
        "keywords": ["nilgiri verde", "nilgiri green", "tè verde indiano", "India", "Camellia sinensis"],
        "origine": "India",
        "stile": "nilgiri",
        "caffeina": "Media",
        "stagione": "Tutto l'anno",
        "cultivar": "Cultivar dell'altopiano Nilgiri",
        "sort_order": 20,
        "brew": {"temp": 73, "grams": 2.5, "seconds": 90, "infusions": "1-2"},
        "lead": "Monti azzurri del Tamil Nadu: il Nilgiri verde profuma di verdure cotte e lime, liquore dorato leggero — l'India oltre il Darjeeling che già conosci.",
        "sensory": {
            "aspetto": "Foglie grandi, sottili, verde grigiastro",
            "aroma": "Verdure cotte, lime, gardenia",
            "gusto": "Agrumato, vegetale, leggermente tostato",
            "retrogusto": "Vegetale, astringente medio",
        },
        "equipment": ["Teiera in porcellana o terracotta", "Acqua 70–75 °C"],
        "steps": [
            {"text": "2–3 g in 150 ml a 70–75 °C", "duration": "1 min"},
            {"text": "Infusione 1–2 minuti (Sommelier: 70–75 °C)", "duration": "2 min"},
            {"text": "Liquore dorato chiaro: non surinfondere", "duration": "30 sec"},
        ],
        "errors": [
            "Temperatura da tè nero indiano (90 °C)",
            "Confonderlo con Nilgiri CTC per masala chai",
            "Infusione troppo lunga (astringenza)",
        ],
        "callout": "Mentre il Darjeeling verde parla l'himalayano, il Nilgiri verde è più aperto e agrumato — ideale per chi cerca un verde indiano accessibile tutto l'anno, anche fuori stagione del first flush.",
        "pairings": ["Verdure grigliate", "Pesce leggermente speziato"],
        "faq": [
            ("Nilgiri verde e Nilgiri nero sono la stessa cosa?", "Stessa regione, lavorazioni diverse: il verde ortodosso è raro rispetto al CTC per chai."),
            ("Quando è il miglior raccolto?", "Pellegrino indica gennaio come migliore per la regione; il verde premium si trova tutto l'anno con profili variabili."),
        ],
        "deep_title": "Monti azzurri e verde ortodosso",
        "deep_text": "L'altopiano Nilgiri, scoperto nel 1840, è seconda regione produttrice indiana. Raccolta durante tutto l'anno; miglior raccolto a gennaio. Il verde ortodosso (es. estate Hari Talvar) offre foglie grandi verde grigiastro, liquore dorato con note di lime, verdure cotte e noce moscata — corpo leggero, astringenza media.",
        "biblio": [
            {"author": "Bisogno, Victoria; Pettigrew, Jane", "title": "Manuale del sommelier del tè", "tema": "sommelier-degustazione", "sotto_tema": "Tè verde indiano (Nilgiri)", "pages": "2776–2791"},
            {"author": "Rosen, Diana", "title": "Il libro del tè verde", "tema": "rosen-lavorazione", "sotto_tema": "Nilgiri Green", "pages": "1292–1305"},
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Nilgiri (contesto regionale)", "pages": "151"},
        ],
        "related_slugs": ["darjeeling-verde", "sencha"],
        "temi_kb": ["storia_cultura", "degustazione_sensoriale"],
        "momenti": ["pausa"],
        "stagioni_nav": ["inverno", "primavera"],
        "related_links": [
            ("Darjeeling verde", "/varieta/darjeeling-verde/", "India settentrionale"),
            ("Degustazione", "/impara/degustazione/", "scheda sensoriale"),
        ],
        "explore_next": [
            ("Darjeeling verde", "/varieta/darjeeling-verde/", "confronto indiano"),
            ("Storia e cultura", "/impara/storia-cultura/", "India del tè"),
            ("Degustazione", "/impara/degustazione/", "profilo"),
            ("Glossario Darjeeling", "/glossario/darjeeling/", "contesto Himalaya"),
        ],
    },
    {
        "slug": "shincha",
        "title": "Shincha — nuovo tè di primavera",
        "description": "Shincha è il primo raccolto primaverile giapponese: foglie tenere, massima freschezza clorofilica. Disponibilità stagionale e preparazione.",
        "keywords": ["shincha", "tè verde giapponese", "primo raccolto", "Camellia sinensis", "Giappone"],
        "origine": "Giappone",
        "stile": "shincha",
        "caffeina": "Media",
        "stagione": "Primavera",
        "cultivar": "Yabukita (primo raccolto primaverile)",
        "sort_order": 21,
        "brew": {"temp": 75, "grams": 3, "seconds": 120, "infusions": "2-3"},
        "lead": "Nuovo tè: lo shincha è il sencha del primo raccolto, più tenue, più scuro, più vivido — una finestra breve che profuma di erba appena tagliata.",
        "sensory": {
            "aspetto": "Aghi verdi scuri e teneri",
            "aroma": "Clorofilla, erba di montagna",
            "gusto": "Fresco, sapido, leggermente amaro",
            "retrogusto": "Marino, persistente",
        },
        "equipment": ["Kyusu in porcellana o ceramica", "Acqua 75 °C"],
        "steps": [
            {"text": "2–3 g in 150 ml a 75 °C per 2–3 min", "duration": "3 min"},
            {"text": "Stile kyusu: 10 g in 210 ml a 80 °C per 1 min", "duration": "1 min"},
            {"text": "2–3 infusioni con acqua nuova", "duration": "2 min"},
        ],
        "errors": [
            "Conservarlo oltre la stagione aspettandosi la stessa vivacità",
            "Acqua bollente",
            "Confonderlo con sencha tardivo (stesso nome commerciale generico)",
        ],
        "callout": "In Giappone lo shincha si beve appena arrivato: in Italia, cercalo tra aprile e giugno — un rituale primaverile paragonabile al primo olio nuovo.",
        "pairings": ["Pesce crudo", "Verdure al vapore"],
        "faq": [
            ("Shincha e sencha?", "Lo shincha è sencha del primo raccolto primaverile — più pregiato e stagionale."),
            ("Come riconoscerlo?", "Foglie più tenere e scure indicano qualità superiore, come suggerisce Pellegrino."),
        ],
        "deep_title": "Primo raccolto giapponese",
        "deep_text": "Shincha significa «nuovo tè»: il sencha più pregiato del primo raccolto primaverile. Stessa lavorazione al vapore e rolling ad ago, ma foglie più tenere e scure. Profumo di clorofilla e erba di montagna; disponibilità limitata dopo la raccolta.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Sencha (Shincha)", "pages": "126"},
        ],
        "related_slugs": ["sencha", "gyokuro"],
        "temi_kb": ["lavorazione_qualità", "degustazione_sensoriale"],
        "momenti": ["pausa"],
        "stagioni_nav": ["primavera"],
        "related_links": [
            ("Sencha", "/varieta/sencha/", "verde quotidiano"),
            ("Glossario shincha", "/glossario/shincha/", "definizione"),
        ],
        "explore_next": [
            ("Sencha", "/varieta/sencha/", "base quotidiana"),
            ("Primavera", "/italia/stagioni/primavera/", "calendario"),
            ("Glossario shincha", "/glossario/shincha/", "termine"),
            ("Gyokuro", "/varieta/gyokuro/", "passo successivo"),
        ],
        "percorso_tappa": None,
    },
    {
        "slug": "kabusecha",
        "title": "Kabusecha — sencha ombreggiato",
        "description": "Kabusecha è sencha prodotto coprendo le piante con telo prima del raccolto: più umami del sencha, meno estremo del gyokuro.",
        "keywords": ["kabusecha", "tè verde giapponese", "ombreggiatura", "Camellia sinensis", "Giappone"],
        "origine": "Giappone",
        "stile": "kabusecha",
        "caffeina": "Media",
        "stagione": "Primavera",
        "cultivar": "Yabukita (ombreggiatura breve)",
        "sort_order": 22,
        "brew": {"temp": 70, "grams": 3, "seconds": 90, "infusions": "2-3"},
        "lead": "Tra sole e ombra: il kabusecha copre le piante con telo per qualche settimana — più umami del sencha, più accessibile del gyokuro.",
        "sensory": {
            "aspetto": "Aghi verdi medio-scuri",
            "aroma": "Vegetale, alghe, dolcezza discreta",
            "gusto": "Umami moderato, amaro controllato",
            "retrogusto": "Dolce, persistente",
        },
        "equipment": ["Kyusu in ceramica", "Acqua 65–75 °C"],
        "steps": [
            {"text": "2–3 g in 150 ml a 70–75 °C per 2 min", "duration": "2 min"},
            {"text": "Dosaggio generoso in kyusu: infusioni brevi", "duration": "1 min"},
            {"text": "2–3 infusioni con temperatura stabile", "duration": "2 min"},
        ],
        "errors": [
            "Prepararlo come sencha al sole (acqua troppo calda)",
            "Prepararlo come gyokuro puro (dosaggio insufficiente)",
            "Ignorare l'ombreggiatura breve vs gyokuro lungo",
        ],
        "callout": "Ponte pedagogico perfetto: se il gyokuro ti sembra troppo intenso, il kabusecha insegna l'umami senza il prezzo o la difficoltà del «tè delle occasioni speciali».",
        "pairings": ["Pesce crudo", "Riso in bianco"],
        "faq": [
            ("Kabusecha e gyokuro?", "Entrambi ombreggiati, ma il kabusecha resta sencha: telo per settimane, non settimane di ombra totale come il gyokuro."),
            ("Perché esiste?", "Compromesso tra freschezza vegetale del sencha e dolcezza umami dell'ombra."),
        ],
        "deep_title": "Ombra breve",
        "deep_text": "Versione del sencha prodotta coprendo le piante con telo qualche settimana prima della raccolta, come per il gyokuro ma con ombreggiatura più breve. Più aminoacidi e dolcezza rispetto al sencha al sole; profilo intermedio ideale per avvicinarsi all'umami.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Sencha (Kabusecha)", "pages": "126"},
        ],
        "related_slugs": ["sencha", "gyokuro"],
        "temi_kb": ["lavorazione_qualità", "degustazione_sensoriale"],
        "momenti": ["pausa"],
        "stagioni_nav": ["primavera"],
        "related_links": [
            ("Sencha", "/varieta/sencha/", "al sole"),
            ("Gyokuro", "/varieta/gyokuro/", "ombra lunga"),
        ],
        "explore_next": [
            ("Sencha", "/varieta/sencha/", "punto di partenza"),
            ("Gyokuro", "/varieta/gyokuro/", "passo successivo"),
            ("Umami", "/glossario/umami/", "gusto chiave"),
            ("Percorso bancha→matcha", "/gioca/percorsi/dal-bancha-al-matcha/", "tappa intermedia"),
        ],
    },
    {
        "slug": "tencha",
        "title": "Tencha — foglia prima del matcha",
        "description": "Tencha è tè verde giapponese ombreggiato, macinato per il matcha: foglie senza venature, base della cerimonia del tè.",
        "keywords": ["tencha", "matcha", "tè verde giapponese", "Cerimonia del tè", "Camellia sinensis"],
        "origine": "Giappone",
        "stile": "tencha",
        "caffeina": "Alta",
        "stagione": "Primavera",
        "cultivar": "Cultivar ombreggiate (base del matcha)",
        "sort_order": 23,
        "brew": {"temp": 80, "grams": 2, "seconds": 0, "infusions": "1"},
        "lead": "Prima della polvere: il tencha è gyokuro senza arrotolamento — foglie ombreggiate, venature rimosse, destinate al frantoio di pietra che produce il matcha.",
        "sensory": {
            "aspetto": "Foglie piatte verde scuro (non polvere)",
            "aroma": "Vegetale intenso, alghe",
            "gusto": "Umami denso (se infuso raramente)",
            "retrogusto": "Dolce, persistente",
        },
        "equipment": ["Matcha: chawan, chasen, chashaku", "Conservazione in frigo dopo apertura"],
        "steps": [
            {"text": "Il tencha si macina in matcha, non si infonde come sencha", "duration": "—"},
            {"text": "Per matcha: 2 g in 60 ml a 80 °C, frullare con chasen", "duration": "1 min"},
            {"text": "Conserva sottovuoto in frigo dopo apertura", "duration": "—"},
        ],
        "errors": [
            "Infondere tencha come sencha in kyusu (non è il suo uso)",
            "Usare tencha economico per usucha cerimoniale",
            "Conservare al caldo dopo apertura",
        ],
        "callout": "Capire il tencha chiarisce il matcha: non è polvere generica, ma foglia ombreggiata macinata — la stessa filiera del gyokuro verso la cerimonia.",
        "pairings": ["Wagashi", "Pasticceria a bassa grassosità"],
        "faq": [
            ("Si beve il tencha in infusione?", "Raramente: è semilavorato per matcha. Si beve la polvere di tencha macinata."),
            ("Tencha e matcha?", "Il matcha è tencha macinato in frantoio di pietra; qualità e ombreggiatura determinano il grado cerimoniale."),
        ],
        "deep_title": "Dall'ombra al frantoio",
        "deep_text": "Prodotto come il gyokuro con ombreggiatura pre-raccolta; venature rimosse, foglie essiccate piatte. Macinato in frantoi di pietra diventa matcha per la cerimonia del tè. Qualità pregiate da piante mature e raccolto primaverile; grade economiche da aracha per cucina.",
        "biblio": [
            {"author": "Pellegrino, Davide", "title": "Manuale per la preparazione del tè", "tema": "pellegrino-varietà", "sotto_tema": "Matcha (Tencha)", "pages": "127"},
            {"author": "Bisogno, Victoria; Pettigrew, Jane", "title": "Manuale del sommelier del tè", "tema": "sommelier-degustazione", "sotto_tema": "Tencha e matcha", "pages": "1163–1165"},
        ],
        "related_slugs": ["matcha", "gyokuro"],
        "temi_kb": ["cerimonia_spiritualita", "lavorazione_qualità"],
        "momenti": ["pausa"],
        "stagioni_nav": ["primavera"],
        "related_links": [
            ("Matcha", "/varieta/matcha/", "prodotto finale"),
            ("Gyokuro", "/varieta/gyokuro/", "stessa ombra"),
        ],
        "explore_next": [
            ("Matcha", "/varieta/matcha/", "polvere in tazza"),
            ("Chasen", "/glossario/chasen/", "strumento"),
            ("Chanoyu", "/glossario/chanoyu/", "cerimonia"),
            ("Percorso bancha→matcha", "/gioca/percorsi/dal-bancha-al-matcha/", "tappa finale"),
        ],
    },
]


def _p(text: str) -> dict:
    return {"type": "paragraph", "spans": [{"type": "text", "value": text}]}


def build_doc(v: dict[str, Any]) -> dict[str, Any]:
    slug = v["slug"]
    brew = v["brew"]
    nav: dict[str, Any] = {
        "related_slugs": v["related_slugs"],
        "temi_kb": v["temi_kb"],
        "controversie": [],
        "momenti": v.get("momenti", ["pausa"]),
        "stagioni": v.get("stagioni_nav", ["primavera"]),
        "explore_next": [{"name": n, "url": u, "reason": r} for n, u, r in v["explore_next"]],
    }
    if v.get("percorso_tappa") is not None:
        nav["percorso_tappa"] = v["percorso_tappa"]

    blocks: list[dict] = [
        _p(v["lead"]),
        {"type": "sensory_profile", **v["sensory"]},
        {"type": "brew_params", **brew},
        {"type": "equipment", "items": v["equipment"]},
        {"type": "steps", "items": v["steps"]},
        {"type": "errors", "items": v["errors"]},
        {"type": "callout", "variant": "italia", "spans": [{"type": "text", "value": v["callout"]}]},
        {"type": "pairings", "items": v["pairings"]},
        {
            "type": "faq",
            "items": [
                {"question": q, "answer_spans": [{"type": "text", "value": a}]}
                for q, a in v["faq"]
            ],
        },
        {
            "type": "level_section",
            "level": "deep",
            "blocks": [
                {"type": "heading", "level": 2, "spans": [{"type": "text", "value": v["deep_title"]}]},
                _p(v["deep_text"]),
                {"type": "bibliography", "items": v["biblio"]},
            ],
        },
        {
            "type": "related_links",
            "items": [{"name": n, "url": u, "reason": r} for n, u, r in v["related_links"]],
        },
    ]

    return {
        "schema_version": "1.0",
        "type": "variety",
        "slug": slug,
        "meta": {
            "title": v["title"],
            "description": v["description"],
            "keywords": v["keywords"],
            "canonical_path": f"/varieta/{slug}/",
        },
        "seo": {"robots": "index,follow", "og_type": "article"},
        "navigation": nav,
        "taxonomy": {
            "origine": v["origine"],
            "stile": v["stile"],
            "caffeina": v["caffeina"],
            "stagione": v["stagione"],
            "cultivar": v["cultivar"],
            "sort_order": v["sort_order"],
            "brew": brew,
        },
        "body": {"blocks": blocks},
    }


def main() -> None:
    for v in VARIETIES:
        path = VAR_DIR / f"{v['slug']}.json"
        if path.exists():
            print(f"Skip existing {v['slug']}")
            continue
        doc = build_doc(v)
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Created {v['slug']}")


if __name__ == "__main__":
    main()
