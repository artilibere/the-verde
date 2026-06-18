#!/usr/bin/env python3
"""One-shot engagement enricher: glossary depth, hub impara, explore_next reasons."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

GENERIC_MARKERS = (
    "collega gesto e cultura",
    "In Italia puoi incontrarlo nei tea shop",
    "Nel tè verde, Sencha non è un'etichetta generica",
    "Nel tè verde, Gyokuro non è un'etichetta generica",
    "Nel tè verde, Matcha non è un'etichetta generica",
    "Nel tè verde, Bancha non è un'etichetta generica",
)

GLOSSARY_ENRICHMENTS: dict[str, dict] = {
    "roji": {
        "paragraph": "Pietre levigate, lanterne di pietra, muschio umido: il roji è progettato per rallentare il passo prima del chashitsu. In scuole di chanoyu a Milano o Roma si simula spesso con un corridoio silenzioso o un angolo di giardino — l'intenzione conta più della perfezione botanica.",
        "faq2": ("Serve un giardino grande?", "No: anche tre metri quadrati con una pianta e un secchio d'acqua possono segnare il passaggio dal quotidiano al rito."),
    },
    "koicha": {
        "paragraph": "Si prepara con il doppio della polvere dell'usucha e meno acqua: il risultato è una pasta viscosa, quasi oleosa, che si beve in pochi sorsi condivisi. Richiede matcha cerimoniale di altissima qualità — polveri amare o granulose tradiscono il gesto.",
        "faq2": ("Quanta polvere per il koicha?", "Circa 4 g per 40 ml d'acqua tiepida — il doppio dell'usucha, con mescolatura lenta e senza schiuma grossolana."),
    },
    "usucha": {
        "paragraph": "L'usucha è il matcha «tè leggero»: più acqua, schiuma fine, corpo arioso. È la forma quotidiana del chanoyu e il punto di partenza per chi impara a usare il chasen senza la densità intimidatoria del koicha.",
        "faq2": ("Usucha e matcha latte?", "Niente a che fare: il latte maschera la polvere; l'usucha tradizionale è solo acqua e matcha frullato."),
    },
    "chanoyu": {
        "paragraph": "Codificato da Sen no Rikyū nel XVI secolo, il chanoyu unisce estetica wabi-sabi, architettura dello spazio e preparazione del matcha. Non è spettacolo: è presenza condivisa. In Italia si pratica in scuole dedicate o si attinge al gesto lento senza recitare ogni regola.",
        "faq2": ("Chanoyu e cerimonia del tè cinese?", "Tradizioni distinte: il chanoyu è giapponese con matcha; il gong fu cha cinese usa foglia intera e gaiwan — non confonderli."),
    },
    "gong-fu-cha": {
        "paragraph": "Letteralmente «tè con arte»: infusioni brevi in gaiwan o teiera yixing, tazze minute, ospitalità come valore centrale. Il gong fu esalta oolong e pu-erh, ma funziona benissimo anche con dragon well e bi luo chun — ideal per chi ama la degustazione vino.",
        "faq2": ("Quante infusioni in gong fu?", "Spesso 5–8 versate da pochi secondi: ogni infusione rivela un strato diverso della foglia."),
    },
    "chasen": {
        "paragraph": "Frusta di bambou con 80–120 renghe: il gesto del chasen incorpora aria e crea la schiuma fine del matcha. Si bagnano le setole prima dell'uso e si asciugano a testa in su — un oggetto fragile ma essenziale per usucha e koicha.",
        "faq2": ("Posso usare un frullino elettrico?", "Per cucina sì; per matcha tradizionale no — la schiuma del chasen ha texture e temperatura diverse."),
    },
    "chawan": {
        "paragraph": "Ciotola di ceramica per matcha: forma aperta per usucha, più profonda per koicha. Ogni pezzo racconta stagione e maestro ceramista. In Italia ne trovi di produzione giapponese o artigianale locale — non serve un antico raku per imparare.",
        "faq2": ("Quale dimensione per iniziare?", "Circa 12 cm di diametro per usucha: spazio sufficiente per il gesto del chasen senza schizzi."),
    },
    "kyusu": {
        "paragraph": "Teiera giapponese con manico laterale e filtro integrato: pensata per sencha quotidiano e reinfusioni brevi. Il terracotta poroso esiste ma la ceramica smaltata è la scelta più pratica per chi alterna varietà.",
        "faq2": ("Kyusu o tazza con infusore?", "L'infusore va bene; il kyusu distribuisce meglio la foglia e rende omaggio al gesto giapponese quotidiano."),
    },
    "gaiwan": {
        "paragraph": "Coppa con coperchio e sottocoppa: strumento versatile del gong fu cha. Permette di controllare tempo e temperatura guardando la foglia che si apre — perfetto per dragon well, bi luo chun e oolong leggeri.",
        "faq2": ("Gaiwan solo per esperti?", "No: è tra gli strumenti più accessibili; richiede solo attenzione al bordo caldo quando versi."),
    },
    "yixing": {
        "paragraph": "Teiera di argilla porosa del Jiangsu: assorbe oli della foglia e «seasoning» con il tempo. Si dedica a una famiglia di tè — mescolare sencha e pu-erh nella stessa yixing confonde i profili.",
        "faq2": ("Serve seasoning prima dell'uso?", "Tradizione vuole bollire la teiera con foglia scartata; oggi molti la usano subito con cura — l'importante è non cambiare famiglia di tè."),
    },
    "yunomi": {
        "paragraph": "Tazza alta senza manico per sencha quotidiano: si tiene con entrambe le mani, si assapora l'aroma prima del sorso. Forme e smalti variano; in casa italiana può convivere con tazze da caffè senza conflitto estetico.",
        "faq2": ("Yunomi e tazza da tè inglese?", "La yunomi è più alta e stretta, pensata per sorbi piccoli e reinfusioni — non per zuccherare o aggiungere latte."),
    },
    "wok": {
        "paragraph": "Padella di ferro o acciaio per la fixation cinese: la foglia salta a fuoco vivo, si ferma l'ossidazione, nascono note di nocciola e fagiolino tipiche del Long Jing. Il wok è il cuore della lavorazione di molti verdi cinesi, opposto al vapore giapponese.",
        "faq2": ("Il wok lascia sapore di padella?", "No se la lavorazione è corretta: il calore breve stabilizza senza bruciare — il profilo tostato è voluto, non difetto."),
    },
    "vapore": {
        "paragraph": "Lo steaming giapponese fissa la foglia in 15–30 secondi preservando clorofilla e note marine. Sencha, gyokuro e bancha condividono questo metodo; la differenza nasce poi da ombra, raccolto e arrotolatura.",
        "faq2": ("Vapore o padella: quale è «migliore»?", "Nessuno vince: sono due estetiche. Il vapore esalta verde intenso; la padella cinese privilegia nocciola e morbidezza."),
    },
    "tencha": {
        "paragraph": "Foglia ombreggiata non arrotolata, destinata alla macinatura: è la materia prima del matcha. Non si infusiona — si macina a pietra o a macchina e si beve sospeso in acqua.",
        "faq2": ("Tencha e matcha sono la stessa cosa?", "Quasi: il matcha è tencha macinato. La tencha intera esiste ma raramente si trova fuori dal Giappone."),
    },
    "shincha": {
        "paragraph": "Primo raccolto dell'anno giapponese: foglie tenere, alta umami, prezzo premium. In Italia arriva in primavera come evento per appassionati — da consumare entro pochi mesi per freschezza.",
        "faq2": ("Shincha e sencha di primavera?", "Lo shincha è il sencha del very first flush — massima vivacità, scorta limitata."),
    },
    "cold-brew": {
        "paragraph": "Estrazione a freddo per 4–8 ore: meno caffeina, zero amaro, profilo dolce. Ideale per estate italiana e aperitivo analcolico. Gyokuro e sencha premium rendono meglio di polveri industriali.",
        "faq2": ("Cold brew con acqua calda veloce?", "No: il freddo estrae lentamente catechine amare — la pazienza è parte del metodo."),
    },
    "egcg": {
        "paragraph": "Epigallocatechina gallato: la catechina più studiata in laboratorio. Nel tè verde è abbondante; nel matcha ancora di più perché bevi la foglia intera. Gli integratori concentrano dosi che la tazza quotidiana non raggiunge — dibattito aperto in KB.",
        "faq2": ("Più EGCG = più beneficio?", "Non linearmente: eccesso può irritare fegato in integratori; la bevanda modera dose e piacere."),
    },
    "catechine": {
        "paragraph": "Famiglia di polifenoli antiossidanti: non solo EGCG. Temperatura e tempo modulano quanto finisce in tazza — acqua bollente estrae più amaro, non necessariamente «più salute» in modo lineare.",
        "faq2": ("Decaffeinazione perde catechine?", "In parte sì: i processi industriali alterano anche polifenoli e profilo sensoriale."),
    },
    "l-teanina": {
        "paragraph": "Aminoacido che modula la caffeina: vigilanza più stabile, meno picco nervoso. Abonda nei verdi ombreggiati (gyokuro, matcha). Spiega perché molti italiani abituati all'espresso trovano il tè «più dolce» sulla stimolazione.",
        "faq2": ("L-teanina come integratore?", "Esiste in capsule; nel tè convive con centinaia di composti — effetto diverso dal mono-ingrediente."),
    },
    "astringenza": {
        "paragraph": "Sensazione di ruvidità sulla lingua, distinta dall'amaro: arriva dai tannini estratti troppo a lungo o troppo caldi. Un filo può strutturare la tazza; in eccesso segnala errore di preparazione.",
        "faq2": ("Astringenza e stomaco vuoto?", "I tannini su mucosa sensibile irritano: meglio bancha o genmaicha a digiuno, non gyokuro scottato."),
    },
    "umami": {
        "paragraph": "Quinto gusto, sapidità rotonda: nel tè emerge soprattutto dopo ombreggiatura e lavorazione che preserva aminoacidi. Ponte naturale per chi in Italia conosce parmigiano e colatura — senza forzare paragoni snobistici.",
        "faq2": ("Umami solo nel gyokuro?", "Iconico lì, ma compare in matcha e sencha premium; raramente in gunpowder o hojicha tostato."),
    },
    "genmaicha": {
        "paragraph": "Bancha o sencha con riso tostato soffiato: profilo di pane caldo e nocciola. Comfort food giapponese che in inverno italiano dialoga con zuppe e castagne — bassa caffeina, gesto semplice.",
        "faq2": ("Genmaicha fa ingrassare per il riso?", "No: le calorie del riso soffiato sono trascurabili; è bevanda, non piatto."),
    },
    "hojicha": {
        "paragraph": "Bancha o kukicha tostata a high heat: colore ambrato, caffeina ridotta, note di caramello. La scelta serale per eccellenza in Italia — dopo cena senza disturbare il sonno come un espresso.",
        "faq2": ("Hojicha è tè nero?", "No: resta verde non ossidato, solo tostato — Camellia sinensis, non tisana."),
    },
    "kukicha": {
        "paragraph": "Tè di rametti e foglioline: leggerissimo, bassa caffeina, profilo dolce. Ideale per bambini giapponesi e per chi in Italia cerca un verde serale senza intensità.",
        "faq2": ("Kukicha e bancha?", "Entrambi leggeri; il kukicha usa parti di stelo, il bancha foglie mature — profili simili, origine diversa."),
    },
    "bancha": {
        "paragraph": "Foglie mature raccolte dopo il sencha principale: quotidiano giapponese, basso costo, bassa caffeina. Perfetto per chi in Italia inizia dal verde senza investire in gyokuro.",
        "faq2": ("Bancha è tè scadente?", "No: è scelta di lavorazione e stagione — meno pregiato del sencha prima qualità, ma legittimo e delizioso."),
    },
    "sencha": {
        "paragraph": "Verde giapponese al sole, fissato al vapore: erbaceo, marine, amaro controllato a 75 °C. È la grammatica base per capire gyokuro (ombra) e bancha (foglia matura).",
        "faq2": ("Sencha in bustina al supermercato?", "Spesso polvere fine o tagli grossolani scadenti — non rappresenta il sencha specialty in foglia."),
    },
    "gyokuro": {
        "paragraph": "Ombreggiato 20+ giorni prima del raccolto: massima L-teanina, umami denso, infusione a 50–60 °C. Il vertice del verde giapponese — non per chi cerca semplicità da bustina bollente.",
        "faq2": ("Gyokuro a colazione?", "Possibile se tolleri caffeina; molti preferiscono sencha al mattino e gyokuro nel pomeriggio."),
    },
    "matcha": {
        "paragraph": "Tencha macinato, bevuto intero: catechine concentrate, gesto del chasen, usucha o koicha. In Italia è ingrediente pasticceria e bevanda trendy — due mondi, stessa polvere di origine diversa.",
        "faq2": ("Matcha cerimoniale e da cucina?", "Stessa pianta, qualità diverse: il culinary grade colora e profuma; il cerimoniale ha umami e dolcezza superiori in tazza."),
    },
    "gunpowder": {
        "paragraph": "Zhu Cha cinese, perle arrotolate: robusto, tollera 85 °C, profilo affumicato leggero. Indulgente per chi sbaglia temperatura — ponte accessibile dal tè amaro in bustina.",
        "faq2": ("Perché «gunpowder»?", "Nome occidentale per la forma a pallottola che ricorda polvere da sparo — non ha sapore di fumo come lapsang souchong."),
    },
    "longjing": {
        "paragraph": "Dragon Well, Long Jing: tè piatto di Zhejiang, pan-firing nel wok, nocciola e fagiolino. Uno dei verdi cinesi più riconoscibili — ideale per palati abituati a vini bianchi morbidi.",
        "faq2": ("Long Jing autentico?", "Il mercato è pieno di imitazioni; provenienza West Lake (Xihu) e prezzo coerente sono segnali utili."),
    },
    "darjeeling": {
        "paragraph": "Verde himalayano: mineralità, muschio, note floreali montane. Diverso dai verdi giapponesi al vapore — parallelo con bianchi strutturati dell'Alto Adige per chi viene dal vino.",
        "faq2": ("Darjeeling verde e nero?", "Stessa regione, lavorazione diversa: il verde non ossida; profili non sono intercambiabili."),
    },
    "camellia-sinensis": {
        "paragraph": "Unica specie del tè vero: verde, nero, oolong, bianco sono lavorazioni diverse della stessa pianta. Camomilla, menta, rooibos non sono tè — distinzione essenziale nel mercato italiano pieno di «tisane verdi».",
        "faq2": ("Tè verde decaffeinato è altra pianta?", "No: stessa Camellia sinensis, processo di decaffeinazione che altera anche il profilo."),
    },
}

HUB_PARAGRAPHS: dict[str, str] = {
    "cerimonia": "In Italia il rituale può essere minimo: scaldare la kyusu, versare tre volte, silenzio di un minuto. Non serve sala tatami — serve interruzione consapevole dalla fretta del telefono. Il percorso «Rituale è quotidiano» collega gong fu, chanoyu e bancha in bottiglia senza gerarchie moralistiche.",
    "cucina": "Genmaicha in tempura di verdure, matcha in panna cotta, hojicha in gelato: il verde esce dalla tazza quando la polvere è fresca e dosata con parsimonia. In pasticceria italiana il matcha funziona con marron glacé e agrumi canditi meglio che con panna montata zuccherata.",
    "caffeina": "In ufficio italiano la pausa delle 16 è territorio del caffè: un sencha o un gyokuro offrono focus diverso — meno picco, più plateau. Per la sera, hojicha e kukicha sono la scelta prudente; il matcha dopo cena resta per chi tolera bene la caffeina.",
    "degustazione": "A casa puoi allenare il naso con tre tazze side-by-side: stessa quantità, stessa acqua, tempi diversi — vedrai come secondi e gradi cambiano amaro e corpo. Annotare in diario aiuta più di decine di schede teoriche.",
    "lavorazione": "Leggere l'etichetta aiuta: «steamed» vs «pan-fired», raccolto primaverile, origine prefecture o provincia. In Italia spesso manca tracciabilità — meglio rivenditori specialty che dichiarano lotto e data.",
    "salute": "Nessun contenuto qui sostituisce il medico: il tè verde può far parte di uno stile di vita equilibrato, non di protocolli detox da influencer. Bevi per piacere; eventuali benefici sono plus, non promessa — coerente con i Termini del sito.",
}

REASON_UPGRADES: dict[str, str] = {
    "hub": "approfondisci il tema",
    "scheda": "prova in tazza",
    "contesto": "leggi il filo",
    "termine": "definizione collegata",
    "metodo": "tecnica passo passo",
    "cerimonia": "rito e gesto",
    "confronto": "confronta i profili",
    "esempio": "vedi in pratica",
    "strumento": "utensile essenziale",
    "verifica": "metti alla prova",
    "successivo": "prossimo passo",
    "prossimo passo": "continua il percorso",
    "profilo": "scopri il tuo stile",
    "dibattito KB": "leggi le posizioni",
    "posizioni KB": "leggi le posizioni",
    "catalogo": "sfoglia le varietà",
    "guide tematiche": "esplora Impara",
    "termini": "apri il glossario",
    "contesto locale": "tè verde in Italia",
    "inizia qui": "percorso guidato",
    "scopri il profilo": "quiz personalità",
    "gastronomia": "abbinamenti a tavola",
    "cucina": "ricette e usi",
    "momento": "scegli l'orario",
    "stagione": "calendario del gusto",
    "sera": "dopo cena leggero",
    "leggero": "bassa intensità",
    "quotidiano": "tazza di tutti i giorni",
    "preparazione": "grammi e gradi",
    "steaming": "lavorazione al vapore",
    "ombra": "verde ombreggiato",
    "alternativa leggera": "meno caffeina",
    "composti": "chimica in tazza",
    "catechina studiata": "EGCG spiegato",
    "panoramica": "visione d'insieme",
    "tre dibattiti": "percorso critico",
    "verifica pratica": "quiz preparazione",
    "apprendimento": "percorso guidato",
    "prospettive": "quotidiano vs rito",
    "tecnica base": "parametri infusione",
    "cerimoniale": "matcha lento",
    "via cinese": "gong fu cha",
    "in cucina": "matcha fuori tazza",
    "controversia": "tema aperto",
    "prima tappa": "inizia dal bancha",
    "parametri": "temperatura e tempo",
    "prossimo percorso": "continua a Gioca",
    "confronto cinese": "verde in padella",
    "lessico": "termini del gusto",
    "rito": "tradizione giapponese",
    "dibattito 1": "salute e scienza",
    "dibattito 2": "tazza vs integratore",
    "dibattito 3": "caffeina e calma",
    "tappa 1": "bancha quotidiano",
    "tappa 3": "gyokuro d'ombra",
    "tappa 4": "matcha intero",
    "percorso successivo": "palato italiano",
    "bassa caffeina": "sera senza nervi",
    "alta caffeina": "focus intenso",
    "quando bere": "momento giusto",
    "inizia": "da dove partire",
    "definizione collegata": "termine correlato",
    "foglia intera": "bevi la polvere",
    "scheda completa": "parametri e gusto",
    "scheda pratica": "infusione passo passo",
    "scheda estiva": "cold brew",
    "scheda sensoriale": "leggi il profilo",
    "hub salute": "benessere senza hype",
    "hub": "approfondisci il tema",
}


def _paragraph_block(text: str) -> dict:
    return {"type": "paragraph", "spans": [{"type": "text", "value": text}]}


def _faq_item(question: str, answer: str) -> dict:
    return {"question": question, "answer_spans": [{"type": "text", "value": answer}]}


def _deep_blocks(doc: dict) -> list[dict] | None:
    for block in doc["body"]["blocks"]:
        if block.get("type") == "level_section" and block.get("level") == "deep":
            return block["blocks"]
    return None


def enrich_glossary(path: Path) -> bool:
    doc = json.loads(path.read_text(encoding="utf-8"))
    slug = doc["slug"]
    data = GLOSSARY_ENRICHMENTS.get(slug)
    if not data:
        return False

    blocks = _deep_blocks(doc)
    if not blocks:
        return False

    changed = False
    new_para = data.get("paragraph")
    if new_para:
        for i, block in enumerate(blocks):
            if block.get("type") != "paragraph":
                continue
            text = block["spans"][0]["value"]
            if any(m in text for m in GENERIC_MARKERS) or len(text.split()) < 25:
                blocks[i] = _paragraph_block(new_para)
                changed = True
                break
        else:
            # insert before related_links
            for i, block in enumerate(blocks):
                if block.get("type") == "related_links":
                    blocks.insert(i, _paragraph_block(new_para))
                    changed = True
                    break

    faq2 = data.get("faq2")
    if faq2:
        for block in blocks:
            if block.get("type") == "faq" and len(block.get("items", [])) == 1:
                block["items"].append(_faq_item(faq2[0], faq2[1]))
                changed = True
                break

    if changed:
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def enrich_hub(path: Path) -> bool:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("type") != "hub":
        return False
    slug = doc["slug"]
    extra = HUB_PARAGRAPHS.get(slug)
    if not extra:
        return False

    blocks = _deep_blocks(doc)
    if not blocks:
        return False

    for i, block in enumerate(blocks):
        if block.get("type") == "related_links":
            blocks.insert(i, _paragraph_block(extra))
            path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return True
    return False


def upgrade_reasons(path: Path) -> bool:
    doc = json.loads(path.read_text(encoding="utf-8"))
    nav = doc.get("navigation") or {}
    explore = nav.get("explore_next") or []
    if not explore:
        return False

    changed = False
    for link in explore:
        reason = link.get("reason", "")
        url = link.get("url", "")
        new_reason = REASON_UPGRADES.get(reason)
        if reason == "hub" and "/italia" in url:
            new_reason = "contesto italiano"
        elif reason == "hub" and "/impara" in url:
            new_reason = "approfondisci il tema"
        elif reason == "hub" and "/gioca" in url:
            new_reason = "gioca e impara"
        if new_reason and new_reason != reason:
            link["reason"] = new_reason
            changed = True

    if changed:
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    gloss_changed = sum(
        enrich_glossary(p) for p in sorted((CONTENT / "glossario").glob("*.json"))
    )
    hub_changed = sum(enrich_hub(p) for p in sorted((CONTENT / "impara").glob("*.json")))

    reason_paths = list(CONTENT.rglob("*.json"))
    reason_paths = [
        p
        for p in reason_paths
        if "_schemas" not in str(p) and "_config" not in str(p) and p.name != "relazioni.json"
    ]
    reason_changed = sum(upgrade_reasons(p) for p in reason_paths)

    print(f"Glossary enriched: {gloss_changed}")
    print(f"Hub impara enriched: {hub_changed}")
    print(f"explore_next reasons upgraded: {reason_changed}")


if __name__ == "__main__":
    main()
