# Piano di lavoro e consegna

Questo documento serve a chi riprende il lavoro in una sessione nuova, senza la
memoria di quelle precedenti. Il **come è fatto** il progetto sta in
`docs/superpowers/specs/2026-08-10-anki-istologia-design.md`. Qui c'è **a che
punto siamo, con quali convenzioni, e cosa fare dopo**.

Aggiornare questo file fa parte del lavoro: se lo stato qui non corrisponde più
a `cards/`, la prossima sessione lavora su informazioni false.

---

## 1. Prima di toccare qualsiasi cosa

`build/` e `dist/` sono in `.gitignore`, quindi dopo un clone **non esistono**.
Le carte referenziano immagini come `lab_p042_2435.jpg` che senza questo passaggio
non sono sul disco, e la validazione fallisce su ogni carta con immagine.

```sh
cd /Users/pietrodibello/tools/anki-istologia
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt

DL=/Users/pietrodibello/Downloads
./venv/bin/python scripts/extract.py --pdf "$DL/Istologia Laboratorio combinato.pdf" --source-id lab --out build/lab
./venv/bin/python scripts/extract.py --pdf "$DL/Istologia 5th gen-combinato.pdf" --source-id teoria --out build/teoria
./venv/bin/python scripts/segment.py --build build/lab
./venv/bin/python scripts/segment.py --build build/teoria

./venv/bin/python -m pytest tests/ -q          # atteso: 151 passed
```

L'estrazione della teoria richiede qualche minuto: 256 pagine e 463 immagini.

Poi, per leggere una sezione su cui lavorare:

```sh
./venv/bin/python scripts/show_section.py --build build/lab --id 015
```

E per ricostruire il pacchetto (la validazione parte da sola, e se fallisce il
pacchetto non viene scritto):

```sh
./venv/bin/python -m scripts.build_apkg --cards cards/laboratorio \
    --media build/lab/images --out dist/Istologia-Laboratorio.apkg

./venv/bin/python -m scripts.build_apkg --cards cards/teoria \
    --media build/teoria/images --out dist/Istologia-Teoria.apkg
```

**Due pacchetti, uno per fonte**, non uno solo: `--media` è una singola
directory e le immagini stanno in due alberi separati (`build/lab/images` e
`build/teoria/images`). In Anki non cambia nulla, i mazzi restano sotto lo
stesso genitore `Istologia::` e i tag `argomento::` continuano a pescare da
entrambe le fonti. Così la teoria si consegna un capitolo per volta senza
rispedire ogni volta le 673 note del laboratorio.

---

## 2. Stato al 2026-08-11

**673 note** di Laboratorio + **707 di Teoria**, 276 immagini, 151 test verdi.
**Il Laboratorio è finito**: tutte e 106 le pagine sono coperte. **La Teoria è
aperta**: 8 capitoli su 18, pagine 1-16 e 28-93 di 256.

Lo stile delle carte è stato **approvato da Pietro** dopo aver importato un
campione in Anki. Non va reinventato: vedi le convenzioni al punto 3.

### Laboratorio (106 pagine, 28 sezioni)

| File | Note | Copre |
|---|---|---|
| `01-colorazioni.jsonl` | 38 | sezioni 002-005, pagine 2-6 |
| `02-tessuti-epiteliali.jsonl` | 34 | sezioni 006-007, pagine 6-8 |
| `03-ghiandolare-esocrino.jsonl` | 35 | sezione 009, classificazione, pagine 14-16 |
| `03b-esocrino-vetrini.jsonl` | 48 | sezione 009, vetrini 1-13, pagine 17-25 |
| `04a-endocrino-classificazione.jsonl` | 15 | sezione 011, pagine 28-29 |
| `04b-endocrino-ipofisi-tiroide-paratiroide.jsonl` | 26 | sezione 011, vetrini 1-3, pagine 29-32 |
| `04c-quiz-endocrino.jsonl` | 18 | generato, pagine 40-42 |
| `04d-quiz-endocrino-aperte.jsonl` | 4 | scritto a mano, domande 19-22 |
| `05a-tessuti-connettivi.jsonl` | 41 | sezioni 013-015, vetrini 1-7, pagine 43-50 |
| `05c-quiz-connettivi.jsonl` | 21 | generato, pagine 51-54 |
| `06a-cartilagine.jsonl` | 25 | sezione 018, pagine 55-57 |
| `06b-tessuto-osseo.jsonl` | 32 | sezione 019, pagine 57-58 |
| `06c-sangue-e-linfoide.jsonl` | 26 | sezione 019, pagine 59-60 |
| `06d-vetrini.jsonl` | 45 | sezione 019, vetrini 1-11, pagine 61-70 |
| `06e-quiz-connettivi-specializzati.jsonl` | 30 | generato, pagine 71-75 |
| `06f-timo.jsonl` | 15 | sezione 026, pagine 104-105 |
| `07a-tessuto-muscolare.jsonl` | 24 | sezione 020, pagine 76-77 |
| `07b-vetrini-muscolari.jsonl` | 20 | sezione 022, vetrini 1-3, pagine 82-85 |
| `08a-tessuto-nervoso.jsonl` | 27 | sezione 021, pagine 78-80 |
| `08b-snp-nervi-e-gangli.jsonl` | 18 | sezione 022, pagine 80-81 |
| `08b2-vetrini-nervoso.jsonl` | 39 | sezione 022, vetrini 4-9, pagine 86-91 |
| `08c-quiz-nervoso.jsonl` | 24 | generato, pagine 92-95: **domande 1-15 sul muscolare**, 16-24 sul nervoso |
| `09a-embriologia.jsonl` | 20 | sezione 025, pagine 96-97 |
| `09b-modellini-embriologia.jsonl` | 37 | sezione 026, modellini 1-9, pagine 98-103 |
| `10a-tonsilla-palatina.jsonl` | 11 | sezione 027, pagina 106 |

**La sezione 019 non è solo il tessuto osseo**, nonostante il titolo. Copre
osso, sangue, sistema linfoide, undici vetrini e il quiz finale, tutto dentro
il capitolo `06 - Tessuti connettivi specializzati` aperto dalla cartilagine.
I quattro file `06b`-`06e` la chiudono per intero.

**Anche la sezione 022 mescola gli argomenti**, come già il suo quiz: i primi
tre dei nove vetrini sono di tessuto **muscolare** (lingua, cuore, intestino).
Le loro carte stanno in `07b`, nel mazzo `07 - Tessuto muscolare`, perché è lì
che Pietro ripassa il muscolare; il campo `source` rimanda comunque alle pagine
82-85. Il precedente di `06d` (deck del capitolo dove sta la pagina) non si
applicava: lì tutti gli argomenti appartenevano davvero a quel capitolo.
Spostare una carta di mazzo è comunque sicuro, il guid dipende solo dall'id.

Il nome `08b2` esiste perché `08c` era già occupato dal quiz, generato prima
che il capitolo fosse scritto: `08b` è la teoria del periferico, `08b2` i suoi
vetrini, e l'ordine alfabetico resta quello delle pagine.

### Teoria (256 pagine, 111 sezioni)

| File | Note | Copre |
|---|---|---|
| `01-preparazione-preparato.jsonl` | 64 | sezioni 001-006, pagine 1-7 |
| `02-colorazioni-istochimiche.jsonl` | 60 | sezioni 007-009 + inizio 010, pagine 7-12 |
| `03-tessuti-e-rinnovamento.jsonl` | 58 | sezione 010, seconda metà, pagine 12-15 |
| `06a-epiteli-di-rivestimento.jsonl` | 84 | sezione 021, pagine 28-37 |
| `06b-giunzioni-e-dominio-basale.jsonl` | 74 | sezioni 022-023, pagine 38-48 |
| `07-concetti-base-di-microscopia.jsonl` | 89 | sezione 024, pagine 49-59 |
| `08a-epitelio-di-rivestimento.jsonl` | 132 | sezioni 025-033, pagine 60-75 |
| `08b-cellule-epidermide-e-sommario.jsonl` | 39 | sezioni 034-035, pagine 76-82 |
| `08c-quiz-tessuto-epiteliale.jsonl` | 12 | sezione 036, pagine 82-84 |
| `09-epiteli-ghiandolari.jsonl` | 22 | sezioni 037-039, pagine 85-86 |
| `10-ghiandole-esocrine.jsonl` | 73 | sezioni 040-041, pagine 86-93 |

**Il capitolo 01 non esiste come titolo nel PDF.** Le pagine 1-7 non hanno
intestazione di capitolo: sono la definizione di istologia e le cinque fasi di
preparazione del campione (fissazione, disidratazione, inclusione, taglio,
colorazione). Sono materiale d'esame come il resto, quindi hanno un mazzo loro.

Nel capitolo 01 rientrano anche l'Ematossilina-Eosina e le tricromiche, perché
la colorazione è la quinta fase della preparazione. Il capitolo `02 -
Colorazioni istochimiche` è un'altra cosa: PAS, Sudan e simili.

Otto delle nove figure del capitolo 01 sono state usate. La nona,
`teoria_p007_22.jpg`, è il solito caso di sovrapposizione ai bordi (punto 6):
sta a pagina 7 ma illustra le colorazioni istochimiche. È stata poi usata nel
capitolo 02, dove appartiene.

**Il capitolo 02 si ferma a pagina 12, non a pagina 24.** A pagina 12 la
sbobina apre `TESSUTI E RINNOVAMENTO`, un titolo che `segment.py` non riconosce;
il segmentatore attribuisce perciò alle "Colorazioni istochimiche" tutte le
pagine fino al titolo successivo che riconosce, a pagina 24. Vedi qui sotto la
ricognizione dei titoli mancanti: sono tre in tutto e sono stati tutti trovati,
quindi **la numerazione dei mazzi qui sotto è definitiva** e non verrà più
spostata.

**Il capitolo 03 sta dentro la sezione 010 e occupa le pagine 12-15.** Comincia
a metà di pagina 12, alla riga `TESSUTI E RINNOVAMENTO`: quello che sta sopra
sono gli artefatti di preparazione, già coperti dal mazzo 02. Finisce alla fine
di pagina 15; pagina 16 riparte con `CELLULE STAMINALI E POTENZIALE
DIFFERENZIATIVO`, che è il mazzo 04. La tabella dei mazzi dice "12-16" perché
indica la pagina in cui il capitolo successivo comincia, non l'ultima scritta.

Le pagine 12-15 hanno cinque figure e **sono state usate tutte**. Due sono
schemi con i nomi stampati sopra (`teoria_p013_47` sul differenziamento,
`teoria_p015_56` sulla divisione asimmetrica) e stanno sul retro; le due
tavole di microfotografie dei tessuti muscolari (`teoria_p013_45`) e del
connettivo dell'epiglottide (`teoria_p012_42`) pure, la prima perché la sbobina
non dice quale pannello sia quale, la seconda perché porta le sigle `Ep`, `TCL`
e `TCD` stampate sopra. Solo la tavola dei tre epiteli (`teoria_p012_41`) è
senza etichette, e sta sul fronte.

---

## 3. Convenzioni delle carte

Questa è la parte che una sessione nuova dedurrebbe in modo leggermente diverso,
rendendo il mazzo incoerente a metà. Vanno seguite alla lettera.

### Identificatori

```
"id": "<fonte>-<argomento>-<NNN>"      es. lab-epiteli-012, lab-quiz-nervoso-003
```

Zero-padded a tre cifre. **Un id pubblicato non si cambia mai.** Il guid della
nota Anki deriva solo dall'id: cambiarlo fa perdere a Pietro lo storico di
ripetizione di quella carta. Correggere il testo invece va benissimo, è proprio
il caso d'uso per cui il guid è costruito così. Anche i **tag** si correggono
liberamente: non entrano nel guid.

**La numerazione prosegue per argomento, non per file.** Un argomento ripartito
su più file continua da dove il file precedente si era fermato, perché l'id deve
restare unico dentro tutto il mazzo:

| Argomento | Dove sta |
|---|---|
| `lab-osso` | `06b` 001-032, poi `06d` 033-046 |
| `lab-cartilagine` | `06a` 001-025, poi `06d` 026-043 |
| `lab-muscolare` | `07a` 001-024, poi `07b` 025-044 |
| `lab-nervoso` | `08a` 001-027, poi `08b` 028-045, poi `08b2` 046-084 |
| `lab-linfoide` | `06c` 001-012, `06d` 013-021, `06f` 022-036, poi `10a` 037-047 |
| `lab-embriologia` | `09a` 001-020, poi `09b` 021-057 |
| `teoria-tecnica` | `01` 001-038, poi `02` 039-049 |
| `teoria-colorazioni` | `01` 001-026, `02` 027-075, poi `10` 076-079 |
| `teoria-ghiandole` | `09` 001-016, poi `10` 017-085 |

**Il capitolo 03 apre quattro argomenti che appartengono a capitoli successivi.**
È la panoramica dei quattro tessuti fondamentali, quindi qualche sua carta parla
di epiteli, connettivi, muscolare e nervoso prima che i mazzi 06, 12, 17 e 18
esistano. Quelle carte portano l'`argomento::` del tessuto di cui parlano, non
`tessuti`, così la selezione trasversale le pesca insieme al capitolo che verrà;
di conseguenza il loro id segue lo stesso argomento. Chi scriverà quei capitoli
**non riparte da 001**:

| Argomento | Già usato dal capitolo 03 | Il prossimo capitolo riparte da |
|---|---|---|
| `teoria-epiteli` | 001 | 002, ed è già stato fatto: il capitolo 06 occupa 002-159 e il capitolo 08 occupa 160-342 |
| `teoria-connettivi` | 001-004 | 005 |
| `teoria-muscolare` | 001 | 002 |
| `teoria-nervoso` | 001-002 | 003 |

**Lo stesso è successo con il capitolo 09 e l'endocrino.** Il 09 confronta le
ghiandole esocrine con le endocrine, quindi sei delle sue carte parlano di
endocrino prima che il mazzo 11 esista: portano `argomento::endocrino` e l'id
`teoria-endocrino-001`-`006`. **Chi scriverà il mazzo 11 riparte da 007.**

I salti sono ammessi (`lab-esocrino` passa da 035 a 040): serve che i numeri
crescano e non si ripetano, non che siano contigui. Prima di aprire un file
nuovo, controlla dove è arrivato l'argomento:

```sh
grep -ho '"id": "lab-osso-[0-9]*"' cards/laboratorio/*.jsonl | sort | tail -1
```

### Mazzi

```
Istologia::Laboratorio::<NN> - <Nome capitolo>
Istologia::Laboratorio::Quiz              (unico, per tutti i quiz)
Istologia::Teoria::<NN> - <Nome capitolo>
```

La numerazione segue l'ordine delle pagine nella sbobina, così i mazzi si
ordinano da soli come il corso.

### Tag

Tre assi indipendenti, più uno di segnalazione:

| Asse | Valori usati finora |
|---|---|
| `fonte::` | `lab`, `teoria` |
| `argomento::` | `colorazioni`, `epiteli`, `ghiandole`, `endocrino`, `connettivi`, `cartilagine`, `osso`, `sangue`, `linfoide`, `muscolare`, `nervoso`, `embriologia`, `tecnica-istologica`, `tessuti`, `staminali`, `microscopia` |
| `tipo::` | `definizione`, `classificazione`, `elenco`, `sequenza`, `riconoscimento`, `confronto`, `quiz` |
| segnalazione | `da-verificare`, `non-trattato` |

Riusa i valori esistenti prima di inventarne di nuovi: i tag servono a Pietro per
studiare in trasversale, e un sinonimo in più rompe la selezione.

`argomento::` **attraversa le due fonti apposta**: le carte di teoria sulla
Ematossilina-Eosina portano `argomento::colorazioni` come quelle di laboratorio,
così una selezione per argomento pesca da entrambi i tagli. `tecnica-istologica`
è stato introdotto dai capitoli 01-02 della Teoria e copre il metodo
(fissazione, inclusione, taglio, congelamento) più le carte introduttive sulla
disciplina.

Il capitolo 03 ha aggiunto gli ultimi due valori e non se ne prevedono altri:

- `tessuti` — la panoramica: che cos'è un tessuto, l'equilibrio dinamico, le
  popolazioni perenni, stabili e labili, le due vie del rinnovamento. Sono le
  carte che non appartengono a nessuno dei quattro tessuti in particolare.
- `staminali` — le cellule staminali, che avranno per sé i mazzi 04 e 05.

`embriologia` invece **non è nuovo**: esisteva già nel Laboratorio (mazzi 09a e
09b) ed è stato riusato per gastrulazione, foglietti embrionali e creste neurali,
che sono lo stesso argomento visto dal lato dei meccanismi.

Il capitolo 07 ne ha aggiunto uno solo, `microscopia`, che copre tutta l'ottica
e la strumentazione: occhio, lenti, aberrazioni, diffrazione, obiettivi, metodi
di contrasto e fluorescenza. Non è stato accorpato a `tecnica-istologica` perché
quello è il **metodo di preparazione** del campione, mentre qui si parla dello
**strumento** con cui lo si guarda, e da solo vale quasi novanta carte.

Il capitolo 08 **non ne ha aggiunti**: le sue 183 carte stanno quasi tutte su
`epiteli`, e le poche che parlano d'altro riusano valori esistenti
(`sangue` per gli eritrociti, `linfoide` per i linfociti intraepiteliali e per
le cellule di Langerhans, `nervoso` per le terminazioni nervose libere,
`staminali` per le cripte intestinali, `tecnica-istologica` per
l'immunoistochimica, `colorazioni` per la PAS sulle cellule caliciformi).

**Nemmeno i capitoli 09 e 10 ne hanno aggiunti.** Riusano `ghiandole` e
`endocrino`, che il Laboratorio aveva già introdotto con `lab-esocrino` e
`lab-endocrino`, e `colorazioni` per le quattro carte il cui contenuto è la
colorazione e non la ghiandola: mucina invisibile alle colorazioni comuni,
tricromica e PAS sull'intestino tenue, Alcian blu sul colon, secreto mucoso
invisibile in ematossilina-eosina. Non è stato inventato un `esocrino` a parte:
nel Laboratorio l'argomento delle esocrine si chiama già `ghiandole`.

### Il tag `non-trattato`

La sbobina marca alcuni passaggi con un riquadro laterale **"Argomento non
trattato nell'anno 2024/2025"**. Le carte si scrivono lo stesso — il materiale
è nella dispensa e potrebbe tornare — ma portano il tag `non-trattato` e lo
dicono in fondo al `back`, così Pietro può sospenderle in blocco con
`tag:non-trattato` se decide di fidarsi del programma dell'anno.

Il primo caso è `teoria-microscopia-015` (immagine reale e virtuale, pagina 50).
Il riquadro va guardato nel PDF renderizzato, perché nel testo estratto compare
come tre parole isolate e non si capisce quanta parte copra:

```sh
./venv/bin/python -c "import pymupdf; \
  pymupdf.open('$DL/Istologia 5th gen-combinato.pdf')[49].get_pixmap(dpi=110).save('/tmp/p50.png')"
```

Da non confondere con il caso del **timo** del Laboratorio, dove la sbobina dice
il contrario: non trattato a lezione **ma presente all'esame**. Quelle carte non
vanno sospese e infatti non portano il tag.

`quiz_to_cards.py` applica gli stessi tag a tutte le carte che genera, ma **un
quiz copre spesso più di un capitolo**: quello di pagina 71-75 va dalla
cartilagine al linfoide, quello di pagina 92-95 dedica al muscolare 15 domande
su 24 nonostante si chiami `08c-quiz-nervoso`. L'`argomento::` va quindi
riletto e corretto a mano dopo la generazione, domanda per domanda, altrimenti
quelle carte spariscono dalle selezioni trasversali. Il file committato è la
versione corretta, non quella appena uscita dal generatore, e il generatore si
rifiuta di sovrascriverlo (vedi punto 6).

Correggere i tag è sempre sicuro: il guid della nota dipende **solo dall'id**,
quindi ritaggare non tocca lo storico di ripetizione di Pietro.

### Campo `source`

Sempre valorizzato, sempre con la pagina: `Laboratorio p. 15`, `5th gen p. 42`.
È quello che permette di risalire all'originale quando una carta non convince.

### Immagini

| Caso | Dove va |
|---|---|
| Microfotografia senza etichette scritte | **fronte**, `"image_side": "front"` |
| Microfotografia annotata con richiami che non nominano la struttura | **fronte** |
| Schema con il nome della struttura stampato sopra | **retro** |
| Screenshot di quiz con marcatori numerati | **fronte** |
| Icona, logo, striscia di layout | scartata |

Il criterio è uno solo: **la figura sul fronte deve porre una domanda senza
contenerne la risposta.** In caso di dubbio va sul retro, che è il default se
`image_side` non è specificato.

Le immagini vanno **guardate una per una** prima di decidere: la didascalia
estratta è solo un aiuto e a volte è sbagliata (vedi punto 5).

### Cloze

Al massimo 4-5 eliminazioni per nota, e devono partire da `c1`. Il validatore
rifiuta una numerazione che non parte da c1 e una sintassi malformata.

Ricorda che una nota cloze con 4 buchi genera **4 carte**: è il motivo per cui il
README raccomanda a Pietro di attivare la sepoltura dei fratelli.

### Fedeltà alla sbobina

**Non correggere mai in silenzio.** Se un passaggio sembra sbagliato:

1. la carta riporta quello che dice la sbobina
2. tag `da-verificare`
3. nel campo `extra` (cloze) o in fondo al `back` (base), la spiegazione di cosa
   non torna e cosa ci si aspetterebbe

Il motivo è che una correzione silenziosa è indistinguibile da un errore mio, e
Pietro non ha modo di sapere quali carte controllare. Quelle segnalate le
verifica sul libro e decide lui.

I refusi puramente grammaticali della sbobina (parola caduta, accordo sbagliato)
si sistemano invece senza cerimonie: non cambiano il contenuto.

---

## 4. Cosa resta, in ordine

Resta la sola Teoria. **L'ordine di lavorazione è stato concordato con Pietro il
2026-08-10** e sta qui sotto.

### Laboratorio

**Non resta niente.** Le 28 sezioni sono coperte tutte; le sole saltate sono la
024 e la 023 nella parte non-quiz, che contengono solo link a video di ripasso.

Due cose trovate lungo la strada che il piano non prevedeva, da non perdere se
si torna sul Laboratorio:

- **Il timo** (pagine 104-105) non era elencato da nessuna parte: sta dentro la
  sezione dei modellini perché il professore lo ha ripreso a fine corso, per un
  vetrino che non era stato osservato. La nota dice esplicitamente che **non è
  stato trattato durante il corso ma sarà presente all'esame**. Le sue carte
  stanno in `06f`, nel mazzo 06 con il resto del linfoide.
- Della **tonsilla palatina** il professore **non ha specificato** se sarà
  all'esame. Ha un mazzo suo (`10`), quindi Pietro può sospenderlo se decide di
  lasciarla perdere.

Delle 45 figure della sezione 022 ne sono state usate 35. Le dieci scartate
sono quasi tutte doppioni dello stesso campo a ingrandimento simile
(`lab_p082_5330`, `lab_p082_5332`, `lab_p083_5371`, `lab_p088_5555`,
`lab_p088_5557`, `lab_p089_5593`), più tre casi su cui non si poteva costruire
una domanda onesta: `lab_p084_5401` e `lab_p085_5433` non sono identificabili
con certezza, e `lab_p085_5429`/`lab_p085_5431` sono quelle di cui **il prof
stesso dice di non essere sicuro della colorazione**. Non c'è materiale rimasto
da recuperare lì.

Attenzione al conteggio delle parole di una sezione: quello di `sections.jsonl`
comprende anche le descrizioni dei vetrini e le pagine di quiz, che sono lavoro
diverso dalla teoria. La sezione 019 dichiarava 4.260 parole ed erano in realtà
due pagine di teoria sull'osso, due sul sangue e sul linfoide, undici vetrini e
trenta domande di quiz: quattro file di carte, non uno.

I quiz del Laboratorio sono **tutti fatti**: pagine 40-42, 51-54, 71-75 e 92-95.
Se ne emergessero altri, il generatore gestisce già le quattro convenzioni di
marcatura.

### Teoria

111 sezioni, 98.000 parole, 463 immagini, **diciotto mazzi**.

I quindici capitoli elencati nella prima stesura di questo piano erano quelli
che `segment.py` riconosce come titolo. Ne mancano tre, cercati e trovati tutti
(la ricognizione è qui sotto), e la numerazione che ne risulta è **definitiva**.

La colonna "pagine" è l'**estensione reale**, non la pagina del titolo. La
colonna "ordine" è la sequenza di lavorazione concordata.

| Mazzo | Pagine | pp | Ordine | Stato |
|---|---|---|---|---|
| 01 - Preparazione del preparato istologico | 1-7 | 7 | 1 | **fatto**, 64 note |
| 02 - Colorazioni istochimiche | 7-12 | 6 | 2 | **fatto**, 60 note |
| 03 - Tessuti e rinnovamento | 12-16 | 5 | 3 | **fatto**, 58 note |
| 04 - Cellule staminali e potenziale differenziativo | 16-24 | 9 | 16 | |
| 05 - Applicazioni terapeutiche delle cellule staminali | 24-28 | 5 | 17 | |
| 06 - Tessuti epiteliali | 28-49 | 22 | 5 | **fatto**, 158 note in due file |
| 07 - Concetti base di microscopia | 49-60 | 12 | 4 | **fatto**, 89 note |
| 08 - Epitelio di rivestimento | 60-85 | 26 | 6 | **fatto**, 183 note in tre file |
| 09 - Epiteli ghiandolari | 85-86 | 2 | 7 | **fatto**, 22 note |
| 10 - Ghiandole esocrine | 86-93 | 8 | 7 | **fatto**, 73 note |
| 11 - Ghiandole endocrine | 93-111 | 19 | 8 | |
| 12 - Tessuti connettivi | 111-137 | 27 | 9 | |
| 13 - Tessuti connettivi di sostegno | 137-149 | 13 | 10 | |
| 14 - Tessuto osseo | 149-177 | 29 | 14 | |
| 15 - Il sangue | 177-198 | 22 | 13 | |
| 16 - Sistema linfatico | 198-205 | 8 | 11 | |
| 17 - Tessuto muscolare | 205-227 | 23 | 12 | |
| 18 - Il tessuto nervoso | 227-256 | 30 | 15 | |

Il criterio dell'ordine: **i capitoli corti e a basso rischio prima**, per rodare
le convenzioni della teoria dove un errore costa poco rifarlo; **i quattro
capitoli più densi in fondo** (12 connettivi, 15 sangue, 14 osseo, 18 nervoso);
le staminali (04 e 05) per ultime perché sono in buona parte un excursus
clinico, non istologia di base, e quindi le prime sacrificabili se il tempo
stringe. Il 09 e il 10 sono stati fatti insieme, perché il 09 è di due pagine e
da solo non è una sessione di lavoro; **un mazzo suo però ce l'ha**, e il perché
sta più sotto.

Il `08 - Epitelio di rivestimento` **copre le pagine 60-84**, non 60-85: pagina
85 apre già `EPITELI GHIANDOLARI`, che è il mazzo 09. Attenzione anche all'altro
lato: la sezione `024` dichiara le pagine 49-60, ma pagina 60 è interamente
dell'08 e il 07 si chiude a 59. Il capitolo copre le sezioni da `025` a `036` e
due lezioni, quella del 18-03-2025 e quella del 20-03-2025.

Venticinque pagine e 59 figure sono troppe per un file solo, quindi è stato
**diviso in tre**. Il taglio principale è a **pagina 76**, dove cambia la lezione
e cambiano gli sbobinatori, ed è anche un confine di contenuto: fino a 75 si
percorrono i tipi di epitelio, da 76 si passa alle altre popolazioni cellulari
dell'epidermide.

| File | Pagine | Contenuto |
|---|---|---|
| `08a-epitelio-di-rivestimento.jsonl` | 60-75 | pavimentoso semplice, endotelio, capillari, periciti, alveoli, cubico e cilindrico semplice, epitelio intestinale, pseudostratificato, cubico e cilindrico pluristratificato, urotelio, pavimentoso pluristratificato, epidermide |
| `08b-cellule-epidermide-e-sommario.jsonl` | 76-82 | melanociti e donazione del pigmento, meccanocettori, cellule di Merkel e di Langerhans, sommario con i criteri di riconoscimento |
| `08c-quiz-tessuto-epiteliale.jsonl` | 82-84 | le otto domande del quiz finale |

**Il quiz sta nel mazzo del capitolo, non in un mazzo `Quiz` a parte.** Il mazzo
`Istologia::Laboratorio::Quiz` esiste perché lì i quiz sono quattro, novantatré
carte in tutto, prodotti dal generatore e ciascuno a cavallo di più capitoli:
raccoglierli conveniva. Qui il quiz è **uno solo**, dodici carte, scritto a mano
e intitolato dalla sbobina stessa "Quiz finale - tessuto epiteliale": un mazzo
suo aggiungerebbe un livello di navigazione senza dare niente in cambio. Le tre
domande sulle giunzioni appartengono in realtà al capitolo 06, ma portano lo
stesso `argomento::epiteli`, quindi la selezione trasversale le pesca comunque.
Come per `06a`/`06b`, tutti e tre i file usano lo stesso nome di mazzo
`Istologia::Teoria::08 - Epitelio di rivestimento`.

**Il quiz non è leggibile da `scripts/quiz.py`.** Non usa le caselle spuntate
delle quattro convenzioni del Laboratorio: è prosa, con le etichette "Domanda" e
"Risposta" e note `[N.d.S.]` che spiegano perché le altre opzioni erano
sbagliate. È stato scritto a mano, e le sette immagini delle pagine 82-84 sono
screenshot delle slide del quiz **senza le risposte**, quindi stanno tutte sul
fronte.

Delle 59 figure ne sono state usate **48**. Le undici scartate sono il caso
delle immagini ritagliate da un clip path descritto al punto 6: dieci screenshot
di browser alle pagine 70-75 e la `teoria_p065_468`, che contiene due disegni
impilati di cui la pagina mostra solo il primo. Non si perde contenuto, perché
erano tutte slide con le risposte stampate sopra, cioè materiale da retro che il
testo copre già; si perde solo l'illustrazione dell'urotelio e degli strati
dell'epidermide.

Il `03 - Tessuti e rinnovamento` è stato messo terzo perché è la **panoramica
dei quattro tessuti fondamentali** e delle popolazioni cellulari perenni,
stabili e labili: fa da indice mentale a tutto il resto del corso, e cinque
pagine sono poche. **È fatto**, e con lui il `07 - Concetti base di
microscopia`, il `06 - Tessuti epiteliali`, l'`08 - Epitelio di rivestimento`,
il `09 - Epiteli ghiandolari` e il `10 - Ghiandole esocrine`: il prossimo in
ordine è l'`11 - Ghiandole endocrine`, pagine 93-111.

Il `07` è l'unico capitolo che **non è istologia**: è ottica e strumentazione,
dalla struttura dell'occhio ai fluorofori. Sta nella sezione 024, occupa le
pagine 49-59 (pagina 60 apre l'`EPITELIO DI RIVESTIMENTO`, mazzo 08) e ha venti
figure, **tutte usate**. Sono quasi tutte schemi e tabelle con le didascalie
stampate sopra, quindi stanno sul retro; l'unica sul fronte è la coppia di
dischi di Airy al limite di Rayleigh, che non ha etichette.

Il `06 - Tessuti epiteliali` **finisce a pagina 48**, non a 49: la tabella qui
sopra dice 28-49 perché la sezione 023 sconfina di una riga, ma pagina 49 apre
già `CONCETTI BASE DI MICROSCOPIA`. Copre tre sezioni (021, 022, 023) e due
lezioni, quella del 06-03-2025 e quella dell'11-03-2025, che riprende da capo
con un cappello di ripasso a pagina 38. È stato **diviso in due file** su quel
confine, che è anche un confine di contenuto:

| File | Pagine | Contenuto |
|---|---|---|
| `06a-epiteli-di-rivestimento.jsonl` | 28-37 | generalità, classificazione, pseudostratificato, urotelio, polarità, dominio apicale (microvilli, stereociglia, ciglia) |
| `06b-giunzioni-e-dominio-basale.jsonl` | 38-48 | complesso giunzionale, le tre giunzioni, CAM, lamina basale, emidesmosomi, adesioni focali, pieghe basali, membrane mucose e sierose |

Come nel Laboratorio (`09a` e `09b`), i due file **condividono lo stesso mazzo**
`Istologia::Teoria::06 - Tessuti epiteliali`: dividere è una comodità di
scrittura, non una scelta di studio.

Le quarantuno figure delle pagine 28-48 sono **tutte usate, tutte sul retro**.
Il capitolo non offre niente da mettere sul fronte: le micrografie senza
etichette (microvilli e stereociglia al microscopio elettronico) sono
indistinguibili l'una dall'altra fuori dal contesto, e tutto il resto sono schemi
molecolari e tabelle con le risposte stampate sopra. Una sola carta viene da
**pagina 48** pur stando in `06a`: la domanda sul movimento delle ciglia, che la
sbobina stessa dichiara posta nella lezione precedente.

#### I capitoli 09 e 10, e dove finisce davvero l'esocrino

**Il `10 - Ghiandole esocrine` finisce a pagina 93, non a 97.** La riga di
questa tabella diceva 86-97 ed era sbagliata. La sezione `042` si chiama
"Ghiandole endocrine", va da pagina 93 a 97 ed è attribuita dal segmentatore al
capitolo `GHIANDOLE ESOCRINE`, ma il suo contenuto è **interamente endocrino**:
le principali ghiandole endocrine, gli ormoni per composizione chimica, i
recettori, il feedback, e la classificazione in ghiandole a cordoni, a follicolo,
a isolotti, interstiziali e a secrezione mista.

Il confine è stato deciso guardando le pagine 93 e 94 renderizzate. A **pagina
93**, sotto il paragrafo sulle cellule mioepiteliali, c'è un titolo `Ghiandole
endocrine` **della stessa dimensione** dei titoli di capitolo (`EPITELI
GHIANDOLARI`, `GHIANDOLE ESOCRINE`), non delle intestazioni di paragrafo che lo
circondano. **Lì comincia il mazzo 11**, e quello che segue non va preso
scrivendo il 10. Le pagine 94-97 lo confermano: parlano solo di endocrino.

È il caso di pagina 205 rovesciato. Lì il segmentatore non vedeva il titolo
giusto e ne riconosceva uno più avanti; qui **il titolo che riconosce, a pagina
97, è quello sbagliato**: a pagina 97 non comincia il capitolo, comincia una
lezione nuova (27-03-2025, sbobinatori diversi) che il capitolo già aperto a 93
prosegue. La ricognizione delle righe maiuscole qui sotto non poteva trovarlo,
perché `Ghiandole endocrine` a pagina 93 **non è in maiuscolo**.

**Il 09 ha un mazzo suo**, contro quanto diceva la prima stesura di questo piano
("da solo non è un mazzo"). La frase valeva per l'ordine di lavorazione: due
pagine non sono una sessione di lavoro, e infatti 09 e 10 sono stati scritti
insieme. Ma la tabella dei mazzi è dichiarata definitiva e il 09 ci figura, e
soprattutto **il suo contenuto non è esocrino**: è la premessa comune a esocrine
ed endocrine (che cos'è un epitelio ghiandolare, secrezione costitutiva e
regolata, le differenze fra i due tipi, lo sviluppo di entrambi). Infilarlo nel
`10 - Ghiandole esocrine` metterebbe la distinzione esocrino/endocrino dentro il
mazzo dell'esocrino, dove chi ripassa l'endocrino non la cercherebbe.

È il ragionamento opposto a quello fatto per il quiz del capitolo 08, e per lo
stesso motivo: lì un mazzo a parte avrebbe aggiunto navigazione senza dare
niente in cambio, perché il quiz apparteneva al capitolo che lo precede; qui il
09 non appartiene a nessuno dei due mazzi che lo circondano. Le sue sei carte
endocrine portano comunque `argomento::endocrino`, quindi la selezione
trasversale le pesca insieme al mazzo 11 quando sarà scritto.

Le **25 figure** delle pagine 85-93 sono state **usate tutte**, 2 nel mazzo 09 e
23 nel mazzo 10. Erano state passate al controllo del clip path (punto 6) e
corrispondono tutte a quello che si vede sulla pagina. Sette stanno sul fronte:
le microfotografie senza etichette (tricromica e PAS sull'intestino tenue, Alcian
blu sul colon, le quattro forme di adenomero, le tubulari glomerulari in
tricromica, la sebacea olocrina e il dotto mammario con le frecce sulle
protrusioni apicali). Tutto il resto sono schemi, tabelle e figure di libro con
la **didascalia stampata sopra**, che è già la risposta, e sta quindi sul retro.

#### Due cose che aspettano il mazzo 11

Trovate lavorando ai confini del 10, non ancora usate perché il capitolo non è
scritto. Vanno lette **prima** di cominciarlo.

**Le pagine 93-99 sono sbobinate due volte.** La sezione `042` (pagine 93-96,
lezione del 25-03-2025, sbobinatori Maccarini e Bergamin) e le sezioni
`043`-`047` (pagine 97-99, lezione del 27-03-2025, sbobinatori Hasanaj e
Cerqueti) coprono **gli stessi cinque argomenti**: che cos'è una ghiandola
endocrina, il confronto fra sistema endocrino e sistema nervoso, la
classificazione degli ormoni per natura chimica, il meccanismo di feedback e la
classificazione strutturale delle ghiandole endocrine. Non sono due argomenti
diversi, sono due passate sulla stessa lezione, con dettagli in più ora da una
parte ora dall'altra: le ghiandole a cordoni, per esempio, sono molto più ricche
nella seconda.

**Vanno fuse, non scritte due volte.** Il validatore blocca solo le domande
identiche nello stesso mazzo: due parafrasi della stessa carta gli passano
davanti e finiscono nei ripassi di Pietro come doppioni. Per ogni fatto va
tenuta la versione più completa, con il `source` che punta alla pagina da cui
viene.

**L'`11 - Ghiandole endocrine` finisce a pagina 110, non a 111.** La riga della
tabella dice 93-111 secondo la convenzione della colonna, che indica la pagina in
cui comincia il capitolo successivo, ma **pagina 111 è interamente del mazzo
12**: si apre in cima con l'intestazione di una lezione nuova (01-04-2025,
sbobinatori Zamboni e Webber) e subito sotto con il titolo `TESSUTI CONNETTIVI`.
La figura di pagina 111 appartiene quindi al 12. È lo stesso caso dell'`08`, che
la tabella dà per 60-85 e che si ferma a 84.

Il capitolo resta comunque grande: **18 pagine, circa 6.800 parole, 27 figure**
fra pagina 95 e pagina 110 (le tre di pagina 93 sono del mazzo 10; le pagine 94,
96 e 110 non ne hanno). Non ci sta in un file solo. I tagli naturali sono
`042`-`047` per le generalità, `048`-`050` per ipofisi, paratiroidi e tiroide, e
`051` per il surrene, e lasciano tre blocchi di dimensione simile.

Attenzione infine al **controllo del clip path** del punto 6: è stato fatto fino
a pagina 97 e lì tutte le figure corrispondevano, ma **da 98 a 110 non è mai
stato eseguito**.

#### I tre titoli che il segmentatore non vede

`segment.py` non riconosce alcuni titoli di capitolo, e attribuisce le loro
pagine al capitolo precedente. La ricerca è stata fatta sulle 256 pagine
cercando le righe interamente maiuscole che non corrispondono a una sezione
nota, e ha restituito **tutti** i casi:

| Pagina | Titolo | Effetto |
|---|---|---|
| 12 | `TESSUTI E RINNOVAMENTO` | apre il mazzo 03 |
| 16 | `CELLULE STAMINALI E POTENZIALE DIFFERENZIATIVO` | apre il mazzo 04 |
| 205 | `TESSUTO MUSCOLARE` | il muscolare inizia qui, non a 208 |

Il caso di pagina 205 è il più insidioso, perché il segmentatore *un* titolo lo
riconosce: `TESSUTO MUSCOLARE STRIATO SCHELETRICO` a pagina 208. Le pagine
205-207, che introducono i tre tipi di tessuto muscolare, finiscono così dentro
il Sistema linfatico. Chi scriverà il mazzo 16 non deve prenderle.

**"Tutti i casi" vale solo per i titoli in maiuscolo.** La ricognizione cerca
righe interamente maiuscole, quindi non poteva trovare il `Ghiandole endocrine`
di pagina 93, che è scritto in tondo pur avendo il corpo di un titolo di
capitolo (vedi qui sopra). Prima di scrivere un capitolo, **guarda comunque la
pagina renderizzata** al confine dichiarato dalla tabella: il conteggio delle
maiuscole non è una garanzia.

Per rifare la ricognizione da capo:

```sh
./venv/bin/python -c "
import json
secs=[json.loads(l) for l in open('build/teoria/sections.jsonl')]
titles={s['title'].strip().upper() for s in secs}
for l in open('build/teoria/pages.jsonl'):
    p=json.loads(l)
    for line in p['text'].splitlines():
        t=line.strip()
        if not 6 <= len(t) <= 70: continue
        alpha=[c for c in t if c.isalpha()]
        if alpha and all(c.isupper() for c in alpha) and t.upper() not in titles:
            print(p['page'], t)"
```

**I numeri di mazzo seguono le pagine, non l'ordine di lavorazione.** In Anki i
mazzi restano quindi nell'ordine del corso qualunque sia la sequenza in cui
vengono scritti, e l'ordine qui sopra si può cambiare senza toccare niente.

Attenzione: la teoria ripete argomenti già coperti dal Laboratorio, ma da un
punto di vista diverso (meccanismi invece che riconoscimento al vetrino). Non è
duplicazione da evitare, sono due tagli complementari. Il validatore blocca solo
i duplicati esatti dentro lo stesso mazzo.

### Ritmo di consegna

Un capitolo per volta: scrivere le carte, `build_apkg` (che valida), commit.
Ogni capitolo committato è un incremento che Pietro può già importare.

---

## 5. Segnalazioni `da-verificare` già trovate

Trentacinque carte taggate, più due figure scartate senza produrre carta. Vale la pena
rileggerle prima di scriverne di nuove, per calibrare quanto è alta l'asticella.

| Carta | Cosa non torna |
|---|---|
| `lab-epiteli-031` | la sbobina scrive cavità "portorie", termine inesistente, con ogni probabilità per cavità sierose |
| `lab-esocrino-033` | porta le ghiandole di Cowper come esempio di ghiandola intraepiteliale; le bulbouretrali non lo sono, l'esempio atteso sono le ghiandole di Littré |
| `lab-endocrino-014` | attribuisce il testosterone ai tubuli seminiferi invece che alle cellule di Leydig, gli estrogeni al corpo luteo invece del progesterone, e classifica il corpo luteo fra le interstiziali dopo averlo messo fra quelle a cordoni solidi |
| `lab-connettivi-037` | descrive la giunzione miotendinea come formata da cartilagine ialina; è classicamente un'interdigitazione fra membrana delle fibre muscolari e collagene, la fibrocartilagine sta semmai all'entesi |
| `lab-linfoide-015` | identifica le plasmacellule con i linfociti B maturi del centro germinativo splenico; le plasmacellule sono la forma terminale differenziata e stanno soprattutto nella polpa rossa |
| `lab-osso-046` | il vetrino 10 mette dei condroblasti lungo le pareti dei canali di Havers; lì ci si aspettano cellule osteoprogenitrici e osteoblasti |
| `lab-quiz-connettivi-specializzati-001` | la casella spuntata è "Fibroblasto" per la cellula che sintetizza la matrice cartilaginea; è il condrocita |
| `lab-quiz-connettivi-specializzati-026` | conta la riserva energetica fra le funzioni **non** associate ai connettivi specializzati, contraddicendo le domande 11 e 13 dello stesso quiz sul tessuto adiposo |
| `lab-linfoide-022` | inquadra il timo come "tessuto connettivo specializzato con funzione trofica"; è un organo, e la sua funzione è la maturazione e selezione dei linfociti T |
| `lab-linfoide-039` | dà l'epitelio di rivestimento della tonsilla palatina per pavimentoso stratificato **cheratinizzato**; è classicamente non cheratinizzato, come il resto dell'orofaringe. La sbobina cita come fonte un sito divulgativo, non il libro |
| `lab-nervoso-069` | il vetrino 7 dichiara la tecnica di Golgi, ma descrive un citoplasma ricco di corpi di Nissl "visibili come zone basofile"; il Golgi impregna di nero pochi neuroni interi su fondo chiaro e non dà basofilia, e nelle figure si vedono tutti i neuroni con le loro cellule satelliti |
| `lab-nervoso-015` | dice che la sostanza tigroide si vede **solo** con colorazioni speciali e non con ematossilina-eosina; i corpi di Nissl sono fortemente basofili e in un preparato EE si vedono come zolle basofile nel citoplasma |
| `lab-muscolare-016` | nega che il miocardio sia un sincizio funzionale e attribuisce l'espressione al muscolo scheletrico; è il contrario, il cuore è il sincizio funzionale classico grazie alle gap junction dei dischi intercalari, mentre lo scheletrico è un sincizio strutturale |
| `teoria-tecnica-030` | la sbobina dà due spessori diversi per le sezioni istologiche: 5-20 micron per il microscopio ottico (p. 2) e 1-10 µm per il taglio al microtomo (p. 4), senza spiegare la differenza |
| `teoria-colorazioni-021` | descrive come "strati di muscolatura liscia" la banda pallida sotto la mucosa in un vetrino di trachea fetale; per aspetto e per anatomia è cartilagine ialina, e la muscolatura liscia della trachea sta nella parte membranacea posteriore |
| `teoria-colorazioni-024` | classifica l'Azocarminio come colorante **basico** e nella stessa frase gli attribuisce la colorazione dei granuli **acidofili** dell'ipofisi; l'azocarminio è classicamente descritto come colorante acido |
| `teoria-epiteli-001` | il pannello a della tavola dei tre epiteli è dato per **pancreas**, ma mostra una cavità piena di materiale eosinofilo omogeneo circondata da un solo strato di cellule cubiche, cioè un follicolo (tiroideo o ovarico); il pancreas esocrino è ad acini sierosi. L'epitelio resta comunque monostratificato cubico |
| `teoria-connettivi-002` | chiama sangue e linfa connettivi "trofici o **propriamente detti**"; i propriamente detti sono classicamente il lasso e il denso, mentre sangue, cartilagine, osso e adiposo stanno fra gli specializzati |
| `teoria-microscopia-033` | definisce l'ingrandimento come il rapporto fra le dimensioni **dell'oggetto e quelle dell'immagine**; è il capovolgimento del rapporto giusto, altrimenti un'immagine ingrandita darebbe un valore minore di 1 |
| `teoria-microscopia-036` | dà 100 nm come limite di risoluzione del microscopio ottico a immersione; con luce visibile e NA 1,4 la formula 0,61·λ/NA dà ancora circa 200 nm. Il numero serve però al calcolo dell'ingrandimento utile di 1000x fatto subito dopo |
| `teoria-microscopia-055` | dà gli obiettivi apocromatici a 23 mm di planarità di campo, mentre la tabella della stessa pagina dice 25; e il testo li definisce i migliori, il che con 23 mm li metterebbe sotto i semi-apocromatici |
| `teoria-epiteli-019` | dà tutto il tratto gastrointestinale per rivestito da epiteli pluristratificati "per resistenza meccanica"; pluristratificati sono solo le estremità, esofago e canale anale, come conferma la tabella della pagina dopo |
| `teoria-epiteli-053` | dà le stereociglia "lunghe 100-120 µm", mentre la tabella riassuntiva della pagina successiva scrive "fino a 120 µm" |
| `teoria-epiteli-063` | scrive l'assetto delle ciglia mobili come "9 + 1", mentre la tabella della stessa dispensa dice "9 + 2"; la descrizione a parole della stessa carta, nove doppiette periferiche più una coppia centrale, è però corretta |
| `teoria-epiteli-089` | elenca il complesso giunzionale come zonula occludente, zonula aderente e "una zonula con le giunzioni comunicanti"; il terzo elemento classico è la macula aderente (desmosoma), e le giunzioni comunicanti non formano una zonula |
| `teoria-epiteli-100` | chiama "Freeze Capture" la tecnica di criofrattura; il nome corretto è freeze-fracture |
| `teoria-epiteli-183` | mette l'aumento delle fenestrazioni dei capillari intestinali durante l'assorbimento dentro il paragrafo sui capillari **sinusoidali**, dopo aver appena elencato l'intestino fra le sedi dei **fenestrati** e i sinusoidali fra i soli organi emopoietici |
| `teoria-epiteli-203` | fa nascere i microvilli dell'enterocita dal **corpo basale**; il corpo basale ancora un ciglio, mentre i microvilli originano dalla trama terminale, che è probabilmente la struttura descritta |
| `teoria-epiteli-265` | mette il **retto** fra le sedi del pavimentoso pluristratificato non cheratinizzato; il retto è classicamente cilindrico semplice, ed è il canale anale a essere pluristratificato. Stesso equivoco di `teoria-epiteli-019` |
| `teoria-epiteli-282` | la stessa dispensa dà allo strato spinoso "cinque o sei strati" a pagina 73 e "4-8 strati" a pagina 74, senza spiegare la differenza |
| `teoria-epiteli-338` | nella risposta alla domanda 5 del quiz convivono due numerazioni: "2, 3, 6, 7" sono le opzioni corrette, mentre "1, 6 e 7" della nota sono i tipi di epitelio privi di specializzazioni. Nessuna delle due si riconcilia con i numeri stampati sulla figura |
| `teoria-epiteli-340` | il quiz dà "zonulina" come proteina di placca della giunzione occludente; la proteina classica è la ZO-1 (zonula occludens-1), mentre la zonulina è un'altra molecola |
| `teoria-ghiandole-028` | lo schema di pagina 85 porta stampato "ADENOMERO = Parenchima (cellule) + Stroma (matrice extracellulare)", mentre il testo di pagina 87 dice che il parenchima è composto da adenomero e dotto escretore e che lo stroma è connettivale. I due rapporti sono l'uno il rovescio dell'altro |
| `teoria-ghiandole-043` | dà la ghiandola mammaria per composta da più ghiandole, ciascuna responsabile di una diversa sostanza del secreto (lipidi, glucidi, proteine); classicamente sono 15-20 ghiandole tubulo-alveolari composte, ciascuna con il proprio dotto galattoforo, e sono le stesse cellule alveolari a produrre sia i lipidi, per secrezione apocrina, sia le proteine e il lattosio, per secrezione merocrina |
| `teoria-ghiandole-070` | dice che nelle ghiandole miste sono "le porzioni acinose" a rappresentare la parte più esterna dell'adenomero, ma sia le sierose sia le mucose sono acinose; la didascalia della figura 13.16, nelle stesse pagine, dice che sono le cellule sierose a circondare le mucose formando le semilune di Giannuzzi |
| (nessuna carta) | a pagina 4 una microfotografia è didascalizzata "colon" ma mostra tessuto adiposo e vasi: non ne è stata fatta una carta di riconoscimento |
| (nessuna carta) | `lab_p070_4344.jpg` è un ritaglio con un solo leucocita fra gli eritrociti, non identificabile con certezza |

Casi risolti senza tag, perché il refuso è evidente e non c'è dubbio di contenuto:
la sbobina scrive adiposo "multicolore" per multiloculare (`lab-connettivi-030`).

---

## 6. Trappole note

**Le didascalie estratte sono inaffidabili.** `caption_for_image` prende il blocco
di testo più vicino sotto la figura, che spesso è prosa qualsiasi. Su 222 immagini
del Laboratorio solo 94 hanno una didascalia, e non tutte sono corrette. Servono
come indizio, non come verità: guarda l'immagine.

**Le risposte dei quiz non sono nel testo.** Sono marcate graficamente, in
quattro modi diversi a seconda della lezione: casella spuntata (endocrino),
casella vuota con risposta in grassetto (connettivi), punto elenco con risposta
in grassetto (nervoso), e casella spuntata ma **domande non numerate** (quiz
finale dei connettivi specializzati). `scripts/quiz.py` le gestisce tutte e
quattro e solleva `AmbiguousCheckbox` invece di indovinare quando il segnale non
è chiaro.

Se una nuova sezione di quiz esce con **zero domande** il problema è il
riconoscimento della domanda, non delle caselle; se esce con zero **risposte** è
il contrario. In entrambi i casi renderizza la pagina e guardala prima di
toccare le soglie:

```sh
./venv/bin/python -c "import pymupdf; \
  pymupdf.open('PDF')[70].get_pixmap(dpi=140).save('/tmp/p71.png')"
```

**I file di quiz pubblicati non sono più solo il prodotto del generatore.**
Nei quiz misti l'`argomento::` è assegnato a mano domanda per domanda, e le
risposte che non tornano portano una nota in fondo al `back` e il tag
`da-verificare`. Niente di questo si ricava dal PDF, quindi `quiz_to_cards.py`
**si rifiuta di scrivere su un file che esiste già**.

Dopo qualunque modifica a `quiz.py`, il controllo di non-regressione va fatto
generando su un percorso temporaneo e confrontando `front` e `back`: le uniche
differenze attese sono le carte taggate `da-verificare`.

```sh
S=/tmp/checkquiz && mkdir -p $S
./venv/bin/python -m scripts.quiz_to_cards --pdf "$DL/Istologia Laboratorio combinato.pdf" \
    --from-page 71 --to-page 75 --deck "Istologia::Laboratorio::Quiz" \
    --prefix lab-quiz-connettivi-specializzati --tags "fonte::lab" \
    --source "Laboratorio p. 71-75" --out $S/06e.jsonl

./venv/bin/python -c "
import json
core = lambda p: [(c['id'], c['front'], c['back']) for c in map(json.loads, open(p))]
a, b = core('$S/06e.jsonl'), core('cards/laboratorio/06e-quiz-connettivi-specializzati.jsonl')
print([x[0] for x, y in zip(a, b) if x != y])"
```

Atteso oggi: `['lab-quiz-connettivi-specializzati-001',
'lab-quiz-connettivi-specializzati-026']`, le due carte annotate a mano.
Qualsiasi altro id nell'elenco è una regressione su carte che Pietro sta già
ripassando.

**Il validatore considera l'immagine parte della domanda.** Molte carte di
riconoscimento hanno lo stesso fronte ("Che epitelio è questo?") e sono distinte
solo dalla figura. Se compare un errore di domanda duplicata su carte che hanno
davvero immagini diverse, il bug è altrove.

**La cwd della shell si resetta fra un comando e l'altro.** Usa percorsi assoluti
o prefissa `cd /Users/pietrodibello/tools/anki-istologia &&`.

**Una figura può stare sulla pagina dopo il testo che illustra.** La
microfotografia dell'osteone è estratta come `lab_p059_4057.jpg` ma illustra il
testo di pagina 58, ed è finita sulla carta giusta solo perché è stata guardata.
Il campo `source` della carta segue il **testo**, non la pagina della figura.

**`segment.py` non vede tutti i titoli di capitolo, e nessuno se ne accorge.**
Le pagine di un capitolo non riconosciuto vengono attribuite in silenzio al
capitolo precedente, che risulta così molto più lungo di quello che è: le
"Colorazioni istochimiche" sembravano coprire 18 pagine e ne coprono 6. Il
sintomo è una sezione che dichiara molte pagine e cambia argomento a metà.
Nella Teoria i tre casi sono stati trovati tutti e sono elencati al punto 4;
sul Laboratorio la ricognizione non è mai stata fatta, ma lì i capitoli sono
chiusi e verificati pagina per pagina.

**Le sezioni si sovrappongono ai bordi.** `images_for_section` assegna per
intervallo di pagine, quindi una figura a cavallo di due sezioni compare in
entrambe. Va scelta a giudizio, non usata due volte.

**Il file estratto non è sempre quello che si vede sulla pagina.**
`extract.py` salva l'immagine **grezza** incorporata nel PDF (`extract_image`),
ignorando il *clip path* con cui la pagina la ritaglia. Se lo sbobinatore ha
incollato uno screenshot intero e poi lo ha ritagliato dentro il documento, sul
file finiscono la finestra del browser, le schede e la barra delle applicazioni,
che sulla pagina non si vedono. Nelle pagine 70-75 della Teoria sono dieci
figure su dieci, e altre tre (`teoria_p060_430`, `teoria_p060_431`,
`teoria_p069_503`) sono slide intere di cui la pagina mostra solo un pezzo.

Il controllo dei bordi non basta, perché il clip può stare tutto dentro la
pagina. Il modo affidabile è **confrontare il file estratto con la regione
renderizzata** e guardare i casi che non corrispondono:

```sh
./venv/bin/python -c "
import pymupdf, io, statistics
from PIL import Image
d = pymupdf.open('\$DL/Istologia 5th gen-combinato.pdf')
thumb = lambda im: list(im.convert('L').resize((48, 48)).getdata())
def corr(a, b):
    ma, mb = statistics.mean(a), statistics.mean(b)
    da, db = [x - ma for x in a], [y - mb for y in b]
    den = (sum(x * x for x in da) * sum(y * y for y in db)) ** 0.5
    return sum(x * y for x, y in zip(da, db)) / den if den else 0.0
for pno in range(60, 85):
    page = d[pno - 1]
    for info in page.get_images(full=True):
        xref = info[0]
        src = thumb(Image.open(io.BytesIO(d.extract_image(xref)['image'])))
        best = -2
        for r in page.get_image_rects(xref):
            clip = r & page.rect
            if clip.is_empty or clip.width < 5 or clip.height < 5:
                continue
            pix = page.get_pixmap(clip=clip, dpi=72)
            shown = thumb(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))
            best = max(best, corr(src, shown))
        if best < 0.80:
            print(f'p{pno} xref{xref} corr={best:.2f}')"
```

Una figura che non corrisponde va **guardata comunque**: se il file è una slide
intera e leggibile si può usare sul **retro** (è pur sempre la fonte), se è una
finestra di browser va scartata. Recuperare il ritaglio richiederebbe di leggere
il clip path dal content stream: né `get_image_rects` né `get_image_info` lo
riportano, e non vale la pena per delle illustrazioni da retro. Se un giorno
servisse, è un intervento su `extract.py` che cambia l'output di **entrambe** le
fonti, quindi va fatto prima di scrivere altre carte, non dopo.
