# Catalogo varietà — riferimento operativo

Guida per **variare** gli esempi nelle risposte: non limitarsi a matcha, sencha e gyokuro. Ancorare sempre a `books/knowledge-base.json` e, per le schede del sito, a `content/varieta/`.

## Principio di rotazione

Quando illustri un concetto (preparazione, stagionalità, abbinamento, caffeina, ritualità):

1. Scegli una varietà **diversa** da quelle usate negli ultimi esempi della conversazione.
2. Preferisci varietà **presenti su the-verde.it** se la risposta è editoriale o di navigazione.
3. Cita la KB per parametri tecnici; non inventare profili sensoriali assenti dalle fonti.
4. Distingui **verde non ossidato** da oolong, tisane e matcha-latte industriali.

## Le 12 varietà del sito (`content/varieta/`)

Mappa temi KB da `content/relazioni.json` → `varieta_temi`.

| Slug | Nome | Origine | Caffeina | Profilo in breve | Temi KB | Momento IT |
|------|------|---------|----------|------------------|---------|------------|
| `bancha` | Bancha | Giappone | Bassa | Foglia matura, erba leggera, quotidiano | preparazione, caffeina | Colazione alternativa, stomaco vuoto |
| `sencha` | Sencha | Giappone | Media | Verde brillante, marinezza, amaro controllato | preparazione, degustazione | Pausa lavoro, quotidianità |
| `gyokuro` | Gyokuro | Giappone | Media-alta | Ombreggiato, umami denso, setoso | lavorazione, degustazione | Degustazione attenta, non di fretta |
| `matcha` | Matcha | Giappone | Alta | Polvere di tencha, corpo pieno, cerimonia/cucina | cerimonia, cucina | Pasticceria, ritualità, attenzione |
| `genmaicha` | Genmaicha | Giappone | Bassa | Riso tostato + bancha, cereale, comfort | cucina, preparazione | Inverno, dopo cena, neofiti |
| `hojicha` | Hojicha | Giappone | Molto bassa | Foglia tostata, nocciola, zero nervosismo | lavorazione, caffeina | Sera, bambini, alternative al decaffeinato |
| `kukicha` | Kukicha | Giappone | Bassa | Rametti e fogli, dolce leggero, economico | caffeina, preparazione | Tutto il giorno, bassa caffeina |
| `dragon-well` | Long Jing (Dragon Well) | Cina (Zhejiang) | Media | Nocciola, fagiolini, piatto in tazza | storia, degustazione | Primavera, abbinamento vegetali |
| `gunpowder` | Gunpowder (Zhu Cha) | Cina | Media | Perle arrotolate, robusto, resiste al calore | storia, preparazione | Autunno, teiera grande, viaggio |
| `bi-luo-chun` | Bi Luo Chun | Cina (Jiangsu) | Media | Spirali primaverili, floreale, frutta bianca | lavorazione, degustazione | Primavera, gaiwan, palato raffinato |
| `darjeeling-verde` | Darjeeling verde | India (Himalaya) | Media | Muschio, montagna, mineralità | storia, degustazione | Chi ama vini bianchi minerali |
| `cold-brew-gyokuro` | Cold brew gyokuro | Giappone | Bassa-media | Umami freddo, dolcezza, zero amaro | preparazione, caffeina | Estate, Ferragosto, aperitivo |

### Schede tecniche rapide (sito)

Parametri da front matter delle schede — usarli per consigli pratici, non come dogma universale:

| Varietà | °C | g/100 ml | Secondi | Infusioni |
|---------|-----|----------|---------|-----------|
| Bancha | 80 | 3 | 60 | 2 |
| Sencha | 75 | 3 | 60 | 2–3 |
| Gyokuro | 50–60 | 4 | 90 | 2–3 |
| Matcha | — | 2 g / 70 ml | frusta | 1 |
| Genmaicha | 85 | 3 | 45 | 2 |
| Hojicha | 90 | 3 | 30 | 2–3 |
| Kukicha | 80 | 3 | 60 | 2 |
| Dragon Well | 80 | 3 | 120 | 2–3 |
| Gunpowder | 85 | 3 | 90 | 2–3 |
| Bi Luo Chun | 75 | 3 | 90 | 3 |
| Darjeeling verde | 80 | 3 | 180 | 2 |
| Cold brew gyokuro | freddo | 5 | 4–8 h | 1 |

## Famiglie e lavorazione

### Giappone — vapore (steaming)

| Famiglia | Varietà | Nota distintiva |
|----------|---------|-----------------|
| Ombreggiati | Gyokuro, matcha (da tencha) | Shade-growing → clorofilla, L-teanina, umami |
| Esposti al sole | Sencha, bancha | Più catechine; amaro se scottato |
| Derivati | Kukicha (rametti), hojicha (tostato), genmaicha (blend) | Economia della pianta, profili accessibili |
| Stagionali | Shincha (primo raccolto sencha) | In KB e mercato JP; narrativa primavera |

**Fonti KB:** `pellegrino` → verdi giapponesi (pp. 123–128); `rosen` → lavorazione bancha/sencha; `onuma` → consumo quotidiano vs Chado.

### Cina — padella (pan-firing) o vapore

| Famiglia | Varietà | Nota distintiva |
|----------|---------|-----------------|
| Tè famosi | Long Jing, Bi Luo Chun | Forma foglia, raccolto primaverile, terroir |
| Quotidiani | Gunpowder | Perle compatte, conservazione, infusioni ripetute |
| Altri (in KB, non ancora su sito) | Huangshan Maofeng, Liu'an Guapian… | Citare da `pellegrino` se serve ampliare |

**Fonti KB:** `sommelier` → scheda Lung Ching (pp. 3103–3120); `pellegrino` → verdi cinesi (pp. 112–122).

### India e mondo

| Varietà | Nota | Fonte KB |
|---------|------|----------|
| Darjeeling verde | Raro, muschiato, lontano dal Darjeeling nero | `pellegrino`, contesto indiano in `rosen` |
| Nilgiri verde | Scheda sensoriale in `sommelier` (pp. 3178–3194) | Degustazione professionale |
| Jeoncha (Corea) | Tradizione mondiale in `pellegrino` | Cerimonia e quotidianità coreana |

## Varietà per tipo di domanda

| Domanda utente | Varietà da privilegiare | Evitare come unico esempio |
|----------------|-------------------------|----------------------------|
| «Primo tè verde» | Bancha, genmaicha, kukicha | Gyokuro (troppo esigente) |
| «Sostituto caffè pomeridiano» | Sencha, dragon well, darjeeling verde | Matcha (caffeina alta) |
| «Prima di dormire» | Hojicha, kukicha, bancha | Sencha, matcha, gyokuro |
| «Estate / freddo» | Cold brew gyokuro, bancha freddo | Gyokuro caldo a 60 °C |
| «Cerimonia / mindfulness» | Matcha, gyokuro | Gunpowder |
| «Cucina / ricette» | Matcha, hojicha in dessert | Dragon well (da bere) |
| «Regalo in Italia» | Set misto: sencha + matcha + hojicha | Solo matcha latte trend |
| «Amaro / errore preparazione» | Sencha (acqua troppo calda), bi luo chun (troppa foglia) | — |
| «Storia e cultura» | Dragon well, gunpowder, matcha | Cold brew |
| «Salute / catechine» | Matcha (foglia intera), sencha quotidiano | Claim su bancha senza fonte |

## Confronti utili (non banali)

| Confronto | Cosa impara il lettore |
|-----------|------------------------|
| Sencha vs gyokuro | Sole vs ombra; temperatura e umami |
| Dragon well vs bi luo chun | Due primavere cinesi: nocciola piana vs spirale floreale |
| Bancha vs kukicha | Foglia matura vs rametti; entrambi leggeri |
| Hojicha vs genmaicha | Tostatura foglia vs riso tostato; due «comfort» diversi |
| Gunpowder vs sencha | Robustezza cinese vs delicatezza giapponese |
| Matcha vs sencha in polvere | Cerimoniale vs culinary grade; non sono intercambiabili |
| Darjeeling verde vs Nilgiri | Due India verdi (KB sommelier) per chi cerca mineralità |
| Gyokuro caldo vs cold brew gyokuro | Stessa foglia, estrazione diversa, estate vs inverno |

## Abbinamenti gastronomici italiani per varietà

| Varietà | Abbinamento sensato | Da evitare |
|---------|---------------------|------------|
| Dragon well | Risotto primaverile, fagiolini, pesce di lago | Sugo pomodoro acido |
| Bi luo chun | Mozzarella di bufala, fiori di zucca | Formaggi blue |
| Gunpowder | Bruschette, olive, antipasti mediterranei | Dolci al cioccolato bianco |
| Genmaicha | Zuppa di legumi, pane toscano | Caffè subito dopo |
| Hojicha | Cantucci, cioccolato fondente 70% | Agrumi molto acidi |
| Kukicha | Merenda leggera, frutta | — |
| Darjeeling verde | Formaggi di montagna delicati, tartare | Parmigiano 36 mesi |
| Cold brew gyokuro | Aperitivo estivo, insalate | Piatti piccanti |

## Errori comuni per varietà (Italia)

| Varietà | Errore italiano tipico | Correzione |
|---------|------------------------|------------|
| Sencha | Acqua dell'ebollitore | 70–80 °C |
| Gyokuro | Infusione lunga «come il tè in bustina» | 50–60 °C, secondi brevi |
| Matcha | Polvere da supermercato zuccherata in latte | Grado cerimoniale/cucina, frusta chasen |
| Dragon well | Acqua troppo calda che appiattisce nocciola | 75–80 °C, acqua dolce |
| Gunpowder | Trattarlo come tè delicato | Può reggere temperature più alte |
| Hojicha | Confonderlo con tè nero | È verde tostato, bassa caffeina |
| Bancha | Snobismo («è tè povero») | Tradizione quotidiana giapponese autentica |
| Darjeeling verde | Aspettarsi muscat del Darjeeling nero | Profilo verde, montagna, altra bevanda |

## Varietà citate in KB ma non (ancora) sul sito

Citare quando arricchiscono la risposta; non inventare schede tecniche oltre la KB.

| Nome | Origine | Dove in KB |
|------|---------|------------|
| Shincha | Giappone | Stagionalità, primo raccolto sencha |
| Tencha | Giappone | Base del matcha (ombreggiato, non arrotolato) |
| Nilgiri verde | India | `sommelier` → degustazione (pp. 3178–3194) |
| Jeoncha | Corea | `pellegrino` → tradizioni mondiali |
| Huangshan Maofeng, Liu'an Guapian | Cina | `pellegrino` → verdi cinesi (elenco) |

## Percorsi di degustazione suggeriti

Per lettori italiani che vogliono **esplorare senza ripetere sempre matcha**:

1. **Percorso quotidiano:** bancha → sencha → genmaicha
2. **Percorso primavera:** bi luo chun → dragon well → shincha (se disponibile)
3. **Percorso umami:** sencha → gyokuro → matcha koicha
4. **Percorso sera:** kukicha → hojicha
5. **Percorso Cina:** gunpowder → dragon well → bi luo chun
6. **Percorso estate:** sencha freddo → cold brew gyokuro
7. **Percorso mondo:** sencha → darjeeling verde → (Nilgiri da KB)

## Collegamenti interni

- Temi trasversali per varietà: `content/relazioni.json` → `varieta_temi`
- Percorsi gamificati: `content/_config/paths.json`, `content/_config/quizzes.json`
- Voce e formato scheda: [voice-guide.md](voice-guide.md)
- Contesto Italia: [cultura-italiana.md](cultura-italiana.md)
