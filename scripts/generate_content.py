#!/usr/bin/env python3
"""Generate Markdown content for the-verde.it MVP."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content"

VARIETIES = {
    "bancha": {
        "title": "Bancha — il verde quotidiano e leggero",
        "origine": "Giappone", "stile": "bancha", "caffeina": "Bassa", "stagione": "Estate",
        "brew_temp": 80, "brew_grams": 3, "brew_seconds": 60, "brew_infusions": "2-3",
        "sort_order": 1, "momenti": ["colazione", "dopo-cena"], "stagioni": ["estate"],
        "temi_kb": ["preparazione_servizio", "caffeina_tannini"],
        "related_slugs": ["kukicha", "hojicha"],
        "percorso_tappa": "dal-bancha-al-matcha", "badge_sblocco": "esploratore-verde",
        "body": """Il bancha è il tè che accompagna la giornata giapponese senza pretese: foglie più mature, sapore morbido, caffeina contenuta.

## Profilo sensoriale

- **Aspetto:** Foglie larghe, verde oliva
- **Aroma:** Vegetale leggero, note di fieno
- **Gusto:** Morbido, poco astringente
- **Retrogusto:** Pulito e breve

**Origine:** Giappone — **Stile:** bancha

## Attrezzatura

- Teiera o tazza grande
- Acqua a temperatura controllata

## I passaggi

1. Scalda l'acqua a 80 °C - 2 min
2. Infusiona 3 g per 100 ml per 60 secondi - 1 min
3. Versa tutto il liquore - 30 sec

## Errori comuni

- Acqua troppo bollente
- Infusione eccessivamente lunga

## In Italia

Il bancha e ideale per chi cerca un'alternativa delicata al cappuccino: non compete con il latte, accompagna una colazione leggera. Si trova nei tea shop specialty e online.

## Abbinamenti

- Biscotti secchi, fette biscottate
- Frutta fresca di stagione

## Domande frequenti

### Il bancha fa bene alla salute?

Il consumo regolare di tè verde può supportare uno stile di vita sano grazie alle catechine, ma non sostituisce una dieta equilibrata né le cure mediche.

## Varietà simili

- **Kukicha** (/varieta/kukicha/) — ancora più leggero, rametti e piccioli
- **Hojicha** (/varieta/hojicha/) — tostato, note nocciola
""",
    },
    "sencha": {
        "title": "Sencha — il verde quotidiano del Giappone",
        "origine": "Giappone", "stile": "sencha", "caffeina": "Media", "stagione": "Primavera",
        "brew_temp": 75, "brew_grams": 3, "brew_seconds": 60, "brew_infusions": "2-3",
        "sort_order": 2, "momenti": ["pausa"], "stagioni": ["primavera", "estate"],
        "temi_kb": ["preparazione_servizio", "degustazione_sensoriale"],
        "controversie": ["caffeina-stimolazione"],
        "related_slugs": ["gyokuro", "bancha"],
        "percorso_tappa": "dal-bancha-al-matcha",
        "body": """Ago verdi, profumo di erba tagliata al mattino: il sencha è il battito cardiaco del tè giapponese.

## Profilo sensoriale

- **Aspetto:** Ago sottili, verde brillante
- **Aroma:** Vegetale, erba tagliata
- **Gusto:** Umami delicato, amaro controllato
- **Retrogusto:** Persistente, fresco

**Origine:** Giappone — **Stile:** sencha

## Attrezzatura

- Kyusu o teiera occidentale
- Termometro

## I passaggi

1. Scalda l'acqua a 75 °C - 2 min
2. Infusiona 3 g per 100 ml per 60 secondi - 1 min
3. Versa e degusta - 1 min

## Errori comuni

- Acqua bollente (amaro eccessivo)
- Infusione troppo lunga

## In Italia

Dopo un pranzo in un ristorante giapponese, il sencha è spesso la prima rivelazione: non sa di erba amara se preparato bene. Perfetto per la pausa delle 16:00.

## Abbinamenti

- Pesce crudo, sashimi
- Pasticceria a bassa grassosità

## Domande frequenti

### Sencha o gyokuro?

Il sencha è più quotidiano e vegetale; il gyokuro è ombreggiato, più umami e dolce.

## Varietà simili

- **Gyokuro** (/varieta/gyokuro/) — più umami e ombreggiato
- **Bancha** (/varieta/bancha/) — più leggero
""",
    },
    "gyokuro": {
        "title": "Gyokuro — ombra e umami",
        "origine": "Giappone", "stile": "gyokuro", "caffeina": "Alta", "stagione": "Primavera",
        "brew_temp": 60, "brew_grams": 4, "brew_seconds": 90, "brew_infusions": "2-3",
        "sort_order": 3, "momenti": ["pausa"], "stagioni": ["primavera"],
        "temi_kb": ["lavorazione_qualità", "degustazione_sensoriale"],
        "related_slugs": ["sencha", "matcha"],
        "percorso_tappa": "dal-bancha-al-matcha",
        "body": """Tre settimane di ombra prima del raccolto: la pianta produce clorofilla e L-teanina, e in tazza nasce un brodo verde quasi burroso.

## Profilo sensoriale

- **Aspetto:** Ago scuri, verde intenso
- **Aroma:** Umami profondo, alghe marine
- **Gusto:** Dolcezza vegetale, burroso
- **Retrogusto:** Lungo e setoso

**Origine:** Giappone — **Stile:** gyokuro

## Attrezzatura

- Kyusu piccola
- Tazze yunomi

## I passaggi

1. Scalda l'acqua a 60 °C - 2 min
2. Infusiona 4 g per 100 ml per 90 secondi - 2 min
3. Versa lentamente - 1 min

## Errori comuni

- Temperatura troppo alta
- Dosaggio insufficiente

## In Italia

Il gyokuro dialoga con il pesce crudo e i vini bianchi strutturati: un ponte tra degustazione giapponese e abitudini italiane al mare.

## Abbinamenti

- Sashimi, ceviche
- Formaggi freschi delicati

## Domande frequenti

### Perché così cara?

L'ombreggiatura riduce la resa e richiede manodopera: paghi qualità e lavorazione.

## Varietà simili

- **Matcha** (/varieta/matcha/) — stessa pianta ombreggiata, macinata
- **Sencha** (/varieta/sencha/) — più accessibile
""",
    },
    "matcha": {
        "title": "Matcha — polvere di presenza",
        "origine": "Giappone", "stile": "matcha", "caffeina": "Alta", "stagione": "Primavera",
        "brew_temp": 80, "brew_grams": 2, "brew_seconds": 0, "brew_infusions": "1",
        "sort_order": 4, "momenti": ["pausa"], "stagioni": ["primavera"],
        "temi_kb": ["cerimonia_spiritualita", "cucina_usi_pratici"],
        "controversie": ["bevanda-vs-integratore"],
        "related_slugs": ["gyokuro", "genmaicha"],
        "percorso_tappa": "dal-bancha-al-matcha", "badge_sblocco": "esploratore-verde",
        "quiz_correlati": ["che-varieta-sei"],
        "body": """Non lo infusi: lo sbattevi. Bevi la foglia intera, sospesa in acqua, e il mondo rallenta per un istante.

## Profilo sensoriale

- **Aspetto:** Polvere verde brillante
- **Aroma:** Vegetale intenso, erba fresca
- **Gusto:** Umami, leggermente amaro, dolcezza finale
- **Retrogusto:** Persistente, quasi cremoso

**Origine:** Giappone — **Stile:** matcha

## Attrezzatura

- Chawan (ciotola)
- Chasen (frusta di bambu)
- Chashaku (paletta)

## I passaggi

1. Setaccia 2 g di matcha nel chawan - 1 min
2. Aggiungi 70 ml di acqua a 80 °C - 30 sec
3. Frusta a M con il chasen fino a schiuma fine - 1 min

## Errori comuni

- Matcha da cucina per usucha cerimoniale
- Acqua bollente che brucia il sapore

## In Italia

Il matcha in pasticceria ha aperto porte, ma la preparazione tradizionale resta un altra esperienza: come il pistacchio di Bronte, è diventato ingrediente status — e anche gesto lento.

## Abbinamenti

- Wagashi, marron glace
- Pasticceria a bassa grassosità

## Domande frequenti

### Matcha latte da bar e matcha cerimoniale?

Prodotti diversi: il primo è spesso zuccherato; il secondo richiede tencha di qualità e gesto.

## Varietà simili

- **Gyokuro** (/varieta/gyokuro/) — stessa origine ombreggiata
- **Genmaicha** (/varieta/genmaicha/) — quotidiano tostato
""",
    },
    "genmaicha": {
        "title": "Genmaicha — riso tostato e foglia verde",
        "origine": "Giappone", "stile": "genmaicha", "caffeina": "Bassa", "stagione": "Inverno",
        "brew_temp": 85, "brew_grams": 3, "brew_seconds": 45, "brew_infusions": "2",
        "momenti": ["colazione", "dopo-cena"], "stagioni": ["inverno", "autunno"],
        "temi_kb": ["cucina_usi_pratici", "preparazione_servizio"],
        "related_slugs": ["hojicha", "bancha"],
        "body": """Il profumo di popcorn nel teiere: genmaicha unisce foglie di bancha e riso tostato in un abbraccio caldo.

## Profilo sensoriale

- **Aspetto:** Foglie verdi con chicchi di riso
- **Aroma:** Cereale tostato, nocciola
- **Gusto:** Morbido, leggermente salato
- **Retrogusto:** Comfort, breve

**Origine:** Giappone — **Stile:** genmaicha

## Attrezzatura

- Teiera grande
- Acqua non bollente

## I passaggi

1. Scalda l'acqua a 85 °C - 2 min
2. Infusiona 3 g per 100 ml per 45 secondi - 1 min
3. Versa tutto - 30 sec

## Errori comuni

- Infusione troppo lunga (amaro)

## In Italia

Perfetto nelle sere d'inverno, quando cerchi calore senza la pesantezza del tè nero speziato.

## Abbinamenti

- Zuppe leggere, risotti delicati
- Biscotti semplici

## Domande frequenti

### Quanta caffeina?

Bassa: il riso diluisce la foglia e spesso si usa bancha.

## Varietà simili

- **Hojicha** (/varieta/hojicha/) — tostato senza riso
- **Bancha** (/varieta/bancha/) — base vegetale
""",
    },
    "hojicha": {
        "title": "Hojicha — il verde che abbraccia",
        "origine": "Giappone", "stile": "hojicha", "caffeina": "Bassa", "stagione": "Autunno",
        "brew_temp": 90, "brew_grams": 3, "brew_seconds": 30, "brew_infusions": "2-3",
        "momenti": ["dopo-cena", "aperitivo"], "stagioni": ["autunno", "inverno"],
        "temi_kb": ["lavorazione_qualità", "caffeina_tannini"],
        "related_slugs": ["genmaicha", "kukicha"],
        "body": """Tostato su carbone o forno: l'hojicha trasforma il verde in note di nocciola e caramello, con quasi niente caffeina.

## Profilo sensoriale

- **Aspetto:** Foglie bruno-rossastre
- **Aroma:** Tostato, nocciola, caramello
- **Gusto:** Morbido, zero amarezza aggressiva
- **Retrogusto:** Caldo e rassicurante

**Origine:** Giappone — **Stile:** hojicha

## Attrezzatura

- Teiera
- Acqua calda ma non bollente

## I passaggi

1. Scalda l'acqua a 90 °C - 2 min
2. Infusiona 3 g per 100 ml per 30 secondi - 1 min
3. Versa - 30 sec

## Errori comuni

- Trattarlo come sencha delicato

## In Italia

Dopo cena, quando il palato chiede qualcosa di caldo senza tenere svegli: dialoga con cioccolato fondente e cantucci.

## Abbinamenti

- Cioccolato fondente
- Biscotti di Prato

## Domande frequenti

### Si può bere la sera?

Si: bassa caffeina, ideale dopo cena.

## Varietà simili

- **Kukicha** (/varieta/kukicha/) — leggero, a volte tostato
- **Genmaicha** (/varieta/genmaicha/) — cereale e verde
""",
    },
    "kukicha": {
        "title": "Kukicha — twig tea leggero",
        "origine": "Giappone", "stile": "kukicha", "caffeina": "Bassa", "stagione": "Estate",
        "brew_temp": 80, "brew_grams": 3, "brew_seconds": 60, "brew_infusions": "2-3",
        "momenti": ["colazione", "dopo-cena"], "stagioni": ["estate"],
        "temi_kb": ["caffeina_tannini", "preparazione_servizio"],
        "related_slugs": ["bancha", "hojicha"],
        "body": """Piccioli e rametti: il kukicha è economico, gentile, perfetto per chi inizia senza paura dell'amaro.

## Profilo sensoriale

- **Aspetto:** Rametti verdi e chiari
- **Aroma:** Leggero, legnoso
- **Gusto:** Dolce vegetale, poco tannico
- **Retrogusto:** Pulito

**Origine:** Giappone — **Stile:** kukicha

## Attrezzatura

- Teiera
- Termometro opzionale

## I passaggi

1. Acqua a 80 °C - 2 min
2. 3 g per 100 ml, 60 secondi - 1 min
3. Versa - 30 sec

## Errori comuni

- Dosaggio eccessivo

## In Italia

Ottima proposta per colazione leggera: non compete con cappuccino e cornetto.

## Abbinamenti

- Frutta, yogurt
- Miele leggero

## Domande frequenti

### È un tè di seconda scelta?

No: e un prodotto intenzionale, valorizzato per leggerezza.

## Varietà simili

- **Bancha** (/varieta/bancha/) — foglia matura
- **Hojicha** (/varieta/hojicha/) — versione tostata
""",
    },
    "dragon-well": {
        "title": "Dragon Well — Longjing della Cina",
        "origine": "Cina", "stile": "longjing", "caffeina": "Media", "stagione": "Primavera",
        "brew_temp": 80, "brew_grams": 3, "brew_seconds": 120, "brew_infusions": "3-4",
        "momenti": ["pausa"], "stagioni": ["primavera"],
        "temi_kb": ["storia_cultura", "degustazione_sensoriale"],
        "related_slugs": ["bi-luo-chun", "gunpowder"],
        "body": """Foglie appiattite a lancia nel wok: il Longjing profuma di castagna tostata e erba fresca.

## Profilo sensoriale

- **Aspetto:** Foglie piatte, verde giallastro
- **Aroma:** Castagna, erba fresca
- **Gusto:** Dolce, nocciola, vegetale
- **Retrogusto:** Pulito e persistente

**Origine:** Cina — **Stile:** longjing

## Attrezzatura

- Gaiwan o bicchiere alto
- Acqua a 80 °C

## I passaggi

1. Scalda il recipiente - 1 min
2. Infusiona 3 g per 100 ml per 2 minuti - 2 min
3. Rein infusiona più volte - 2 min

## Errori comuni

- Acqua bollente

## In Italia

Un cinese tra i verdi più accessibili al palato italiano: note tostate che ricordano frutta secca.

## Abbinamenti

- Pesce al vapore
- Verdure di stagione

## Domande frequenti

### Perché si chiama pozzo del drago?

Leggenda locale a West Lake: il nome e parte della storia del Longjing.

## Varietà simili

- **Bi Luo Chun** (/varieta/bi-luo-chun/) — spirale primaverile
- **Gunpowder** (/varieta/gunpowder/) — perle verdi
""",
    },
    "gunpowder": {
        "title": "Gunpowder — perle verdi cinesi",
        "origine": "Cina", "stile": "gunpowder", "caffeina": "Media", "stagione": "Autunno",
        "brew_temp": 85, "brew_grams": 3, "brew_seconds": 90, "brew_infusions": "2-3",
        "momenti": ["pausa"], "stagioni": ["autunno"],
        "temi_kb": ["storia_cultura", "preparazione_servizio"],
        "related_slugs": ["dragon-well", "genmaicha"],
        "body": """Foglie arrotolate a pallottola: il gunpowder tiene a lungo aroma e resiste a infusioni più calde.

## Profilo sensoriale

- **Aspetto:** Perle verdi compatte
- **Aroma:** Fumo leggero, erba
- **Gusto:** Robusto, leggermentè affumicato
- **Retrogusto:** Persistente

**Origine:** Cina — **Stile:** gunpowder

## Attrezzatura

- Teiera
- Acqua 85 °C

## I passaggi

1. Risciacqua le perle con acqua calda - 30 sec
2. Infusiona 3 g per 100 ml, 90 secondi - 2 min
3. Seconda infusione più breve - 1 min

## Errori comuni

- Confonderlo con tè affumicato lapsang

## In Italia

Storico nelle miscele al menta del Maghreb: in tazza pura rivela un verde più rustico e onesto.

## Abbinamenti

- Cucina mediterranea leggera
- Olive e pane

## Domande frequenti

### Perché gunpowder?

Le perle ricordano la polvere da sparo — nome evocativo, non di qualità.

## Varietà simili

- **Dragon Well** (/varieta/dragon-well/) — cinese più fine
- **Genmaicha** (/varieta/genmaicha/) — spesso usa base gunpowder
""",
    },
    "bi-luo-chun": {
        "title": "Bi Luo Chun — conchiglie verdi di primavera",
        "origine": "Cina", "stile": "bi-luo-chun", "caffeina": "Media", "stagione": "Primavera",
        "brew_temp": 75, "brew_grams": 3, "brew_seconds": 90, "brew_infusions": "3",
        "momenti": ["pausa"], "stagioni": ["primavera"],
        "temi_kb": ["lavorazione_qualità", "degustazione_sensoriale"],
        "related_slugs": ["dragon-well", "sencha"],
        "body": """Spiralate come conchiglie: un raccolto precoce che profuma di frutta e fiori primaverili.

## Profilo sensoriale

- **Aspetto:** Spirali sottili verde argento
- **Aroma:** Floreale, frutta bianca
- **Gusto:** Dolce, delicato
- **Retrogusto:** Fresco

**Origine:** Cina — **Stile:** bi-luo-chun

## Attrezzatura

- Gaiwan
- Acqua 75 °C

## I passaggi

1. Poca acqua, alta foglia - 30 sec
2. 3 g per 100 ml, 90 secondi - 2 min
3. Infusioni brevi successive - 1 min

## Errori comuni

- Temperatura troppo alta che uccide i fiori

## In Italia

In primavera, in parallelo con asparagi e fave: un verde che celebra la rinascita.

## Abbinamenti

- Primavera: verdure tenere
- Dolci poco burrosi

## Domande frequenti

### Cosa significa Bi Luo Chun?

Conchiglia di giada verde — nome poetico cinese.

## Varietà simili

- **Dragon Well** (/varieta/dragon-well/) — altro grande verde cinese
- **Sencha** (/varieta/sencha/) — giapponese primaverile
""",
    },
    "darjeeling-verde": {
        "title": "Darjeeling verde — Himalaya in tazza",
        "origine": "India", "stile": "darjeeling", "caffeina": "Media", "stagione": "Primavera",
        "brew_temp": 80, "brew_grams": 3, "brew_seconds": 180, "brew_infusions": "2",
        "momenti": ["pausa"], "stagioni": ["primavera"],
        "temi_kb": ["storia_cultura", "degustazione_sensoriale"],
        "related_slugs": ["dragon-well", "sencha"],
        "body": """Dalle pendici dell'Himalaya: un verde raro, muschiato e floreale, lontano dai cliché del Darjeeling nero.

## Profilo sensoriale

- **Aspetto:** Foglie scure con punture argento
- **Aroma:** Muschio, fiori di montagna
- **Gusto:** Complesso, leggermente astringente
- **Retrogusto:** Mineralità

**Origine:** India — **Stile:** darjeeling

## Attrezzatura

- Teiera porcellana
- Acqua 80 °C

## I passaggi

1. Infusiona 3 g per 100 ml - 1 min
2. Attendi 3 minuti - 3 min
3. Versa con calma - 1 min

## Errori comuni

- Trattarlo come Darjeeling nero (tempi diversi)

## In Italia

Per chi ama i vini montani: un verde con personalità e terroir leggibile.

## Abbinamenti

- Formaggi medi
- Piatti speziati leggeri

## Domande frequenti

### E lo stesso del Darjeeling nero?

No: stessa regione, lavorazione non ossidata — profilo diverso.

## Varietà simili

- **Dragon Well** (/varieta/dragon-well/) — altro verde con note tostate
- **Sencha** (/varieta/sencha/) — confronto quotidiano
""",
    },
    "cold-brew-gyokuro": {
        "title": "Cold brew gyokuro — estate in bicchiere",
        "origine": "Giappone", "stile": "gyokuro", "caffeina": "Media", "stagione": "Estate",
        "brew_temp": 4, "brew_grams": 5, "brew_seconds": 7200, "brew_infusions": "1",
        "momenti": ["aperitivo"], "stagioni": ["estate"],
        "temi_kb": ["preparazione_servizio", "caffeina_tannini"],
        "related_slugs": ["gyokuro", "sencha"],
        "body": """Ore in frigorifero: il gyokuro freddo esce dolce, setoso, senza amarezza — aperitivo analcolico raffinato.

## Profilo sensoriale

- **Aspetto:** Liquore verde pallido
- **Aroma:** Umami dolce, alghe
- **Gusto:** Setoso, zero astringenza
- **Retrogusto:** Lungo e fresco

**Origine:** Giappone — **Stile:** gyokuro cold brew

## Attrezzatura

- Bottiglia o barattolo
- Frigorifero

## I passaggi

1. 5 g di gyokuro in 500 ml acqua fredda - 2 min
2. Refrigerare 2-4 ore - 4 ore
3. Filtra e servi freddo - 2 min

## Errori comuni

- Usare foglia scadente
- Troppo tempo (amaro)

## In Italia

Alternativa all'aperitivo estivo: elegante, senza zucchero, perfetta per Ferragosto.

## Abbinamenti

- Crudite, bruschette leggere
- Frutta estiva

## Domande frequenti

### Quanta caffeina nel cold brew?

Moderata: estrazione fredda più dolce ma non priva di caffeina.

## Varietà simili

- **Gyokuro** (/varieta/gyokuro/) — versione calda
- **Hojicha freddo** (/varieta/hojicha/) — più tostato
""",
    },
}


def write_variety(slug: str, data: dict) -> None:
    fm_lines = [
        "---",
        f'title: "{data["title"]}"',
        f"slug: {slug}",
        f'meta_description: "Profilo, preparazione e contesto italiano del {slug}."',
        f"origine: {data['origine']}",
        f"stile: {data['stile']}",
        f"caffeina: {data['caffeina']}",
        f"stagione: {data['stagione']}",
        f"brew_temp: {data['brew_temp']}",
        f"brew_grams: {data['brew_grams']}",
        f"brew_seconds: {data['brew_seconds']}",
        f'brew_infusions: "{data["brew_infusions"]}"',
        f"sort_order: {data.get('sort_order', 99)}",
    ]
    if data.get("temi_kb"):
        fm_lines.append("temi_kb: [" + ", ".join(data["temi_kb"]) + "]")
    if data.get("controversie"):
        fm_lines.append("controversie: [" + ", ".join(data["controversie"]) + "]")
    if data.get("related_slugs"):
        fm_lines.append("related_slugs: [" + ", ".join(data["related_slugs"]) + "]")
    if data.get("momenti"):
        fm_lines.append("momenti: [" + ", ".join(data["momenti"]) + "]")
    if data.get("stagioni"):
        fm_lines.append("stagioni: [" + ", ".join(data["stagioni"]) + "]")
    if data.get("percorso_tappa"):
        fm_lines.append(f"percorso_tappa: {data['percorso_tappa']}")
    if data.get("badge_sblocco"):
        fm_lines.append(f"badge_sblocco: {data['badge_sblocco']}")
    if data.get("quiz_correlati"):
        fm_lines.append("quiz_correlati: [" + ", ".join(data["quiz_correlati"]) + "]")
    fm_lines.append("---\n")
    path = ROOT / "varietà" / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(fm_lines) + f"# {data['title'].split('—')[0].strip()}\n\n" + data["body"], encoding="utf-8")


IMPARA_HUBS = {
    "storia-cultura": ("Storia e cultura del tè verde", "Dalle origini cinesi alla tavola italiana."),
    "lavorazione": ("Lavorazione e qualità", "Come la foglia diventa verde in tazza."),
    "preparazione": ("Preparazione e servizio", "Temperatura, tempo, utensili."),
    "degustazione": ("Degustazione sensoriale", "Leggere foglia, liquore e palato."),
    "salute": ("Salute e catechine", "Evidenze sobrie, senza hype detox."),
    "cerimonia": ("Cerimonia e spiritualita", "Rituale codificato e gesto quotidiano."),
    "caffeina": ("Caffeina e tannini", "Quale tè a che ora."),
    "cucina": ("Cucina e usi pratici", "Matcha, riuso foglie, cosmetica."),
}

CONTROVERSIES = {
    "salute-scienza-vs-tradizione": {
        "title": "Quanto è davvero dimostrato che il tè verde faccia bene?",
        "desc": "Scienza e tradizione a confronto sulle catechine.",
        "posizioni": [
            {"fonte": "hara", "tesi": "Servono trial clinici e biodisponibilita misurabile per affermare effetti terapeutici."},
            {"fonte": "rosen", "tesi": "Secoli di medicina cinese e studi epidemiologici supportano benefici su cuore e invecchiamento."},
            {"fonte": "onuma", "tesi": "La saggezza popolare giapponese conferma virtu salutari prima dei paper."},
            {"fonte": "pellegrino", "tesi": "Il tè verde va nella prevenzione, ma non sostituisce le terapie del medico."},
        ],
        "body": "## Per iniziare\n\nIl tè verde contiene catechine con potenziale antiossidante documentato. Quanto possiamo promettere in tazza, però, resta dibattuto.\n\n## Il cuore della questione\n\nTradizione e laboratorio convergono sulla prevenzione, ma divergono su dosi efficaci e certezza delle affermazioni.\n\n## Approfondimento\n\nHara è il più cauto; Rosen e Onuma più divulgativi. In Italia, diffida di chi vende miracoli detox.",
    },
    "bevanda-vs-integratore": {
        "title": "Meglio in tazza o in capsula?",
        "desc": "Bevanda, rituale o estratto di EGCG.",
        "posizioni": [
            {"fonte": "rosen", "tesi": "Gli integratori offrono dosi concentrate ma privano del piacere rituale."},
            {"fonte": "pellegrino", "tesi": "Il matcha, bevendo la foglia intera, concentra antiossidanti più di un infusione filtrata."},
            {"fonte": "hara", "tesi": "I trial usano spesso estratti standardizzati, non tazze di sencha."},
        ],
        "body": "## Per iniziare\n\nCapsule o tazza? Non e solo chimica: e anche cultura e piacere.\n\n## Sintesi\n\nLa bevanda integra gesto e salute; gli estratti servono a chi cerca dosi precise.",
    },
    "cerimonia-cina-vs-giappone": {
        "title": "Gong fu cha o chanoyu: due anime del rituale",
        "desc": "Convivialita cinese e codice giapponese.",
        "posizioni": [
            {"fonte": "sommelier", "tesi": "Il Gong fu Cha e conviviale, centrato su ospitalita e abilita tecnica."},
            {"fonte": "pellegrino", "tesi": "Il Chanoyu e evento formale con koicha, usucha, giardino roji."},
            {"fonte": "onuma", "tesi": "La cerimonia giapponese incarna semplicita adottabile anche in Occidente."},
        ],
        "body": "## Per iniziare\n\nEntrambe elevano acqua e foglia ad arte, con anime diverse.\n\n## Approfondimento\n\nIl gong fu è più sociale; il chanoyu più spirituale e codificato.",
    },
    "qualità-sensoriale-vs-chimica": {
        "title": "Cosa rende un tè verde buono?",
        "desc": "Palato, occhio e laboratorio.",
        "posizioni": [
            {"fonte": "sommelier", "tesi": "Scheda sensoriale: equilibrio corpo/astringenza, assenza difetti."},
            {"fonte": "onuma", "tesi": "Aroma di erba fresca e sapore equilibrato; il prezzo non è l'unico indicatore."},
            {"fonte": "hara", "tesi": "Catechine, cultivar e processo determinano il profilo salutare."},
            {"fonte": "rosen", "tesi": "La bellezza della foglia è il piacere in tazza sono criteri legittimi."},
        ],
        "body": "## Per iniziare\n\nUn tè eccellente al palato tende a essere anche ricco di principi attivi se fresco e ben lavorato.\n\n## Approfondimento\n\nDue linguaggi per valutare la stessa foglia.",
    },
    "caffeina-stimolazione": {
        "title": "Stimola o rilassa? Dipende",
        "desc": "Caffeina, L-teanina e varietà scelta.",
        "posizioni": [
            {"fonte": "pellegrino", "tesi": "Stimola senza eccitare: caffeina legata ai tannini, L-teanina calma."},
            {"fonte": "sommelier", "tesi": "L-teanina aumenta onde alfa e concentrazione."},
            {"fonte": "onuma", "tesi": "Gyokuro prima dello sport si; prima di dormire no."},
        ],
        "body": "## Per iniziare\n\nIl tè verde contiene caffeina ma il profilo dipende da varietà e tempo di infusione.\n\n## In sintesi\n\nScegli la foglia in base al momento della giornata.",
    },
    "consumo-quotidiano-vs-rituale": {
        "title": "Pane quotidiano o occasione speciale?",
        "desc": "Bancha in bottiglia e Chado nello stesso Paese.",
        "posizioni": [
            {"fonte": "onuma", "tesi": "Presenza costante dalla colazione al ristorante."},
            {"fonte": "rosen", "tesi": "Il quotidiano convive con la cerimonia formale."},
            {"fonte": "pellegrino", "tesi": "In Giappone non c e contraddizione tra i due registri."},
        ],
        "body": "## Per iniziare\n\nLa stessa bevanda attraversa registri opposti: abitudine e festa.\n\n## Approfondimento\n\nIn Italia possiamo adottare entrambi senza snaturare le origini.",
    },
}

GLOSSARIO = {
    "sencha": ("Sencha", "Tè verde giapponese non ombreggiato, il più consumato in Giappone."),
    "gyokuro": ("Gyokuro", "Te ombreggiato prima del raccolto, ricco di umami e L-teanina."),
    "matcha": ("Matcha", "Polvere di tencha: si beve la foglia intera sospesa in acqua."),
    "bancha": ("Bancha", "Te da foglie mature, bassa caffeina, sapore morbido."),
    "hojicha": ("Hojicha", "Tè verde tostato, note di nocciola, quasi privo di caffeina."),
    "genmaicha": ("Genmaicha", "Tè verde con riso tostato aggiunto."),
    "kukicha": ("Kukicha", "Te di piccioli e rametti, leggero e dolce."),
    "umami": ("Umami", "Quinto gusto, sapidita brodosa percepita nei verdi giapponesi di alta gamma."),
    "chanoyu": ("Chanoyu", "Via del tè giapponese: cerimonia codificata del matcha."),
    "gong-fu-cha": ("Gong fu cha", "Arte cinese del tè: piccole infusioni multiple in gaiwan o teiera Yixing."),
    "kyusu": ("Kyusu", "Teiera giapponese con manico laterale, spesso per sencha."),
    "yunomi": ("Yunomi", "Tazza cilindrica giapponese senza manico."),
    "chasen": ("Chasen", "Frusta di bambu per preparare il matcha."),
    "chawan": ("Chawan", "Ciotola per matcha nella cerimonia del tè."),
    "tencha": ("Tencha", "Foglia ombreggiata destinata alla macinatura in matcha."),
    "shincha": ("Shincha", "Primo raccolto primaverile, massima freschezza."),
    "catechine": ("Catechine", "Polifenoli antiossidanti, soprattutto EGCG nel tè verde."),
    "egcg": ("EGCG", "Epigallocatechina gallato, catechina più studiata."),
    "l-teanina": ("L-teanina", "Aminoacido del tè che modula gli effetti della caffeina."),
    "camellia-sinensis": ("Camellia sinensis", "Pianta del tè vero, distinta dalle tisane."),
    "longjing": ("Longjing", "Dragon Well: famoso verde cinese appiattito a wok."),
    "gaiwan": ("Gaiwan", "Bicchiere con coperchio per infusioni stile gong fu."),
    "yixing": ("Yixing", "Argilla porosa per teiere dedicate a un solo tipo di te."),
    "astringenza": ("Astringenza", "Sensazione di ruvidita al palato data dai tannini."),
    "wok": ("Wok", "Padella cinese per stabilizzare il tè verde a calore diretto."),
    "vapore": ("Vapore", "Metodo giapponese di stabilizzazione che preserva colore e umami."),
    "usucha": ("Usucha", "Matcha rassente, schiuma leggera."),
    "koicha": ("Koicha", "Matcha denso cerimoniale, più concentrato."),
    "roji": ("Roji", "Giardino del tè che precede la sala cerimoniale."),
    "darjeeling": ("Darjeeling", "Regione himalayana; esiste anche versione verde non ossidata."),
    "cold-brew": ("Cold brew", "Infusione a freddo, estrazione dolce e bassa in tannini."),
    "gunpowder": ("Gunpowder", "Te cinese arrotolato a perle."),
}

MOMENTI = {
    "colazione": ("Tè verde a colazione", "Alternative delicate al cappuccino.", ["bancha", "kukicha", "genmaicha"]),
    "pausa": ("Tè verde in pausa", "Pausa delle 10 o delle 16 senza nervosismo del caffè.", ["sencha", "dragon-well"]),
    "dopo-cena": ("Tè verde dopo cena", "Calore leggero senza tenere svegli.", ["hojicha", "kukicha"]),
    "aperitivo": ("Tè verde all'aperitivo", "Cold brew e hojicha freddo analcolici.", ["cold-brew-gyokuro", "hojicha"]),
}

STAGIONI = {
    "primavera": ("Primavera", "Shincha e primi raccolti.", ["sencha", "bi-luo-chun", "dragon-well"]),
    "estate": ("Estate", "Freddo e leggerezza.", ["cold-brew-gyokuro", "bancha"]),
    "autunno": ("Autunno", "Note tostate.", ["hojicha", "genmaicha", "gunpowder"]),
    "inverno": ("Inverno", "Comfort caldo.", ["genmaicha", "hojicha"]),
}


def main() -> None:
    for slug, data in VARIETIES.items():
        write_variety(slug, data)

    for slug, (title, desc) in IMPARA_HUBS.items():
        p = ROOT / "impara" / f"{slug}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"""---
title: "{title}"
slug: {slug}
meta_description: "{desc}"
---

## Per iniziare

{desc}

## Approfondimento

Esplora le varietà collegate e le controversie di questo tema nel catalogo The Verde.
""", encoding="utf-8")

    for slug, data in CONTROVERSIES.items():
        p = ROOT / "impara" / "controversie" / f"{slug}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        pos_yaml = "\n".join(f'  - fonte: {x["fonte"]}\n    tesi: "{x["tesi"]}"' for x in data["posizioni"])
        p.write_text(f"""---
title: "{data['title']}"
slug: {slug}
meta_description: "{data['desc']}"
posizioni:
{pos_yaml}
---

{data['body']}
""", encoding="utf-8")

    gloss_dir = ROOT / "glossario"
    gloss_dir.mkdir(parents=True, exist_ok=True)
    for slug, (title, desc) in GLOSSARIO.items():
        (gloss_dir / f"{slug}.md").write_text(f"""---
title: "{title}"
slug: {slug}
meta_description: "{desc}"
---

## Per iniziare

{desc}

## Approfondimento

Consulta le schede varietà e le guide collegate per approfondire.
""", encoding="utf-8")

    italia = ROOT / "italia"
    italia.mkdir(parents=True, exist_ok=True)
    (italia / "index.md").write_text("""---
title: "In Italia"
slug: italia
meta_description: "Ponte culturale tra tradizioni del tè e abitudini italiane."
---

## Per iniziare

Il tè verde in Italia non sostituisce il caffè: si affianca come gesto lento e scoperta sensoriale.

## Momenti e stagioni

Esplora hub per colazione, pausa, dopo cena e calendario stagionale.
""", encoding="utf-8")

    for slug, (title, desc, vars_) in MOMENTI.items():
        (italia / "momenti").mkdir(parents=True, exist_ok=True)
        (italia / "momenti" / f"{slug}.md").write_text(f"""---
title: "{title}"
slug: {slug}
meta_description: "{desc}"
varieties: [{", ".join(vars_)}]
---

## Per iniziare

{desc}

## Varietà consigliate

Vedi le schede nel catalogo per preparazione e abbinamenti italiani.
""", encoding="utf-8")

    for slug, (title, desc, vars_) in STAGIONI.items():
        (italia / "stagioni").mkdir(parents=True, exist_ok=True)
        (italia / "stagioni" / f"{slug}.md").write_text(f"""---
title: "{title}"
slug: {slug}
meta_description: "{desc}"
varieties: [{", ".join(vars_)}]
---

## Per iniziare

{desc}
""", encoding="utf-8")

    (italia / "abbinamenti.md").write_text("""---
title: "Abbinamenti gastronomici italiani"
slug: abbinamenti
meta_description: "Tè verde e cucina italiana: cosa funziona davvero."
---

## Per iniziare

Gyokuro con pesce crudo, hojicha con cioccolato fondente, matcha con pasticceria leggera.

## Approfondimento

Evita abbinamenti con acidità forte del pomodoro; onestà su caffeina e digestione.
""", encoding="utf-8")

    guide_dir = ROOT / "guide"
    guide_dir.mkdir(exist_ok=True)
    (guide_dir / "matcha-italia.md").write_text("""---
title: "Perché il matcha non è una moda passeggera in Italia"
slug: matcha-italia
meta_description: "Dal boom pasticceria al matcha cerimoniale."
published: 2026-03-15
---

Il matcha è arrivato nelle vetrine italiane come ingrediente, non come rituale.

## Per iniziare

Tiramisu matcha e gelato verde hanno aperto porte; la ciotola cerimoniale resta un altra storia.

## Approfondimento

Distingui matcha da supermercato zuccherato e tencha cerimoniale di qualità.
""", encoding="utf-8")

    (guide_dir / "te-italia-storia.md").write_text("""---
title: "Il tè verde in Italia: una storia di nicchia"
slug: te-italia-storia
meta_description: "Da Venezia al boom wellness: come il verde e entrato nelle case italiane."
published: 2026-04-01
---

## Per iniziare

Il caffè domina il bar italiano; il tè verde cresce nei tea shop specialty delle grandi città.

## Approfondimento

Oggi: matcha in pasticceria, interesse per single origin, corsi con autori italiani.
""", encoding="utf-8")

    percorsi = ROOT / "gioca" / "percorsi"
    percorsi.mkdir(parents=True, exist_ok=True)
    for slug, title, body in [
        ("dal-bancha-al-matcha", "Dal bancha al matcha", "Quattro tappe dal verde più leggero al matcha cerimoniale."),
        ("palato-italiano", "Il palato italiano", "Degustazione e tre varietà con abbinamenti."),
        ("scienza-tradizione", "Scienza o tradizione", "Tre controversie sulla salute del tè."),
        ("rituale-quotidiano", "Rituale è quotidiano", "Cerimonia, preparazione e due varietà."),
    ]:
        (percorsi / f"{slug}.md").write_text(f"""---
title: "{title}"
slug: {slug}
meta_description: "{body}"
---

## Per iniziare

{body}

Completa ogni tappa e rispondi al micro-quiz per sbloccare il badge.
""", encoding="utf-8")

    pagine = ROOT / "pagine"
    pagine.mkdir(exist_ok=True)
    (pagine / "home.md").write_text("---\ntitle: Home\n---\n", encoding="utf-8")
    (pagine / "privacy.md").write_text("""---
title: Privacy policy
slug: privacy
---

Informazioni sul trattamento dei dati. Il diario in fase 1 resta sul tuo dispositivo (localStorage).
""", encoding="utf-8")
    (pagine / "termini.md").write_text("""---
title: Termini di utilizzo
slug: termini
---

Contenuti editoriali a scopo informativo. Non sostituiscono parere medico.
""", encoding="utf-8")

    print(f"Generated content in {ROOT}")


if __name__ == "__main__":
    main()
