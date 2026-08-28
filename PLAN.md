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

./venv/bin/python -m pytest tests/ -q          # atteso: 163 passed
```

L'estrazione della teoria richiede qualche minuto: 256 pagine e 486 immagini.

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

Atteso oggi: **1872 carte, 18 mazzi, 453 immagini** per la Teoria e **960 carte,
12 mazzi, 212 immagini** per il Laboratorio.

E per rigenerare l'elenco delle segnalazioni da portare al libro (vedi punto 5):

```sh
./venv/bin/python -m scripts.da_verificare --cards cards --out DA_VERIFICARE.md
```

Atteso oggi: **112 carte**. Questo comando legge solo `cards/`, non serve
`build/`.

**Due pacchetti, uno per fonte**, non uno solo: `--media` è una singola
directory e le immagini stanno in due alberi separati (`build/lab/images` e
`build/teoria/images`). In Anki non cambia nulla, i mazzi restano sotto lo
stesso genitore `Istologia::` e i tag `argomento::` continuano a pescare da
entrambe le fonti. Così la teoria si consegna un capitolo per volta senza
rispedire ogni volta le 944 note del laboratorio.

---

## 2. Stato al 2026-08-12

**944 note** di Laboratorio + **1872 di Teoria**, 663 immagini, 163 test verdi.

**Il progetto è finito.** Il Laboratorio copre tutte e 106 le sue pagine, la
Teoria tutti e **diciotto** i capitoli e tutte e 256 le pagine. Non c'è più
nessun buco, né in fondo né in mezzo.

**Anche il follow-up delle dieci figure recuperate è chiuso**: sono state
guardate tutte e dieci e collocate, con il bilancio che il punto 6 riporta. Resta
aperto **solo** il clip path di `extract.py`, che non è lavoro sulle carte e che
il piano raccomanda di **non fare**. Vedi la chiusura del punto 4.

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
| `05a-tessuti-connettivi.jsonl` | 41 | sezioni 013-015, vetrini 1-7, pagine 43-49 |
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
| `vetrini-01-colorazioni.jsonl` | 24 | mazzo `Vetrini`, 8 vetrini delle pagine 3-5 |
| `vetrini-02-epiteli.jsonl` | 42 | mazzo `Vetrini`, 8 vetrini + 4 schermate di quiz, pagine 8-12 |
| `vetrini-03a-esocrino.jsonl` | 29 | mazzo `Vetrini`, classificazione + vetrini 1-7, pagine 15-21 |
| `vetrini-03b-esocrino.jsonl` | 30 | mazzo `Vetrini`, vetrini 8-13 + 3 schermate di quiz, pagine 21-27 |
| `vetrini-04a-endocrino.jsonl` | 30 | mazzo `Vetrini`, vetrini 1-3, pagine 30-32 |
| `vetrini-04b-endocrino.jsonl` | 47 | mazzo `Vetrini`, vetrini 4-8, pagine 33-39 |
| `vetrini-05-connettivi.jsonl` | 44 | mazzo `Vetrini`, vetrini 1-5, 7-10 + 3 figure di classificazione, pagine 44-50 |
| `vetrini-06-specializzati.jsonl` | 25 | mazzo `Vetrini`, vetrini 3-8, 10 e 11, pagine 63-70 |
| `vetrini-08-nervoso.jsonl` | 16 | mazzo `Vetrini`, vetrini 4-7 e 9, pagine 86-91 |

**La sezione 019 non è solo il tessuto osseo**, nonostante il titolo. Copre
osso, sangue, sistema linfoide, undici vetrini e il quiz finale, tutto dentro
il capitolo `06 - Tessuti connettivi specializzati` aperto dalla cartilagine.
I quattro file `06b`-`06e` la chiudono per intero, e
`vetrini-06-specializzati.jsonl` vi si affianca con le domande di dettaglio del
mazzo `Vetrini`: è quindi l'unica sezione del progetto che alimenta **cinque**
file e **quattro** argomenti diversi.

**Anche la sezione 022 mescola gli argomenti**, come già il suo quiz: i primi
tre dei nove vetrini sono di tessuto **muscolare** (lingua, cuore, intestino).
Le loro carte stanno in `07b`, nel mazzo `07 - Tessuto muscolare`, perché è lì
che Pietro ripassa il muscolare; il campo `source` rimanda comunque alle pagine
82-85. Il precedente di `06d` (deck del capitolo dove sta la pagina) non si
applicava: lì tutti gli argomenti appartenevano davvero a quel capitolo.
Spostare una carta di mazzo è comunque sicuro, il guid dipende solo dall'id.

Lo stesso taglio vale nel mazzo `Vetrini`: `vetrini-08-nervoso.jsonl` prende
solo i vetrini **nervosi** (4-7 e 9, pagine 86-91), e i tre vetrini muscolari
delle pagine 82-85 restano all'iterazione 9, che ha un file suo
(`vetrini-07-10-coda.jsonl`) e prosegue il contatore `lab-muscolare`.

Il nome `08b2` esiste perché `08c` era già occupato dal quiz, generato prima
che il capitolo fosse scritto: `08b` è la teoria del periferico, `08b2` i suoi
vetrini, e l'ordine alfabetico resta quello delle pagine.

### Teoria (256 pagine, 111 sezioni)

| File | Note | Copre |
|---|---|---|
| `01-preparazione-preparato.jsonl` | 64 | sezioni 001-006, pagine 1-7 |
| `02-colorazioni-istochimiche.jsonl` | 60 | sezioni 007-009 + inizio 010, pagine 7-12 |
| `03-tessuti-e-rinnovamento.jsonl` | 58 | sezione 010, seconda metà, pagine 12-15 |
| `04-cellule-staminali-e-potenziale-differenziativo.jsonl` | 37 | sezioni 011-017, pagine 16-24 (prima metà) |
| `05-applicazioni-terapeutiche-delle-cellule-staminali.jsonl` | 21 | sezioni 018-020, pagine 24 (seconda metà)-27 |
| `06a-epiteli-di-rivestimento.jsonl` | 84 | sezione 021, pagine 28-37 |
| `06b-giunzioni-e-dominio-basale.jsonl` | 74 | sezioni 022-023, pagine 38-48 |
| `07-concetti-base-di-microscopia.jsonl` | 89 | sezione 024, pagine 49-59 |
| `08a-epitelio-di-rivestimento.jsonl` | 132 | sezioni 025-033, pagine 60-75 |
| `08b-cellule-epidermide-e-sommario.jsonl` | 39 | sezioni 034-035, pagine 76-82 |
| `08c-quiz-tessuto-epiteliale.jsonl` | 12 | sezione 036, pagine 82-84 |
| `09-epiteli-ghiandolari.jsonl` | 22 | sezioni 037-039, pagine 85-86 |
| `10-ghiandole-esocrine.jsonl` | 73 | sezioni 040-041, pagine 86-93 |
| `11a-endocrino-generalita.jsonl` | 35 | sezioni 042-047, pagine 93-99 |
| `11b-ipofisi-paratiroidi-tiroide.jsonl` | 48 | sezioni 048-050, pagine 99-105 |
| `11c-surrene-e-pancreas-endocrino.jsonl` | 37 | sezione 051, pagine 105-110 |
| `12a-matrice-extracellulare.jsonl` | 44 | sezioni 052-062, pagine 111-116 |
| `12b-fibre-collagene-ed-elastiche.jsonl` | 48 | sezione 062, pagine 116-123 |
| `12c-cellule-del-connettivo.jsonl` | 39 | sezioni 063-064, pagine 123-128 |
| `12d-classificazione-dei-connettivi.jsonl` | 36 | sezioni 065-067, pagine 128-131 e 134-137 |
| `12e-confronti-al-microscopio.jsonl` | 12 | sezioni 065-066, pagine 131-134, **mazzi 10 e 11** |
| `13a-cartilagine-generalita.jsonl` | 51 | sezioni 068-069, pagine 137-144 |
| `13b-tipi-di-cartilagine.jsonl` | 26 | sezione 069, pagine 145-148 |
| `14a-generalita-e-matrice.jsonl` | 31 | sezioni 070-071, pagine 149-152 |
| `14b-osso-lamellare-e-immaturo.jsonl` | 29 | sezione 072, pagine 152-157 |
| `14c-osteone-e-canali.jsonl` | 27 | sezione 073, prima parte, pagine 157-161 |
| `14d-le-cellule-del-tessuto-osseo.jsonl` | 33 | sezione 073, seconda parte, pagine 161-167 |
| `14e-ossificazione.jsonl` | 33 | sezioni 073 (terza parte)-076, pagine 167-173 |
| `14f-rimodellamento-riparazione-midollo.jsonl` | 22 | sezioni 077-079, pagine 173-176 |
| `15a-sangue-e-plasma.jsonl` | 39 | sezione 080, prima parte, pagine 177-180 |
| `15b-eritrociti-e-gruppi-sanguigni.jsonl` | 26 | sezione 080, seconda parte, pagine 180-184 |
| `15c-leucociti.jsonl` | 42 | sezione 081, prima parte, pagine 184-189 |
| `15d-piastrine-ed-emostasi.jsonl` | 30 | sezione 081, seconda parte, pagine 189-193 |
| `15e-emopoiesi-e-midollo-osseo.jsonl` | 36 | sezioni 082-084, pagine 193-198 |
| `16-sistema-linfatico.jsonl` | 77 | sezioni 085-089, pagine 198-205 |
| `17a-generalita-e-fibra-muscolare.jsonl` | 49 | sezioni 090-094, pagine 205-212 |
| `17b-contrazione-e-tipi-di-fibre.jsonl` | 44 | sezioni 095-097, pagine 212-219 |
| `17c-tessuto-muscolare-cardiaco.jsonl` | 24 | sezione 098, pagine 219-222 |
| `17d-tessuto-muscolare-liscio.jsonl` | 25 | sezione 099, pagine 223-226 |
| `18a-generalita-e-sistema-nervoso.jsonl` | 31 | sezioni 100-103, pagine 227-231 |
| `18b-sistema-nervoso-periferico.jsonl` | 20 | sezioni 104-105 (1ª parte), pagine 231-234 |
| `18c-il-neurone.jsonl` | 30 | sezione 105 (2ª parte), pagine 234-239 |
| `18d-sinapsi-e-neurotrasmettitori.jsonl` | 23 | sezione 105 (3ª parte), pagine 239-246 |
| `18e-fibre-nervose-e-neuroglia.jsonl` | 33 | sezioni 106-107, pagine 246-251 |
| `18f-staminali-neurali-e-rigenerazione.jsonl` | 27 | sezioni 108-110, pagine 251-256 |

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

**Le figure di pagina 7 sono poi diventate tre**, non due: `teoria_p007_21` è
una delle dieci recuperate abbassando la soglia di `is_artifact` (punto 6), è la
micrografia di cripte intestinali in Alcian blu, ed è finita anche lei nel
capitolo 02, sul **fronte** di `teoria-colorazioni-033`. Le pagine 1-7 hanno
quindi dieci figure e le pagine 7-12 dodici, tutte usate.

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

Le pagine 12-15 hanno **sei** figure e **sono state usate tutte**. La sesta è
`teoria_p013_46`, una delle dieci recuperate dalla soglia (punto 6): è la
sezione trasversale di nervo del paragrafo "Tessuto nervoso", **senza etichette**,
ed è finita sul **fronte** di `teoria-nervoso-002`, che la descriveva a parole
senza mostrarla. Le altre cinque: due sono
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
| `lab-colorazioni` | `01` 001-038, poi `vetrini-01` 039-062 |
| `lab-epiteli` | `02` 001-034, poi `vetrini-02` 035-076 |
| `lab-esocrino` | `03` 001-035, `03b` 040-087, `vetrini-03a` 088-116, poi `vetrini-03b` 117-146 |
| `lab-endocrino` | `04a` 001-015, `04b` 020-045, `vetrini-04a` 046-075, poi `vetrini-04b` 076-122 |
| `lab-connettivi` | `05a` 001-041, poi `vetrini-05` 042-085 |
| `lab-osso` | `06b` 001-032, `06d` 033-046, poi `vetrini-06` 047-055 |
| `lab-cartilagine` | `06a` 001-025, `06d` 026-043, poi `vetrini-06` 044-049 |
| `lab-sangue` | `06c` 001-014, `06d` 015-018, poi `vetrini-06` 019-022 |
| `lab-muscolare` | `07a` 001-024, poi `07b` 025-044 |
| `lab-nervoso` | `08a` 001-027, `08b` 028-045, `08b2` 046-084, poi `vetrini-08` 085-100 |
| `lab-linfoide` | `06c` 001-012, `06d` 013-021, `06f` 022-036, `10a` 037-047, poi `vetrini-06` 048-053 |
| `lab-embriologia` | `09a` 001-020, poi `09b` 021-057 |
| `teoria-tecnica` | `01` 001-038, poi `02` 039-049 |
| `teoria-colorazioni` | `01` 001-026, `02` 027-075, `10` 076-079, `12a` 080, `12b` 081, `12d` 082-085, `13a` 086-087, `13b` 088, `15a` 089-090, `14a` 091, poi `18a` 092-094 e `18c` 095 |
| `teoria-ghiandole` | `09` 001-016, `10` 017-085, poi `12e` 086-094 |
| `teoria-endocrino` | `09` 001-006, `11a` 007-041, `11b` 042-089, `11c` 090-121, poi `12e` 122-124 |
| `teoria-connettivi` | `03` 001-004, `12a` 005-043, `12b` 044-090, `12c` 091-129, `12d` 130-160, poi `13a` 161 |
| `teoria-embriologia` | `03` 001-022, `12a` 023-026, poi `13a` 027, `13b` 028 |
| `teoria-cartilagine` | `13a` 001-047, poi `13b` 048-071 |
| `teoria-linfoide` | `16` 001-077 |
| `teoria-muscolare` | `03` 001, `17a` 002-047, `17b` 048-091, `17c` 092-115, poi `17d` 116-140 |
| `teoria-osso` | `14a` 001-030, `14b` 031-059, `14c` 060-086, `14d` 087-119, `14e` 120-152, poi `14f` 153-168 |
| `teoria-sangue` | `15a` 001-039 (senza 007-008), `15b` 040-065, `15c` 066-107, `15d` 108-137, `15e` 138-168, poi `14f` 169-174 |
| `teoria-staminali` | `03` 001-011, `11c` 012-016, `12d` 017, `17a` 018-020, `15e` 021-025, `18f` 026-040, `04` 041-077, poi `05` 078-098 |
| `teoria-nervoso` | `03` 001-002, `18a` 003-030, `18b` 031-050, `18c` 051-079, `18d` 080-102, `18e` 103-135, poi `18f` 136-147 |

`teoria-sangue-007` e `008` **non esistono**: erano le due carte sulla
colorazione di Wright, spostate su `teoria-colorazioni-089` e `090` mentre il
file era ancora in scrittura. I salti sono ammessi e non è stato rinumerato il
resto del file.

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
| `teoria-connettivi` | 001-004 | 005, ed è già stato fatto: il capitolo 12 occupa 005-160 |
| `teoria-muscolare` | 001 | 002, ed è già stato fatto: il capitolo 17 occupa 002-140 |
| `teoria-nervoso` | 001-002 | 003, ed è già stato fatto: il capitolo 18 occupa 003-147 |

**Lo stesso è successo con il capitolo 09 e l'endocrino.** Il 09 confronta le
ghiandole esocrine con le endocrine, quindi sei delle sue carte parlano di
endocrino prima che il mazzo 11 esista: portano `argomento::endocrino` e l'id
`teoria-endocrino-001`-`006`. Il mazzo 11 è **ripartito da 007** e ha chiuso a
121.

**E il capitolo 11 ha fatto la stessa cosa con le staminali.** Le cinque carte
sulla terapia cellulare del diabete di tipo I (pagina 109) parlano di cellule
staminali e di iPS, non di ghiandole: portano `argomento::staminali` e gli id
`teoria-staminali-012`-`016`, che proseguono la numerazione aperta dal capitolo
03. Il capitolo 12 ne ha aggiunta una sola, `017`, sulle biobanche del cordone
ombelicale; il capitolo 17 tre, `018`-`020`, sulle **cellule satellite** del
muscolo (che cosa sono, come rigenerano la fibra, perché la loro capacità si
esaurisce): sono staminali a tutti gli effetti, e la dispensa le chiama così.
Le carte sulla **distrofia di Duchenne** restano invece su `muscolare`, perché
sono una malattia del muscolo e non una questione di staminalità.
Il capitolo 15 ne ha aggiunte cinque, `021`-`025`, sulle **cellule staminali
emopoietiche**: la nicchia, l'autorinnovamento, la divisione simmetrica e
asimmetrica, l'MPP e le staminali mesenchimali del midollo. È lo stesso criterio
delle cellule satellite: ciò che parla di **staminalità** va su `staminali`,
mentre la filiera che porta alle cellule mature (CFU, precursori, eritropoiesi,
trombopoiesi) resta su `sangue`.
Il capitolo 18 ne ha aggiunte quindici, `026`-`040`, sulle **cellule staminali
neurali**: l'origine dagli astrociti, la neurogenesi adulta nell'ippocampo, la
glia radiale come progenitore, e i due esperimenti di *birth-dating* (BrdU nel
topo, carbonio-14 nell'uomo). Stesso criterio: la **rigenerazione dell'assone**
dopo una lesione resta invece su `nervoso`, perché non è una questione di
staminalità — le staminali neurali, dice la dispensa stessa a pagina 255, **non
partecipano** alla rigenerazione.
**I mazzi 04 e 05 hanno poi chiuso il contatore**, il 04 da `041` a `077` e il
05 da `078` a `098`: sono gli unici due capitoli in cui `staminali` è l'**unico**
`argomento::` su tutte le carte, come `linfoide` nel 16. Le carte dei capitoli
precedenti restano nel mazzo dove la sbobina le colloca, ma la selezione per
argomento le pesca insieme a questi due.

**Il capitolo 12 riapre `embriologia` e prosegue `connettivi`.** Le quattro
carte sull'origine mesenchimale dei connettivi (mesoderma, creste neurali,
migrazione e differenziamento delle cellule mesenchimali) sono embriologia,
non connettivi: portano `argomento::embriologia` e gli id
`teoria-embriologia-023`-`026`, che proseguono la numerazione aperta dal
capitolo 03. Le carte di connettivo vero e proprio ripartono invece da `005`,
dove il capitolo 03 si era fermato, come la tabella qui sopra prevedeva.

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
Istologia::Laboratorio::Vetrini           (unico, allenamento al riconoscimento)
Istologia::Teoria::<NN> - <Nome capitolo>
```

La numerazione segue l'ordine delle pagine nella sbobina, così i mazzi si
ordinano da soli come il corso.

### Il mazzo `Vetrini`

Aperto il 2026-08-27 su richiesta di Pietro, per allenare il **riconoscimento
dei vetrini** in vista dell'esame pratico. È la seconda eccezione alla regola
"un mazzo per capitolo", dopo `Quiz`, e per la stessa ragione: è un percorso di
studio a sé, con opzioni di mazzo proprie.

Regole, tutte diverse dal resto del progetto e da rispettare:

- **immagine sempre sul fronte**, `"image_side": "front"`, e sempre `basic`
  (il notetype Cloze non ha un campo per l'immagine sul fronte, e non lo
  tocchiamo);
- **3-4 domande sullo stesso vetrino**, con un mix fisso: identificazione,
  carattere distintivo, colorazione, struttura visibile nel campo. La quarta
  solo se il campo ha davvero qualcosa da indicare: **meglio tre carte solide
  che quattro con una inventata**;
- **regola anti-spoiler**: solo la domanda di identificazione tace il nome del
  tessuto, tutte le altre lo dichiarano *nella domanda* (`Vetrino di colon:
  ...`). Sono note separate, quindi la sepoltura dei fratelli non le divide: la
  disciplina di scrittura è l'unica difesa. Non scrivere mai il nome del
  tessuto solo nella risposta di una carta di dettaglio;
- `tipo::riconoscimento` su **tutte**, comprese quelle su colorazione e
  tecnica: partono tutte da una figura, ed è quello il senso del tag;
- gli **id proseguono il contatore dell'argomento** come ovunque: le carte del
  capitolo 01 sono `lab-colorazioni-039`-`062`, non ripartono da 001;
- **un file per capitolo**, `cards/laboratorio/vetrini-NN-<nome>.jsonl`.

**Le carte con immagine sul fronte già esistenti restano nel loro mazzo di
capitolo.** Non vanno spostate qui: Anki, al reimport, aggiorna i campi della
nota ma non necessariamente il mazzo della carta, quindi lo spostamento non
sarebbe affidabile. Le nuove domande sullo stesso vetrino vanno comunque nel
mazzo `Vetrini`, e prima di scriverle **va letta la carta che già esiste**:

```sh
grep -h "lab_p005_290.jpg" cards/laboratorio/*.jsonl
```

Il validatore intercetta i doppioni solo *dentro* lo stesso mazzo, quindi
questo controllo è manuale.

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

Il capitolo 03 ha aggiunto gli ultimi due valori, e nessuno dei quindici
capitoli scritti dopo di lui ne ha aggiunti altri: **l'elenco qui sopra è
chiuso**.

- `tessuti` — la panoramica: che cos'è un tessuto, l'equilibrio dinamico, le
  popolazioni perenni, stabili e labili, le due vie del rinnovamento. Sono le
  carte che non appartengono a nessuno dei quattro tessuti in particolare.
- `staminali` — le cellule staminali. È diventato il tag più trasversale del
  progetto: **otto capitoli** lo usano, e i due che ne portano il nome (il `04`
  e il `05`) sono stati gli ultimi a essere scritti, non i primi.

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

**Nemmeno il capitolo 11**, che è il più grosso dei tre: le sue 120 carte stanno
quasi tutte su `endocrino`, e le cinque sulla terapia cellulare del diabete di
tipo I usano `staminali`, che il capitolo 03 aveva già introdotto.

**E nemmeno il capitolo 12**, che è il più grosso di tutti con 179 carte. Sta
quasi tutto su `connettivi`, che il Laboratorio aveva già introdotto; riusa
`embriologia` per l'origine mesenchimale, `staminali` per le biobanche del
cordone ombelicale, `colorazioni` per le sei carte il cui contenuto è la
colorazione e non il tessuto (Alcian Blu sulla sostanza fondamentale,
aldeide-fucsina e orceina sulle fibre elastiche, osmio e Sudan sui lipidi,
Azan-Mallory e Verhoeff sulla tavola comparativa dei connettivi), e
`ghiandole` ed `endocrino` per l'excursus delle pagine 131-134. **Non è stato
inventato un `adiposo` a parte**: il tessuto adiposo sta su `connettivi`, come
già nel Laboratorio (`lab-connettivi-030`).

**E nemmeno il capitolo 13.** Sta quasi tutto su `cartilagine`, che **esisteva
già nel Laboratorio** (mazzi `06a` e `06d`, `lab-cartilagine-001`-`043`) ma che
nella Teoria non era mai stato usato: `teoria-cartilagine` apre quindi il
contatore da `001` pur non essendo un tag nuovo. Riusa poi `connettivi` per la
carta introduttiva sui connettivi di sostegno, `embriologia` per l'origine dalle
creste neurali e per la notocorda, e `colorazioni` per le tre carte il cui
contenuto è la colorazione e non il tessuto (Alcian blu-PAS sulle zone della
matrice, basofilia della capsula, Verhoeff sulla cartilagine elastica).

**E nemmeno il capitolo 16.** Sta **interamente** su `linfoide`, che
**esisteva già** in entrambe le fonti: nel Laboratorio con `lab-linfoide-001`-`047`
e nella Teoria con cinque carte del capitolo 08 (linfociti intraepiteliali e
cellule di Langerhans) che portano però id `teoria-epiteli-*`. `teoria-linfoide`
apre quindi il contatore da `001` pur non essendo un tag nuovo, esattamente come
`teoria-cartilagine` nel 13. È l'unico capitolo della Teoria con **un solo**
`argomento::` su tutte le carte: anche l'immunologia generale (antigene, MHC,
tolleranza, risposta innata e adattativa) ci sta sotto, perché nessun altro
valore esistente la copre e il capitolo non ne giustifica uno nuovo. Non è stato
aggiunto un `endocrino` alla carta sugli ormoni timici, che parla del timo:
**nessuna carta del progetto porta due `argomento::`**, e non è il caso di
cominciare qui.

**E nemmeno il capitolo 15.** Sta quasi tutto su `sangue`, che **esisteva già**
in entrambe le fonti (nel Laboratorio con `lab-sangue-001`-`018` e nella Teoria
con `teoria-epiteli-198` sulla forma biconcava degli eritrociti):
`teoria-sangue` apre quindi il contatore da `001` pur non essendo un tag nuovo,
esattamente come `teoria-cartilagine` nel 13 e `teoria-linfoide` nel 16. Riusa
poi `colorazioni` per le due carte il cui contenuto è la colorazione e non il
tessuto (quali coloranti usa la Wright, che rapporto ha con la Giemsa) e
`staminali` per le cinque sulle staminali emopoietiche.

**E nemmeno il capitolo 14.** Sta quasi tutto su `osso`, che **esisteva già nel
Laboratorio** (`lab-osso-001`-`046`, file `06b` e `06d`) ma che nella Teoria non
era mai stato usato come prefisso di id: `teoria-osso` apre quindi il contatore
da `001` pur non essendo un tag nuovo, esattamente come `teoria-cartilagine` nel
13, `teoria-linfoide` nel 16 e `teoria-sangue` nel 15. Riusa poi `colorazioni`
per la sola carta il cui contenuto è la colorazione e non il tessuto (perché
l'osso appare più rosa della cartilagine: il collagene è una proteina basica e
lega l'eosina) e `sangue` per le sei del **midollo osseo**, sul perché vedi qui
sotto.

**Le sei carte sul midollo osseo del 14 portano `argomento::sangue`**, non
`osso`, e stanno comunque nel mazzo 14. Il motivo è che la sezione `079`
(pagine 175-176) e la `083` (pagine 194-197, già cardata dal 15) descrivono
**la stessa cosa**: se le prime finissero su `osso` e le seconde su `sangue`, la
selezione trasversale spezzerebbe in due un unico argomento. Il precedente
contrario esiste (`lab-osso-038`, sul midollo giallo o rosso negli spazi
intertrabecolari, sta su `osso`), ma lì la carta è un **riconoscimento su un
vetrino di osso**, non una descrizione del midollo. **Non è stato inventato un
`midollo` a parte**, e nessuna carta porta due `argomento::`.

**I linfociti stanno su `sangue`, non su `linfoide`**, ed è una scelta
deliberata: nel capitolo 15 il taglio è quello del **leucocita nello striscio**
(morfologia, formula leucocitaria, diapedesi, riconoscimento al microscopio),
non quello dell'organo linfoide di cui si occupa il 16. Le due letture
restano vicine — `teoria-sangue-102`-`107` sui linfociti e `teoria-sangue-168`
sull'istruzione antigenica hanno il loro seguito naturale nel mazzo 16 — ma
**nessuna carta del progetto porta due `argomento::`**, e raddoppiare qui
avrebbe rotto la regola.

**E nemmeno il capitolo 17.** Sta quasi tutto su `muscolare`, che **esisteva
già** in entrambe le fonti (`lab-muscolare-001`-`044` e la carta
`teoria-muscolare-001` del capitolo 03), e riusa `staminali` per le tre carte
sulle cellule satellite. Non è stato inventato un `cardiaco` o un `liscio` a
parte: sono i tre tipi di uno stesso tessuto, e separarli spezzerebbe proprio
la selezione trasversale che serve per i confronti, che sono la parte più
richiesta del capitolo.

**E nemmeno il capitolo 18**, che è il più lungo della Teoria. Sta quasi tutto
su `nervoso`, che **esisteva già** in entrambe le fonti (`lab-nervoso-001`-`084`
e le due carte `teoria-nervoso-001` e `002` del capitolo 03); riusa `staminali`
per le quindici carte sulle staminali neurali e `colorazioni` per le **quattro**
carte il cui contenuto è la colorazione e non il tessuto: che cosa si vede del
tessuto nervoso in ematossilina-eosina (`092`), la colorazione di Golgi e il suo
5% di cellule (`093`), il Nissl su sostanza bianca e grigia (`094`) e il cresil
violetto sui corpi di Nissl (`095`).

Due scelte di questo capitolo meritano di essere ricordate, perché non erano
obbligate:

- il **Brainbow** e l'**immunoistochimica anti-GFAP** stanno su `nervoso`, non
  su `tecnica-istologica`. Il criterio è quello già usato: `tecnica-istologica`
  è il **metodo di preparazione** del campione, mentre queste sono tecniche che
  esistono solo per rispondere a una domanda sul tessuto nervoso (che circuito è
  questo, che cellula è questa) e fuori da quel contesto non dicono niente. Le
  quattro carte su `colorazioni` sono invece colorazioni vere e proprie, che
  Pietro incontra anche altrove;
- l'**origine embrionale** delle cellule nervose (neuroectoderma per il SNC,
  creste neurali per il SNP, mesoderma per la microglia) sta su `nervoso` e
  **non** apre carte su `embriologia`, al contrario di quanto fatto nel 12 con
  l'origine mesenchimale dei connettivi. Lì l'argomento era la gastrulazione e i
  foglietti; qui è un **criterio di classificazione delle cellule gliali**, ed è
  presentato dalla dispensa dentro l'elenco della neuroglia. Il **tubo neurale**
  e la **glia radiale** di pagina 252 stanno invece su `staminali`, perché sono
  la filiera dei progenitori.

**E nemmeno i mazzi 04 e 05, gli ultimi.** Sono gli unici due capitoli in cui
`argomento::staminali` sta su **tutte** le carte, senza una sola eccezione: è la
situazione del 16 con `linfoide`. Una scelta però non era obbligata e va
ricordata.

**Le pagine 17-18 sono embriologia, e stanno lo stesso su `staminali`.**
Descrivono zigote, segmentazione, morula, blastocisti, trofoblasto, massa
cellulare interna, annessi extraembrionali e gastrulazione, cioè materia che nel
mazzo 03 ha prodotto `teoria-embriologia-001`-`022`. Restano su `staminali` per
due motivi: la dispensa le presenta dentro la **scala della potenza**
(totipotente → pluripotente → multipotente), che è il tema del capitolo, e
soprattutto la massa cellulare interna era **già** su `staminali`
(`teoria-staminali-006`, mazzo 03). Metterci sopra `embriologia` avrebbe
separato la blastocisti dalle cellule che contiene. È il criterio del 18 con
l'origine embrionale delle cellule gliali, non quello del 12 con l'origine
mesenchimale dei connettivi: lì l'argomento *era* la gastrulazione, qui è la
potenza differenziativa.

Nessuna carta di questi due mazzi porta `embriologia`, `muscolare` o
`epiteli`, benché il 04 parli di distrofie muscolari e il 05 di epidermide e
cornea: in tutti e tre i casi l'oggetto della carta è il **compartimento
staminale**, non il tessuto. È lo stesso criterio con cui il 17 ha messo le
cellule satellite su `staminali` e la distrofia di Duchenne su `muscolare`.

### Il tag `non-trattato`

La sbobina marca alcuni passaggi con un riquadro laterale **"Argomento non
trattato nell'anno 2024/2025"**. Le carte si scrivono lo stesso — il materiale
è nella dispensa e potrebbe tornare — ma portano il tag `non-trattato` e lo
dicono in fondo al `back`, così Pietro può sospenderle in blocco con
`tag:non-trattato` se decide di fidarsi del programma dell'anno.

Il primo caso è `teoria-microscopia-015` (immagine reale e virtuale, pagina 50).
Il secondo è il blocco in corsivo che va da metà di **pagina 201** a metà di
**pagina 202** (movimento e percorso della linfa, definizione di essudato):
quattro carte, `teoria-linfoide-040`-`043`.

Il capitolo 17 ne ha aggiunti altri due, entrambi **riquadri brevi e ben
delimitati**, non blocchi a cavallo di più pagine come quello del linfatico:

- **pagina 209**, "Organizzazione delle cellule muscolari": il ruolo della
  componente connettivale nel coordinare la contrazione. Due carte,
  `teoria-muscolare-018` e `019`.
- **pagina 221**, "Battito cardiaco": sistole e diastole, propagazione via gap
  junction, fasi dal nodo SA ai ventricoli. Due carte,
  `teoria-muscolare-112` e `113`.

Il capitolo 15 ne ha aggiunti altri due, entrambi verificati sulla pagina
renderizzata perché **l'estensione non si capisce dal testo estratto**:

- **pagina 178**, "Ripasso sui circuiti sanguigni": copre il **solo blocco in
  corsivo** con la figura del circolo, e finisce dove comincia `Analisi del
  sangue`. Tre carte, `teoria-sangue-009`-`011`.
- **pagina 197**, che apre il riquadro su `Monocitopoiesi`: copre **sia la
  monocitopoiesi sia la granulocitopoiesi**, con le loro due figure, e prosegue
  fino a metà di pagina 198. La **linfocitopoiesi**, subito sotto, è in tondo e
  **non** è marcata: è materiale trattato. Quattro carte,
  `teoria-sangue-163`-`166`.

Il capitolo 14 ne ha aggiunti **tre**, ed è il capitolo che ne ha di più. Tutti e
tre sono **riquadri brevi e ben delimitati**, come quelli del 17, e tutti e tre
sono stati verificati sulla pagina renderizzata:

- **pagina 170**, `Approfondimento del docente` sul **VEGF**: il fattore di
  crescita dei vasi, la **degenerazione maculare** e la terapia con
  **anti-VEGF**. Copre il solo blocco in corsivo e finisce dove riprende il
  testo in tondo («L'osso neoformato assume la struttura di spicole…»). Due
  carte, `teoria-osso-135` e `136`.
- **pagina 172**, `Approfondimento del docente` sulla **menopausa**: il calo
  degli estrogeni, lo squilibrio fra riassorbimento e deposizione,
  l'**osteoporosi**. Due carte, `teoria-osso-151` e `152`. Il riquadro sta a
  pagina 172, in coda alle condrodisplasie, ma parla dell'**equilibrio del
  rimodellamento**, che il testo in tondo introduce solo a pagina 173: è
  collocato prima dell'argomento a cui si riferisce.
- **pagina 173**, il riquadro che descrive la **figura dell'unità di
  rimodellamento**: cono di escavazione e cono di riempimento, gli osteoclasti
  in verde, la matrice in viola, il nuovo osteone. Finisce dove comincia
  `Dinamica del modellamento`. Due carte, `teoria-osso-156` e `157`.

**Il capitolo 18 ne ha aggiunti sette, ed è di gran lunga il capitolo che ne ha
di più**: diciotto carte su 164. Il riquadro è sempre fatto allo stesso modo, e
una volta capito si riconosce a colpo d'occhio sulla pagina renderizzata: la
dicitura sta nel **margine sinistro**, e copre il **blocco in corsivo** che le
sta a destra, fino a dove riprende il testo in tondo. Un blocco può avere **più
sottotitoli in corsivo** al suo interno e restare un riquadro solo, e può
proseguire sulla pagina dopo **senza ripetere la dicitura**.

| Pagine | Riquadro | Carte |
|---|---|---|
| 232 | `Vie afferenti ed efferenti` | `037`-`038` |
| 236 | `In base alla forma del pirenoforo` **e** `In base alla lunghezza dell'assone` | `059`-`063` |
| 237 | `Citoscheletro dei neuroni` | `066` |
| 239 | `Il valore soglia` | `079` |
| 240-241 | `Tipi di sinapsi` **e** `Struttura delle sinapsi` | `085`-`087` |
| 245-246 | tutta la **seconda stesura** dei neurotrasmettitori | `098`-`102` |
| 250-251 | `Struttura della barriera ematoencefalica` | `133` |

Due di questi vanno guardati con attenzione:

- quello di **pagine 245-246** non è un riquadro breve ma **due pagine intere**,
  ed è il più importante del capitolo perché coincide con una **doppia stesura**
  (vedi la sottosezione del mazzo 18);
- quello di **pagina 237**, sul citoscheletro, **si sovrappone al testo in
  tondo** che lo segue: il riquadro dice che i dendriti sono lunghi al massimo
  700 micron e parla di spine dendritiche, e il paragrafo `Dendriti` subito
  sotto **ripete gli stessi due fatti** in tondo. Le carte sui dendriti
  (`067`-`069`) sono quindi materiale **trattato** e non portano il tag; solo la
  carta sulle tre componenti del citoscheletro (`066`) lo porta.

**Il mazzo 04 ne ha aggiunti due, e sono i primi due del PDF**, alle pagine 16 e
17. Sono fatti come tutti gli altri — dicitura nel margine sinistro, blocco in
corsivo a destra — ma hanno una particolarità che li avvicina alla doppia
stesura del 18: **ripetono materiale trattato altrove**, e vanno quindi letti
prima di scrivere, non dopo.

| Pagine | Riquadro | Carte |
|---|---|---|
| 16 | `Meccanismi Maladattativi` | `042`-`043` |
| 17 | `Classificazione` | `048`-`052` |

- quello di **pagina 16** rifà in breve ciò che il testo in tondo delle pagine
  21-22 dice per esteso (squilibrio del compartimento, distrofie muscolari,
  tumori). Ne restano due carte: la **via WNT** iperattivata nelle cellule
  tumorali, che il tondo non nomina, e l'**età e le cause della morte** nelle
  distrofie, che `teoria-muscolare-022` non ha;
- quello di **pagina 17** è più insidioso, perché ripete la classificazione
  cronologica delle staminali che il **mazzo 03** ha già cardato da pagina 15
  (`teoria-staminali-005`-`011`), e in più contraddice il testo in tondo della
  **stessa pagina** sullo stadio in cui finisce la totipotenza. Ne restano
  cinque carte, tutte su fatti che né il 03 né il tondo hanno: l'**epiblasto** come
  origine delle embrionali, gli **aborti spontanei** come provenienza delle
  fetali, il perché la **donazione del cordone** sia utile, le **cellule
  germinali** come secondo esempio di unipotenti e i due esempi contrapposti di
  turnover (sangue ed epidermide contro muscolo cardiaco).

Attenzione al riquadro di pagina 173 del mazzo 14: il riquadro descrive la figura, ma il **processo** che
la figura illustra è trattato subito sotto, in tondo, ed è materiale normale
(`teoria-osso-158`-`161`). Non tutta la figura è "non trattata": lo sono i **due
coni** e la lettura dei colori.

Il riquadro va guardato nel PDF
renderizzato, perché nel testo estratto compare come tre parole isolate e non si
capisce quanta parte copra:

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

**La copertura delle due sbobine è completa**, e quello che segue è il registro
di come ogni capitolo è stato deciso: serve a chi dovrà *correggere* una carta,
non più a chi deve scriverne. L'ordine di lavorazione qui sotto è quello
concordato con Pietro il 2026-08-10 ed è stato seguito fino in fondo.

**Resta invece aperto il mazzo `Vetrini`**, cominciato il 2026-08-27: vedi il
punto 4-bis.

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
stesso dice di non essere sicuro della colorazione**.

Quel «non c'è materiale rimasto da recuperare» valeva per i mazzi di capitolo,
**non** per il mazzo `Vetrini`: due di quelle dieci (`lab_p088_5557` e
`lab_p089_5593`) sono diventate carte con l'immagine sul fronte con
l'iterazione 7, e altre cinque delle pagine 82-85 aspettano l'iterazione 9. Un
doppione dello stesso campo è un doppione quando si spiega un tessuto; è un
**secondo campo su cui allenarsi** quando lo si deve riconoscere.

Attenzione al conteggio delle parole di una sezione: quello di `sections.jsonl`
comprende anche le descrizioni dei vetrini e le pagine di quiz, che sono lavoro
diverso dalla teoria. La sezione 019 dichiarava 4.260 parole ed erano in realtà
due pagine di teoria sull'osso, due sul sangue e sul linfoide, undici vetrini e
trenta domande di quiz: quattro file di carte, non uno.

I quiz del Laboratorio sono **tutti fatti**: pagine 40-42, 51-54, 71-75 e 92-95.
Se ne emergessero altri, il generatore gestisce già le quattro convenzioni di
marcatura.

### Teoria

111 sezioni, 98.000 parole, 486 immagini, **diciotto mazzi**.

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
| 04 - Cellule staminali e potenziale differenziativo | 16-24 | 9 | 16 | **fatto**, 37 note |
| 05 - Applicazioni terapeutiche delle cellule staminali | 24-28 | 5 | 17 | **fatto**, 21 note |
| 06 - Tessuti epiteliali | 28-49 | 22 | 5 | **fatto**, 158 note in due file |
| 07 - Concetti base di microscopia | 49-60 | 12 | 4 | **fatto**, 89 note |
| 08 - Epitelio di rivestimento | 60-85 | 26 | 6 | **fatto**, 183 note in tre file |
| 09 - Epiteli ghiandolari | 85-86 | 2 | 7 | **fatto**, 22 note |
| 10 - Ghiandole esocrine | 86-93 | 8 | 7 | **fatto**, 73 note |
| 11 - Ghiandole endocrine | 93-111 | 19 | 8 | **fatto**, 120 note in tre file |
| 12 - Tessuti connettivi | 111-137 | 27 | 9 | **fatto**, 179 note in cinque file |
| 13 - Tessuti connettivi di sostegno | 137-149 | 13 | 10 | **fatto**, 77 note in due file |
| 14 - Tessuto osseo | 149-176 | 28 | 14 | **fatto**, 175 note in sei file |
| 15 - Il sangue | 177-198 | 22 | 13 | **fatto**, 173 note in cinque file |
| 16 - Sistema linfatico | 198-205 | 8 | 11 | **fatto**, 77 note |
| 17 - Tessuto muscolare | 205-227 | 23 | 12 | **fatto**, 142 note in quattro file |
| 18 - Il tessuto nervoso | 227-256 | 30 | 15 | **fatto**, 164 note in sei file |

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
il `09 - Epiteli ghiandolari`, il `10 - Ghiandole esocrine`, l'`11 - Ghiandole
endocrine`, il `12 - Tessuti connettivi`, il `13 - Tessuti connettivi di
sostegno`, il `14 - Tessuto osseo`, il `15 - Il sangue`, il `16 - Sistema
linfatico`, il `17 - Tessuto muscolare` e il `18 - Il tessuto nervoso`.

**Il `04` e il `05`, le cellule staminali, sono stati gli ultimi**, e con loro
la Teoria si è chiusa. La loro sottosezione sta in fondo a questo punto.

Il `07` è l'unico capitolo che **non è istologia**: è ottica e strumentazione,
dalla struttura dell'occhio ai fluorofori. Sta nella sezione 024, occupa le
pagine 49-59 (pagina 60 apre l'`EPITELIO DI RIVESTIMENTO`, mazzo 08) e ha venti
figure, **tutte usate**. Sono quasi tutte schemi e tabelle con le didascalie
stampate sopra, quindi stanno sul retro; l'unica sul fronte è la coppia di
dischi di Airy al limite di Rayleigh, che non ha etichette.

**Le figure sono poi diventate venticinque**, cinque delle quali recuperate
abbassando la soglia di `is_artifact` (punto 6). **Ne sono usate 23**: tre sono
andate sul **retro** di carte che esistevano già (lo schema del campo chiaro
`teoria_p057_406` su `teoria-microscopia-066`, la coppia campo chiaro/contrasto
di fase `teoria_p057_408` su `072`, i due spettri dello Stokes shift
`teoria_p058_417` su `080`); le altre due **non sono figure** e restano
scartate, ed è il caso descritto al punto 6: `teoria_p053_371` è la formula
dell'ingrandimento totale e `teoria_p056_398` la tabella degli spessori del
coprioggetto. Il capitolo resta con **una sola figura sul fronte**.

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

Le **quarantadue** figure delle pagine 28-48 sono **tutte usate, tutte sul
retro**. La quarantaduesima è `teoria_p042_279`, recuperata dalla soglia (punto
6): è la micrografia al ME delle **interdigitazioni laterali** della membrana,
con la didascalia del libro stampata sopra, e sta sul retro di
`teoria-epiteli-122`. Attenzione: non va su `teoria-epiteli-095`, che parla
delle interdigitazioni del dominio **basale**.
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
trasversale le pesca insieme al mazzo 11, che è stato poi scritto.

Le **25 figure** delle pagine 85-93 sono state **usate tutte**, 2 nel mazzo 09 e
23 nel mazzo 10. Erano state passate al controllo del clip path (punto 6) e
corrispondono tutte a quello che si vede sulla pagina. Sette stanno sul fronte:
le microfotografie senza etichette (tricromica e PAS sull'intestino tenue, Alcian
blu sul colon, le quattro forme di adenomero, le tubulari glomerulari in
tricromica, la sebacea olocrina e il dotto mammario con le frecce sulle
protrusioni apicali). Tutto il resto sono schemi, tabelle e figure di libro con
la **didascalia stampata sopra**, che è già la risposta, e sta quindi sul retro.

#### Il mazzo 11 e la sua doppia sbobinatura

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

**Sono state fuse, non scritte due volte.** Il validatore blocca solo le domande
identiche nello stesso mazzo: due parafrasi della stessa carta gli passano
davanti e finiscono nei ripassi di Pietro come doppioni. Il metodo seguito è
stato: leggere per intero entrambe le stesure prima di scrivere una riga, e per
ogni fatto tenere **una sola carta**, quella costruita sulla versione più
completa. Il `source` porta allora **entrambe le pagine** (`5th gen p. 95 e p.
98`), che è la convenzione già usata per `teoria-tecnica-030`; quando invece una
sola delle due stesure contiene il fatto, il `source` è una pagina sola. Le
trentacinque carte di `11a` coprono così ciò che nella sbobina occupa sette
pagine.

Anche **le figure sono doppie**: `teoria_p095_689` e `teoria_p098_712` sono lo
stesso schema del feedback, la seconda con il titolo stampato sopra. È stata
usata **solo la seconda**, ed è l'unica delle 27 figure del capitolo a non
essere finita su una carta.

Due delle sette segnalazioni `da-verificare` del capitolo nascono proprio dalla
doppia stesura, cioè da punti in cui le due passate **si contraddicono**
(`teoria-endocrino-019` sulle catecolamine, `teoria-endocrino-085` sul trasporto
degli ormoni tiroidei). In questi casi la carta tiene la versione corretta e
l'altra è citata nella nota in corsivo, così Pietro sa che cosa ha letto
altrove.

**L'`11 - Ghiandole endocrine` finisce a pagina 110, non a 111.** La riga della
tabella dice 93-111 secondo la convenzione della colonna, che indica la pagina in
cui comincia il capitolo successivo. **Pagina 111 è stata renderizzata e
guardata, ed è interamente del mazzo 12**: si apre in cima con l'intestazione di
una lezione nuova (01-04-2025, sbobinatori Zamboni e Webber) e subito sotto con
il titolo `TESSUTI CONNETTIVI`, seguito dallo schema di classificazione dei
connettivi. La figura `teoria_p111_808` appartiene quindi al 12 e **non va
ripresa**. È lo stesso caso dell'`08`, che la tabella dà per 60-85 e che si
ferma a 84.

**Diviso in tre file**, perché 18 pagine, circa 6.800 parole e 27 figure non
stanno in un file solo. I tagli seguono i confini di sezione e lasciano tre
blocchi di dimensione simile:

| File | Sezioni | Pagine | Contenuto |
|---|---|---|---|
| `11a-endocrino-generalita.jsonl` | `042`-`047` | 93-99 | ormoni, recettori, feedback, classificazione strutturale delle endocrine (**è qui che sta la doppia sbobinatura**) |
| `11b-ipofisi-paratiroidi-tiroide.jsonl` | `048`-`050` | 99-105 | ipofisi, sistema ipotalamo-ipofisario, cellule dell'adenoipofisi, paratiroidi, tiroide |
| `11c-surrene-e-pancreas-endocrino.jsonl` | `051` | 105-110 | surrene, pancreas endocrino, diabete di tipo I, cellule non epiteliali a funzione endocrina |

Come per `06a`/`06b` e `08a`/`08b`/`08c`, tutti e tre condividono lo stesso mazzo
`Istologia::Teoria::11 - Ghiandole endocrine`. Il terzo file **non si chiama come
la sezione**: la `051` si intitola "Ghiandole endocrine del surrene" ma il
surrene finisce a pagina 107 e il resto è pancreas endocrino, diabete e cellule
non epiteliali.

**Nessun tag nuovo.** Il capitolo riusa `endocrino` (che viene dal Laboratorio,
mazzi `04a` e `04b`) e `staminali` per le cinque carte sulla terapia cellulare
del diabete.

Delle **27 figure** ne sono state usate **26**, l'unica scartata essendo il
doppione del feedback di cui sopra. Il **controllo del clip path** del punto 6,
che il piano dichiarava fatto solo fino a pagina 97, **è stato completato da 98 a
110**: due figure sono uscite sotto soglia e sono state guardate una per una.
Nessuna delle due è il caso della finestra di browser che aveva costretto a
scartarne undici nell'`08`: `teoria_p100_726` (origine embrionale dell'ipofisi)
esce a 0,43 perché il file estratto include la riga di didascalia del libro che
la pagina taglia via, e `teoria_p104_757` (schema del follicolo tiroideo) esce a
0,72 perché la pagina ne rifila il bordo destro. Entrambe sono complete e
leggibili, ed entrambe sono state usate sul retro.

Cinque figure stanno sul **fronte**, e sono tutte micrografie senza etichette:
l'adenoipofisi con i richiami muti `A`, `B` e `C` (`teoria_p101_734`), la
paratiroide a basso ingrandimento (`teoria_p103_747`) e i follicoli tiroidei
(`teoria_p104_756`). Tutto il resto sono schemi, tavole anatomiche e figure di
libro con la didascalia stampata sopra, cioè materiale da retro.

**L'aggancio con `lab-endocrino-014` si chiude qui, e la teoria dà ragione al
sospetto.** Il Laboratorio attribuiva il testosterone ai tubuli seminiferi e
metteva il corpo luteo fra le ghiandole interstiziali; la teoria, a pagina 96 e a
pagina 99, dice che a produrre testosterone sono le **cellule di Leydig**, che
stanno *negli interstizi fra* i tubuli seminiferi (è `teoria-endocrino-039`), e a
pagina 110 elenca il corpo luteo fra le **cellule endocrine associate alle
gonadi**, non fra le interstiziali (`teoria-endocrino-118`). La teoria quindi
**corregge il Laboratorio**, e non è stata aperta una segnalazione nuova: quella
sul Laboratorio resta e ora ha una risposta.

#### Il mazzo 12 e l'excursus sulle ghiandole

**Il `12 - Tessuti connettivi` va da pagina 111 a metà di pagina 137.** Pagina
137 è stata renderizzata e guardata: in cima ci sono ancora le due tavole
comparative delle colorazioni che chiudono il 12, e solo sotto comincia il
titolo `TESSUTI CONNETTIVI DI SOSTEGNO`. Le figure `teoria_p137_968`, `969` e
`970` (le tre righe della tavola: ematossilina-eosina, Azan-Mallory, Verhoeff)
appartengono quindi al **12**, non al 13, benché `images_for_section` le
assegni a entrambe le sezioni. Solo `teoria_p137_971`, la microfotografia di
cartilagine, è del 13.

**Diviso in cinque file**: 26 pagine, circa 10.400 parole e 59 figure sono il
capitolo più grosso della Teoria. I tagli seguono i confini di contenuto.

| File | Pagine | Contenuto |
|---|---|---|
| `12a-matrice-extracellulare.jsonl` | 111-116 | generalità e classificazione, origine embrionale e strutturale, ECM, sostanza fondamentale, GAG, acido ialuronico, proteoglicani, glicoproteine adesive, integrine |
| `12b-fibre-collagene-ed-elastiche.jsonl` | 116-123 | componente fibrillare, collagene (struttura, sintesi, tipi, FACIT), fibre reticolari, collagenopatie, fibre elastiche, elastina, Marfan |
| `12c-cellule-del-connettivo.jsonl` | 123-128 | cellule residenti e transitorie, fibroblasti, fibrociti, miofibroblasti, macrofagi, mastociti, adipociti |
| `12d-classificazione-dei-connettivi.jsonl` | 128-131, 134-137 | mesenchima, mucoso, lasso, denso (regolare, irregolare, a fasci incrociati), reticolare, elastico, tessuto adiposo, confronto delle colorazioni |
| `12e-confronti-al-microscopio.jsonl` | 131-134 | l'excursus sulle ghiandole (vedi qui sotto) |

I primi quattro condividono il mazzo `Istologia::Teoria::12 - Tessuti
connettivi`, come `06a`/`06b` e `08a`/`08b`/`08c`. Il quinto no.

**Le pagine 131-134 non parlano di connettivi.** Sono un `[N.d.S.]`: un
confronto al microscopio fra **parotide e pancreas** e fra **corticale
surrenale e adenoipofisi**, riportato "a fronte di dubbi sorti nelle lezioni
precedenti". Sta dentro la lezione sui connettivi solo perché il professore lo
ha ripreso lì. Le sue **12 carte stanno quindi nei mazzi `10 - Ghiandole
esocrine` e `11 - Ghiandole endocrine`**, che è dove Pietro ripassa quegli
argomenti, e portano gli id `teoria-ghiandole-086`-`094` e
`teoria-endocrino-122`-`124`.

È il precedente di **`07b` del Laboratorio**, non quello di `06d`: il criterio
"deck del capitolo dove sta la pagina" vale quando gli argomenti appartengono
davvero a quel capitolo, e qui non è il caso. Diverso è invece il caso delle
carte su `embriologia` e `staminali`, che parlano comunque di connettivo visto
da un altro lato e restano nel mazzo 12 con il loro `argomento::`.

Il contenuto di `12e` è quasi tutto **riconoscimento**: la teoria della
corticale surrenale e delle cellule dell'adenoipofisi era già coperta dal mazzo
11 (`teoria-endocrino-055`-`058` e `095`-`098`), quindi da lì si sono prese solo
le immagini e il criterio con cui distinguere i due tessuti.

**Le 60 figure sono state usate tutte.** La sessantesima è `teoria_p125_906`,
recuperata dalla soglia (punto 6): è la micrografia dei **macrofagi** con la
scritta `Macrofagi` stampata sopra, e sta sul retro di `teoria-connettivi-109`,
la carta della morfologia stellata. Il controllo del clip path del punto 6
è stato eseguito sulle pagine 111-137 e ha segnalato quattro figure sotto
soglia, tutte guardate una per una e tutte utilizzabili:

- `teoria_p126_909` (mastociti, corr 0,01): il file estratto è lo **stesso**
  campo della pagina, ma **ruotato di 90°**; la correlazione crolla per la
  rotazione, non per un ritaglio.
- `teoria_p133_945` (corr 0,17): è l'immagine **intera** delle tre zone della
  corticale surrenale impilate, che la pagina spezza in tre riquadri distanziati.
  Il file estratto è più completo della pagina, ed è stato usato così.
- `teoria_p136_962` (mesentere murino, corr 0,80) e `teoria_p123_898`: al limite
  della soglia, ma integri.

Nessuna è il caso della finestra di browser che aveva costretto a scartarne
undici nell'`08`.

**Attenzione a due figure che illustrano una pagina diversa dalla propria**,
il caso del punto 6: `teoria_p113_828`, lo schema delle cellule del connettivo,
sta a pagina 113 in mezzo alla sostanza fondamentale ma illustra il testo di
pagina 123; e `teoria_p111_808`, lo schema di classificazione, apre il capitolo
12 pur stando sulla pagina che il mazzo 11 chiude.

#### Il mazzo 13 e la cartilagine

**Il `13 - Tessuti connettivi di sostegno` va da metà di pagina 137 a fine
pagina 148.** La riga della tabella dice 137-149 secondo la convenzione della
colonna, che indica la pagina in cui comincia il capitolo successivo. **Pagina
149 è stata renderizzata e guardata, ed è interamente del mazzo 14**: si apre in
cima con il titolo `TESSUTO OSSEO`. La figura `teoria_p149_1023` (sezione di
femore) appartiene quindi al 14 e **non va ripresa**, benché
`images_for_section` la assegni alla sezione `069`.

All'altro capo, le figure `teoria_p137_968`, `969` e `970` sono le tre righe
della tavola comparativa delle colorazioni che chiude il 12 e sono **già usate
da `12d`**. Solo `teoria_p137_971`, la microfotografia di cartilagine, è del 13.

Il capitolo copre le sezioni `068` (il cappello di tre righe sui connettivi di
sostegno) e `069` (tutta la cartilagine), e due lezioni. **Diviso in due file**
sul cambio di lezione a pagina 145, che porta un'intestazione nuova
(sbobinatori Ognibeni e Giovannini, 10-04-2025) e la riga
`[continuazione della lezione precedente sulla CARTILAGINE]`:

| File | Pagine | Contenuto |
|---|---|---|
| `13a-cartilagine-generalita.jsonl` | 137-144 | definizione, localizzazione, i tre tipi, funzioni, matrice extracellulare e aggregati di proteoglicani, resistenza alla compressione, pericondrio, condroblasti e condrociti, gruppi isogeni, aree della matrice, condrogenesi, accrescimento |
| `13b-tipi-di-cartilagine.jsonl` | 145-148 | cartilagine ialina (vie respiratorie, cartilagine di accrescimento e ossificazione endocondrale, cartilagine articolare), elastica, fibrosa, dischi intervertebrali |

Come per `06a`/`06b` e `08a`/`08b`/`08c`, i due file **condividono lo stesso
mazzo** `Istologia::Teoria::13 - Tessuti connettivi di sostegno`.

**La seconda lezione ripassa un pezzo della prima**, come già le pagine 93-99
del mazzo 11, anche se in misura molto minore: pagina 145 rielenca i tre tipi di
cartilagine (già a pagina 138) e rispiega la colorazione differenziale della
matrice (già a pagine 142-143). Non sono state scritte due volte: `13a` tiene la
prima stesura, e `13b` prende dalla seconda **solo ciò che aggiunge**, cioè la
composizione della matrice tipo per tipo. Il punto in cui le due passate si
contraddicono è diventato una segnalazione (`teoria-cartilagine-050`).

**Le 28 figure delle pagine 137-148 sono state usate tutte.** La ventottesima è
`teoria_p148_1016`, recuperata dalla soglia (punto 6) e l'**unica delle dieci a
valere una carta nuova**: è il disco intervertebrale in sezione longitudinale,
con i richiami muti `V`, `NP` e `AF`, ed è il pannello di sinistra della coppia
di pagina 148 di cui `teoria-cartilagine-070` usa già il destro. Sta sul
**fronte** di `teoria-cartilagine-071`. Il controllo del
clip path del punto 6 è stato eseguito sulle pagine 137-149 e ha segnalato
cinque figure sotto soglia, tutte guardate una per una e tutte utilizzabili.
Nessuna è il caso della finestra di browser che aveva costretto a scartarne
undici nell'`08`. Sono tutte **figure composite di più pannelli**, e la
correlazione crolla per due motivi diversi:

*Il file estratto è più completo della pagina*, come `teoria_p133_945`:

- `teoria_p137_971` (corr 0,50): due pannelli impilati e **ruotati di 90°**, di
  cui la pagina mostra solo il primo. Usato così, come `teoria_p126_909`.
- `teoria_p141_987` (corr 0,55): include in cima lo schema
  "Organizzazione cellulare ed extracellulare della cartilagine", che la pagina
  taglia via.

*La pagina mostra tutto, ma spezzato in placement separati e riordinati*, quindi
nessun singolo ritaglio somiglia al file intero:

- `teoria_p141_989` (corr 0,58): microfotografia al ME e schema del condrocita,
  che la pagina affianca in ordine invertito.
- `teoria_p144_999` (corr 0,75): le due modalità di accrescimento in una figura
  sola; la pagina colloca prima il pannello B (interstiziale) e poi l'A
  (apposizione), accanto ai rispettivi paragrafi.
- `teoria_p148_1020` (corr 0,73): la tavola delle vertebre più il disegno di
  midollo e radici nervose, che la pagina mette in due punti diversi.

**Cinque** figure stanno sul **fronte**, e sono le sole che portino marcatori
muti: `teoria_p137_971` (la sigla `L` sulle lacune), `teoria_p142_993` (`C`, `AT`,
`AI` sulle zone della matrice in Alcian blu-PAS), `teoria_p145_1003` (`TCD`,
`P`, `CA`, `MT`, `MI`, `N`), `teoria_p148_1017` (`C`, `M`, `NP` sulla
fibrocartilagine) e `teoria_p148_1016` (`V`, `NP`, `AF` sul disco intero). Tutto il resto sono schemi, tavole e figure di libro con la
**didascalia stampata sopra**, cioè materiale da retro.

#### Il mazzo 14 e il tessuto osseo

**Il `14 - Tessuto osseo` va da inizio pagina 149 a fine pagina 176.** Entrambi i
confini erano già stati verificati e sono stati riconfermati:

- **pagina 149** è interamente del 14 (si apre con il titolo `TESSUTO OSSEO`) e
  la figura `teoria_p149_1023`, la sezione di femore, è sua, benché
  `images_for_section` la assegni alla sezione `069`;
- **pagina 176** chiude il capitolo con l'elenco delle cellule del midollo rosso
  ed è **mezza vuota**; pagina 177 si apre con l'intestazione della lezione del
  13-05-2025 e il titolo `IL SANGUE`. Pagina 176 **non ha figure**.

Il capitolo copre le sezioni da `070` a `079`, **circa 12.700 parole**, ed è il
**più grosso della Teoria**: più del 12 (10.400) e del 15 (9.800). È **diviso in
sei file**, il numero più alto finora.

| File | Sezioni | Pagine | Contenuto |
|---|---|---|---|
| `14a-generalita-e-matrice.jsonl` | `070`-`071` | 149-152 | definizione, funzioni, classificazione macroscopica, matrice organica e inorganica, osteonectina e osteocalcina, mineralizzazione e demineralizzazione, i due metodi di preparazione, lacune e canalicoli |
| `14b-osso-lamellare-e-immaturo.jsonl` | `072` | 152-157 | osso lamellare compatto e spugnoso, osso immaturo, trabecole e linee di forza (**è qui che sta la doppia stesura**) |
| `14c-osteone-e-canali.jsonl` | `073` (1ª parte) | 157-161 | tavolati, osteone, lamelle interstiziali e circonferenziali, formazione dell'osteone, osteoni secondari, canali di Havers e di Volkmann, periostio, fibre di Sharpey, endostio |
| `14d-le-cellule-del-tessuto-osseo.jsonl` | `073` (2ª parte) | 161-167 | i quattro citotipi, linea mesenchimale e BMP, osteoblasti e osteoide, cellule di rivestimento, osteociti meccanorecettori, osteoclasti, lacuna di Howship, riassorbimento |
| `14e-ossificazione.jsonl` | `073` (3ª parte)-`076` | 167-173 | tipi di ossificazione, intramembranosa (**seconda doppia stesura**), endocondrale, cartilagine di accrescimento, condrodisplasie |
| `14f-rimodellamento-riparazione-midollo.jsonl` | `077`-`079` | 173-176 | rimodellamento, unità di rimodellamento, riparazione delle fratture, midollo osseo |

Come per `06a`/`06b`, `08a`-`08c`, `11a`-`11c`, `15a`-`15e` e `17a`-`17d`, tutti
e sei i file condividono lo stesso mazzo `Istologia::Teoria::14 - Tessuto osseo`.

**Come sono stati decisi i tagli.** Il capitolo ha **due cambi di lezione al suo
interno** (pagine 154 e 169; il terzo, a pagina 177, apre il 15) e **due doppie
stesure**, e sono queste ultime a decidere tutto:
un taglio in mezzo a una doppia stesura avrebbe messo le due passate in file
diversi, con il rischio di due parafrasi della stessa carta, che il validatore
**non** intercetta perché blocca solo le domande identiche.

- **La sezione `072` (pagine 152-157) è tutta doppia stesura.** Le pagine 152-153
  chiudono la prima lezione con osso lamellare e osso immaturo; pagina 154 apre
  la lezione del **15-04-2025** (sbobinatori Benedetti e Benacchio) con la riga
  `[continuazione della lezione precedente sul TESSUTO OSSEO]` e **rifà gli
  stessi argomenti**: immaturo contro maturo, spugnoso contro compatto. Il cambio
  di lezione a pagina 154 era il taglio più ovvio ed è stato **scartato**: `14b`
  tiene entrambe le passate, esattamente come `17a` tiene le due stesure
  dell'introduzione al muscolare.
- **Anche la sezione `073` finisce dentro una doppia stesura.** Pagina 169 apre
  la lezione del **06-05-2025** (sbobinatori Calone e Airoma) con un `[N.d.S.:
  questi argomenti sono stati trattati velocemente nella lezione precedente. Si
  riporta, per completezza, anche quanto detto in questa lezione]`, e rifà i
  **tipi di ossificazione** e l'**ossificazione intramembranosa**, già trattati
  alle pagine 167-168. La seconda passata finisce dove un secondo `[N.d.S.: da
  qui cominciano gli argomenti trattati esclusivamente il 06-05-2025]`, a metà di
  **pagina 170**, dichiara chiuso il ripasso. Il taglio è quindi a **pagina 167**,
  all'inizio di `Tipi di ossificazione`: così `14e` contiene tutte e due le
  passate.
- **La `073` da sola vale 5.900 parole**, quasi metà del capitolo, e va spezzata
  al suo interno in tre. Il primo taglio, fra `14c` e `14d`, cade a pagina 161 su
  un **confine di contenuto netto**: sopra la **struttura** dell'osso compatto
  (lamelle, canali, involucri), sotto il titolo `Le cellule del tessuto osseo`.
  Il secondo è quello di pagina 167 appena descritto.

**Le due doppie stesure sono state fuse, non scritte due volte**, con il metodo
del mazzo 11: una sola carta per fatto, costruita sulla **versione più completa**,
e `source` con **entrambe le pagine** (`5th gen p. 152 e p. 154`) quando il fatto
sta in tutte e due. La seconda passata della `072` è quella più ricca su
spugnoso, compatto e linee di forza; la prima è l'unica ad avere filogenesi
dell'osso immaturo, sedi nell'adulto, spessore delle lamelle e forma delle lacune.

**Un terzo caso di ripetizione non è un cambio di lezione**, ed è più insidioso
perché a cavallo di due file: **periostio, endostio, lacune e canalicoli
compaiono due volte**, brevemente a pagina 151 (sezione `071`) e per esteso a
pagina 161 (sezione `073`). Le carte sono state scritte **una volta sola**, sulla
versione di pagina 161, con `source` `5th gen p. 151 e p. 161`, e stanno in `14c`:
`14a` non le ripete. Stesso trattamento per i **due metodi di preparazione**
(demineralizzazione e sezione per usura), descritti nelle integrazioni di pagine
150-151 e poi di nuovo a pagina 156: le carte stanno in `14a` con `source`
`5th gen p. 150-151 e p. 156`, e `14b` usa la figura di pagina 156 per una carta
di **riconoscimento**, che è cosa diversa.

**Il midollo osseo si sovrappone al mazzo 15, e questa è la trappola peggiore
del capitolo.** La sezione `079` (pagine 175-176) e la sezione `083` (pagine
194-197, già cardata in `15e`) hanno **lo stesso titolo e in parte lo stesso
contenuto**. Il 15 aveva già coperto consistenza e stroma gelatinoso
(`teoria-sangue-139`), peso di 2,6 kg e 4% del peso corporeo (`140`), differenza
fra midollo rosso e giallo (`141`), sedi del rosso nell'adulto (`142`) e le tre
categorie di cellule midollari (`teoria-staminali-021`). **Quelle carte non sono
state riscritte.** Il `14f` prende solo ciò che il 15 non ha:

- le **tre funzioni** del midollo osseo, che sono l'angolo del capitolo sull'osso
  (`teoria-sangue-169`);
- il passaggio **rosso → giallo con l'età** (dai 20 anni) e le **sedi del
  midollo giallo** (omero e femore), che il 15 non nomina (`170`);
- l'elenco dei **sette citotipi** del midollo rosso, molto più fine delle tre
  categorie di `teoria-staminali-021`, con lo **0,1%** delle staminali
  emopoietiche (`171`-`174`).

Il validatore **non avrebbe visto niente**, perché i due mazzi sono diversi e
controlla i duplicati solo dentro lo stesso mazzo: chi tocca questo confine deve
rileggere `15e` prima di scrivere.

**Il controllo del clip path del punto 6 è stato eseguito sulle pagine 149-176 e
ha segnalato quattro placement su 54.** È l'esito più pulito dopo il 16. Nessuna
finestra di browser:

- `teoria_p151_1030` (corr 0,77): al limite della soglia, **integra**, con il
  bordo appena rifilato. È la sezione per usura con i marcatori muti `CH`, `LO`,
  `CV`, ed è usata sul **fronte**.
- `teoria_p156_1051` (corr 0,34, segnalata **due volte** perché la pagina la
  colloca in due punti): il file estratto è la **figura intera a due pannelli**
  `A`/`B`, che la pagina **spezza in due ritagli separati** e distanti. È il caso
  di `teoria_p144_999` nel 13. Usata intera, sul **fronte**.
- `teoria_p165_1091` (corr −0,49, 301x138): **non è una figura**. È uno dei
  **rettangoli colorati sovrapposti** allo schema dell'osteoclasto di pagina 165
  (quello blu sulla regione basolaterale), estratto come un rettangolo nero con
  il bordo blu. **Scartata.**

Quest'ultima merita attenzione: era **l'unica figura del capitolo recuperata
abbassando la soglia di `is_artifact`** scrivendo il 15, e il piano la dava per
materiale da recuperare. Non lo era. Il capitolo **non ha guadagnato niente** da
quella modifica, al contrario del 15 che ci ha guadagnato otto figure.

**Delle 53 figure delle pagine 149-176 ne sono state usate 47.** Le sei scartate
sono `teoria_p165_1091`, il rettangolo di cui sopra, e **cinque doppioni della
doppia stesura**, per i quali è stata tenuta ogni volta la **versione più
grande**:

| Scartata | Tenuta | Che cos'è |
|---|---|---|
| `teoria_p152_1035` | `teoria_p154_1042` | osteone in ematossilina-eosina con il marcatore muto `O` |
| `teoria_p152_1036` | `teoria_p154_1041` | osso immaturo in ematossilina-eosina |
| `teoria_p169_1104` | `teoria_p167_1097` | schema a quattro pannelli dell'ossificazione intramembranosa |
| `teoria_p170_1107` | `teoria_p168_1100` | schema del centro di ossificazione più microfotografia |
| `teoria_p170_1108` | `teoria_p168_1101` | sezione di mandibola, figura 8.19 |

**Quindici figure su 47 stanno sul fronte** (32%), ed è la **proporzione più alta
di tutta la Teoria** (nel 15 erano otto su 29, cioè il 28%). Il motivo è che
l'osso si studia su **due tipi di preparato**, il demineralizzato e la sezione
per usura, e le microfotografie di entrambi portano quasi sempre **marcatori muti
a due lettere** invece di didascalie: `CO`, `LO`, `CH`, `CV`, `OST`, `T`, `MO`,
`VS`, `Ob`, `Oc`, `O`. Sono `teoria_p150_1026`, `p150_1027`, `p151_1030`,
`p154_1041`, `p154_1042`, `p155_1046`, `p156_1051`, `p157_1054`, `p160_1069`,
`p163_1081`, `p164_1085` e `p166_1094`. Le altre tre sono **senza alcuna
etichetta**: `p161_1073` (le fibre di Sharpey che entrano nelle lamelle
circonferenziali), `p170_1109` (osso spugnoso in via di formazione) e
`p174_1125` (la microradiografia con gli osteoni a mineralizzazione diversa).

Tutto il resto sono schemi, tavole e figure di libro con la **didascalia stampata
sopra**, cioè materiale da retro.

Un caso è al limite e vale la pena spiegarlo: `teoria_p166_1094` porta stampata
la didascalia del libro «Fotografia al microscopio ottico di un **osteoclasto**
su una spicola ossea», ma la carta che ci sta sopra chiede di distinguere
**osso e cartilagine** dentro la stessa spicola, cosa che la didascalia non
rivela. È il criterio di `teoria_p203_1222` nel 16: le etichette danno il
contesto senza dare la risposta.

**Dodici segnalazioni su 175 carte** (6,9%), fra il tasso del 15 (5,8%) e quello
del 16 (9,1%). **Sette nascono da contraddizioni interne alla dispensa**, ed è la
quota più alta di tutta la Teoria:

- le lamelle circonferenziali interne date insieme «a contatto con il canale di
  Havers» e come quelle che «separano l'osso dalla cavità midollare» (`063`);
- le lamelle deposte **verso l'interno** del canale che però lo renderebbero
  «più grande» (`074`) — a pagina 173 la stessa dispensa dice che si dispongono
  «dalla periferia verso il centro» e che alla fine «rimane solo una cavità
  centrale»;
- l'osso compatto resistente in **una sola direzione** a pagina 152 e «alle
  sollecitazioni provenienti dalle diverse direzioni» a pagina 156, cioè il punto
  in cui le due stesure della `072` divergono (`037`);
- le **lacune ossee** collocate dentro le **cavità midollari** una riga prima di
  dire che gli osteociti sono «immersi nella matrice ossea mineralizzata»
  (`050`);
- l'osteoclasto di **100 micron** paragonato a «cellule come i **monociti**», che
  ne misurano quindici (`103`);
- gli osteociti che «non hanno un ruolo primario nel rimodellamento» due
  paragrafi prima di essere quelli che producono i segnali chemiotattici che
  attivano gli osteoclasti, e dopo che pagina 149 li ha indicati come i
  captatori dello stimolo (`102`);
- il **cranio** che cresce «per deposizione di nuovo osso sulla superficie
  esterna» e che due frasi dopo riassorbe proprio sulla superficie esterna
  (`134`).

Le altre cinque sono errori verso la nozione classica: i **canalicoli**
identificati con i canali trasversali «di Voorman» (`049`), i **canali
trasversali** chiamati «osteoni» nella didascalia di pagina 151 (`023`), le
«cellule **epiteliali**» elencate fra quelle dell'endostio nella didascalia della
figura (`086`), la «forte capacità **mitotica**» attribuita agli osteoblasti
(`097`) e il recettore del **FGF** dato per acceleratore della crescita ossea
mentre la sua mutazione **attivatoria** causa il nanismo (`150`).

**Due refusi sono stati risolti senza tag**, perché non c'è dubbio di contenuto:

- la dispensa chiama **«canale trasversale di Voorman»** quello che a pagina 160,
  e in tutte le figure delle pagine 158 e 160, chiama correttamente **canale di
  Volkmann**. Il nome è stato scritto giusto nelle carte. Resta invece la
  segnalazione `049`, che non è sul **nome** ma sulla **cosa**: lì i canalicoli e
  i canali trasversali sono dati per la stessa struttura.
- il titoletto di pagina 164 dice **«Gli osteoclasti come meccanorecettori»** ma
  il paragrafo parla per intero degli **osteociti**, come tutto il resto del
  capitolo. È un lapsus di intestazione e non tocca il contenuto.
- a pagina 152 la dispensa scrive «scheletro inferiore dei vertebrati» per
  «scheletro dei **vertebrati inferiori**»: è un'inversione di parole, ed è
  segnalata in corsivo sulla carta `045` senza tag.

**L'aggancio con `lab-osso-046` si chiude qui, e la teoria dà ragione al
sospetto.** Il Laboratorio metteva dei **condroblasti** lungo le pareti dei canali
di Havers. La teoria dice, a pagina 161, che i canali di Havers e di Volkmann sono
rivestiti da **endostio**, il quale contiene «cellule di rivestimento, cellule
osteoprogenitrici, osteoblasti e osteoclasti» (`teoria-osso-085` e `086`), e
ripete a pagina 162 che «le cellule osteoprogenitrici si trovano [...] anche
all'interno dei canali di Havers e di Volkmann, che sono anch'essi rivestiti da
endostio» (`teoria-osso-090`). I condroblasti non ci sono, e le cellule attese
sono esattamente quelle che il Laboratorio non nominava. La teoria quindi
**corregge il Laboratorio**, e non è stata aperta una segnalazione nuova: quella
sul Laboratorio resta e ora ha una risposta, come per `lab-endocrino-014`,
`lab-muscolare-016` e `lab-linfoide-015`.

**Per il resto le due fonti non si contraddicono.** Il Laboratorio
(`lab-osso-001`-`046`, file `06b` e `06d`) guarda il **vetrino** e il
riconoscimento; la Teoria i **meccanismi**. Dove si toccano dicono la stessa
cosa: le fibre di Sharpey che si addentrano nel sistema di lamelle
(`lab-osso-012` e `teoria-osso-084`), i canali di Volkmann (`lab-osso-027` e
`teoria-osso-077`), i due metodi di preparazione (`lab-osso-006`-`009` e
`teoria-osso-021`-`022`).

**Un `[N.d.S.]` non produce carte**: quello di pagina 173, che riporta il link a
un video sul rimodellamento visionato in aula. È il caso dei video di pagina 217 e
226 nel 17.

**Le integrazioni sono tutte additive**, come nel 15 e nel 16 e a differenza del
17. Sono quattro, tutte fra le pagine 150 e 151: tre `[Integrazione da sbobina
2023/2024]` (la microfotografia di osso demineralizzato, la preparazione della
sezione per usura, il destino dell'osteoblasto inglobato) e una `[Integrazione da
sbobina 2022/2023]` (la **calcinazione**, cioè la combustione in ossigeno che
rende l'osso friabile come la porcellana). Nessuna ripete il testo principale, e
tutte sono citate in corsivo in fondo al `back`.

#### Il mazzo 15 e il sangue

**Il `15 - Il sangue` va da inizio pagina 177 a metà di pagina 198.** Entrambi i
confini sono stati renderizzati e guardati: pagina 177 si apre con
l'intestazione di lezione nuova e il titolo `IL SANGUE`, e pagina 198 chiude con
la linfocitopoiesi, **sopra** il titolo `SISTEMA LINFATICO`. La figura
`teoria_p198_1206` (granulocitopoiesi) è del 15; `teoria_p198_1207` (la tavola
del corpo con linfonodi e organi linfatici) è del 16 e ha già la sua carta.

Il capitolo copre le sezioni da `080` a `084`, circa 9.800 parole, ed è **diviso
in cinque file**. È la prima volta che due sezioni vanno spezzate **al loro
interno**: la `080` vale 3.566 parole e la `081` 4.155, cioè ciascuna più di un
intero file del 17.

| File | Pagine | Contenuto |
|---|---|---|
| `15a-sangue-e-plasma.jsonl` | 177-180 | generalità, funzioni, striscio e colorazione di Wright, ripasso dei circuiti (non trattato), analisi del sangue, composizione, plasma e sue proteine, complemento |
| `15b-eritrociti-e-gruppi-sanguigni.jsonl` | 180-184 | globulo rosso, membrana e citoscheletro di spettrina, sistema AB0, fattore Rh, emoglobina |
| `15c-leucociti.jsonl` | 184-189 | formula leucocitaria, diapedesi, neutrofili, eosinofili, basofili, monociti e sistema dei fagociti mononucleati, linfociti |
| `15d-piastrine-ed-emostasi.jsonl` | 189-193 | piastrine, megacariociti, le quattro fasi dell'emostasi, cascata coagulativa, via intrinseca e via comune |
| `15e-emopoiesi-e-midollo-osseo.jsonl` | 193-198 | sedi dell'emopoiesi, midollo rosso e giallo, staminali emopoietiche, citochine e ormoni, eritropoiesi, trombopoiesi, monocitopoiesi e granulocitopoiesi (non trattate), linfocitopoiesi |

Come per `06a`/`06b`, `08a`-`08c`, `11a`-`11c` e `17a`-`17d`, tutti e cinque i
file condividono lo stesso mazzo `Istologia::Teoria::15 - Il sangue`.

**Come sono stati decisi i tagli.** I due dentro le sezioni seguono un confine
di contenuto:

- dentro la `080`, fra le **generalità** (plasma, complemento) e gli
  **eritrociti**: il primo blocco parla della matrice, il secondo dei corpuscoli;
- dentro la `081`, **non** fra granulociti e agranulociti e **non** al cambio di
  lezione di pagina 192, ma alla fine dei **linfociti**, cioè dove finiscono i
  leucociti veri e propri e cominciano le piastrine.

Il taglio a pagina 192 era il candidato più ovvio, ed è stato **scartato di
proposito**: la nuova lezione si apre con un `[Nota del supervisore]` che
riporta le **fasi dell'emostasi** dalla stesura dell'altro anno «che chiarisce
meglio l'ultimo argomento della lezione precedente». L'emostasi sta quindi **a
cavallo del cambio di lezione** (pagine 190-191 e poi 192), e tagliare lì
avrebbe messo le due passate in due file diversi, con il rischio di due
parafrasi della stessa carta: il validatore blocca solo le domande **identiche**.
È lo stesso motivo per cui `17a` arriva fino alla sezione `094`.

**Le due passate sull'emostasi sono state fuse**, con il metodo del mazzo 11:
una sola carta per fatto, costruita sulla versione più completa, e `source` con
**entrambe le pagine** (`5th gen p. 191 e p. 192`). Non è però il caso del 17:
qui la seconda passata non ricomincia il capitolo da capo, ma **riprende un solo
argomento**, e aggiunge le quattro fasi numerate, il nome *trombo bianco*, i
tempi e la definizione di **siero**. Le altre due note del supervisore (via
classica e via comune, pagine 192-193) **aggiungono soltanto**, e sono state
cardate normalmente.

**I quattro blocchi di integrazione sono tutti additivi**, come nel 16 e a
differenza del 17: la composizione del plasma (p. 179), il pattern di
donazione-ricezione AB0 (pp. 182-183), il sistema dei fagociti mononucleati
(p. 188) e le citochine e gli ormoni dell'emopoiesi (pp. 195-196) dicono cose
che il testo principale non dice. Nessuno di loro ripete, quindi non c'è stato
niente da fondere.

**Il primo `[N.d.S.]` di pagina 177 è un caso nuovo: lo sbobinatore corregge la
docente.** La tecnica descritta a lezione come "colorazione di Giemsa" è in
realtà la **colorazione di Wright**, ed entrambe derivano da Romanowsky. Le
carte (`teoria-colorazioni-089` e `090`) sono scritte sulla **versione corretta**
e la nota è riportata in corsivo, ma **senza `da-verificare`**: la dispensa non
si contraddice, si è già corretta da sola. Il secondo `[N.d.S.]`, a pagina 180,
segnala la **via delle lectine** del complemento, non nominata a lezione: è
citata nella carta `teoria-sangue-029`, dove per giunta la figura della stessa
pagina la disegna.

**Le 29 figure delle pagine 177-198 sono state usate tutte.** Il controllo del
clip path del punto 6 è stato eseguito su quelle pagine e ha segnalato **due
figure sotto soglia su 29**, entrambe utilizzabili e usate: `teoria_p186_1165`
(neutrofilo al ME, corr 0,72) e `teoria_p187_1168` (basofilo al ME, corr 0,73).
In tutti e due i casi il file estratto **è più completo della pagina**, perché
include il pannello di testo con la legenda dei colori che la pagina taglia via;
è lo stesso caso di `teoria_p141_987` nel 13. **Nessuna finestra di browser**,
al contrario dell'`08` e del 17.

**Otto figure su 29 stanno sul fronte, ed è la proporzione più alta di tutta la
Teoria** (nel 17 erano cinque su 26, nel 16 due su otto). Il motivo è che il
sangue si studia sugli **strisci**, e uno striscio senza etichette è esattamente
il materiale da fronte: lo striscio colorato di Wright (`teoria_p177_1134`),
quello della porzione corpuscolata (`teoria_p180_1143`), gli eritrociti al SEM
(`teoria_p181_1146`), l'eosinofilo con il **marcatore muto `D`**
(`teoria_p186_1163`), il monocita al ME (`teoria_p187_1169`), la piastrina
indicata da una **freccia muta** (`teoria_p189_1174`), i due linfociti
(`teoria_p189_1175`) e il confronto fra midollo rosso e midollo giallo
(`teoria_p194_1190`). Tutto il resto sono schemi e tavole con i nomi stampati
sopra.

**Otto delle 29 figure esistono solo perché la soglia di `is_artifact` è stata
abbassata** all'inizio di questo capitolo (vedi punto 6): `teoria_p177_1134`,
`p180_1143`, `p182_1150`, `p182_1151`, `p186_1163`, `p189_1174`, `p189_1175` e
`p197_1202`. Senza quella modifica il capitolo avrebbe perso lo **schema
dell'eritropoiesi**, il citoscheletro dell'eritrocita, gli antigeni AB0 e
**cinque delle otto figure finite sul fronte**.

**Dieci segnalazioni su 173 carte** (5,8%), cioè poco più del tasso del 17
(4,9%) e circa i due terzi di quello del 16 (9,1%). Quattro nascono da **contraddizioni interne alla dispensa**: le NK
elencate fra i sottotipi dei linfociti T due righe dopo essere state distinte da
loro (`107`), il fattore IX dato per componente della via comune che il
paragrafo successivo fa cominciare dal fattore X (`132`), la sigla CFU-M usata
per il progenitore mieloide dopo essere stata usata per i monociti sette pagine
prima (`144`), e l'esito dell'incompatibilità Rh dato per fatale "nel 100% dei
casi" subito dopo averlo definito un "rischio molto elevato" (`060`). Le altre
sei sono errori verso la nozione classica, fra cui un altro **scambio di unità**
(`044`, i 5,4 milioni di eritrociti per **millilitro** invece che per microlitro)
e un'**inversione di funzione** (`091`, gli eosinofili che rilasciano istamina
invece di inattivarla).

**L'aggancio con `lab-linfoide-015` e `teoria-linfoide-016` non si chiude qui**,
ma il capitolo dà un indizio nella stessa direzione. Le due segnalazioni
identificano le **plasmacellule con i linfociti B maturi**; il 15 non lo dice
mai, e anzi tratta le due cose come **distinte**: gli anticorpi sono prodotti
dalle **plasmacellule** (p. 179, `teoria-sangue-027`), mentre il **linfocita B
maturo** è quello che lascia il midollo e va incontro all'**istruzione
antigenica** negli organi linfoidi secondari (p. 198, `teoria-sangue-168`), cioè
uno stadio che **precede** l'incontro con l'antigene. Le due segnalazioni
restano aperte, ma nessuna carta del 15 le conferma.

**Il Laboratorio aveva già coperto il sangue** con `lab-sangue-001`-`018` (file
`06c` e `06d`), e le due fonti **non si contraddicono**: il Laboratorio guarda
lo striscio e il riconoscimento, la Teoria i meccanismi. L'unico contatto diretto
è `teoria-epiteli-198` del capitolo 08, che chiede *perché* gli eritrociti hanno
forma biconcava; qui `teoria-sangue-042` chiede invece *che cosa* li rende
deformabili, e risponde con il citoscheletro di spettrina.

#### Il mazzo 16 e il sistema linfatico

**Il `16 - Sistema linfatico` va da metà di pagina 198 a metà di pagina 205.**
Entrambi i confini sono stati renderizzati e guardati, e **entrambi cadono a
metà pagina**: è l'unico capitolo della Teoria fatto così.

A **pagina 198**, sopra il titolo `SISTEMA LINFATICO`, ci sono ancora la
granulocitopoiesi e la linfocitopoiesi, che sono del **`15 - Il sangue`**, non
ancora scritto. La figura `teoria_p198_1206` (schema della granulocitopoiesi)
appartiene quindi al 15 e **non è stata presa**; solo `teoria_p198_1207`, la
tavola del corpo con linfonodi, vasi linfatici e organi linfatici primari, è
del 16.

A **pagina 205** il capitolo si chiude con la riga
`[Fine integrazione slides 2024-2025]` che termina la milza, e subito sotto
comincia il titolo `TESSUTO MUSCOLARE`. Pagina 205 **non ha figure**, quindi al
confine di valle non c'è niente da contendersi. Le pagine 205-207 sono del mazzo
17, benché le sezioni `090` e `091` portino `chapter: 'SISTEMA LINFATICO'`: è il
caso descritto qui sotto, in cui il campo `chapter` mente e i titoli delle
sezioni sono invece corretti.

Il capitolo copre le sezioni da `085` a `089`, circa 3.000 parole, e **sta in un
file solo**: `16-sistema-linfatico.jsonl`, 77 note.

**Nessuna delle 9 figure delle pagine 198-205 è sotto soglia.** Il controllo del
clip path del punto 6 è stato eseguito su quelle pagine e ha dato `corr=1.00` su
tutte e nove, cioè il file estratto coincide esattamente con ciò che la pagina
mostra. È il primo capitolo in cui il controllo non segnala niente. Delle nove,
otto sono del 16 e **sono state usate tutte**; la nona è quella della
granulocitopoiesi, che è del 15.

Due figure stanno sul **fronte**, e sono le sole che pongano una domanda senza
contenerne la risposta:

- `teoria_p204_1226`, la micrografia con le sigle mute `VEA` e `VAE` sulle venule
  ad alto endotelio. È il caso classico del marcatore muto, come le quattro del
  capitolo 13.
- `teoria_p203_1222`, il timo fetale in ematossilina-eosina. È l'unico caso finora
  di una figura **usata su due carte con lati diversi**: la tavola porta stampate
  `cortex`, `medulla`, `capsule` e `connective tissue trabeculae`, quindi sta sul
  **retro** della carta che chiede come si distinguono corteccia e midollare
  (`teoria-linfoide-057`); ma il riquadro in alto a destra, il corpuscolo di
  Hassall, **non ha etichette**, e su quello si può costruire una domanda di
  riconoscimento con la figura sul **fronte** (`teoria-linfoide-059`). Le
  etichette presenti danno il contesto (è un timo) senza dare la risposta.

Tutto il resto sono schemi, tavole anatomiche e figure di libro con la
didascalia stampata sopra, cioè materiale da retro.

**Le tre integrazioni.** La dispensa segnala esplicitamente il materiale preso da
altre annate: `[integrazione sbobina 2022-2023]` per la suddivisione dei linfociti
in T e B (pagina 199), `[integrazione sbobina 2023-2024]` per il riconoscimento
dei vasi linfatici in ematossilina-eosina (pagina 201) e per l'apoptosi dei
linfociti (pagina 202), `[integrazione slides 2024-2025]` per le zone del centro
germinativo e per tutta la milza (pagine 204-205). Non è il caso della doppia
sbobinatura del mazzo 11: qui le integrazioni **aggiungono** materiale invece di
ripetere, quindi non c'è stato niente da fondere. Le carte lo dicono in corsivo in
fondo al `back`, così Pietro sa quali parti non vengono dalla lezione dell'anno.

**Sette segnalazioni su 77 carte**, che è il livello del capitolo 13. Quattro
nascono da **contraddizioni interne alla dispensa**: le MHC collocate sul
patogeno e poi descritte come presentanti (`014`), l'essudato usato prima per il
drenaggio fisiologico e poi definito come materiale dell'infiammazione (`043`),
i vasi afferenti fatti arrivare alla midollare mentre lo schema della stessa
pagina disegna il seno sottocapsulare (`067`), le venule ad alto endotelio messe
nella midollare mentre la paracorticale è elencata ma **mai descritta** (`068`).

#### Il mazzo 17 e il tessuto muscolare

**Il `17 - Tessuto muscolare` va da metà di pagina 205 a fine pagina 226.** La
riga della tabella dice 205-227, ma **pagina 227 è stata renderizzata e guardata
ed è interamente del mazzo 18**: si apre con l'intestazione di una lezione nuova
(22-05-2025, sbobinatori Bergamin e Maccarini) e subito sotto con il titolo
`IL TESSUTO NERVOSO`. Le **due figure di pagina 227** (`teoria_p227_1335`, la
tavola del tessuto nervoso, e `teoria_p227_1336`, lo schema SNC/SNP) appartengono
quindi al 18 e **non vanno riprese**, benché `images_for_section` le assegni alla
sezione `099`. È lo stesso caso delle pagine 111 e 149.

Il confine di monte, a metà di pagina 205, era già stato verificato scrivendo il
mazzo 16 e non è stato toccato: sotto la riga `[Fine integrazione slides
2024-2025]` che chiude la milza comincia il titolo `TESSUTO MUSCOLARE`, e pagina
205 non ha figure. Il capitolo copre le sezioni `090`-`091` e `093`-`099`; la
`092` è vuota perché il segmentatore riconosce a pagina 208 un secondo titolo
`TESSUTO MUSCOLARE STRIATO SCHELETRICO` identico a quello della `091`.

**Le pagine 205-207 e 208-210 sono due stesure della stessa introduzione.** È il
fatto che decide tutto il resto, e il piano precedente non lo prevedeva. Le
pagine 205-207 appartengono alla lezione del **16-05-2025** (la stessa del
linfatico: non portano intestazione propria, e l'ultima prima di loro è a pagina
192), mentre pagina 208 apre una **lezione nuova**, quella del **20-05-2025**
sbobinata da Moussaoui e Guiducci, che **ricomincia da capo**: fibra muscolare
come sincizio cilindrico multinucleato, fusione dei mioblasti, nuclei periferici,
endomisio-perimisio-epimisio, vasi e nervi, tendini. È il caso delle pagine 93-99
del mazzo 11, non quello delle integrazioni del 16.

**Sono state fuse, non scritte due volte**, con lo stesso metodo del mazzo 11:
una sola carta per fatto, costruita sulla versione più completa (quasi sempre la
seconda, che aggiunge sarcolemma, sarcoplasma, mioglobina, aponeurosi e ventre
muscolare), e `source` con **entrambe le pagine** (`5th gen p. 206 e p. 208`)
quando il fatto sta in tutte e due. Lo stesso vale per la **distrofia di
Duchenne**, che compare a pagina 207 dal lato delle cellule satellite e a pagina
212 dal lato della distrofina come proteina della linea Z: una sola coppia di
carte, `teoria-muscolare-021` e `022`, con entrambe le pagine nel `source`.

**Anche due figure sono doppie**, come lo schema del feedback nel mazzo 11:
`teoria_p206_1231` e `teoria_p208_1237` sono lo stesso schema dell'organizzazione
generale del muscolo, `teoria_p206_1232` e `teoria_p209_1240` la stessa
microfotografia. In entrambi i casi è stata usata **solo la versione della
seconda stesura**, che è più grande e meno rifilata.

**Diviso in quattro file.** I tagli seguono i confini di sezione, ma il primo è
deciso dalla fusione: `17a` deve contenere **tutte e due** le stesure, altrimenti
il validatore, che blocca solo le domande identiche, lascerebbe passare due
parafrasi nello stesso mazzo. Per questo `17a` arriva fino alla `094` e non si
ferma alla `091` come la sola conta delle pagine suggerirebbe.

| File | Sezioni | Pagine | Contenuto |
|---|---|---|---|
| `17a-generalita-e-fibra-muscolare.jsonl` | `090`-`094` | 205-212 | i tre tipi di tessuto muscolare, fibra muscolare e involucri connettivali, cellule satellite e distrofie, struttura della fibra, actina e miosina, sarcomero e bande (**è qui che sta la doppia stesura**) |
| `17b-contrazione-e-tipi-di-fibre.jsonl` | `095`-`097` | 212-219 | troponina e tropomiosina, unità motoria, giunzione neuromuscolare, scivolamento dei filamenti, triade, accoppiamento eccitazione-contrazione, tipi di fibre |
| `17c-tessuto-muscolare-cardiaco.jsonl` | `098` | 219-222 | parete cardiaca, cardiomiociti, dischi intercalari, diadi, i tre citotipi, sistema di conduzione, ECG |
| `17d-tessuto-muscolare-liscio.jsonl` | `099` | 223-226 | miociti lisci, localizzazioni, caveole, corpi densi, calmodulina e fosforilazione della miosina, schema riassuntivo di riconoscimento |

Il confine `094`/`095` è anche un confine di contenuto: la `094` chiude la
**struttura** del sarcomero (bande, proteine accessorie), la `095` apre le
proteine **regolatrici** che portano alla contrazione. Come per `06a`/`06b`,
`08a`/`08b`/`08c` e `11a`/`11b`/`11c`, tutti e quattro i file condividono lo
stesso mazzo `Istologia::Teoria::17 - Tessuto muscolare`.

**Le cinque integrazioni dalla sbobina 2023-2024 sono un caso misto**, e questa è
la seconda cosa che il piano precedente non prevedeva. Tre **aggiungono**
materiale, come nel 16, e sono state cardate normalmente citando l'integrazione
in corsivo in fondo al `back`: le sezioni trasversali delle bande al ME (p. 212),
l'origine dei nomi dei recettori diidropiridinici e rianodinici (p. 216) e le
localizzazioni del muscolo liscio (p. 223). Due invece **ripetono** ciò che il
testo principale ha appena detto, e da quelle è stata presa **solo la parte che
aggiunge**, come fra `13a` e `13b`: l'integrazione di pagina 220-221 rispiega la
diade appena descritta e aggiunge i **tre citotipi** del miocardio;
l'integrazione di pagine 225-226 rispiega le **caveole** già trattate a pagina
224 e aggiunge l'**assenza della troponina** e il controllo ormonale via IP3.

**I due `[N.d.S.]` non sono equivalenti.** Quello di pagina 217, sui tre video
riassuntivi visionati a lezione, non produce carte, come i link ai video di
pagina 226. Quello di pagina 226 invece annuncia uno **schema riassuntivo utile
per il riconoscimento dei vetrini** che è materiale d'esame vero: sta nella
figura `teoria_p226_1327`, che è una finestra di browser e come **immagine** è
scartata, ma il cui contenuto è perfettamente leggibile ed è stato trascritto in
tre carte, `teoria-muscolare-138`-`140`, una per tipo di tessuto, ciascuna con i
criteri in sezione longitudinale e trasversale. **Non cercarlo nel testo
estratto: lì l'N.d.S. è una riga sola.**

**Il controllo del clip path del punto 6 è stato eseguito sulle pagine 205-227 e
ha segnalato undici figure su 39 sotto soglia.** È l'esito peggiore dopo l'`08`,
e per la stessa ragione: **nove sono finestre di browser** (`teoria_p222_1289`,
`1291`, `1293`; `teoria_p223_1300`; `teoria_p224_1307`, `1309`;
`teoria_p226_1323`, `1325`, `1327`), tutte screenshot di Safari con barra degli
indirizzi e schede, di cui la pagina mostra solo il riquadro della slide. Sono
state **scartate**, come le dieci dell'`08`. Si perdono i tre vetrini di cuore
(Em-Eo 40x, Em-Eo 63x con i dischi intercalari, Azan-Mallory con le fibre di
Purkinje cerchiate) e i due di muscolo liscio (tuba uterina, intestino): il
**testo** che li descrive è stato cardato lo stesso, ma **senza figura**, quindi
quelle sono carte di riconoscimento senza vetrino.

Le altre due sotto soglia sono invece **integre e sono state usate**, ed è il
caso solito della figura più completa della pagina: `teoria_p215_1261` (la
tavola della giunzione neuromuscolare, corr 0,19) include la didascalia del libro
che la pagina taglia via, e `teoria_p219_1277` (schema della parete del cuore,
corr 0,77) è al limite della soglia con il bordo rifilato.

**Delle 37 figure delle pagine 205-226 ne sono state usate 26.** Le undici
scartate sono le **nove finestre di browser** più i **due doppioni di pagina 206**
della prima stesura.

**Cinque figure su 26 stanno sul fronte**, ed è la proporzione attesa per un
capitolo fatto quasi tutto di schemi con i nomi stampati sopra. Due sono il caso
del marcatore muto:

- `teoria_p209_1240`, la microfotografia di muscolo scheletrico: le etichette
  presenti (`epimisio`, `fascicolo`, `nervo`, `fibra`) danno il contesto senza
  dare la risposta, che è da che cosa derivano le striature del riquadro *b*. È
  il caso di `teoria_p203_1222` del mazzo 16.
- `teoria_p212_1250`, la micrografia al ME del sarcomero, con le sigle mute `Z`,
  `I`, `A`, `H`, `M`: la figura marca la banda H ma non dice che cosa contenga.

Le altre tre sono **senza alcuna etichetta**: `teoria_p214_1257` (il ME della
giunzione neuromuscolare), `teoria_p219_1278` (il miocardio con le **frecce
mute** sui dischi intercalari) e `teoria_p223_1298` (il muscolo liscio in
sezione longitudinale e trasversale sullo stesso campo).

Tutto il resto sono schemi, tavole e figure di libro con la didascalia stampata
sopra, cioè materiale da retro.

**Sette segnalazioni su 142 carte**, che è la metà del tasso del 16 e del 13,
come è ragionevole per un capitolo di meccanismi molecolari dove la dispensa ha
poco spazio per contraddirsi. Due nascono da **contraddizioni interne**: le fibre
che percorrono o no l'intera lunghezza del muscolo (`005`, ed è proprio il punto
in cui le due stesure divergono, con lo stesso quadricipite come esempio) e i
filamenti intermedi del muscolo liscio dati per equivalenti di troponina e
tropomiosina due pagine prima che la dispensa dichiari assente la troponina
(`127`). Le altre cinque sono errori verso la nozione classica, fra cui uno
**scambio di unità di misura** (`069`, tubulo T e cisterne "separate da circa 10
micron") e un'**inversione di effetto** (`134`, l'ossitocina che "favorisce il
rilassamento" dell'utero durante il parto).

**L'aggancio con `lab-muscolare-016` si chiude qui, e la teoria dà ragione al
sospetto.** Il Laboratorio negava che il miocardio fosse un sincizio funzionale e
attribuiva l'espressione al muscolo scheletrico. La teoria dice il contrario da
entrambi i lati: le fibre **scheletriche** sono "sincizi cilindrici
multinucleati" perché **derivano dalla fusione dei mioblasti** (pagine 206 e 208,
`teoria-muscolare-011`), cioè un sincizio **strutturale**; mentre nel
**miocardio** i cardiomiociti restano cellule distinte, uni- o binucleate, e sono
le **giunzioni comunicanti dei dischi intercalari** a permettere la
"depolarizzazione simultanea" (pagina 220, `teoria-muscolare-099` e `112`), cioè
esattamente il sincizio **funzionale**. La teoria quindi **corregge il
Laboratorio**, e non è stata aperta una segnalazione nuova: quella sul
Laboratorio resta e ora ha una risposta, come per `lab-endocrino-014`.

#### Il mazzo 18 e il tessuto nervoso

**Il `18 - Il tessuto nervoso` va da inizio pagina 227 a fine pagina 256**, cioè
alla **fine del PDF**. Entrambi i confini sono verificati:

- **pagina 227** era già stata renderizzata scrivendo il 17 ed è interamente
  sua: si apre con l'intestazione della lezione del 22-05-2025 (sbobinatori
  Bergamin e Maccarini) e subito sotto con il titolo `IL TESSUTO NERVOSO`. Le due
  figure `teoria_p227_1335` e `teoria_p227_1336` sono sue, benché
  `images_for_section` le assegni alla sezione `099`;
- **pagina 256** chiude davvero il capitolo, e il capitolo chiude davvero il
  PDF: la pagina finisce con una `Divagazione del docente` sui trial clinici
  della riparazione del midollo spinale, e sotto non c'è altro. **Non ha
  figure.** Il capitolo non finisce prima: le pagine 254-256 sono la
  rigenerazione neurale, che è materia sua a tutti gli effetti.

Il capitolo copre le sezioni da `100` a `110`, **11.650 parole**, ed è il **più
lungo della Teoria** per numero di pagine (30) benché non per parole: il 14 ne
ha 12.700 in 28 pagine. È **diviso in sei file**, come il 14.

| File | Sezioni | Pagine | Contenuto |
|---|---|---|---|
| `18a-generalita-e-sistema-nervoso.jsonl` | `100`-`103` | 227-231 | generalità del tessuto e della sua matrice, divisione anatomica del sistema nervoso, neuroni e circuiti, connettoma e Brainbow, colorazioni elettive (ematossilina-eosina, Golgi, Nissl), Golgi contro Cajal, encefalo, midollo spinale |
| `18b-sistema-nervoso-periferico.jsonl` | `104`-`105` (1ª parte) | 231-234 | gangli e nervi, classificazione ed elenco dei nervi cranici, vie afferenti ed efferenti, arco riflesso, suddivisione del SNP, simpatico e parasimpatico, sistema nervoso enterico |
| `18c-il-neurone.jsonl` | `105` (2ª parte) | 234-239 | soma, assone e dendriti, le quattro classificazioni dei neuroni, corpi di Nissl e pericarion, citoscheletro e spine dendritiche, trasporto assonico, NGF, monticolo assonico e potenziale d'azione |
| `18d-sinapsi-e-neurotrasmettitori.jsonl` | `105` (3ª parte) | 239-246 | sinapsi chimiche ed elettriche, neurexine e neuroligine, tipi e struttura, neurotrasmettitori e loro rimozione, sinapsi eccitatorie e inibitorie, antidepressivi (**è qui che sta la doppia stesura**) |
| `18e-fibre-nervose-e-neuroglia.jsonl` | `106`-`107` | 246-251 | fibre mieliniche e amieliniche, fascio di Remak, mielinizzazione e nodi di Ranvier, i tre involucri del nervo, gangli, cellule satelliti, microglia, astrociti, barriera ematoencefalica, cellule ependimali e liquor |
| `18f-staminali-neurali-e-rigenerazione.jsonl` | `108`-`110` | 251-256 | cellule staminali neurali, neurogenesi adulta, glia radiale, *birth-dating* con BrdU e carbonio-14, rigenerazione nel SNP, limiti della rigenerazione nel SNC |

Come per `06a`/`06b`, `08a`-`08c`, `11a`-`11c`, `14a`-`14f`, `15a`-`15e` e
`17a`-`17d`, tutti e sei i file condividono lo stesso mazzo
`Istologia::Teoria::18 - Il tessuto nervoso`.

**Come sono stati decisi i tagli, e perché il cambio di lezione è stato di nuovo
scartato.** Il capitolo ha **un solo cambio di lezione al suo interno**, a
**pagina 244**, dove comincia la lezione del **23-05-2025** (sbobinatori Bogo,
Jona e Zattara) con la riga `[Continuazione dell'argomento della lezione
precedente: TESSUTO NERVOSO]`. Era il taglio più ovvio, ed è **sbagliato**, per
la terza volta di fila dopo il 14 e il 15:

- le pagine **242-243** chiudono la prima lezione con i **neurotrasmettitori**,
  i criteri per definirne uno, la classificazione delle sinapsi in eccitatorie e
  inibitorie e gli antidepressivi;
- le pagine **245-246** sono la **seconda stesura degli stessi argomenti**:
  modalità d'azione dei neurotrasmettitori, sinapsi eccitatorie e inibitorie,
  rimozione del neurotrasmettitore, serotonina e depressione.

Tagliare a pagina 244 avrebbe messo le due passate in **file diversi**, con il
rischio delle due parafrasi che il validatore non intercetta. `18d` le contiene
quindi **entrambe**, e va da pagina 239 a pagina 246.

**Questa doppia stesura ha però una particolarità che le altre non avevano: la
seconda passata è marcata `non-trattato`.** Le pagine 245-246 stanno per intero
dentro un riquadro `Argomento non trattato nell'anno 2024/2025`, mentre le
pagine 242-243 sono in tondo. La fusione è stata quindi più facile che nel mazzo
11 o nel 17: **le carte sono state costruite sulla prima passata**, quella
trattata, e dalla seconda è stato preso **solo ciò che aggiunge**, con il tag
`non-trattato`. Sono cinque carte, `teoria-nervoso-098`-`102`:

- il nome **neuromodulazione** per la trasmissione lenta;
- i nomi **EPSP** e **IPSP** dei due potenziali postsinaptici, che la prima
  passata descrive senza nominare;
- l'**acetilcolinesterasi** e i suoi prodotti (colina e acido acetico);
- la **ricaptazione da parte delle cellule della glia**, che la prima passata non
  nomina (a pagina 242 la ricaptazione è del solo neurone presinaptico);
- il **GABA non sempre inibitorio** nello sviluppo embrionale.

Gli altri due tagli dentro la `105`, che da sola vale **4.719 parole** cioè il
40% del capitolo, seguono **confini di contenuto netti**:

- fra `18b` e `18c`, a **pagina 234**, al titolo `Neurone`: sopra c'è
  l'**organizzazione** del sistema nervoso periferico (somatico, autonomo,
  enterico), sotto comincia la **cellula**;
- fra `18c` e `18d`, a **pagina 239**, al titolo `Sinapsi`: sopra c'è il
  **neurone** con la sua struttura, il suo citoscheletro e il potenziale
  d'azione che genera, sotto comincia **come quel potenziale passa alla cellula
  successiva**.

Il primo di questi due tagli spiega anche perché `18b` è il file più corto (20
carte): la prima parte della `105` vale meno di mille parole ed è stata unita
alla `104`, con cui forma un blocco unico sul SNP.

**Le due integrazioni dalla sbobina 2023/2024 sono entrambe additive**, come nel
15 e nel 16 e a differenza del 17. Sono il **midollo spinale** (pagine 230-231:
coda equina, corna della sostanza grigia, loro variazione lungo i tratti) e la
**classificazione dei nervi cranici** (pagine 231-232, con l'elenco dei dodici
come approfondimento del docente). Nessuna delle due ripete il testo principale,
e tutte le carte lo citano in corsivo in fondo al `back`.

**Il controllo del clip path del punto 6 è stato eseguito sulle pagine 227-256 e
ha segnalato due placement su 47.** È l'esito più pulito di tutta la Teoria dopo
il 16, e **non c'è nessuna finestra di browser**, benché il piano avvisasse che
lo sbobinatore dell'`08` e del 17 poteva ricomparire: gli sbobinatori di questo
capitolo sono altri, e le loro figure sono quasi tutte scansioni di libro.
Entrambe le segnalate sono il caso solito del **file estratto più completo della
pagina**, ed entrambe sono state usate:

- `teoria_p239_1458` (corr 0,33): lo schema degli stimoli sotto e sopra soglia,
  il cui file include la **didascalia del libro** («Fig. 5.20 — Relazione tra
  l'intensità degli impulsi di corrente depolarizzante...») che la pagina taglia
  via;
- `teoria_p248_1550` (corr 0,68): la micrografia del ganglio, il cui file
  include la **colonna di etichette** (`Pericarion del neurone`, `Nucleo`,
  `Cellule satelliti`, `Tessuto connettivo`) che la pagina rifila.

**Delle 47 figure delle pagine 227-256 ne sono state usate 46.** L'unica
scartata è `teoria_p245_1516`, lo schema della giunzione neuromuscolare con
l'acetilcolina: è un **doppione** di `teoria_p246_1526`, che è lo stesso schema
alla tappa successiva, con l'acetilcolinesterasi cerchiata in rosso. Tenuta la
seconda, che è quella su cui la carta è costruita.

**Dieci figure su 46 stanno sul fronte** (22%), che è la proporzione più bassa
dopo quella del 17. Il motivo è l'opposto di quello del 14: qui il capitolo è
fatto quasi tutto di **schemi e tavole di libro con i nomi stampati sopra**, e
le poche microfotografie sono l'eccezione. Otto delle dieci sono **senza alcuna
etichetta**: il nervo sciatico in ematossilina-eosina (`p229_1351`), la coppia
colorazione argentica / Nissl (`p236_1421`), l'immunofluorescenza sui neuroni di
tipo II di Golgi (`p236_1423`), il ganglio in tricromica (`p249_1560`), la
microglia (`p249_1561`), l'astrocita in anti-GFAP (`p249_1562`), le cellule
ependimali (`p251_1582`), il cono di crescita nel tubo di Schwann (`p254_1614`) e
l'assone rimielinizzato (`p255_1622`). La decima, `p237_1435`, è il caso del
**marcatore muto**: la micrografia al ME del citoscheletro porta le sigle `m`,
`mt`, `nf`, `ser`, `ger` e `s` senza scioglierle.

**Nove segnalazioni su 164 carte** (5,5%), cioè poco sopra il tasso del 15
(5,8%) e sotto quello del 14 (6,9%). **Sei nascono da contraddizioni interne
alla dispensa**, e quattro di queste sono contraddizioni **con una figura della
stessa pagina**, che è una quota più alta del solito:

- il tessuto nervoso che «non è innervato: non sono presenti fibre nervose al
  suo interno» (`008`), che è una frase che si contraddice da sola;
- l'**ipotalamo** dato per «situato posteriormente al talamo» mentre la tavola
  della stessa pagina lo disegna **sotto** (`023`);
- il **mesencefalo** dato per struttura di collegamento fra telencefalo e tronco
  encefalico mentre la tavola della stessa pagina lo **include** nel tronco
  encefalico (`025`);
- la **via motoria** (muscolo) contrapposta alla **via efferente** (ghiandola)
  una riga prima di dire che «le vie afferenti ed efferenti possono essere sia
  somatiche sia viscerali» (`041`);
- i **neuroni piramidali** dati per «ultima porzione delle vie sensoriali»
  mentre la pagina precedente li fa origine della **via piramidale motoria**
  (`060`);
- la **microglia** elencata **due volte nello stesso elenco**, fra le gliali di
  origine neuroectodermica e come derivata dal mesoderma (`120`).

Le altre tre sono errori verso la nozione classica: l'**adrenalina** data per
neurotrasmettitore dei neuroni gangliari del simpatico invece della
noradrenalina (`048`), il **GABA eccitatorio** nello sviluppo spiegato con
l'*entrata* di cloro invece che con la sua uscita (`102`), e gli **astrociti
reattivi** che «diventano neurotrofici» formando una cicatrice che blocca la
ricrescita degli assoni (`145`).

**Tre refusi sono stati risolti senza tag**, perché non c'è dubbio di contenuto:

- a pagina 232 la dispensa scrive che l'assone del motoneurone «esce dalla parte
  del **cranio** del midollo spinale»: lo schema della stessa pagina lo chiama
  `Assone della cellula del **corno anteriore**`. È il precedente di
  Voorman/Volkmann nel 14, e le carte usano il termine giusto;
- a pagina 242 la dispensa scrive «recettori accoppiati a **dendriti**» dove a
  pagina 245 scrive correttamente «recettori legati alla **proteina G**»;
- a pagina 254 scrive «degenerazione **Welleriana**» per degenerazione
  **walleriana**, da Augustus Waller.

**Le due segnalazioni aperte sul Laboratorio si chiudono qui, e in due modi
opposti.** Vale la pena tenerle vicine, perché mostrano che una segnalazione può
chiudersi anche *senza* che la teoria dia ragione al sospetto:

- **`lab-nervoso-069` si chiude come `lab-osso-046`: la teoria corregge il
  Laboratorio.** Il Laboratorio dichiarava per il vetrino 7 la tecnica di Golgi
  e poi descriveva corpi di Nissl «visibili come zone basofile». La teoria dice,
  a pagina 229, che la colorazione di Golgi è **argentica**, a base di cromo e
  argento, che ha **bassa affinità** per il tessuto e colora **solo il 5% delle
  cellule, 1 su 20**, e che colora **di nero** il corpo cellulare e i
  prolungamenti (`teoria-colorazioni-093`); la **basofilia** con le zolle di
  sostanza tigroide è invece l'effetto del **Nissl** o del **cresil violetto**,
  che sono una colorazione diversa e che la teoria descrive separatamente a
  pagina 236 (`teoria-colorazioni-095`). Le due cose non possono stare nello
  stesso vetrino, e la segnalazione del Laboratorio ora ha una risposta;
- **`lab-nervoso-015` si chiude al contrario: la teoria dà ragione al
  Laboratorio, non alla nozione classica.** Il Laboratorio diceva che la
  sostanza tigroide si vede *solo* con colorazioni speciali e non in
  ematossilina-eosina, e la segnalazione obiettava che i corpi di Nissl sono
  fortemente basofili e in un preparato EE si vedono. La teoria, a pagina 229,
  dice che in ematossilina-eosina il tessuto nervoso è **difficile da
  visualizzare**, che si distinguono «solo delle porzioni bianche» e che si
  identificano **solo le macrostrutture** (`teoria-colorazioni-092`), e per i
  corpi di Nissl nomina esclusivamente il **cresil violetto** e il **Nissl
  staining**. Le due fonti quindi **concordano fra loro** e divergono entrambe
  dalla nozione classica: non è una contraddizione interna alla dispensa, ed è
  un caso da portare al libro. Nessuna segnalazione nuova è stata aperta, come
  per `lab-endocrino-014`, `lab-muscolare-016` e `lab-osso-046`.

**Per il resto le due fonti non si contraddicono**, ed è notevole perché il
Laboratorio aveva coperto il nervoso più estesamente di qualsiasi altro
argomento (`lab-nervoso-001`-`084`, quattro file). Il taglio è quello solito: il
Laboratorio guarda il **vetrino** (nervo in sezione, ganglio spinale, midollo
spinale, cervelletto), la Teoria i **meccanismi** (potenziale d'azione, sinapsi,
mielinizzazione, rigenerazione). Dove si toccano dicono la stessa cosa: i tre
involucri connettivali del nervo, il fascio di Remak, i nodi di Ranvier, le
cellule satelliti attorno ai pirenofori dei gangli.

**Due `[N.d.S.]` sono di tipo diverso.** Quello di **pagina 244** è l'unico
contenuto di quella pagina e riporta una **precisazione della docente** sui
neuroni pseudounipolari (il prolungamento unico si comporta tutto da assone,
con un ramo periferico e uno centrale): è materiale vero, ed è finito su
`teoria-nervoso-057`, con `source` a **entrambe le pagine** (`5th gen p. 235 e
p. 244`) perché completa la classificazione di pagina 235. Quello di **pagina
249** invece **non produce carte**: dice solo che le cellule di Schwann sono già
state descritte trattando le fibre nervose.

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

#### I mazzi 04 e 05, le cellule staminali

**Il `04 - Cellule staminali e potenziale differenziativo` va da inizio pagina
16 a metà di pagina 24; il `05 - Applicazioni terapeutiche delle cellule
staminali` da metà di pagina 24 a fine pagina 27.** Sono gli unici due capitoli
che **non stanno in fondo al PDF ma in mezzo**, fra il mazzo 03 che chiude a
fine pagina 15 e il mazzo 06 che apre a pagina 28. Sono anche gli ultimi due
scritti, e con loro il progetto si è chiuso.

Tutti e tre i confini sono stati renderizzati e guardati:

- **pagina 16** è interamente del 04: si apre con l'intestazione della lezione
  del 04-03-2025 (sbobinatori Pagliarini e Gasparini), la riga
  `[continuazione della lezione precedente sulle CELLULE STAMINALI]` e subito
  sotto il titolo `CELLULE STAMINALI E POTENZIALE DIFFERENZIATIVO`, che è uno
  dei tre titoli che il segmentatore non vede. Per questo le sezioni
  `011`-`017` portano ancora `chapter: 'Colorazioni istochimiche'`: **il campo
  `chapter` mente**, i titoli delle sezioni sono corretti;
- **pagina 24** si spezza **a metà esatta**. Sopra ci sono ancora le tre
  modalità di divisione, le nicchie e i tre tipi di segnale, che sono la fine
  della sezione `017` e quindi del 04, con **entrambe** le figure della pagina
  (`teoria_p024_97` e `teoria_p024_98`); sotto comincia il titolo
  `APPLICAZIONI TERAPEUTICHE DELLE CELLULE STAMINALI`. È il caso di pagina 198
  fra il 15 e il 16, e di pagina 205 fra il 16 e il 17;
- **pagina 28 non è contesa**: il piano avvisava che il 05 poteva sconfinarci e
  che il `06a` l'aveva già cardata, ma la pagina si apre in cima con
  l'intestazione di una **lezione nuova** (06-03-2025, sbobinatrici De Zordo e
  Delpero) e subito sotto con `TESSUTI EPITELIALI`. **È tutta del 06**, e il 05
  si ferma a fine pagina 27. Pagina 28 non ha figure: la prima della sezione
  `021` è `teoria_p029_132`.

Il 04 copre le sezioni da `011` a `017` (**3.209 parole**) e il 05 le sezioni da
`018` a `020` (**1.395 parole**). **Un file per mazzo è bastato**, come il piano
prevedeva, e i due sono stati scritti nella stessa sessione come il 09 e il 10.

Attenzione al titolo della sezione `019`, che il segmentatore restituisce come
`incontrollata.] Proliferazione in vitro di cellule somatiche cutanee`: la
prima parola è la **coda di un `[N.d.S.]`** finito dentro il titolo. Non è il
nome di niente.

**Il vero problema di questi due capitoli non era il confine: era che quasi
tutto il loro contenuto era già stato cardato altrove.** `staminali` era il tag
più trasversale del progetto — sei capitoli lo avevano già usato prima che il
suo capitolo esistesse — e il 05 racconta per esteso storie cliniche che il 06
e il 12 avevano già toccato. È la trappola di `14f`/`15e`, ma su scala molto
più grande, e il validatore **non ne vede niente**, perché i mazzi sono diversi.
Il metodo è stato quello del 14: rileggere per intero le carte esistenti prima
di scrivere una riga, e prendere solo ciò che non c'è.

**Il tondo di pagina 16 non ha prodotto una sola carta.** Dice tre cose — le
staminali somatiche mantengono l'omeostasi e la rigenerazione, la capacità
rigenerativa varia col tessuto, «adulte» è un termine impreciso — e tutte e tre
erano già `teoria-staminali-009`, `010` e `011`, scritte dal mazzo 03 su pagina
15. Non è un caso: pagina 16 **dichiara essa stessa** di continuare la lezione
precedente. L'unica carta della pagina (`041`) sta sul solo fatto che quelle
carte non hanno, cioè che il nome preferito è **«cellule staminali somatiche»**,
l'espressione usata nella letteratura in lingua inglese.

Le altre sovrapposizioni risolte, in ordine di insidiosità:

| Già coperto da | Che cosa il 04 o il 05 ha preso lo stesso |
|---|---|
| `teoria-staminali-005`-`011` (03, p. 15) | niente del tondo di p. 16; del riquadro di p. 17 solo epiblasto, aborti spontanei, donazione del cordone, cellule germinali, i due esempi di turnover |
| `teoria-staminali-025` (15e, p. 195) | il **nome** *transit amplifying cells* e il loro ciclo; il *perché* (rischio di mutazioni) è finito **dentro** la carta di definizione (`070`), non in una carta sua |
| `teoria-staminali-036` (18f, p. 253) | la sola **identificazione per ritenzione del marcatore** e l'immunoistochimica (`074`); il principio di diluizione della BrdU non è stato riscritto |
| `teoria-staminali-018`-`020` e `teoria-muscolare-021`-`022` (17a, p. 207) | il solo **perché il compartimento si esaurisce** (`069`): il muscolo scheletrico non è a elevato turnover |
| `teoria-epiteli-035` (06a, p. 31), `136` (06b, p. 43), `teoria-connettivi-074` (12b, p. 120) | dell'epidermolisi bollosa: il caso del **2017**, i **tre tipi** e le quattro sigle, gli **olocloni**, i **due metodi** di correzione genica. Non è stata riscritta né la definizione né il ruolo del collagene VII |

`teoria-epiteli-136` merita una nota: descrive già, in due righe, la terapia
genica di De Luca e Pellegrini («ricercatori italiani hanno inserito il gene
corretto nelle cellule staminali epiteliali, fatto crescere lembi di pelle in
vitro e trapiantati sul paziente»). È la stessa vicenda che il 05 racconta su
tre pagine. Chi tocca l'una deve ricordarsi dell'altra.

**Le 22 figure delle pagine 16-27 sono state controllate con il clip path del
punto 6**: 22 placement su 22 sopra soglia, con correlazione **fra 0,96 e
1,00**. Solo il 16 ha fatto meglio, con 9 su 9 a `corr=1.00`, ma su meno della
metà delle figure. Nessuna finestra di browser, come nel 18. Le quattro figure
recuperate abbassando la soglia di `is_artifact` scrivendo il 15 (`teoria_p016_59`,
`teoria_p019_77`, `teoria_p019_78`, `teoria_p021_84`) **sono tutte integre e
tutte usate**: al contrario di `teoria_p165_1091` nel 14, qui il recupero ha
davvero fruttato, e fra le quattro c'è lo schema delle tre modalità di divisione
con i loro contesti biologici, che è la figura più utile del 04.

**Delle 22 ne sono state usate 21.** L'unica scartata è `teoria_p025_104`, il
**ritratto fotografico di Howard Green**: non è materiale istologico, e una
carta di riconoscimento su un volto non è materia d'esame. È il primo scarto del
progetto per questo motivo, diverso sia dalle finestre di browser sia dai
doppioni.

**Il 04 non ha nessuna figura sul fronte**, ed è il secondo capitolo così dopo
il `06`: le sue quattordici figure sono tutte schemi e tavole con i nomi
stampati sopra, dal `Depauperamento delle stem cells` alla filiera delle
*transit amplifying cells*. Il 05 ne ha **due su sette** (29%), ed è la
proporzione più alta della Teoria dopo il 14: la **coppia di cornee prima e dopo
il trapianto** (`teoria_p026_114`, senza etichette a parte un `6 yr`) e la
**cornea prodotta in vitro** nella piastra Petri (`teoria_p027_121`, la cui
didascalia sta sulla pagina ma **non è stampata sull'immagine**).

**Quattro segnalazioni su 58 carte** (6,9%), cioè il tasso del 14. Una nel 04 e
tre nel 05. Quella del 04 nasce da una **contraddizione fra il riquadro non
trattato e il tondo della stessa pagina 17** — la totipotenza data per finita a
«circa otto cellule» dal tondo e a «circa 16 cellule» dal riquadro — ed è il
caso di `teoria-endocrino-019` nel mazzo 11: la carta tiene la versione del
testo trattato, che è anche quella classica, e cita l'altra in corsivo.

Le tre del 05 sono di natura diversa e vale la pena distinguerle, perché **due
sono contraddette da una figura della stessa dispensa**:

- `teoria-staminali-088`, i tre tipi di epidermolisi bollosa: la
  `Divagazione del docente` definisce il tipo **distrofico** come quello in cui
  «la mutazione è a livello **giunzionale**», due righe dopo aver elencato il
  tipo giunzionale come categoria a sé e due righe dopo aver attribuito la forma
  distrofica al **collagene di tipo VII**. Lo schema di pagina 26 disegna DEB al
  livello del collagene VII e JEB a quello della laminina 332, cioè su **due
  piani diversi**;
- `teoria-staminali-096`, le SCID: la dispensa attribuisce l'immunodeficienza
  alla «mancanza delle cellule che combattono le infezioni (**cellule B**)», ma
  SCID sta per immunodeficienza **combinata** grave e lo schema della stessa
  pagina 27 mostra la ricostituzione di **tutte le linee linfoidi**;
- `teoria-staminali-092`, il limbus: dato per il confine fra l'**iride** e la
  sclera. È classicamente la giunzione **corneo-sclerale**, ed è la sola lettura
  coerente con il fatto che quella nicchia rigeneri l'epitelio corneale. Qui non
  c'è figura a smentire, ma c'è la frase successiva della dispensa stessa.

**Il Laboratorio non ha mai coperto le staminali**, quindi per questi due
capitoli non c'era nessun confronto fra le due fonti da fare, e nessuna
segnalazione del Laboratorio si chiude qui. È la situazione del `07`, ed è
l'unico altro caso della Teoria.

**Due `[N.d.S.]` e tre blocchi del docente producono carte**, e nessuno è di
quelli che si possono saltare: l'`[N.d.S.]` di pagina 18 sull'uso del termine
«multipotente» (citato in corsivo dentro `057`), quello di pagina 24 sulle
staminali embrionali (due carte, `081` e `082`, sul loro vantaggio teorico e sul
doppio problema etico e tecnico), la `Divagazione del docente` di pagina 25 sui
tre tipi di epidermolisi, le `Osservazioni del docente` di pagina 26 su vettori
virali e CRISPR, e la `Divagazione` di pagina 27 su malattie rare e Telethon.

#### Il progetto è finito

Con il 04 e il 05 non resta più niente da cardare: **1872 note di Teoria e 673
di Laboratorio, 2545 in tutto**, su 362 pagine di sbobina.

Le **dieci figure recuperate in capitoli già scritti** (pagine 7, 13, 42, 53,
56, 57 ×2, 58, 125, 148) sono state guardate tutte e collocate: il bilancio, e
il ragionamento carta per carta, stanno al punto 6. In sintesi **una carta
nuova, otto figure attaccate a carte che esistevano già e due scarti**, il che
conferma che l'attesa di "due o tre carte" era giusta e semmai generosa.

Resta il **solo follow-up del clip path**, che è lavoro sugli strumenti e non
sulle carte, e che nessuno è obbligato a fare:

- il **clip path di `extract.py`**, l'unica modifica pianificata e mai fatta.
  Cambierebbe il **contenuto** di file già referenziati dalle carte consegnate a
  Pietro, quindi non è additiva come l'abbassamento della soglia: andava fatta
  prima di scrivere le carte, non dopo. Oggi che le carte ci sono tutte,
  rifarla vorrebbe dire ricontrollare le 453 immagini del pacchetto. Le
  **diciannove** finestre di browser che il ritaglio recupererebbe (dieci
  nell'`08`, nove nel 17) sono già state scartate a ragion veduta, e il loro
  **contenuto**, dove valeva qualcosa, è stato trascritto a mano: vedi lo schema
  riassuntivo dei vetrini del 17. Restano le tre slide intere di pagine 60 e 69,
  che sono già usate sul retro e che il ritaglio non migliorerebbe. **Il costo
  supera il beneficio**, ed è la raccomandazione con cui questo piano si chiude.

### Ritmo di consegna

Un capitolo per volta: scrivere le carte, `build_apkg` (che valida), commit.
Ogni capitolo committato è un incremento che Pietro può già importare. È il
ritmo con cui tutti e diciotto i mazzi della Teoria sono stati consegnati, e
resta quello giusto anche per una correzione: **si ricostruisce e si rispedisce
il pacchetto intero**, e Anki riconosce le note dal guid senza toccare lo
storico di ripetizione.

---

## 4-bis. Il mazzo `Vetrini`, capitolo per capitolo

Lavoro aperto il 2026-08-27. Le convenzioni stanno al punto 3; qui c'è **a che
punto siamo**. Ogni riga è un'iterazione auto-contenuta: ci si può fermare dopo
una qualsiasi di esse e il mazzo resta coerente.

| # | File | Capitolo / pagine | Vetrini | Carte | Stato |
|---|---|---|---|---|---|
| 1 | `vetrini-01-colorazioni.jsonl` | 01 Colorazioni, pp. 3-5 | 8 | 24 | **fatto** |
| 2 | `vetrini-02-epiteli.jsonl` | 02 Epiteli, pp. 8-12 | 13 | 42 | **fatto** |
| 3a | `vetrini-03a-esocrino.jsonl` | 03 Ghiand. esocrino, classificazione + vetrini 1-7, pp. 14-21 | 12 | 29 | **fatto** |
| 3b | `vetrini-03b-esocrino.jsonl` | 03 Ghiand. esocrino, vetrini 8-13 + quiz, pp. 21-27 | 11 | 30 | **fatto** |
| 4a | `vetrini-04a-endocrino.jsonl` | 04 Ghiand. endocrino, vetrini 1-3, pp. 28-32 | 13 | 30 | **fatto** |
| 4b | `vetrini-04b-endocrino.jsonl` | 04 Ghiand. endocrino, vetrini 4-8, pp. 33-39 | 17 | 47 | **fatto** |
| 5 | `vetrini-05-connettivi.jsonl` | 05 Connettivi, vetrini 1-5 e 7-10, pp. 44-50 | 16 | 44 | **fatto** |
| 6 | `vetrini-06-specializzati.jsonl` | 06 Conn. specializzati, vetrini 3-8, 10 e 11, pp. 63-70 | 8 | 25 | **fatto** |
| 7 | `vetrini-08-nervoso.jsonl` | 08 Nervoso/SNP, vetrini 4-7 e 9, pp. 86-91 | 5 | 16 | **fatto** |
| 8 | *(nessun file)* | 09 Embriologia, pp. 96-105 | 0 | **0** | **fatto, senza carte** |
| 9 | `vetrini-07-10-coda.jsonl` | 07 Muscolare (vetrini 1-3, pp. 82-85) + 10 Tonsilla (p. 106) | 4 | ~20 | da fare |

Le stime valgono come tetto, non come obiettivo: assumono che ogni immagine sia
un vetrino distinto, e una parte sono duplicati dello stesso campo a
ingrandimenti diversi o schemi da scartare. Le iterazioni 3 e 4 sono state
spezzate nelle due metà a e b; l'iterazione 7 **non** è stata spezzata, perché
non ci è andata nemmeno vicino: vedi qui sotto.

La riga 3 è stata sdoppiata il 2026-08-27, come il piano prevedeva. La stima di
~95 carte si è però rivelata larga di molto: il capitolo 03 è l'unico finora in
cui la sezione era **già cardata per intero** nel mazzo di capitolo, e nove
figure hanno già la loro carta con immagine sul fronte. Il totale reale delle
due metà è di **59 carte**, non 95.

La riga 4 è stata sdoppiata il 2026-08-27, come il piano prevedeva: 30 figure
utilizzabili sono troppe per una sola sessione. Anche qui la stima di ~109
carte era larga, ma per il motivo opposto a quello del capitolo 03: le 45 carte
già esistenti del capitolo 04 sono **tutte di solo testo**, nessuna figura era
già stata usata, e il taglio è quindi sceso solo per gli scarti. Il totale
reale delle due metà è di **77 carte**, ed è l'unica stima del mazzo che si sia
rivelata **stretta** invece che larga.

La riga 6 **non** è stata sdoppiata, benché il capitolo copra 21 pagine contro le
7 del capitolo 05: la stima di ~30 carte si è rivelata quasi esatta (25) perché la
sezione 019 era **già cardata per intero**, quiz compreso. Il perimetro reale è
**pagine 63-70**, non 55-76: vedi il registro del capitolo 06 qui sotto.

La riga 5 **non** è stata sdoppiata: le 44 carte stanno sotto la soglia delle
~50 e il capitolo 05 si chiude in una sola iterazione. La stima di ~48 carte era
quasi esatta, ma per compensazione: le figure utilizzabili sono state 16 e non
14, e sei figure sono state scartate. Il perimetro reale è **pagine 44-50**, non
43-55: a pagina 43 ci sono due soli schemi, le pagine 51-54 sono il quiz già
cardato e senza figure, e l'unica figura di pagina 55 è della cartilagine.

La riga 7 **non** è stata sdoppiata, ed è la stima più larga di tutto il mazzo:
~78 carte previste, **16** scritte. Il motivo è la somma di tre cose che si
vedono solo guardando le figure una per una: le pagine 78-81 non danno **niente**
(sono schemi e microfotografie annotate), le pagine 92-96 non hanno **nemmeno una
figura**, e i tre vetrini muscolari delle pagine 82-85 sono passati
all'iterazione 9. Il perimetro reale è **pagine 86-91**. È lo stesso fenomeno del
capitolo 06, portato all'estremo: la sezione era già cardata per intero, e
**undici** delle ventiquattro figure delle pagine 86-91 hanno già la loro carta
con l'immagine sul fronte.

**La riga 8 si è chiusa senza scrivere una sola carta**, ed è l'unica del mazzo:
~32 carte previste, **zero**. Il file `vetrini-09-embriologia.jsonl` **non
esiste e non va creato**. Le tredici figure delle pagine 98-105 sono state
guardate tutte, e ognuna cade per **due** ragioni indipendenti: le nove dei
modellini non sono campi al microscopio, e tutte e tredici hanno già la loro
carta con l'immagine sul fronte. È il fenomeno delle righe 6 e 7 portato al suo
limite: quando una sezione è già cardata per intero **e** le sue figure sono
tutte sul fronte, al mazzo `Vetrini` non resta niente. Vedi il registro del
capitolo 09 qui sotto.

Il perimetro è **solo il Laboratorio**. La Teoria ha 453 immagini e lo stesso
trattamento sarebbe possibile, ma è un lavoro di dimensioni analoghe e va
deciso a parte.

### Procedura di una iterazione

1. leggere la sbobina di quelle pagine con `show_section.py`;
2. elencare le immagini del capitolo con la didascalia e le carte che già le usano;
3. **guardare ogni immagine, una per una**, prima di decidere qualsiasi cosa. Le
   didascalie estratte a volte sono sbagliate (punto 5), e senza guardare non si
   sa nemmeno se la figura è un vetrino o uno schema;
4. leggere le carte che già usano quelle immagini, per non ripetersi;
5. scrivere le carte seguendo il mix fisso e la regola anti-spoiler;
6. ricostruire il pacchetto, far girare i test, rigenerare `DA_VERIFICARE.md`;
7. aggiornare questo punto e i conteggi del punto 1 e 2;
8. un commit `feat(cards)` per le carte e un `docs:` per il piano.

### Capitolo 01, quello che è stato deciso

Otto vetrini delle pagine 3-5: il colon non colorato (p.3), quattro campi del
colon in H&E (p.4) e tre campi dello striscio di sangue in Diff-Quik (p.5).

**Scartata `lab_p004_262.jpg`**: è lo schema dell'esecuzione dello striscio
sanguigno, con il titolo *Esecuzione striscio sanguigno* stampato sopra. Non è
un vetrino, e per la regola delle immagini del punto 3 una figura che contiene
la risposta non va sul fronte.

`lab_p003_226.jpg` (il microtomo) **non è entrato**: è uno strumento, non un
vetrino, e la sua carta `lab-colorazioni-019` resta dov'è.

**Una avvertenza per chi correggerà queste carte.** A queste pagine la sbobina
usa i vetrini solo per illustrare *la colorazione*, e non descrive mai la parete
del colon. Quindi:

- tutto ciò che le risposte dicono su **colorazione, preparazione e tecnica**
  viene dal testo delle pagine 2-5, alla lettera;
- ciò che dicono sulla **morfologia** (ghiandole tubulari sezionate, adipociti,
  vasi, eritrociti) è la descrizione di quello che si vede nel campo, tenuta
  apposta su termini non controversi. Nessuna carta nomina strutture che la
  sbobina non nomina: non si parla di tonache, di cripte del Lieberkühn o di
  cellule caliciformi, che il documento introduce solo più avanti.

Nessuna carta del capitolo 01 ha richiesto il tag `da-verificare`.

### Capitolo 02, quello che è stato deciso

Tredici figure delle pagine 8-12, 42 carte, `lab-epiteli-035`-`076`. Sono gli
**otto vetrini** della sezione 008 — aorta (p.8), rene in **due campi** (p.9),
trachea (p.9), ovidotto (p.10), vescica (p.10), pianta del piede (p.10),
ghiandola sudoripara (p.11), esofago (p.11) — più le **quattro schermate del
quiz Wooclap** di pagina 12, che nessuna carta del progetto usava ancora.

Qui la sbobina ha i blocchi *Vetrino N / Tessuto / Colorazione / Descrizione*,
quindi, al contrario del capitolo 01, **le risposte sulla morfologia vengono dal
documento** e non sono tenute su termini generici. Tutti e otto i vetrini sono
in Ematossilina-Eosina, quindi la colorazione è chiesta **dentro la domanda di
identificazione** (`Di che organo è questa sezione, e con quale colorazione è
preparata?`), come già faceva il capitolo 01: otto carte separate che rispondono
tutte "H&E" non avrebbero insegnato niente.

**Le nove figure delle pagine 6-8 non sono entrate, ed è la decisione che conta.**
Sono le microfotografie e gli schemi che illustrano la *classificazione* degli
epiteli, e il mazzo `02` le ha già cardate per intero:

- cinque hanno **già la loro carta di identificazione con l'immagine sul fronte**
  (`lab-epiteli-009`, `012`, `015`, `018`, `025`, tutte `Che epitelio è questo?`)
  e restano nel mazzo di capitolo, come il punto 3 prescrive;
- tutto il resto che si potrebbe chiedere su di esse — funzione, sedi,
  specializzazioni, come si riconoscono — è **già** in `lab-epiteli-010`, `011`,
  `013`, `014`, `016`, `017`, `019`, `021`-`024`, `027`. Riscriverlo qui sarebbe
  stato il doppione che il punto 3 chiede di evitare leggendo prima le carte
  esistenti.

**Scartate quattro figure**, tutte per la regola delle immagini del punto 3 (una
figura che contiene la risposta non va sul fronte):

- `lab_p006_312.jpg` e `lab_p006_314.jpg`: schemi a blocchi con il nome
  dell'epitelio **stampato sopra** (*Pseudostratificato*, *Semplice / Squamoso /
  Cubico / Cilindrico*);
- `lab_p008_405.jpg`: lo schema dell'epitelio di transizione rilassato e disteso,
  con *Transizione* stampato sopra;
- `lab_p008_403.jpg`: microfotografia dell'epitelio di transizione annotata con
  *Cellule cupoliformi*, *clavate*, *basali*. Non nomina l'epitelio, ma
  "cupoliformi" **è** il carattere che lo identifica: in caso di dubbio la figura
  va sul retro, ed è dove sta già (`lab-epiteli-028`).

`lab_p014_886.jpg` (schema esocrina/endocrina, p.14) **non appartiene a questo
capitolo**: è della sezione 009 e tocca all'iterazione 3, che comunque lo
scarterà perché ha i due nomi stampati sopra.

**Le quattro schermate di quiz hanno due carte l'una, non tre.** Il materiale è
solo la risposta che la sbobina dà, e il punto 3 dice che è meglio una carta in
meno che una inventata. Due deroghe consapevoli alla regola anti-spoiler, che
vale per il *tessuto* e qui non ha un tessuto unico da tacere:

- `lab_p012_680.jpg` ha **due marcatori** su due epiteli diversi, quindi due
  carte di identificazione, una per marcatore;
- su `lab_p012_678.jpg` le due carte si identificano a vicenda: `069` dichiara
  l'organo e chiede l'epitelio, `070` dichiara l'epitelio e chiede l'organo.

Nessuna carta del capitolo 02 ha richiesto il tag `da-verificare`: i blocchi
della sezione 008 sono espliciti e non contraddicono il testo delle pagine 6-8.

**Due cose trovate strada facendo, da non perdere** (nessuna delle due è stata
toccata: sono fuori dal perimetro di questa iterazione):

1. **Il quiz delle pagine 11-13 non è mai stato cardato.** Le domande con figura
   (4, 5, 6, 7) le ha adesso il mazzo `Vetrini`; le domande di solo testo
   (1, 2, 3, 8, 9, 10 e l'aperta 11) **non esistono da nessuna parte**. Gli altri
   capitoli hanno un file `NNx-quiz-*.jsonl` generato da `quiz_to_cards.py`; il
   capitolo 02 no. Vale una iterazione a parte.
2. **`lab-epiteli-026` ha probabilmente l'immagine sbagliata sul retro.** La
   carta è un cloze sull'epitelio **cubico** composto, ma `lab_p007_372.jpg`
   mostra un primo strato di cellule nettamente **cilindriche** sopra un secondo
   strato basale, cioè l'epitelio **cilindrico** composto — che è invece la carta
   `lab-epiteli-027`, senza immagine. Le didascalie estratte a pagina 7 sono
   sfasate di un paragrafo, il che spiega lo scambio. Da guardare prima di
   correggere: l'immagine è sul **retro**, quindi non spoilera niente, e il fix
   è spostarla da `026` a `027`.

### Capitolo 03, prima metà: quello che è stato deciso

Dodici figure delle pagine 15-21, 29 carte, `lab-esocrino-088`-`116`. Il taglio
fra le due metà segue i **vetrini** e non le pagine: la 3a arriva fino al
**Vetrino 7** compreso, la 3b riparte dal **Vetrino 8**. Entrambi stanno a
pagina 21, che quindi compare in tutte e due le righe della tabella.

**La decisione che conta è che qui la sezione era già cardata per intero.** Al
contrario del capitolo 02 — dove la sezione 008 non aveva mai prodotto una
carta — la 009 ha già 83 note fra `03-ghiandolare-esocrino.jsonl` (001-035) e
`03b-esocrino-vetrini.jsonl` (040-087), e **nove** delle 37 figure hanno già la
loro carta con immagine sul fronte. Quelle nove non sono state rifatte, per la
regola del punto 3, e restano nel mazzo di capitolo:

| Figura | Carta che la usa già |
|---|---|
| `lab_p017_1000.jpg` | `lab-esocrino-040`, parotide |
| `lab_p018_1039.jpg` | `lab-esocrino-047`, pancreas |
| `lab_p019_1070.jpg` | `lab-esocrino-052`, prostata giovane |
| `lab_p019_1072.jpg` | `lab-esocrino-056`, corpi amilacei |
| `lab_p020_1109.jpg` | `lab-esocrino-058`, mammario attivo |
| `lab_p021_1146.jpg` | `lab-esocrino-062`, papille filiformi |
| `lab_p022_1193.jpg` | `lab-esocrino-067`, papille foliate |
| `lab_p024_1252.jpg` | `lab-esocrino-078`, sottolinguale |
| `lab_p025_1298.jpg` | `lab-esocrino-084`, fondo dello stomaco |

Conseguenza da tenere a mente: la **prostata sparisce dal mazzo `Vetrini`**. È
l'unico vetrino della sezione le cui **due** figure hanno già una carta con
immagine sul fronte, quindi nessuna delle due poteva essere ripresa. Pietro si
allena comunque sul riconoscimento della prostata, ma dal mazzo `03`.

**Le quattro microfotografie delle pagine 15-16 sono la scoperta di questa
iterazione.** Non sono blocchi *Vetrino N*, sono le figure che illustrano il
paragrafo `Tipo di secrezione`, e nessuna carta del progetto le usava. Sono
però **l'unico confronto affiancato dei quattro tipi di secrezione** di tutto il
Laboratorio, ed è esattamente la domanda che l'esame pratico fa davanti a un
campo. Le loro didascalie **non stanno nel testo estratto**: sono testo del PDF
sotto la figura, e si leggono solo rendendo la pagina.

| Figura | Didascalia nel PDF | Tipo di secrezione |
|---|---|---|
| `lab_p015_936.jpg` | *Parotide, ghiandole sierose* | sierosa |
| `lab_p016_959.jpg` | *Sottolinguale, ghiandole mucipare* | mucosa |
| `lab_p016_965.jpg` | *Sottomandibolare, ghiandole miste, mucipare e sierose* | mista |
| `lab_p016_962.jpg` | *ghiandole sebacee, in prossimità di un follicolo pilifero* | lipidica |

Le didascalie sono **testo del PDF, non pixel dell'immagine**: la figura sul
fronte non contiene la risposta e la regola delle immagini è rispettata. Il
testo estratto le sposta di un paragrafo — è lo stesso sfasamento del punto 5 —
quindi l'abbinamento è stato ricavato dalle **coordinate** delle immagini nella
pagina, non dalle didascalie estratte:

```sh
./venv/bin/python -c "import pymupdf; \
  [print(i['xref'], i['bbox']) for i in \
   pymupdf.open('$DL/Istologia Laboratorio combinato.pdf')[15].get_image_info(xrefs=True)]"
```

**Queste quattro figure hanno due carte l'una, non tre**, come le schermate di
quiz del capitolo 02 e per la stessa ragione: il materiale è solo il paragrafo
che le accompagna, e il punto 3 dice che è meglio una carta in meno che una
inventata. Le loro risposte ripetono in parte `lab-esocrino-019`-`030`, che sono
però carte **di solo testo**: lì si chiede di ricordare una definizione, qui di
leggere un campo. È la differenza che giustifica l'intero mazzo `Vetrini`.

**Scartate cinque figure**, quattro per la regola delle immagini del punto 3 e
una perché è di un altro capitolo:

- `lab_p014_886.jpg` e `lab_p028_1584.jpg`: lo **stesso schema** esocrina/endocrina,
  ripetuto a pagina 14 e a pagina 28, con *ghiandola esocrina* e *ghiandola
  endocrina* stampati sopra. Il capitolo 02 aveva già previsto lo scarto del
  primo. Il secondo sta comunque a **pagina 28**, che apre la sezione 011: se
  l'iterazione 4 lo ritrova, è già stato guardato ed è già stato scartato;
- `lab_p015_932.jpg`: la tavola delle otto forme di ghiandola (*Tubulare
  semplice*, *Acinosa composta*…), con tutti i nomi stampati sopra;
- `lab_p015_934.jpg`: lo schema olocrina / merocrina / apocrina, con i tre nomi
  stampati sopra;
- `lab_p016_968.jpg`: lo schemino *Ghiandola intraepiteliale* / *Ghiandola
  esoepiteliale coriale*, con i nomi stampati sotto. È anche minuscolo, 195×127.

**Una carta ha richiesto il tag `da-verificare`, la prima del mazzo `Vetrini`.**
`lab-esocrino-108`: la sbobina dà come colorazione del Vetrino 2 «**blu di
toluene**», che non è una colorazione istologica. Il nome atteso è **blu di
toluidina**, che il progetto incontra fra i coloranti basici
(`teoria-colorazioni-006`). La carta riporta quello che dice la sbobina e
spiega nel `back` che cosa non torna, come prescrive il punto 3.

**Due errori trovati in carte già pubblicate, nessuno dei due corretto.** Sono
fuori dal perimetro di questa iterazione, valgono un lavoro a sé come
`lab-epiteli-026`, e in entrambi i casi il fix è sicuro perché il guid dipende
solo dall'id:

1. **`lab-esocrino-047` ha la risposta sbagliata.** La carta chiede che cosa
   evidenzia il cerchio tratteggiato di `lab_p018_1039.jpg` e risponde «un'isola
   di Langerhans». Il cerchio racchiude invece un **adenomero**, cioè un acino
   con le cellule polarizzate attorno a un lume centrale, e il testo della
   sbobina lo dice esplicitamente: *«Nel primo vetrino è evidenziata la sezione
   di una adenomero, in cui si notano le cellule polarizzate, raggruppate
   attorno a un lume centrale che è l'ingresso di un dotto»*. Le isole di
   Langerhans stanno nella **seconda** figura (`lab_p018_1041.jpg`), non
   cerchiate, e sono le zone più chiare. Si vede anche dalla colorazione: la
   figura cerchiata è azzurra, e la sbobina descrive le isole come «di
   colorazione più chiara» nel campo rosa.
2. **`lab-esocrino-082` ha probabilmente l'immagine sbagliata sul fronte.** La
   carta è `Che ghiandola è questa? → Ghiandola sottomandibolare`, ma usa
   `lab_p024_1258.jpg`, che è la **piccola figura in basso a sinistra** del
   Vetrino 11 (uno dei «due dotti escretori di diverse dimensioni» della
   sottolinguale): adenomeri pallidi, mucosi, con un piccolo lume al centro. La
   sottomandibolare è `lab_p024_1254.jpg`, la figura del **Vetrino 12**, dove le
   cellule sierose scure e granulose circondano quelle mucose chiare. Verificato
   sulle coordinate delle quattro immagini di pagina 24 e sulla pagina resa. Il
   fix è spostare l'immagine da `1258` a `1254`, e l'id resta `082`.

**Il quiz delle pagine 25-27 è nella stessa situazione del quiz delle pagine
11-13**: le tre domande con figura le avrà il mazzo `Vetrini` con
l'iterazione 3b, le **nove domande di solo testo** di pagina 25-26 e l'aperta
di pagina 27 non esistono da nessuna parte, e non c'è nessun file
`03c-quiz-*.jsonl`. È lo stesso buco già segnalato per il capitolo 02: i due
vanno chiusi insieme, in una iterazione a parte.

**Che cosa è passato all'iterazione 3b**, già guardato una per una:

| Pagina | Figure | Vetrino |
|---|---|---|
| 21 | `lab_p021_1151.jpg` | 8, papille foliate |
| 22 | `lab_p022_1195.jpg` | 8, ingrandimento del solco con i bottoni gustativi |
| 23 | `lab_p023_1213.jpg` | 9, papille fungiformi |
| 23 | `lab_p023_1215.jpg` | 10, scalpo, ghiandola sebacea e follicolo |
| 24 | `lab_p024_1256.jpg`, `lab_p024_1258.jpg` | 11, i due dotti escretori della sottolinguale |
| 24 | `lab_p024_1254.jpg` | 12, sottomandibolare, semilune del Giannuzzi |
| 25 | `lab_p025_1300.jpg` | 13, ghiandole gastriche ad alto ingrandimento |
| 27 | `lab_p027_1506.jpg`, `1508`, `1510` | tre schermate di quiz con marcatore |

Sul `lab_p023_1215.jpg` una avvertenza: mostra una ghiandola sebacea accanto a
un follicolo pilifero, come `lab_p016_962.jpg` che la 3a ha già usato. Sono
**due campi diversi** e le carte vanno tenute su tagli diversi: la 962 chiede il
**tipo di secrezione**, la 1215 deve chiedere l'**organo** (scalpo, cute) e la
morfologia olocrina delle cellule.

Sulle tre schermate di quiz vale il precedente del capitolo 02: **due carte
l'una, non tre**, perché il materiale è solo la risposta che la sbobina dà. Le
risposte sono, nell'ordine, *ghiandola sottomandibolare a secrezione mista*,
*pancreas* e *fondo dello stomaco*. Attenzione: le didascalie estratte per
queste tre sono **sfasate di una domanda**, e vanno rilette sulla pagina resa.

### Capitolo 03, seconda metà: quello che è stato deciso

Undici figure delle pagine 21-27, 30 carte, `lab-esocrino-117`-`146`: tre carte
per ciascuna delle otto microfotografie e due per ciascuna delle tre schermate
del quiz. Tutte sono note `basic`, con immagine sul fronte e
`tipo::riconoscimento`.

**Nessuna delle undici figure è stata scartata.** Le otto microfotografie sono
campi istologici senza etichette che contengano la risposta; le tre schermate
del quiz mostrano soltanto il marcatore `1`, mentre domanda e soluzione sono
testo esterno al ritaglio. Tutte erano quindi adatte al fronte. Le immagini
uniche del pacchetto aumentano però di **dieci**, non undici:
`lab_p024_1258.jpg` era già conteggiata perché usata, con l'abbinamento
sbagliato, da `lab-esocrino-082`.

La distribuzione delle domande segue i campi, non ripete semplicemente le carte
di solo testo già presenti:

| Figure | Carte | Taglio |
|---|---:|---|
| `lab_p021_1151.jpg`, `lab_p022_1195.jpg` | 6 | papille foliate a piccolo ingrandimento; solco, bottoni e pori gustativi ad alto ingrandimento |
| `lab_p023_1213.jpg` | 3 | papille fungiformi: identificazione, differenza dalle filiformi, rivestimento |
| `lab_p023_1215.jpg` | 3 | scalpo: organo, morfologia olocrina delle sebacee, muscolo erettore del pelo |
| `lab_p024_1256.jpg`, `lab_p024_1258.jpg` | 6 | i due dotti escretori di diverso calibro della sottolinguale e gli adenomeri mucosi circostanti |
| `lab_p024_1254.jpg` | 3 | sottomandibolare: classificazione mista, semilune del Giannuzzi, confronto sieroso/mucoso |
| `lab_p025_1300.jpg` | 3 | ghiandole gastriche propriamente dette ad alto ingrandimento |
| `lab_p027_1506.jpg`, `1508`, `1510` | 6 | due carte per quiz: sottomandibolare mista, pancreas, fondo dello stomaco |

La sovrapposizione fra le due immagini di ghiandola sebacea è stata risolta
come previsto dalla 3a: `lab_p016_962.jpg` continua a chiedere il **tipo di
secrezione**; `lab_p023_1215.jpg` chiede invece di riconoscere lo **scalpo**, la
morfologia chiara delle cellule olocrine e il muscolo erettore del pelo.

`lab_p024_1258.jpg` è stata usata correttamente come **piccolo dotto escretore
della sottolinguale**, ma `lab-esocrino-082` non è stata modificata: la sua
correzione resta il lavoro separato già annotato nella prima metà. Lo stesso
vale per `lab-esocrino-047`, `lab-epiteli-026` e per i quiz di solo testo delle
pagine 11-13 e 25-27.

Le tre risposte del quiz sono state abbinate rileggendo la **pagina 27 resa**,
non le didascalie estratte: `1506` è la sottomandibolare a secrezione mista,
`1508` il pancreas, `1510` il fondo dello stomaco. Nessuna nuova carta ha
richiesto il tag `da-verificare`: il totale resta **107**.

### Capitolo 04, prima metà: quello che è stato deciso

Tredici figure delle pagine 30-32, 30 carte, `lab-endocrino-046`-`075`: i
**vetrini 1, 2 e 3** (ipofisi, tiroide, paratiroide). Il taglio fra le due metà
segue i vetrini come nel capitolo 03, e cade dove finisce il blocco del collo:
la 4a arriva fino al **Vetrino 3** compreso, la 4b riparte dal **Vetrino 4**
(ovaio). Tutte le carte sono `basic`, con immagine sul fronte e
`tipo::riconoscimento`. Nessuna ha richiesto il tag `da-verificare`: il totale
resta **107**.

**La situazione di partenza è l'opposto di quella del capitolo 03.** Le 45
carte che il capitolo 04 aveva già (`04a` 001-015 e `04b` 020-045) sono
**tutte di solo testo**: nessuna figura delle pagine 28-39 era mai stata usata
da nessuna carta del progetto. Non c'è quindi stato niente da escludere per la
regola "le carte con immagine sul fronte restano nel loro mazzo", e nessun
vetrino sparisce dal mazzo `Vetrini` come era successo alla prostata. La
sovrapposizione con le carte di solo testo esistenti è voluta ed è la stessa
già accettata nella 3a: lì si chiede di ricordare una definizione, qui di
leggere un campo.

La distribuzione delle domande segue i campi, non le pagine:

| Figure | Carte | Taglio |
|---|---:|---|
| `lab_p030_1657.jpg` | 2 | ipofisi intera: identificazione, le due porzioni e come si distinguono |
| `lab_p030_1659.jpg` | 2 | adenoipofisi: quale porzione è, cordoni di cellule cuboidi e vascolarizzazione |
| `lab_p030_1663.jpg` | 2 | cellule acidofile: quali sono, che ormoni fanno, a che servono |
| `lab_p030_1661.jpg` | 2 | cellule basofile: quali sono, che ormoni fanno, e il limite del preparato |
| `lab_p030_1665.jpg` | 2 | cellule cromofobe e le tre categorie per affinità tintoriale |
| `lab_p031_1745.jpg` | 3 | neuroipofisi: pituiciti e fibre, ormoni ipotalamici, origine dal tubo neurale |
| `lab_p031_1747.jpg` | 2 | corpo di Herring cerchiato: che cos'è, perché sta lì |
| `lab_p031_1749.jpg` | 4 | tiroide: identificazione, colloide, tireociti, stato funzionale |
| `lab_p031_1751.jpg` | 2 | cellule C cerchiate: che cosa sono, come si individuano, calcitonina |
| `lab_p032_1800.jpg` | 3 | paratiroide e tiroide affiancate: identificazione, come si distinguono, perché stanno insieme |
| `lab_p032_1802.jpg` | 2 | cellule principali e paratormone |
| `lab_p032_1804.jpg` | 2 | cellule ossifile indicate dalle frecce, e il loro ruolo incerto |
| `lab_p032_1798.jpg` | 2 | adipociti fra i cordoni, e il loro aumento con l'età |

**Le sette figure di pagina 30-31 sono tutte dello stesso vetrino**, l'ipofisi,
ed è il caso più affollato incontrato finora nel mazzo. Le domande sono state
distribuite invece di ripeterle campo per campo: l'identificazione della
ghiandola sta solo sul campo d'insieme (`1657`), quella della *porzione* sui due
ingrandimenti (`1659` adenoipofisi, `1745` neuroipofisi), e i tre campi ad alto
ingrandimento (`1663`, `1661`, `1665`) chiedono ciascuno un tipo cellulare
diverso. Per questo cinque figure hanno **due** carte e non tre: il punto 3 dice
che è meglio una carta in meno che una inventata.

**Una carta dice esplicitamente che il vetrino non basta.** `lab-endocrino-053`
chiede se in questo preparato si riescano a separare acidofile e basofile, e
risponde **no**: la sbobina avverte che «nel vetrino la colorazione non permette
di apprezzare con precisione la differenza». È una carta di riconoscimento che
insegna un limite del riconoscimento, ed è il genere di cosa che all'esame
pratico conviene sapere prima di trovarsi davanti al campo.

**Scartate tre figure, e ne restano fuori altre tre.**

Scartate per la regola delle immagini del punto 3 (una figura che contiene la
risposta non va sul fronte):

- `lab_p028_1584.jpg`: lo **stesso schema** esocrina/endocrina già scartato due
  volte, a pagina 14 dal capitolo 02 e a pagina 28 dalla 3a, che lo aveva
  annunciato a questa iterazione. Guardato di nuovo, confermato: *ghiandola
  esocrina* e *ghiandola endocrina* sono stampati sotto le due colonne;
- `lab_p034_1867.jpg`: microfotografia del follicolo antrale **interamente
  annotata**, con *zona pellucida*, *corona radiata*, *ovocita*, *cellule della
  teca*, *cellule della granulosa* e *antro con liquor follicoli* stampati
  sopra. Contiene la risposta di tutte le domande che si potrebbero fare;
- `lab_p034_1869.jpg`: la stessa cosa in piccolo, con *cumulo ooforo* stampato
  accanto al riquadro che lo indica. Vale il precedente di `lab_p008_403.jpg`
  del capitolo 02: l'annotazione **è** il carattere che si vorrebbe chiedere.

Restano fuori invece, e non è uno scarto, le **tre schermate del quiz di pagina
42** (`lab_p042_2435.jpg`, `2437`, `2439`): hanno **già** la loro carta con
immagine sul fronte in `04d-quiz-endocrino-aperte.jsonl`
(`lab-quiz-endocrino-019`, `020`, `021`, rispettivamente zone del surrene,
neuroipofisi e paratiroidi), e per il punto 3 restano dove sono. È la stessa
situazione delle nove figure del capitolo 03, e la differenza con le schermate
di quiz delle pagine 12 e 27 — che invece nessuno aveva mai cardato — sta tutta
qui. Il quiz del capitolo 04, al contrario di quelli dei capitoli 02 e 03, è
stato cardato per intero: **non** è uno dei buchi da chiudere.

**Che cosa è passato all'iterazione 4b**, già guardato una per una e già
abbinato al vetrino giusto rendendo le pagine:

| Pagina | Figure | Vetrino |
|---|---|---|
| 33 | `lab_p033_1846.jpg` | 4, ovaio: le due regioni, corticale e midollare |
| 33 | `lab_p033_1844.jpg` | 4, ovaio: i follicoli sezionati fra stadio antrale e di Graaf |
| 33 | `lab_p033_1848.jpg` | 4, ovociti con zona pellucida e corona radiata |
| 35 | `lab_p035_1880.jpg` | 4, ovociti primari nei follicoli primordiali della corticale |
| 35 | `lab_p035_1882.jpg` | 5, corpo luteo a piccolo ingrandimento |
| 35 | `lab_p035_1884.jpg` | 5, cellule luteiniche ad alto ingrandimento |
| 36 | `lab_p036_1936.jpg` | 5, ovociti primari: secondo campo, indicazione sull'età |
| 36 | `lab_p036_1938.jpg` | 6, corpi albicanti |
| 37 | `lab_p037_1979.jpg` | 6, corpi albicanti: secondo campo |
| 37 | `lab_p037_1981.jpg` | 7, surrenale: la corticale a strati, con i marcatori 2-5 |
| 37 | `lab_p037_1983.jpg` | 7, zona glomerulare sotto la capsula |
| 38 | `lab_p038_2041.jpg` | 7, zona fascicolata |
| 38 | `lab_p038_2043.jpg` | 7, zona reticolata |
| 38 | `lab_p038_2045.jpg` | 7, midollare |
| 38 | `lab_p038_2047.jpg` | 7, cellule cromaffini ad alto ingrandimento |
| 39 | `lab_p039_2099.jpg` | 8, pancreas a piccolo ingrandimento |
| 39 | `lab_p039_2101.jpg` | 8, pancreas, acini esocrini ad alto ingrandimento |

Tre avvertenze per chi la farà, tutte ricavate dalle **pagine rese**, non dal
testo estratto:

- le figure delle pagine 35-37 sono **sfasate rispetto al vetrino**. Le prime
  immagini di pagina 35 e 37 chiudono il vetrino della pagina precedente:
  `lab_p035_1880.jpg` è ancora il Vetrino 4 e `lab_p037_1979.jpg` è ancora il
  Vetrino 6, benché il testo accanto a loro parli già del vetrino dopo. Il
  campo `source` segue il **testo del vetrino**, non la pagina della figura;
- `lab_p035_1880.jpg` e `lab_p036_1936.jpg` mostrano **lo stesso soggetto**,
  gli ovociti primari nei follicoli primordiali della corticale, a due
  ingrandimenti. Vanno tenuti su tagli diversi come è stato fatto con le due
  ghiandole sebacee della 3a e 3b: la 1880 per il riconoscimento del follicolo
  primordiale e del suo epitelio pavimentoso semplice, la 1936 per
  l'indicazione sull'**età** della paziente;
- il **Vetrino 8**, pancreas, ripete l'errore già segnalato nella 3a: la
  colorazione dichiarata è «**blu di toluene**», che non è una colorazione
  istologica, e il nome atteso è **blu di toluidina**. La carta va scritta come
  prescrive il punto 3, riportando quello che dice la sbobina, taggata
  `da-verificare` e con la spiegazione nel `back`, esattamente come
  `lab-esocrino-108`.

### Capitolo 04, seconda metà: quello che è stato deciso

Diciassette figure delle pagine 33-39, 47 carte, `lab-endocrino-076`-`122`: i
**vetrini 4, 5, 6, 7 e 8** (ovaio con follicoli di Graaf, ovaio con corpo luteo,
ovaio con corpi albicanti, ghiandola surrenale, pancreas). Con questa iterazione
il capitolo 04 è **chiuso**: le due metà valgono 77 carte, e le trenta figure
utilizzabili delle pagine 28-39 sono state usate tutte.

Tutte le carte sono `basic`, con immagine sul fronte e `tipo::riconoscimento`.
**Nessuna figura è stata scartata**: i tre scarti del capitolo li aveva già
fatti la 4a. Una sola carta porta `da-verificare`, ed è quella annunciata dalla
4a: il totale passa da 107 a **108**.

Le tre avvertenze lasciate dalla 4a sono state **tutte confermate** rendendo di
nuovo le pagine 33 e 35-39, e non ce n'erano altre.

La distribuzione delle domande segue i campi, non le pagine:

| Vetrino | Figure | Carte | Taglio |
|---|---|---:|---|
| 4, ovaio | `lab_p033_1846.jpg` | 3 | identificazione, le due regioni, l'ilo e i vasi della midollare |
| 4 | `lab_p033_1844.jpg` | 4 | stadio dei follicoli e antri, liquor follicoli, distacco del cumulo ooforo, follicoli che paiono senza ovocita |
| 4 | `lab_p033_1848.jpg` | 4 | granuli corticali, zona pellucida, granulosa/corona radiata/cumulo ooforo, teche e ormoni |
| 4 | `lab_p035_1880.jpg` | 3 | follicoli primordiali della corticale, epitelio pavimentoso semplice, migrazione in profondità |
| 5, corpo luteo | `lab_p035_1882.jpg` | 3 | identificazione, che cos'è il corpo luteo, che altro c'è nella sezione |
| 5 | `lab_p035_1884.jpg` | 3 | cellule luteiniche e progesterone, morfologia e gocce lipidiche, cellule para luteiniche |
| 5 | `lab_p036_1936.jpg` | 2 | ovociti primari, secondo campo, e l'indicazione sull'età |
| 6, corpi albicanti | `lab_p036_1938.jpg` | 3 | identificazione, come si riconosce l'ovaio senza follicoli, che cos'è il corpo albicante |
| 6 | `lab_p037_1979.jpg` | 3 | aspetto del corpo albicante, confronto con il corpo luteo, la menopausa |
| 7, surrene | `lab_p037_1981.jpg` | 2 | identificazione, e le quattro zone marcate 2-5 |
| 7 | `lab_p037_1983.jpg` | 3 | zona glomerulare e i suoi gomitoli, mineralcorticoidi, come agisce l'aldosterone |
| 7 | `lab_p038_2041.jpg` | 2 | zona fascicolata e glucocorticoidi |
| 7 | `lab_p038_2043.jpg` | 2 | zona reticolata e ormoni sessuali deboli |
| 7 | `lab_p038_2045.jpg` | 2 | midollare e catecolamine |
| 7 | `lab_p038_2047.jpg` | 2 | cellule cromaffini, e da dove viene il loro nome |
| 8, pancreas | `lab_p039_2099.jpg` | 4 | identificazione e colorazione, ghiandola mista, isole di Langerhans, i loro tipi cellulari |
| 8 | `lab_p039_2101.jpg` | 2 | acini sierosi e destinazione del secreto |

**I numeri stampati nelle figure del surrene sono di due specie diverse, e
confonderle rovina la carta.** Sulle pagine 37-38 il numero accanto al bordo
della figura è il numero della **figura** (1-6, richiamato in grassetto dal
testo: «la ghiandola surrenale (1.)», «Zona glomerulare (2.)»); i numeri
`2`, `3`, `4`, `5` stampati **dentro** `lab_p037_1981.jpg` sono invece i
**marcatori delle zone** su quel campo d'insieme, e rimandano proprio ai
cinque ingrandimenti che seguono. È il motivo per cui `lab-endocrino-105`
chiede le zone marcate 2-5 e non 1-4. I marcatori sono **soli numeri**, senza
nomi stampati: la figura sta sul fronte senza spoilerare niente. Lo stesso vale
per i marcatori `(1.)`, `(2.)`, `(3.)` e `(6.)` del Vetrino 4, che però nel
testo rimandano alle figure e non a punti del campo.

**La figura più affollata è `lab_p033_1848.jpg`, non un campo d'insieme.** È
l'unico caso del mazzo in cui l'alto ingrandimento vale più domande della
panoramica: ci stanno sopra i granuli corticali, la zona pellucida, i tre nomi
della granulosa e le due teche. Il campo d'insieme del vetrino (`1846`) ne ha
invece tre, perché la sbobina di quel campo dice poco più delle due regioni.

**Cinque figure del surrene hanno due carte e non tre**, ed è voluto: dalla
fascicolata in giù la sbobina dà per ciascuna zona **solo la posizione, l'aspetto
e il secreto**. La terza domanda sarebbe stata inventata, e vale il criterio del
punto 3. La zona glomerulare ne ha tre solo perché l'aldosterone ha un
meccanismo d'azione descritto per esteso.

**Una carta mette a confronto due vetrini diversi.** `lab-endocrino-102` chiede
come si distingue un corpo albicante dal corpo luteo del vetrino precedente. È
l'unica carta del capitolo che attraversi due vetrini, e non è una forzatura: i
Vetrini 5 e 6 sono due sezioni dello **stesso organo** che la sbobina presenta
apposta in sequenza, e all'esame pratico la differenza fra le due strutture è
esattamente quello che si deve saper leggere.

**Il pancreas era già nel mazzo `Vetrini`, e le carte nuove non lo ripetono.**
La 3a lo aveva cardato dal lato **esocrino** con `lab-esocrino-103`-`108`
(identificazione, isole come zone più chiare, confronto con la parotide, dotti
intercalari, colorazione). Il Vetrino 8 è un **preparato diverso**, a pagina 39,
e lo guarda dal lato **endocrino**: che cosa contengono le isole, in che
proporzioni, e perché i loro tipi cellulari non si distinguono. Le due domande
che potevano sovrapporsi sono state girate di conseguenza: `119` non chiede
*che cosa siano* le isole, che `lab-esocrino-103` già chiede, ma *come si
presentano* rispetto al parenchima.

**La seconda segnalazione sul «blu di toluene».** `lab-endocrino-117` riporta la
colorazione come la scrive la sbobina e spiega nel `back` che il nome atteso è
**blu di toluidina**, esattamente come `lab-esocrino-108` aveva fatto per il
vetrino di pagina 18. Sono due carte distinte su due vetrini distinti, non un
doppione: la sbobina commette lo stesso errore due volte, e Pietro trova ora
entrambe le occorrenze in `DA_VERIFICARE.md`. Il campo di pagina 39 è
effettivamente **azzurro-violetto**, quindi la colorazione *è* un blu basico e
l'errore è solo nel nome.

**La sovrapposizione con le carte di solo testo del capitolo è voluta**, come
nella 3a e nella 4a. In particolare `lab-endocrino-042`, `043`, `044` e `045`
(pagina 29) definiscono corpo luteo, corpo albicante, il loro rapporto con
l'età e le zone del surrene: lì si chiede di ricordare una definizione, qui di
leggere un campo. Nessuna delle carte nuove è stata tolta per questo.

### Capitolo 05, quello che è stato deciso

Sedici figure delle pagine 44-50, 44 carte, `lab-connettivi-042`-`085`: i
**vetrini 1, 2, 3, 4, 5, 7, 8, 9 e 10** più le **tre microfotografie di
classificazione** delle pagine 44-45. Tutte le carte sono `basic`, con immagine
sul fronte e `tipo::riconoscimento`. Il capitolo si chiude in una sola
iterazione.

**Il perimetro vero è pagine 44-50, non 43-55**, e le tre pagine che restano
fuori non sono un buco:

- **pagina 43** ha due sole figure e sono entrambe schemi con i nomi stampati
  sopra (vedi gli scarti qui sotto);
- **pagine 51-54** sono il quiz, **già cardato per intero** in
  `05c-quiz-connettivi.jsonl` (21 carte) e **senza nessuna figura**. Al
  contrario dei quiz dei capitoli 02 e 03, qui non c'è niente da chiudere;
- **pagina 55** è condivisa con il capitolo 06, ma il taglio non cade a metà
  pagina come era successo con la 21 fra la 3a e la 3b: l'unica figura della 55,
  `lab_p055_3953.jpg`, è la **trachea fetale in Azan-Mallory** della sezione
  018, cioè materiale della cartilagine. Il capitolo 05 finisce al **Vetrino
  10** di pagina 50, e l'iterazione 6 riparte da pagina 55.

**La situazione di partenza è intermedia fra quella del capitolo 03 e quella del
04.** Le 41 carte già esistenti (`05a-tessuti-connettivi.jsonl`, 001-041) sono
quasi tutte di solo testo, ma **due** hanno già l'immagine sul fronte e restano
quindi nel mazzo di capitolo, come il punto 3 prescrive:

| Figura | Carta che la usa già |
|---|---|
| `lab_p046_2866.jpg` | `lab-connettivi-020`, campo d'insieme del Vetrino 1 (connettivo lasso) |
| `lab_p049_2989.jpg` | `lab-connettivi-027`, Vetrino 6 (tessuto reticolare dell'ovaio, Bielschowsky) |

Conseguenza da tenere a mente, la stessa che era toccata alla prostata nella 3a:
il **Vetrino 6 sparisce dal mazzo `Vetrini`**, perché la sua unica figura è già
la domanda di `lab-connettivi-027`. Del Vetrino 1 resta invece molto, perché ha
tre primi piani oltre al campo d'insieme.

**Le tre microfotografie di classificazione delle pagine 44-45 sono la scoperta
di questa iterazione**, ed è lo stesso caso delle quattro figure sui tipi di
secrezione trovate dalla 3a a pagina 15-16: non sono blocchi *Vetrino N*, sono
le figure che accompagnano i paragrafi sui tipi di connettivo, e nessuna carta
del progetto le usava. Due delle tre sono **confronti affiancati** che il resto
del Laboratorio non offre da nessun'altra parte:

| Figura | Che cosa mostra |
|---|---|
| `lab_p044_2671.jpg` | tessuto connettivo embrionale, due campi |
| `lab_p045_2794.jpg` | denso **regolare** a sinistra, denso **irregolare** a destra |
| `lab_p045_2797.jpg` | adiposo **uniloculare** a sinistra, **multiloculare** a destra |

**Le strisce basse e larghe delle pagine 44-45 vanno guardate una per una, e non
sono tutte uguali.** Sette figure di quelle due pagine hanno il formato a
striscia (449x159, 442x164, 438x164, 402x152 e simili) e l'aspettativa era che
fossero schemi; guardate, si sono divise a metà. Le tre della tabella qui sopra
sono **microfotografie affiancate senza etichette** e stanno benissimo sul
fronte; le altre hanno il nome della struttura **stampato sui pixel** e sono
state scartate. Il formato non decide niente: decide solo l'occhio.

La distribuzione delle domande segue i campi, non le pagine:

| Vetrino / figura | Figure | Carte | Taglio |
|---|---|---:|---|
| classificazione, embrionale | `lab_p044_2671.jpg` | 2 | identificazione e fase della vita; come si riconosce la cellula mesenchimale |
| classificazione, denso | `lab_p045_2794.jpg` | 3 | regolare contro irregolare nei due campi, dove si trovano, composizione e fibrocita |
| classificazione, adiposo | `lab_p045_2797.jpg` | 2 | uniloculare contro multiloculare nei due campi, e quanto bruno ha un adulto |
| 1, connettivo lasso | `lab_p046_2868.jpg` | 2 | nuclei dei fibroblasti indicati dalle frecce, e che cosa sia una cellula fissa |
| 1 | `lab_p046_2869.jpg` | 2 | nucleo del macrofago, e che cosa sia una cellula migrante |
| 1 | `lab_p046_2870.jpg` | 2 | nuclei dei mastociti, e il confronto con quello del macrofago |
| 2, tendine | `lab_p047_2912.jpg` | 4 | identificazione, decorso dei fasci e resistenza alla trazione, tendinociti, il denso irregolare sovrastante |
| 3, giunzione muscolo-tendinea | `lab_p047_2914.jpg` | 3 | identificazione delle due metà del campo, fasci e file di nuclei a destra, muscolare liscio contro connettivo denso |
| 4, pianta della mano | `lab_p048_2951.jpg` | 2 | identificazione dalla cheratinizzazione, strutture da cercare per confermare |
| 4 | `lab_p048_2953.jpg` | 2 | derma papillare, e come cambia il connettivo verso il reticolare |
| 5, trachea | `lab_p048_2955.jpg` | 4 | identificazione, l'artefatto di taglio, l'epitelio della mucosa, i condroblasti dello strato condrogenico |
| 7, adiposo | `lab_p049_2991.jpg` | 3 | identificazione e unità funzionale, perché gli adipociti sono trasparenti, le sezioni alveolari |
| 7 | `lab_p049_2992.jpg` | 2 | morfologia dell'adipocita, e dove sta il nucleo |
| 8, aorta H&E | `lab_p050_3030.jpg` | 4 | identificazione, le tre tonache, intima e media, che cosa c'è nell'avventizia |
| 9, aorta Verhoeff | `lab_p050_3031.jpg` | 3 | identificazione e colorazione, l'elastina in viola scuro, arterie contro vene |
| 10, cordone ombelicale | `lab_p050_3032.jpg` | 3+1 | identificazione, dove si osserva il tessuto mucoso, i tre grossi vasi, più la carta segnalata |

**I vetrini 8, 9 e 10 non avevano nessuna carta, in nessun mazzo.** Il file
`05a` si ferma al **Vetrino 7** di pagina 49, mentre la tabella del punto 2 lo
dava per «pagine 43-50»: aorta in ematossilina-eosina, aorta in Verhoeff e
cordone ombelicale, i tre vetrini di pagina 50, erano **scoperti per intero**.
Sono dieci delle 44 carte di questa iterazione, ed è la prima volta che il mazzo
`Vetrini` chiude un buco invece di affiancarsi a carte esistenti. La riga del
punto 2 è stata corretta in «pagine 43-49», che è quello che il file copre
davvero.

**Scartate sei figure**, tutte per la regola delle immagini del punto 3 (una
figura che contiene la risposta non va sul fronte):

- `lab_p043_2572.jpg`: lo schema del differenziamento delle **MSC**, con
  *CARTILAGE*, *BONE*, *MUSCLES*, *SKIN*, *FAT*, *CNS*, *MARROW* e i nomi delle
  cellule figlie stampati attorno;
- `lab_p043_2575.jpg`: la tavola del connettivo con *fibra di collagene*,
  *fibra elastica*, *capillare*, *macrofago*, *fibroblasto*, *mastcellula*,
  *lamina basale* e *glicosaminoglicani* tutti stampati sopra;
- `lab_p044_2672.jpg`: cordone ombelicale in colorazione Ignesti, con
  *Connettivo mucoso maturo* stampato in mezzo al campo. È il caso in cui la
  didascalia sta **sui pixel** e non nel testo del PDF, al contrario delle
  quattro figure sui tipi di secrezione della 3a;
- `lab_p044_2673.jpg`: il pannello di destra è annotato con *Connettivo lasso*,
  *Epitelio di rivestimento (cilindrico semplice)* e *Fibrocellule muscolari
  lisce*. Il pannello di sinistra sarebbe stato usabile, ma le due
  microfotografie sono **una sola immagine estratta** e non si possono separare
  senza ritagliare;
- `lab_p045_2795.jpg`: ovaio in Bielschowsky annotato con *Oocita*, *Follicolo* e
  *Corpo luteo*. Il tessuto reticolare si chiede comunque sul Vetrino 6, che ha
  già la sua carta;
- `lab_p045_2796.jpg`: il pannello di destra è annotato con *Alveoli polmonari* e
  *Tessuto connettivo elastico*. Vale lo stesso discorso del 2673.

**Restano fuori invece, e non è uno scarto, `lab_p046_2866.jpg` e
`lab_p049_2989.jpg`** (già usate dalle carte del capitolo, vedi la tabella
sopra) e **`lab_p055_3953.jpg`**, che ha due ragioni per non entrare: è della
sezione 018, quindi tocca all'iterazione 6, ed è comunque **interamente
annotata** (*Cartilagine ialina immatura*, *Pericondrio (connettivo denso)*,
*Connettivo lasso*, *Epitelio di rivestimento (pseudostratificato ciliato)*).
Sta già dove deve stare: sul **retro** di `lab-cartilagine-011`.

**Due carte portano `da-verificare`, e il totale passa da 108 a 110.**

1. `lab-connettivi-081`, Vetrino 9: la sbobina motiva l'utilità della Verhoeff
   dicendo che «l'elastina è presente **soltanto** nelle arterie». Le vene non
   ne sono prive, ne hanno molta meno e senza una lamina elastica interna
   evidente: quello che la colorazione mostra è una differenza di **quantità**,
   non una presenza contro un'assenza. La carta riporta la sbobina e spiega nel
   `back` che cosa non torna, come prescrive il punto 3;
2. `lab-connettivi-085`, Vetrino 10: la descrizione del **tessuto mucoso** dice
   «struttura stratificata, con uno strato superficiale di cellule epiteliali
   specializzate nella secrezione di muco... e talvolta ghiandole». È la
   descrizione di una **mucosa**, non del tessuto mucoso, e contraddice la
   **stessa sbobina a pagina 44**, dove il tessuto mucoso è il connettivo
   gelatinoso ricco di acido ialuronico del cordone ombelicale (gelatina di
   Wharton). La carta riporta la descrizione e la segnala.

**Un refuso sistemato senza cerimonie, seguendo un precedente.** A pagina 45 la
sbobina scrive che il tessuto adiposo si divide in «uniloculare, detto bianco, e
**multicolore**, detto bruno». `multicolore` non è un termine istologico e il
termine atteso è **multiloculare**: è un refuso, non un errore di contenuto, e
`lab-connettivi-030` lo aveva già normalizzato quando il file `05a` è stato
scritto. `lab-connettivi-047` fa lo stesso, per non contraddire una carta che
Pietro sta già ripassando.

**La tabella del punto 5 aveva perso due righe**, ed è stato sistemato qui.
`lab-esocrino-108` e `lab-endocrino-117`, le due segnalazioni sul «blu di
toluene» scritte dalle iterazioni 3a e 4b, erano finite in `DA_VERIFICARE.md`
(che si genera dalle carte e non può divergere) ma **non** nella tabella scritta
a mano del punto 5, che si era fermata a 106 righe di carta contro 108 tag. Le
quattro righe mancanti — quelle due più le due nuove — ci sono ora, e il
controllo di coerenza è una riga di Python:

```sh
./venv/bin/python -c "
import json, glob
lines = open('PLAN.md').read().split(chr(10))
i = next(n for n, l in enumerate(lines) if l.startswith('| Carta | Cosa non torna |'))
rows = set()
for l in lines[i + 2:]:
    if not l.startswith('|'): break
    rows.add(l.split('|')[1].strip().strip(chr(96)))
tagged = {json.loads(l)['id'] for f in glob.glob('cards/**/*.jsonl', recursive=True)
          for l in open(f) if 'da-verificare' in json.loads(l).get('tags', [])}
print('mancanti dalla tabella:', sorted(tagged - rows))
print('in tabella senza carta:', sorted(rows - tagged))"
```

**La sovrapposizione con le carte di solo testo del capitolo è voluta**, come in
tutte le iterazioni da 3a in poi: `lab-connettivi-013`, `022`, `023`, `033`,
`034`, `035`, `036`, `038`, `039` e `040` dicono in parte le stesse cose. Lì si
chiede di ricordare una definizione, qui di leggere un campo. Due angolature
sono invece state **evitate** perché la carta esistente le esaurisce: il
pericondrio a due strati del Vetrino 5 (`lab-connettivi-040`) e la cartilagine
ialina della giunzione miotendinea (`lab-connettivi-037`, che porta già
`da-verificare`). Al loro posto il Vetrino 5 chiede l'**artefatto di taglio** e
lo **strato condrogenico**, che nessuna carta copriva.

### Capitolo 06, quello che è stato deciso

Dieci figure delle pagine 63-70, 25 carte: `lab-cartilagine-044`-`049`,
`lab-linfoide-048`-`053`, `lab-osso-047`-`055` e `lab-sangue-019`-`022`. Sono i
**vetrini 3, 4, 5, 6, 7, 8, 10 e 11** della sezione 019. È la prima iterazione
del mazzo `Vetrini` che tocca **quattro argomenti** e quindi quattro contatori
di id: cartilagine, linfoide, osso e sangue.

**Il perimetro reale è pagine 63-70, non 55-76**, e le tredici pagine che restano
fuori non sono un buco:

- **pagine 55-60** hanno otto figure e sono **tutte scartate** (vedi sotto): due
  schemi con i nomi stampati sopra, due figure da manuale con la didascalia
  stampata sui pixel, tre microfotografie annotate e lo schema dell'osteone, che
  è un disegno e non un vetrino;
- **pagine 61-62** sono i vetrini 1 e 2, le cui **uniche** figure hanno già la
  loro carta di identificazione con l'immagine sul fronte;
- **pagine 71-75** sono il quiz, **già cardato per intero** in
  `06e-quiz-connettivi-specializzati.jsonl` (30 carte) e **senza nessuna
  figura**. È la situazione del quiz del capitolo 05, non quella dei quiz dei
  capitoli 02 e 03: non c'è niente da chiudere;
- **pagina 76** compare nella sezione 019 ma il testo è del **muscolare**. Il
  taglio è stato deciso sui vetrini, come fra la 3a e la 3b e fra la 4a e la 4b:
  il capitolo 06 finisce al **Vetrino 11** di pagina 70, e le quattro figure
  della 76 passano all'**iterazione 9** (`vetrini-07-10-coda.jsonl`). Sono già
  state guardate tutte e quattro, ed è già stato deciso: **si scartano tutte**
  (vedi in fondo).

**La situazione di partenza è quella del capitolo 03, ma più estrema.** La
sezione 019 ha già 133 note fra `06b`, `06c`, `06d` e `06e`, e `06d-vetrini.jsonl`
copre da solo gli undici vetrini con 45 carte, di cui **undici** hanno già
l'immagine sul fronte. Quelle undici non sono state rifatte, per la regola del
punto 3, e restano nel mazzo di capitolo:

| Figura | Carta che la usa già |
|---|---|
| `lab_p061_4108.jpg` | `lab-cartilagine-026`, Vetrino 1, cartilagine ialina della trachea |
| `lab_p062_4132.jpg` | `lab-cartilagine-031`, Vetrino 2, giunzione muscolotendinea |
| `lab_p063_4148.jpg` | `lab-cartilagine-036`, Vetrino 3, la colorazione Azan-Mallory |
| `lab_p064_4175.jpg` | `lab-cartilagine-040`, Vetrino 4, cartilagine elastica |
| `lab_p065_4201.jpg` | `lab-linfoide-013`, Vetrino 5, milza |
| `lab_p066_4230.jpg` | `lab-linfoide-018`, Vetrino 6, linfonodo |
| `lab_p068_4276.jpg` | `lab-osso-036`, Vetrino 8, osso spugnoso |
| `lab_p069_4297.jpg` | `lab-osso-039`, Vetrino 9, osso decorticato non colorato |
| `lab_p069_4299.jpg` | `lab-osso-042`, Vetrino 10, il piano di taglio |
| `lab_p070_4338.jpg` | `lab-sangue-015`, Vetrino 11, striscio di sangue |
| `lab_p056_3988.jpg` | `lab-cartilagine-020`, cartilagine elastica dell'epiglottide (p. 56) |

Conseguenza, la stessa che era toccata alla prostata nella 3a e al Vetrino 6
nella 5: **i vetrini 1, 2 e 9 spariscono dal mazzo `Vetrini`**, perché la loro
unica figura è già la domanda di una carta del capitolo. Pietro si allena
comunque a riconoscerli, ma dal mazzo `06`.

**La regola seguita per gli altri otto vetrini è quella del capitolo 01, non
quella del 03.** Dove il vetrino ha una **seconda figura libera** — un altro
campo, di solito a ingrandimento maggiore — quella figura entra nel mazzo
`Vetrini` con le domande di dettaglio, che **dichiarano il tessuto nella
domanda** secondo la regola anti-spoiler. La carta di **identificazione** resta
una sola per vetrino: se esiste già nel mazzo di capitolo non è stata rifatta, e
il mazzo `Vetrini` ne scrive una solo dove manca. Manca in tre casi, ed è il
motivo per cui `lab-cartilagine-044` e `lab-osso-047` sono carte di
identificazione:

- **Vetrino 3**: `lab-cartilagine-036` chiede la *colorazione*, non il tessuto;
- **Vetrino 7**: le sue due figure sono **entrambe sul retro**, quindi non c'era
  nessuna carta di identificazione con l'immagine sul fronte;
- **Vetrino 10**: `lab-osso-042` chiede il *piano di taglio* e dichiara il
  tessuto nella domanda. Qui però l'identificazione non è stata rifatta lo
  stesso, perché la figura libera (`4336`) è un dettaglio ad alto ingrandimento
  in cui non si riconosce l'osso nel suo insieme: le sue due carte sono di
  dettaglio.

**Le tre miniature di pagina 70 sono la scoperta di questa iterazione.** Sono le
figure numerate `1.`, `2.` e `3.` accanto al Vetrino 11, ritagli dello striscio
di sangue attorno a un singolo leucocita, e **nessuna carta del progetto le
usava**. Sono minuscole (171×141, 121×126, 272×295) e il formato faceva pensare
a icone di layout, ma guardate sono microfotografie pulite: è esattamente la
domanda che l'esame pratico fa davanti a uno striscio. L'abbinamento numero →
ritaglio è stato verificato sulle **coordinate** delle immagini nella pagina e
sulla pagina resa, non sulle didascalie:

```sh
./venv/bin/python -c "import pymupdf; \
  [print(i['xref'], [round(x) for x in i['bbox']]) for i in \
   pymupdf.open('$DL/Istologia Laboratorio combinato.pdf')[69].get_image_info(xrefs=True)]"
```

La distribuzione delle domande segue i campi:

| Vetrino | Figura | Carte | Taglio |
|---|---|---:|---|
| 3, cartilagine fibrosa | `lab_p063_4150.jpg` | 3 | identificazione e colorazione, i condrociti azzurri nelle lacune, l'assenza di pericondrio |
| 4, cartilagine elastica | `lab_p064_4177.jpg` | 3 | perché i condrociti si vedono male in Weigert, dove stanno le fibre elastiche, matrice e gruppi isogeni contro la ialina |
| 5, milza | `lab_p065_4199.jpg` | 3 | polpa bianca e polpa rossa nel campo, l'arteria centrale eccentrica, le trabecole connettivali |
| 6, linfonodo | `lab_p066_4232.jpg` | 3 | le tre zone dalla capsula all'interno, perché B e T non si distinguono in H&E, che cosa dà l'aspetto punteggiato |
| 7, osso compatto trasversale | `lab_p067_4255.jpg` | 2 | identificazione e colorazione, perché e come si demineralizza |
| 7 | `lab_p067_4257.jpg` | 2 | lacune e canalicoli, l'endostio che separa l'osso dalla cavità midollare |
| 8, osso spugnoso | `lab_p068_4278.jpg` | 3 | il midollo giallo negli spazi intertrabecolari, sedi e vantaggio meccanico delle trabecole, perché gli osteociti sono sparsi |
| 10, osso compatto longitudinale | `lab_p070_4336.jpg` | 2 | che cosa contengono i canali di Havers e i Volkmann, la forma delle lacune osteocitarie |
| 11, striscio, figura `1.` | `lab_p070_4340.jpg` | 2 | identificazione del neutrofilo, i due criteri di classificazione dei leucociti |
| 11, figura `2.` | `lab_p070_4342.jpg` | 1 | identificazione, più la carta segnalata |
| 11, figura `3.` | `lab_p070_4344.jpg` | 1 | identificazione, più la carta segnalata |

**Scartate otto figure**, tutte per la regola delle immagini del punto 3 (una
figura che contiene la risposta non va sul fronte), tranne una che non è un
vetrino:

- `lab_p055_3953.jpg`: la trachea fetale in Azan-Mallory, **interamente
  annotata** (*Cartilagine ialina immatura*, *Pericondrio*, *Connettivo lasso*,
  *Epitelio di rivestimento*). Era già stata guardata e decisa dall'iterazione 5:
  sta sul **retro** di `lab-cartilagine-011` e ci resta;
- `lab_p056_3986.jpg`: cartilagine ialina e fibrosa con *Pericondrio*,
  *Cartilagine ialina immatura* e *Cartilagine fibrosa* stampati sui pixel;
- `lab_p057_4005.jpg`: il **disegno** dell'osso compatto con periostio, fibre di
  Sharpey e osteoni. Non ha etichette, ed è infatti già sul fronte di
  `lab-osso-031`, ma è uno **schema** e non un vetrino: il mazzo `Vetrini` allena
  il riconoscimento di un campo al microscopio;
- `lab_p058_4026.jpg`: figura da manuale (*Figura 16.9*) con la **didascalia
  completa stampata sotto**, compresi il tessuto, la colorazione e le sigle
  *T*, *MO*, *VS*, *Oc*, *Ob*;
- `lab_p058_4028.jpg`: lo schema dell'osso compatto in sezione con *Osteone*,
  *Canale di Havers*, *Periostio*, *Endostio* e tutto il resto stampato attorno;
- `lab_p059_4057.jpg`: l'osteone con *Canale di Havers*, *Canalicoli ossei* e
  *Lacune ossee* stampati sopra e l'osteone tratteggiato in rosa;
- `lab_p060_4081.jpg`: i tre campi dello striscio con *PIASTRINE*, *BASOFILO*,
  *EOSINOFILO* e *NEUTROFILO* stampati sopra. È il confronto affiancato dei
  granulari, e sarebbe stato ottimo per il fronte: le etichette lo escludono;
- `lab_p060_4083.jpg`: lo striscio con *MONOCITA* e *LINFOCITA* stampati sopra.

**E scartate le quattro figure di pagina 76**, che sono già state guardate una
per una benché appartengano all'iterazione 9. Nessuna delle quattro è
utilizzabile, e questo è il bilancio della coda del muscolare per come si vede
da qui:

- `lab_p076_5069.jpg`: lo schema dei tre tipi di tessuto muscolare con
  *TESSUTO MUSCOLARE STRIATO SCHELETRICO*, *… CARDIACO* e *… LISCIO* stampati
  sopra;
- `lab_p076_5071.jpg`: lo schema della fibra striata con *Nucleo*,
  *Lamina esterna* e *Miofibrille*;
- `lab_p076_5073.jpg`: le due microfotografie di muscolo striato scheletrico con
  la **didascalia stampata sotto** entrambe, ingrandimento compreso;
- `lab_p076_5075.jpg`: lo schema del cardiomiocita con *Nucleo*, *Miofibrille* e
  *Dischi intercalari*.

L'iterazione 9 resta comunque da fare — copre anche i vetrini del muscolare
delle pagine 82-85 e la tonsilla di pagina 106 — ma **da pagina 76 non prenderà
niente**.

**Due carte portano `da-verificare`, e il totale passa da 110 a 112.** Sono
`lab-sangue-021` e `lab-sangue-022`, ed è la stessa segnalazione vista da due
lati:

le figure `2.` e `3.` di pagina 70 sembrano **scambiate**. La sbobina numera
`2.` come monocita e `3.` come linfocita, ma la cellula di `4342` (la `2.`) ha un
nucleo rotondo, denso e scuro che occupa quasi tutta la cellula, con un sottile
anello di citoplasma, mentre quella di `4344` (la `3.`) ha un nucleo **pallido e
indentato** e un anello di citoplasma chiaro ben visibile. È l'opposto di quello
che la sbobina scrive nella **stessa pagina**: che il monocita è il leucocita di
maggior calibro, con nucleo ampio a ferro di cavallo, «meno denso e di
conseguenza meno scuro rispetto a quello dei linfociti». Le due carte riportano
quello che dice la sbobina e spiegano nel `back` che cosa non torna, come
prescrive il punto 3.

**La sovrapposizione con le carte di solo testo della sezione è voluta**, come in
tutte le iterazioni da 3a in poi, ma qui è più larga che altrove, perché `06b`,
`06c` e `06d` avevano già cardato la sezione per intero. Le carte che dicono in
parte le stesse cose sono `lab-cartilagine-018`, `019`, `021`, `022`, `037`,
`039`, `042`; `lab-linfoide-002`, `016`, `017`, `020`, `021`; `lab-osso-006`,
`008`, `013`, `014`, `015`, `020`, `021`, `023`, `024`, `027`, `028`, `035`,
`038`; `lab-sangue-011`, `016`. Lì si chiede di ricordare una definizione, qui di
leggere un campo. Tre angolature sono invece state **evitate** perché la carta
esistente le esaurisce e usa la **stessa figura**: l'osso spugnoso e il tendine
in formazione del Vetrino 3 (`lab-cartilagine-038`), gli osteoblasti sulla
superficie delle trabecole del Vetrino 8 (`lab-osso-037`) e i canali di Havers
rosati del Vetrino 7 (`lab-osso-034`). Evitata anche la carta sui condroblasti
lungo le pareti dei canali di Havers, perché `lab-osso-046` porta già
`da-verificare` proprio su quel punto.

### Capitolo 08, quello che è stato deciso

Dieci figure delle pagine 86-91, 16 carte, `lab-nervoso-085`-`100`: i **vetrini
4, 5, 6, 7 e 9** della sezione 022 (cervelletto, motoneurone in Nissl, midollo
spinale, ganglio spinale in Golgi, nervo periferico). Tutte le carte sono
`basic`, con immagine sul fronte e `tipo::riconoscimento`. Nessuna ha richiesto
il tag `da-verificare`: il totale resta **112**.

**Il perimetro reale è pagine 86-91, non 78-96**, ed è il taglio più stretto di
tutto il mazzo rispetto alla stima. Le altre tredici pagine non sono un buco:

- **pagine 78-81** sono la teoria del tessuto nervoso e del SNP (sezione 021 e
  apertura della 022). Hanno dieci figure: due sono già la domanda di
  `lab-nervoso-035` e `036`, e le **altre otto sono tutte da scartare** (vedi
  sotto). Da lì non viene **niente**;
- **pagine 82-85** sono i **tre vetrini muscolari** (lingua, cuore, intestino) e
  passano all'**iterazione 9**, insieme alla tonsilla: vedi più sotto il perché e
  che cosa ci troverà;
- **pagine 92-96** sono il quiz, **già cardato per intero** in
  `08c-quiz-nervoso.jsonl` (24 carte) e **senza nessuna figura**: la sezione 023
  dichiara `images: []` ed è vero, `images.jsonl` non elenca nemmeno un file
  fra pagina 92 e pagina 96. È la situazione dei quiz dei capitoli 05 e 06, non
  quella dei capitoli 02 e 03: non c'è niente da chiudere. Vale anche per
  **pagina 96**, che la tabella del punto 2 dà come condivisa con la sezione 025:
  il taglio con il capitolo 09 **non tocca nessun vetrino**, perché lì di figure
  non ce ne sono.

**Perché i tre vetrini muscolari sono dell'iterazione 9 e non di questa.** La
riga 9 della tabella esiste apposta per il muscolare e la tonsilla, e il taglio
segue i **vetrini** come fra la 3a e la 3b: qui però segue anche l'**argomento**,
perché quelle carte porterebbero id `lab-muscolare` (il contatore è fermo a
`044`) dentro un file che si chiama `vetrini-08-nervoso.jsonl`. La regola del
punto 3 è **un file per capitolo**, e il capitolo del muscolare è il `07`. È lo
stesso ragionamento con cui `07b` tiene le carte dei vetrini 1-3 nel mazzo del
muscolare invece che in quello del nervoso.

**La situazione di partenza è quella del capitolo 06, portata all'estremo.** La
sezione 022 e la 021 hanno già 84 note fra `08a`, `08b` e `08b2`, e il solo
`08b2` copre i vetrini 4-9 con 39 carte. Delle **ventiquattro** figure delle
pagine 86-91, **undici** hanno già la loro carta con l'immagine sul fronte e
restano nel mazzo di capitolo, come il punto 3 prescrive:

| Figura | Carta che la usa già |
|---|---|
| `lab_p086_5472.jpg` | `lab-nervoso-046`, Vetrino 4, cervelletto d'insieme |
| `lab_p087_5502.jpg` | `lab-nervoso-055`, Vetrino 5, motoneuroni in Nissl |
| `lab_p087_5508.jpg` | `lab-nervoso-058`, Vetrino 6, midollo spinale in H&E |
| `lab_p088_5549.jpg` | `lab-nervoso-065`, Vetrino 6, motoneuroni nelle corna ventrali |
| `lab_p088_5551.jpg` | `lab-nervoso-066`, Vetrino 6, il midollo in tecnica di Golgi |
| `lab_p089_5591.jpg` | `lab-nervoso-068`, Vetrino 7, ganglio spinale d'insieme |
| `lab_p089_5599.jpg` | `lab-nervoso-074`, Vetrino 7, i due prolungamenti nervosi |
| `lab_p090_5630.jpg` | `lab-nervoso-077`, Vetrino 8, ganglio spinale in H&E |
| `lab_p090_5632.jpg` | `lab-nervoso-078`, Vetrino 9, nervo periferico d'insieme |
| `lab_p091_5668.jpg` | `lab-nervoso-080`, Vetrino 9, le guaine mieliniche |
| `lab_p091_5672.jpg` | `lab-nervoso-083`, Vetrino 9, sezione longitudinale |

Conseguenza, la stessa che era toccata alla prostata nella 3a, al Vetrino 6
nella 5 e ai vetrini 1, 2 e 9 nella 6: **il Vetrino 8 sparisce dal mazzo
`Vetrini`**, perché la sua unica figura è già la domanda di `lab-nervoso-077`.
Pietro si allena comunque a riconoscere il ganglio in ematossilina-eosina, ma
dal mazzo `08`.

**La carta di identificazione è stata scritta una volta sola**, come nel
capitolo 06, e qui manca in un caso solo: `lab-nervoso-091`, il **midollo
spinale in tecnica di Golgi**. Esiste `058`, che identifica lo stesso vetrino in
H&E, ed esiste `066`, che sulla figura d'insieme in Golgi chiede però la
**colorazione** e non l'organo. È il caso del Vetrino 3 del capitolo 06
(`lab-cartilagine-036`): l'identificazione non c'era, e in Golgi il midollo ha un
aspetto abbastanza diverso da meritarla. Per tutti gli altri vetrini
l'identificazione esiste già e non è stata rifatta.

La distribuzione delle domande segue i campi:

| Vetrino | Figura | Carte | Taglio |
|---|---|---:|---|
| 4, cervelletto | `lab_p086_5474.jpg` | 2 | le tre bande di colore dall'esterno all'interno; perché lo strato molecolare è chiaro e povero di nuclei |
| 4 | `lab_p086_5476.jpg` | 2 | lo strato granulare e il rischio di confondere i granuli con i linfociti; che cosa l'H&E non mostra |
| 5, motoneurone in Nissl | `lab_p087_5506.jpg` | 2 | il materiale basofilo del citoplasma; il nucleolo e che cosa indica |
| 6, midollo spinale in Golgi | `lab_p088_5557.jpg` | 2 | identificazione e tecnica; corna ventrali contro corna dorsali |
| 6, midollo spinale in H&E | `lab_p088_5547.jpg` | 1 | come si distinguono sostanza grigia e sostanza bianca nel campo |
| 6, Golgi ad alto ingrandimento | `lab_p088_5553.jpg` | 1 | corpi e prolungamenti insieme: in che porzione del midollo siamo |
| 7, ganglio spinale | `lab_p089_5593.jpg` | 2 | la capsula e i setti; neuroni in periferia e groviglio di fibre al centro |
| 7 | `lab_p089_5595.jpg` | 1 | perché in un ganglio non si osservano sinapsi |
| 9, nervo periferico | `lab_p091_5666.jpg` | 2 | i fascicoli e i loro rivestimenti; dov'è l'endonevrio e come si intuisce |
| 9 | `lab_p091_5670.jpg` | 1 | gli assoni non si vedono in ematossilina-eosina |

**Scartate otto figure delle pagine 78-81**, tutte per la regola delle immagini
del punto 3 (una figura che contiene la risposta non va sul fronte). Sono la
ragione per cui la sezione 021 non produce nemmeno una carta di riconoscimento:

- `lab_p078_5166.jpg`: lo schema del neurone con *Dendriti*, *Soma*, *Nucleo e
  nucleolo*, *Assone*, *Guaina mielinica*, *Nodo di Ranvier* e *Bottoni
  sinaptici* stampati sopra;
- `lab_p078_5168.jpg`: i tre neuroni in colorazione di Nissl, con *Nucleo*,
  *Sostanza tigroide*, *Nucleolo* stampati sopra e la didascalia *Neuroni:
  nucleo, nucleolo e sostanza tigroide* stampata sotto;
- `lab_p079_5213.jpg`: la tavola della neuroglia con *oligodendrociti*,
  *microglia*, *cellula ependimale*, *cellula di Schwann* e *astrocita*
  stampati attorno;
- `lab_p079_5215.jpg`: la grande tavola orto/parasimpatico, con il nome di ogni
  effetto su ogni organo;
- `lab_p080_5251.jpg`: l'organigramma del sistema nervoso, tutto testo;
- `lab_p080_5253.jpg`: lo schema *I NERVI SPINALI* con *EPINEVRIO*,
  *PERINEVRIO*, *ENDONEVRIO*, *FASCICOLO*, *ASSONE* e *VASI SANGUIGNI* stampati
  attorno;
- `lab_p080_5255.jpg`: lo schema del midollo con *Sostanza grigia*, *Sostanza
  bianca*, *Corno dorsale*, *Ganglio spinale*, *Neurone sensitivo* e tutto il
  resto stampato attorno;
- `lab_p081_5292.jpg`: la sezione di midollo in Golgi da manuale, annotata
  (*Corno posteriore*, *Sostanza grigia*, *Canale ependimale*, *Neuroni
  multipolari*) **e** con la didascalia completa stampata sotto, ingrandimento
  compreso. È il caso di `lab_p058_4026.jpg` del capitolo 06.

**Scartate altre tre figure delle pagine 86-91**, e nessuna delle tre per via
delle etichette:

- `lab_p088_5555.jpg`: campo in Golgi **sfocato e senza una struttura
  riconoscibile**, un passaggio fra sostanza grigia e sostanza bianca su cui non
  si può costruire una domanda onesta;
- `lab_p087_5504.jpg` e `lab_p089_5597.jpg`: figure buone, ma con le
  **angolature esaurite** dalle carte che le usano già sul retro.
  Sulla `5504`, `lab-nervoso-057` chiede che cosa siano i piccoli nuclei scuri
  dello sfondo e `056` la differenza fra dendrite e assone in Nissl; quel che
  resterebbe (che cosa evidenzia la colorazione di Nissl, con quali coloranti)
  è già `lab-nervoso-015` e `039`. Sulla `5597`, che è un campo quasi identico
  alla `5595`, `lab-nervoso-070` esaurisce l'anello di cellule satelliti.
  Non è uno scarto per la regola delle immagini: è la regola del punto 3 sulla
  lettura delle carte esistenti.

**Non è stata riaperta `lab-nervoso-069`**, che porta `da-verificare` sul
Vetrino 7 (la sbobina dichiara la tecnica di Golgi ma descrive corpi di Nissl
basofili e cellule satelliti in tutti i neuroni). Le tre carte nuove sul ganglio
non nominano la colorazione, proprio per non contraddirla: chiedono la capsula,
la distribuzione dei neuroni e l'assenza di sinapsi.

**La sovrapposizione con le carte di solo testo della sezione è voluta**, come in
tutte le iterazioni da 3a in poi: `lab-nervoso-048`, `049`, `051`, `052`, `054`,
`059`, `063`, `071`, `072`, `073`, `082` e `029` dicono in parte le stesse cose.
Lì si chiede di ricordare una definizione, qui di leggere un campo.

**Che cosa troverà l'iterazione 9 alle pagine 82-85**, già guardato una per una
mentre si leggeva la sezione 022, come il capitolo 06 aveva fatto con pagina 76.
Quattro figure hanno già la loro carta con l'immagine sul fronte
(`lab_p082_5334` → `lab-muscolare-031`, `lab_p083_5367` → `030`,
`lab_p084_5399` → `035`, `lab_p085_5435` → `043`). Delle **undici** libere,
sette sono usabili:

| Figura | Che cos'è | Verdetto |
|---|---|---|
| `lab_p082_5330.jpg` | due campi: lingua con papille e fasci di striato scheletrico in tutte le direzioni | **usabile**, senza etichette |
| `lab_p082_5332.jpg` | due papille filiformi della lingua, con una terza sezionata in mezzo | **usabile** |
| `lab_p083_5365.jpg` | cuore a piccolo ingrandimento, fasci ramificati in tutte le direzioni | **usabile** |
| `lab_p083_5369.jpg` | un **nervo** in sezione trasversale in mezzo al muscolo della lingua | **usabile**, è la figura delle «terminazioni nervose» |
| `lab_p083_5371.jpg` | fra le fibre, un piccolo aggregato ghiandolare e adipociti | **da riguardare**: senza etichette, ma il campo è ambiguo |
| `lab_p084_5397.jpg` | cuore, setto connettivale con adipociti e un vaso | **usabile** |
| `lab_p085_5437.jpg` | intestino tenue, le quattro tonache dalla mucosa alla muscolare | **usabile** |

E le quattro da **scartare**, per ragioni che valgono già adesso:

- `lab_p085_5429.jpg` e `lab_p085_5431.jpg`: sono le due figure di cui **il prof
  stesso dice di non essere sicuro della colorazione** (`[N.d.S ... non è
  importante saperlo]`, pagina 85). Il campo è azzurrino e non identificabile
  con certezza;
- `lab_p084_5401.jpg`: campo rosa uniforme di fibre lisce longitudinali, **senza
  un riferimento** che permetta di dire di che organo si tratti;
- `lab_p085_5433.jpg`: due campi in **un unico file estratto**. Quello in basso a
  sinistra è un ottimo intestino tenue, ma quello in alto a destra non è
  identificabile con certezza e i due non si possono separare senza ritagliare.
  È il caso di `lab_p044_2673.jpg` del capitolo 05.

La stima della riga 9 è stata alzata di conseguenza da «2 vetrini, ~5 carte» a
«4 vetrini, ~20 carte», su sette figure libere: i tre vetrini muscolari, che il
registro del capitolo 06 le aveva già assegnato, più la tonsilla di pagina 106.

### Capitolo 09, quello che è stato deciso

**Zero carte, e nessun file.** È l'unica iterazione del mazzo `Vetrini` che si
chiude senza scrivere niente, e il risultato è **definitivo**, non rinviato: le
tredici figure delle pagine 98-105 sono state guardate una per una, e nessuna
può entrare. `vetrini-09-embriologia.jsonl` non è stato creato e non va creato.
I due contatori restano dove erano: `lab-embriologia` fermo a **057**,
`lab-linfoide` a **053**.

**Il perimetro reale è pagine 98-105, non 96-106**, e le pagine che restano
fuori non sono un buco:

- **pagine 96-97** non hanno **nemmeno una figura**. L'iterazione 7 lo aveva già
  verificato per la 96 e vale anche per la 97: `images.jsonl` non elenca niente
  fra pagina 92 e pagina 98, e `get_images` sul PDF conferma le liste vuote. Le
  due pagine sono state comunque **rese e guardate**, perché una figura
  vettoriale non comparirebbe in nessuno dei due elenchi: sono testo puro (la
  fecondazione, la segmentazione, l'impianto, la gastrulazione), e i 49 e 44
  "drawings" che `get_drawings` conta sono i punti elenco e le sottolineature
  dei titoli. Da lì non viene **niente**;
- **pagina 106** è la tonsilla palatina e appartiene all'**iterazione 9**
  (`vetrini-07-10-coda.jsonl`), come il registro del capitolo 08 aveva già
  deciso. Le sue tre figure sono comunque state guardate: vedi in fondo.

**I nove modellini non sono vetrini, e questa è la decisione che conta.** Le
figure delle pagine 98-103 sono **fotografie di modelli in gesso e resina
dipinti a mano**, con i numeri di richiamo scritti a pennarello sul modello
stesso: l'ovocita e i corpi polari dentro la zona pellucida (p. 98), lo stadio a
quattro blastomeri (p. 99), la blastocisti impiantata montata su un piedistallo
metallico con la sua base verde da laboratorio (p. 100), il disco embrionale in
sezione (p. 101), il sacco vitellino e l'allantoide (p. 102), il feto nella
placenta con l'albero coriale (p. 103). Non è un campo al microscopio, e il
mazzo `Vetrini` allena il riconoscimento di un campo al microscopio: è
esattamente la domanda che il capitolo 06 si è posto per lo schema dell'osteone
(`lab_p057_4005.jpg`) e ha risolto scartandolo. Qui la risposta è la stessa,
ripetuta nove volte.

Vale la pena dire perché **non è una perdita**. La pagina 97 riporta una
`Osservazione del docente` secondo cui il riconoscimento dei modellini è
materia d'esame, e infatti Pietro ci si allena già: le nove figure sono i fronti
di `lab-embriologia-021`, `024`, `028`, `029`, `031`, `033`, `038`, `044` e
`053`, tutte carte di identificazione («Che stadio rappresenta questo
modellino?») con l'immagine sul fronte. Si allena dal mazzo `09`, come si allena
sulla prostata dal `03` e sul ganglio in ematossilina-eosina dall'`08`.

**E le tredici figure hanno già tutte la loro carta con l'immagine sul fronte**,
il che le escluderebbe comunque per la regola del punto 3. È il primo capitolo
del progetto in cui il rapporto è **tredici su tredici**: nel 03 erano nove su
37, nel 06 undici su ventuno, nel 07 undici su ventiquattro.

| Figura | Carta che la usa già |
|---|---|
| `lab_p098_6012.jpg` | `lab-embriologia-021`, Modellino 1, ovocita secondario e corpo polare |
| `lab_p098_6014.jpg` | `lab-embriologia-024`, Modellino 2, ingresso dello spermatozoo |
| `lab_p099_6050.jpg` | `lab-embriologia-028`, Modellino 3, i due pronuclei |
| `lab_p099_6052.jpg` | `lab-embriologia-029`, Modellino 4, fusione dei nuclei |
| `lab_p099_6054.jpg` | `lab-embriologia-031`, Modellino 5, stadio a quattro blastomeri |
| `lab_p100_6100.jpg` | `lab-embriologia-033`, Modellino 6, impianto nell'endometrio |
| `lab_p101_6133.jpg` | `lab-embriologia-038`, Modellino 7, disco embrionale |
| `lab_p102_6162.jpg` | `lab-embriologia-044`, Modellino 8, annessi extraembrionali |
| `lab_p103_6187.jpg` | `lab-embriologia-053`, Modellino 9, feto e placenta |
| `lab_p104_6206.jpg` | `lab-linfoide-026`, timo d'insieme, corteccia/midollare/Hassall |
| `lab_p105_6222.jpg` | `lab-linfoide-031`, cellule epiteliali timiche (frecce bianche) |
| `lab_p105_6224.jpg` | `lab-linfoide-032`, mastociti (frecce nere) |
| `lab_p105_6226.jpg` | `lab-linfoide-028`, corpuscolo di Hassall (freccia) |

**Dove cade il taglio con il timo delle pagine 104-105.** Quelle quattro figure
**sono** campi al microscopio, e ottimi: il timo d'insieme con le marcature mute
di corteccia, midollare e corpuscolo di Hassall, e i tre campi ad alto
ingrandimento presi da *histology guide* con frecce che non nominano niente. Se
fossero state libere sarebbero state materiale da fronte perfetto. Ma il timo
appartiene al **capitolo 06**, non al 09: le sue carte stanno in `06f`, nel mazzo
`06` con il resto del linfoide, e sta dentro la sezione dei modellini solo
perché il professore lo ha ripreso a fine corso per un vetrino non osservato
(vedi il punto 4). Il taglio segue quindi l'**argomento** e non la pagina, come
fra il capitolo 08 e i tre vetrini muscolari: anche in presenza di una figura
libera quelle carte avrebbero prolungato `vetrini-06-specializzati.jsonl`, non
aperto un `vetrini-09`. Il punto è teorico, perché figure libere non ce ne sono.

**Perché il timo non è stato ripreso lo stesso sulle figure già usate.** La
tentazione c'era, perché `06f` ha quindici carte e una sola è di
identificazione. Non regge a due controlli. Il primo è il precedente: da
quattro iterazioni la regola è che una figura già sul fronte di una carta di
capitolo **non si riprende**, e il vetrino sparisce dal mazzo `Vetrini` (la
prostata nella 3a, il Vetrino 6 nella 5, i vetrini 1, 2 e 9 nella 6, il Vetrino
8 nella 7). Il secondo è che `06f` **è già** un trattamento in stile `Vetrini`:
`lab-linfoide-028`, `031` e `032` hanno l'immagine sul fronte e chiedono esattamente
«che cosa indica la freccia, e come si riconosce questa cellula», cioè la carta
di dettaglio che il mazzo `Vetrini` scriverebbe. Quello che resterebbe da
chiedere sarebbe una **parafrasi**, cioè il doppione che il validatore **non**
intercetta perché blocca solo le domande identiche: è la lezione di
`teoria_p007_21` al punto 6.

Le **tre eccezioni** che esistono nel mazzo — `lab_p003_229.jpg` e
`lab_p005_290.jpg` (capitolo 01), `lab_p024_1258.jpg` (capitolo 03b) — non
autorizzano una quarta. Le prime due sono dell'iterazione 1, scritta prima che
la dottrina si consolidasse nella 3a, e le carte del mazzo `01` che le usano
chiedono la **preparazione** e la **colorazione**, non il tessuto; la terza è il
caso di `lab-esocrino-082`, la cui carta porta `da-verificare` proprio per
l'**abbinamento sbagliato** dell'immagine, e la figura era quindi di fatto
libera. Nessuna delle tre situazioni si ripresenta qui.

Nessuna carta è stata scritta, quindi nessuna ha richiesto `da-verificare`: il
totale resta **112**, e i conteggi del punto 1 non cambiano (960 carte, 12
mazzi, 212 immagini per il Laboratorio, 163 test verdi).

**Che cosa troverà l'iterazione 9 a pagina 106**, già guardato una per una come
il capitolo 06 aveva fatto con pagina 76 e il capitolo 08 con le pagine 82-85.
Le figure sono tre, e una sola è libera:

| Figura | Che cos'è | Verdetto |
|---|---|---|
| `lab_p106_6255.jpg` | tonsilla ad alto ingrandimento: l'epitelio pavimentoso stratificato che si insinua a formare una cripta, con i noduli linfatici sotto. Nessuna etichetta | **libera e usabile**: oggi sta solo sul **retro** di `lab-linfoide-039`, quindi diventa il fronte delle carte di dettaglio |
| `lab_p106_6257.jpg` | tonsilla d'insieme: la superficie con l'epitelio e i follicoli con i centri germinativi | **già sul fronte** di `lab-linfoide-047` (identificazione), e ci resta. Sta anche sul retro di `043` |
| `lab_p106_6253.jpg` | la tavola da manuale della tonsilla | **scartata**: ha *Epitelio*, *Muscolatura striata*, *Sottomucosa*, *Noduli linfatici*, *Cripta tonsillare* e *Ghiandola salivare* stampati sui pixel. Nessuna carta la usa oggi, ed è giusto così |

Le due fotografie sono **scatti attraverso l'oculare**, 1200x1600, con un ampio
bordo scuro attorno al campo illuminato. La pagina le mostra **ritagliate al
solo cerchio chiaro**, ed è il motivo per cui il controllo del clip path del
punto 6 le segnala con correlazione 0,01 e 0,11: è un falso allarme, il campo
nel file è integro e usabile: si porta dietro il bordo scuro, che sulla carta
non disturba. Stessa cosa per `lab_p104_6206.jpg` (correlazione −0,62) e
`lab_p100_6100.jpg` (−0,09), che sono comunque figure già collocate. **Su queste
pagine il clip path non toglie niente a nessuno.**

La stima della riga 9 **non cambia**: resta «4 vetrini, ~20 carte», su otto
figure libere: le sette delle pagine 82-85 che il capitolo 08 ha elencato, più
`lab_p106_6255.jpg`. Con la riga 8 chiusa a zero, **l'iterazione 9 è l'ultima
del mazzo `Vetrini`**.

## 5. Segnalazioni `da-verificare` già trovate

Centododici carte taggate, più una figura scartata senza produrre carta. Ora che
non c'è più niente da scrivere, questo elenco cambia destinatario: non serve più
a calibrare l'asticella, ma è **la lista di ciò che Pietro deve portare al
libro**. Le carte sono ordinate come i mazzi, quindi si ripercorre nell'ordine
del corso.

**La copia da dare a Pietro è `DA_VERIFICARE.md`, e si genera dalle carte.** La
tabella qui sotto resta la vista per chi lavora al progetto: è scritta a mano,
condensa ogni segnalazione in una riga e non riporta la pagina. Quella che serve
al tavolo col libro è invece generata, porta il `source` di ogni carta e la nota
per esteso, e soprattutto **non può divergere dal mazzo**: una voce sparisce
quando la sua carta perde il tag.

```sh
./venv/bin/python -m scripts.da_verificare --cards cards --out DA_VERIFICARE.md
```

Chiudendo una segnalazione vanno quindi aggiornati **tre** posti: la carta
(testo, nota, tag), questa tabella e `DA_VERIFICARE.md`, che si rigenera. I due
punti senza carta (pagine 4 e 70 del Laboratorio) non hanno tag che li porti,
quindi nel generatore stanno in una costante, `WITHOUT_CARD`: se ne emergessero
altri vanno aggiunti lì, oltre che qui.

**Attenzione a come è fatta la nota sul `back` di una carta basic**, se un
giorno si tocca `da_verificare.py`. La segnalazione comincia dove si apre il
corsivo e arriva in fondo al campo, ma **non coincide con i blocchi `<i>`**: il
corsivo si chiude e riapre attorno a ogni parola in grassetto (in
`teoria-sangue-030` prendere i soli blocchi `<i>` fa sparire il **C4** e il
**C2**, cioè il contenuto della segnalazione), e su cinque carte in corsivo c'è
la sola etichetta mentre la spiegazione prosegue in tondo
(`lab-linfoide-022`, `lab-nervoso-015`, `lab-nervoso-069`, `lab-linfoide-039`,
`lab-osso-046`). Due carte non hanno corsivo affatto, perché lì l'affermazione
dubbia **è** la risposta (`lab-esocrino-033`, `lab-connettivi-037`). I test in
`tests/test_da_verificare.py` descrivono tutti e quattro i casi.

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
| `lab-connettivi-081` | il Vetrino 9 dice che l'elastina è presente **soltanto** nelle arterie; le vene ne hanno molta meno e senza lamina elastica interna evidente, ma non ne sono prive: la Verhoeff mostra una differenza di quantità |
| `lab-connettivi-085` | il Vetrino 10 descrive il **tessuto mucoso** come una struttura stratificata con epitelio secernente muco e ghiandole; è la descrizione di una **mucosa**, e contraddice pagina 44 dove il tessuto mucoso è la gelatina di Wharton |
| `lab-endocrino-117` | il Vetrino 8 del capitolo 04 dà la colorazione per «**blu di toluene**», che non è una colorazione istologica; il nome atteso è **blu di toluidina**, e il campo è effettivamente azzurro-violetto |
| `lab-esocrino-108` | il Vetrino 2 del capitolo 03 dà la colorazione per «**blu di toluene**»; stesso errore, stessa correzione attesa, **blu di toluidina** |
| `lab-sangue-021` | il Vetrino 11 numera «2.» un **monocita**, ma il ritaglio mostra una cellula poco più grande di un eritrocita, con nucleo rotondo denso e scuro che occupa quasi tutta la cellula: è il **linfocita** come lo descrive la sbobina stessa poche righe sotto |
| `lab-sangue-022` | il Vetrino 11 numera «3.» un **linfocita**, ma il ritaglio mostra un nucleo pallido e indentato con un anello di citoplasma chiaro ben visibile: è il **monocita**. Le figure «2.» e «3.» di pagina 70 sembrano scambiate |
| `teoria-tecnica-030` | la sbobina dà due spessori diversi per le sezioni istologiche: 5-20 micron per il microscopio ottico (p. 2) e 1-10 µm per il taglio al microtomo (p. 4), senza spiegare la differenza |
| `teoria-colorazioni-021` | descrive come "strati di muscolatura liscia" la banda pallida sotto la mucosa in un vetrino di trachea fetale; per aspetto e per anatomia è cartilagine ialina, e la muscolatura liscia della trachea sta nella parte membranacea posteriore |
| `teoria-colorazioni-024` | classifica l'Azocarminio come colorante **basico** e nella stessa frase gli attribuisce la colorazione dei granuli **acidofili** dell'ipofisi; l'azocarminio è classicamente descritto come colorante acido |
| `teoria-epiteli-001` | il pannello a della tavola dei tre epiteli è dato per **pancreas**, ma mostra una cavità piena di materiale eosinofilo omogeneo circondata da un solo strato di cellule cubiche, cioè un follicolo (tiroideo o ovarico); il pancreas esocrino è ad acini sierosi. L'epitelio resta comunque monostratificato cubico |
| `teoria-staminali-045` | dà la totipotenza per conservata «fino allo stadio di circa otto cellule», mentre il riquadro non trattato della **stessa pagina 17** la dà «fino allo stadio di circa 16 cellule». La carta tiene la versione del testo in tondo, che è quella trattata e anche quella classica |
| `teoria-staminali-088` | definisce l'epidermolisi bollosa **distrofica** come quella in cui «la mutazione è a livello **giunzionale**», due righe dopo aver elencato il tipo **giunzionale** come categoria a sé e dopo aver attribuito la forma distrofica al **collagene di tipo VII**. Lo schema di pagina 26 disegna DEB al livello del collagene VII, sotto la lamina densa, e JEB a quello della laminina 332: sono due piani diversi |
| `teoria-staminali-092` | colloca il **limbus**, e con esso la nicchia delle staminali limbari, «al confine tra l'**iride** e la sclera»; il limbus è classicamente la giunzione **corneo-sclerale**, che è anche la sola lettura coerente con il fatto che quella nicchia rigeneri l'**epitelio corneale**, come la frase successiva della dispensa stessa dice |
| `teoria-staminali-096` | attribuisce l'immunodeficienza di ADA-SCID e SCID-X1 alla «mancanza delle cellule che combattono le infezioni (**cellule B**)»; SCID sta per immunodeficienza **combinata** grave e il difetto riguarda classicamente sia i linfociti T sia i B, con il blocco anzitutto sui T nella SCID-X1. Lo schema della stessa pagina 27 mostra la ricostituzione di **tutte le linee linfoidi** |
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
| `teoria-endocrino-019` | a pagina 94 le catecolamine sono classificate fra i derivati dell'**acido arachidonico**; a pagina 98, nella seconda stesura della stessa lezione, sono ricondotte alla **fenilalanina e alla tirosina**, che è la via classica. La carta tiene la seconda versione |
| `teoria-endocrino-022` | il testo di pagina 95 e 98 dà gli **steroidei** come gli unici ormoni capaci di attraversare la membrana, ma la figura di pagina 98 disegna anche gli **ormoni tiroidei** diretti al recettore citoplasmatico, e pagina 105 dice che i recettori di T3 sono proteine nucleari |
| `teoria-endocrino-063` | chiama la **prolattina** "PRH", e poche righe dopo usa la stessa sigla per l'ormone ipotalamico che la stimola; la sigla della prolattina è PRL, come riporta la figura 13.21 della stessa dispensa |
| `teoria-endocrino-074` | attribuisce alla **calcitonina** l'aumento dell'assorbimento intestinale di calcio, nella stessa frase in cui dice che riduce la calcemia; la figura 13.24 della stessa pagina le attribuisce il deposito di calcio nelle ossa e la riduzione dell'assorbimento renale, e mette l'assorbimento intestinale sul lato del paratormone |
| `teoria-endocrino-081` | fa secernere all'ipotalamo la **somatostatina insieme al TRH** quando gli ormoni tiroidei calano, e la fa poi ridurre insieme al TRH quando risalgono; la somatostatina inibisce il rilascio di TSH e dovrebbe quindi muoversi in senso opposto |
| `teoria-endocrino-085` | dà gli ormoni tiroidei per legati a **TBG e albumina** perché poco solubili in acqua, mentre pagina 98 dice che i derivati da amminoacidi viaggiano liberi "grazie alla loro solubilità". È l'altro punto in cui le due stesure si contraddicono; qui la versione corretta è quella di pagina 105 |
| `teoria-endocrino-103` | contrappone la rapidità della midollare del surrene all'asse ipotalamo-ipofisi-**gonadi**; il termine di paragone atteso, e quello che il paragrafo successivo usa, è l'asse ipotalamo-ipofisi-**corticale**, cioè l'altra metà della stessa ghiandola |
| `teoria-colorazioni-080` | conclude che l'Alcian Blu, che lega i glicosaminoglicani, permette "di colorare il collagene"; è un colorante cationico dei GAG e dei mucopolisaccaridi acidi, cioè della sostanza fondamentale, mentre il collagene si colora con le tricromiche |
| `teoria-connettivi-041` | mette l'integrina α6β4 "nei contatti focali e negli emidesmosomi"; il capitolo 06 della stessa dispensa la dà come l'integrina del solo **emidesmosoma**, dove lega la laminina 332, e attribuisce alle adesioni focali integrine che legano la fibronectina |
| `teoria-connettivi-054` | la dispensa dà tre diametri diversi per la fibra collagene nel giro di due pagine: "fino a 10 micrometri" (p. 116), "può raggiungere i 300 nanometri" (p. 117, che è però il valore della fibrilla dato tre righe dopo) e "3-4 micron" (p. 118). La figura di pagina 117 dice 0,5-3 µm |
| `teoria-connettivi-066` | i geni delle catene alfa del collagene sono "29" a pagina 116 e "42 geni distinti" a pagina 119; il numero delle molecole identificate (29) resta invece lo stesso |
| `teoria-connettivi-082` | chiama "desmina" e "isodesmina" gli amminoacidi che formano i legami crociati dell'elastina; la figura della stessa pagina 122 li chiama **desmosina** e li fa derivare da lisina e allisina, mentre la desmina è un filamento intermedio del muscolo |
| `teoria-connettivi-088` | dichiara colorata in ematossilina-eosina una sezione di derma in cui le fibre elastiche sono **nere**, il che è tipico delle colorazioni specifiche per l'elastico; la pagina precedente aveva appena detto che in ematossilina-eosina le fibre elastiche non sono facilmente distinguibili |
| `teoria-connettivi-090` | per spiegare il coinvolgimento cardiovascolare nella sindrome di Marfan dice che la fibrillina non è "presente nelle arterie"; due pagine prima aveva detto che le fibre elastiche della parete dei vasi, fatte di elastina e fibrillina, sono prodotte dalle cellule muscolari lisce |
| `teoria-connettivi-108` | subito dopo aver detto che i macrofagi derivano dai **monociti**, li mette in una famiglia di fagociti "derivanti dal mastocito", e inserisce il mastocito nell'elenco insieme a osteoclasto, cellule di Kupffer e microglia |
| `teoria-colorazioni-084` | chiama il blu di anilina "colorante acidofilo"; è un **colorante acido**, mentre acidofilo è il collagene che lo lega. La distinzione era già stata fatta nel capitolo sulle colorazioni |
| `teoria-cartilagine-020` | dà agli aggregati di proteoglicani "dimensioni visibili, talvolta fino a 0,5 cm di lunghezza"; la figura al microscopio elettronico della stessa pagina mostra un aggregato accanto a una barra di scala di 300 nm, cioè lungo qualche micrometro, che è anche il valore classico |
| `teoria-cartilagine-050` | spiega la diversa colorazione delle zone della matrice con il "diverso peso delle molecole", e attribuisce la capsula alle sole glicoproteine adesive; tre pagine prima la stessa dispensa la spiegava con la carica (il blu è basico e si lega ai GAG solforati acidi), che è il criterio giusto. È il punto in cui le due stesure della lezione si contraddicono |
| `teoria-cartilagine-055` | dà l'esofago per rivestito da pavimentoso pluristratificato **cheratinizzato**; nell'uomo è classicamente non cheratinizzato. Stesso equivoco di `lab-linfoide-039` sulla tonsilla palatina |
| `teoria-cartilagine-063` | mette i **piccoli bronchi** fra le sedi della cartilagine elastica; la tavola dei tre tipi di pagina 138 elenca per l'elastica orecchio esterno, punta del naso, epiglottide, canale uditivo e cartilagini cuneiformi laringee, e mette trachea e bronchi fra le sedi della **ialina**, come fa anche pagina 146 |
| `teoria-cartilagine-065` | fa arrivare il nutrimento alla cartilagine fibrosa "tramite i fibroblasti"; i fibroblasti sono cellule, non una via di trasporto, e a pagina 141 la stessa dispensa diceva che la fibrocartilagine dell'anello fibroso è nutrita dal nucleo polposo |
| `teoria-cartilagine-069` | descrive l'ernia del disco come la rottura degli anelli di fibre collagene "i quali fuoriescono"; classicamente a erniare attraverso la lacerazione dell'anulus è il **nucleo polposo**, ed è quello a comprimere le radici nervose |
| `teoria-linfoide-014` | dà le proteine **MHC** per molecole antigeniche che "si trovano sulla superficie di agenti patogeni", e nella frase immediatamente successiva le descrive come le molecole che espongono i frammenti antigenici alle cellule per farli riconoscere dai linfociti T. Le MHC sono classicamente molecole **self**, codificate dal genoma dell'ospite ed espresse dalle sue cellule: è l'antigene a essere di origine patogena, non il presentatore |
| `teoria-linfoide-016` | dà i linfociti B per "noti anche come plasmacellule quando maturi"; il linfocita B maturo è la cellula vergine che esce dal midollo prima di incontrare l'antigene, mentre la plasmacellula è la forma terminale differenziata che compare **dopo** l'attivazione. Stesso equivoco di `lab-linfoide-015` |
| `teoria-linfoide-027` | oppone i capillari linfatici, che si originano "a fondo cieco", a quelli sanguigni, "che sono chiusi"; le due espressioni vogliono dire la stessa cosa. La differenza attesa è che il capillare sanguigno è aperto a entrambe le estremità, in continuità fra arteriola e venula, mentre il linfatico ha un solo capo aperto |
| `teoria-linfoide-043` | definisce l'**essudato** come il materiale che fuoriesce dai capillari "durante processi infiammatori", ma poche righe prima chiama essudato anche il liquido del drenaggio fisiologico che dai capillari passa all'interstizio e da lì ai capillari linfatici; quello è classicamente un **trasudato**, povero di proteine |
| `teoria-linfoide-067` | fa arrivare i **vasi linfatici afferenti** alla zona **midollare** del linfonodo; classicamente sboccano nel **seno sottocapsulare**, e da lì la linfa percola verso l'interno per uscire dall'ilo con il vaso efferente. Lo schema della stessa pagina 204 lo disegna così, e ha "seno sottocapsulare" fra le proprie etichette |
| `teoria-linfoide-068` | colloca le **venule ad alto endotelio** nella rete capillare della **midollare**; sono classicamente descritte nella **paracorticale**, che è la porta d'ingresso dei linfociti circolanti. La dispensa elenca la zona paracorticale fra le tre del linfonodo ma **non la descrive mai**, pur avendone bisogno qui |
| `teoria-linfoide-075` | chiama "**linfonodi** periarteriolari (PALS)" le guaine linfoidi periarteriolari della polpa bianca; la sigla stessa sta per *Periarteriolar Lymphoid Sheath*, cioè **guaina**, e si tratta del manicotto di linfociti T attorno all'arteriola centrale, non di un organo capsulato come i linfonodi descritti nella pagina precedente |
| `teoria-muscolare-005` | a pagina 205 dice che le fibre "in alcuni muscoli possono comporre l'intera lunghezza del muscolo stesso", citando il quadricipite femorale; a pagina 209 dice che **non raggiungono mai** l'intera estensione del muscolo, "neppure nei muscoli più lunghi come il quadricipite femorale". È il punto in cui le due stesure della lezione si contraddicono, e usano lo stesso muscolo come esempio |
| `teoria-muscolare-058` | attribuisce alle **fessure sinaptiche secondarie** il compito di "penetrare profondamente nella cellula, mettendola in contatto con i miofilamenti"; quello è classicamente il compito dei **tubuli T**, che la stessa dispensa descrive correttamente due pagine dopo come "profonde invaginazioni della membrana plasmatica", elencandoli accanto alle fessure secondarie come strutture distinte |
| `teoria-muscolare-069` | dà tubulo T e cisterne terminali per "separate da circa **10 micron**"; è una distanza dell'ordine del diametro dell'intera fibra (10-100 micron secondo la stessa dispensa a pagina 209) e renderebbe impossibile l'accoppiamento fisico fra recettori diidropiridinici e rianodinici descritto due pagine dopo. Il valore classico è dell'ordine dei **10 nanometri**: è verosimilmente uno scambio di unità |
| `teoria-muscolare-093` | definisce l'**endocardio** come "lo strato più interno" della parete cardiaca e lo dice formato da solo tessuto connettivo lasso, per poi descrivere subito dopo un **endotelio ancora più interno** senza dire a quale strato appartenga; classicamente l'endocardio comprende l'endotelio, che ne è la componente più interna |
| `teoria-muscolare-122` | parla di un solo "muscolo dell'iride", il **dilatatore della pupilla**, e fa causare la **miosi** dal suo rilassamento; l'iride ha classicamente **due** muscoli lisci antagonisti, e la miosi è la contrazione attiva dello **sfintere della pupilla**, che la dispensa non nomina mai |
| `teoria-muscolare-127` | dice che desmina e vimentina, filamenti intermedi del muscolo liscio, "svolgono un ruolo simile a quello della **troponina e della tropomiosina**"; sono proteine strutturali, non regolatrici, e due pagine dopo la stessa dispensa dichiara che nel muscolo liscio la **troponina manca del tutto** e che la regolazione avviene per fosforilazione delle teste della miosina |
| `teoria-muscolare-134` | dice che l'**ossitocina favorisce il rilassamento** della tonaca muscolare dell'utero durante il parto; l'ossitocina stimola classicamente la **contrazione** del miometrio, ed è per questo che si usa per indurre il travaglio. L'esempio è per giunta inserito in un paragrafo che sta spiegando come uno stimolo ormonale **inneschi** la contrazione |
| `teoria-sangue-030` | descrive la via classica del complemento come C1 che attiva **C2 e successivamente C4**; nella sequenza classica il C1 attivato taglia prima il **C4** e poi il **C2**, i cui frammenti si associano nella C3-convertasi (C4b2a) |
| `teoria-sangue-044` | dà **5,4 milioni/ml** di eritrociti nell'uomo e 4,8 milioni/ml nella donna; il valore classico è per **microlitro** (mm³), cioè mille volte più concentrato. Espresso per ml, il numero è incompatibile con l'ematocrito del 45% dichiarato dalla stessa pagina precedente |
| `teoria-sangue-060` | dice che nell'incompatibilità Rh, in assenza di interventi, "l'esito è nel **100% dei casi** fatale per il feto", nella frase immediatamente successiva a quella che parla di "rischio molto elevato di aborto o morte fetale". La malattia emolitica del feto e del neonato ha classicamente gravità variabile |
| `teoria-sangue-091` | dice che nelle reazioni allergiche gli eosinofili agiscono "**rilasciando istamina**"; classicamente l'eosinofilo **inattiva** l'istamina con l'istaminasi dei suoi granuli, e a rilasciarla sono basofili e mastociti, come la dispensa stessa dice nella pagina successiva |
| `teoria-sangue-107` | elenca le **cellule NK** fra i sottotipi dei **linfociti T** che "diventano immunocompetenti nel timo", due righe dopo averle distinte dai piccoli linfociti B e T classificandole fra i **grandi linfociti**. Le NK non hanno recettore T e non maturano nel timo |
| `teoria-sangue-114` | mette il **fattore VI** della coagulazione fra i contenuti dei granuli α delle piastrine; un fattore VI non esiste nella nomenclatura corrente (il numero fu assegnato e poi ritirato), e il contenuto classico è fattore V e fattore VIII/von Willebrand |
| `teoria-sangue-115` | chiama **α2β3** l'integrina della membrana piastrinica; l'integrina piastrinica classica è la **αIIbβ3** (GPIIb-IIIa), mentre α2β1 è il recettore del collagene. "α2β3" non corrisponde a nessuna integrina nota |
| `teoria-sangue-132` | dice che il fattore XIa attiva il fattore IX, "**componente essenziale anche della via comune**", ma il paragrafo successivo fa cominciare la via comune dal **fattore X**; il IX appartiene alla sola via intrinseca |
| `teoria-sangue-144` | usa la sigla **CFU-M** per il progenitore **mieloide** comune, mentre a pagina 188 la stessa dispensa usa **M-CFU** per la linea dei soli **monociti**. Nella nomenclatura corrente CFU-M è proprio quest'ultima (*macrophage colony-forming unit*) e il progenitore mieloide comune si indica con CMP |
| `teoria-sangue-160` | dice che il megacariocita poliploide arriva a contenere "fino a **64 cromosomi**"; il valore classico è **64n**, cioè fino a 64 *corredi* (qualche migliaio di cromosomi). Con 64 cromosomi la cellula sarebbe poco più che diploide, e non si spiegherebbero né la poliploidia né le sue dimensioni |
| `teoria-osso-023` | descrivendo la sezione per usura di pagina 151, chiama **osteoni** i canali trasversali visibili in basso: "canali trasversali, gli osteoni, che connettono ciascuna struttura lamellare a quella adiacente". Gli osteoni sono le strutture lamellari stesse; i canali trasversali sono i **canali di Volkmann**, come la stessa dispensa dice a pagina 160 e come stampano le figure di pagina 158 |
| `teoria-osso-037` | a pagina 152 dà l'osso compatto per resistente in **un'unica direzione**, perché le lamelle sono orientate tutte allo stesso modo; a pagina 156, nella seconda stesura della stessa lezione, dice che "la struttura cilindrica degli osteoni è progettata per resistere alle sollecitazioni meccaniche provenienti dalle **diverse direzioni**". È uno dei punti in cui le due stesure si contraddicono |
| `teoria-osso-049` | chiama i **canalicoli** che collegano le lacune "canali trasversali di Voorman". I canali trasversali (di **Volkmann**) collegano invece fra loro i **canali di Havers** e li connettono ai vasi esterni all'osso, come la stessa dispensa dice a pagina 160: sono due strutture diverse, non due nomi della stessa |
| `teoria-osso-050` | fa derivare le **cavità midollari** dai fasci intrecciati di collagene "in seguito alla mineralizzazione" e vi colloca dentro le **lacune ossee** con gli osteociti; la frase immediatamente successiva della stessa pagina dice però che "gli osteociti sono immersi nella matrice ossea mineralizzata", che è dove stanno le lacune |
| `teoria-osso-063` | dà le lamelle circonferenziali interne per "a contatto con il **canale di Havers**" e, nella stessa frase, per quelle che "separano l'osso dalla **cavità midollare** interna". Le due cose non stanno insieme: il canale di Havers è al centro di ogni singolo osteone. Gli schemi di pagina 158 e 159 disegnano le circonferenziali interne al confine con il canale midollare |
| `teoria-osso-074` | dice che le lamelle successive dell'osteone vengono deposte **verso l'interno** del canale, e nella frase dopo che questo rende "il canale di Havers **più grande** man mano che vengono depositate nuove lamelle". Deponendo verso l'interno il lume si restringe, ed è quanto la stessa dispensa dice a pagina 173, dove le lamelle "si dispongono dalla periferia verso il centro" e alla fine "rimane solo una cavità centrale" |
| `teoria-osso-086` | la didascalia della figura dell'endostio elenca fra le sue cellule delle "**cellule epiteliali**", che il testo della stessa pagina non nomina mai; le cellule appiattite dell'endostio sono le **cellule di rivestimento dell'osso**, di origine osteoblastica |
| `teoria-osso-097` | attribuisce agli **osteoblasti** una "forte capacità mitotica"; l'osteoblasto è classicamente una cellula differenziata e secernente, con scarsa o nulla attività proliferativa, ed è la **cellula osteoprogenitrice** a proliferare, come la dispensa stessa lascia intendere chiamandola il precursore che si differenzia "ogni volta che è necessario depositare nuovo osso" |
| `teoria-osso-102` | dice che gli osteociti "non hanno un ruolo primario nel rimodellamento osseo" e che solo "alcuni studi suggeriscono" che ne influenzino il riassorbimento; ma pagina 149 li indica come le cellule che **captano gli stimoli** del rimodellamento, e poche righe sotto sono proprio loro a produrre i **segnali chemiotattici** che attivano gli osteoclasti |
| `teoria-osso-103` | paragona i **100 micron** dell'osteoclasto a "una grandezza simile a quella di cellule come i **monociti**"; il monocita è la più grande cellula del sangue con 15-20 µm, cioè cinque volte meno, e il paragone contraddice la frase stessa, che apre definendo l'osteoclasto una cellula "molto grande" |
| `teoria-osso-134` | fa crescere il **cranio** "principalmente per apposizione, cioè per deposizione di nuovo osso sulla **superficie esterna**" e due frasi dopo dice che "sulla superficie esterna, quella convessa, si verifica un **riassorbimento**" mentre su quella interna avviene la deposizione. Classicamente vale il primo verso: si depone sulla convessa e si riassorbe sulla concava, ed è questo a far ingrandire la volta cranica conservandone la curvatura |
| `teoria-osso-150` | descrive il recettore del **FGF** come quello che "aiuta nell'accrescimento delle ossa", e nella stessa pagina fa causare il **nanismo** da una sua mutazione **attivatoria**. Se aiutasse la crescita, tenerlo acceso darebbe ossa più lunghe; l'FGFR3 è classicamente un **regolatore negativo** della proliferazione dei condrociti |
| `teoria-nervoso-008` | dice che il tessuto nervoso "non è innervato: non sono presenti fibre nervose al suo interno, per cui non percepisce il dolore". La frase si contraddice da sola, perché il tessuto nervoso **è fatto** di fibre nervose; quello che si intende è che il parenchima nervoso è privo di **terminazioni nocicettive proprie** |
| `teoria-nervoso-023` | colloca l'**ipotalamo** "posteriormente al talamo"; la tavola dell'encefalo della stessa pagina 230 lo disegna **al di sotto**, ed è anche ciò che dice il nome |
| `teoria-nervoso-025` | dà il **mesencefalo** per "struttura di collegamento tra il telencefalo e il tronco encefalico", ma la tavola della stessa pagina disegna il tronco encefalico come costituito da **mesencefalo, ponte e midollo allungato**: il mesencefalo farebbe quindi da ponte verso una struttura di cui fa parte |
| `teoria-nervoso-041` | distingue una "via motoria" (organo bersaglio muscolo) da una "via efferente" (organo bersaglio ghiandola), ma una via motoria **è** una via efferente, e la frase successiva della stessa pagina dice che "le vie afferenti ed efferenti possono essere sia somatiche sia viscerali". La contrapposizione attesa è somatico/viscerale, ed è quella che lo schema della stessa pagina disegna |
| `teoria-nervoso-048` | dà l'**adrenalina** per neurotrasmettitore dei neuroni gangliari del simpatico; classicamente è la **noradrenalina**, mentre l'adrenalina è l'ormone che la midollare del surrene riversa nel sangue, come la stessa pagina 234 dice due righe prima |
| `teoria-nervoso-060` | descrive i **neuroni piramidali** della corteccia come "l'ultima porzione delle vie sensoriali"; pagina 235 della stessa dispensa fa partire da loro la **via piramidale**, che è efferente e scende al midollo spinale |
| `teoria-nervoso-102` | spiega l'effetto **eccitatorio** del GABA nello sviluppo embrionale con "l'entrata di cloro" nella cellula; il cloro che entra iperpolarizza sempre, ed è il meccanismo dell'IPSP descritto nella pagina precedente. Classicamente nel neurone immaturo il cloro intracellulare è alto e i canali GABA lo fanno **uscire**, depolarizzando |
| `teoria-nervoso-120` | elenca la **microglia** due volte nello stesso elenco delle origini embrionali: prima fra le gliali del SNC derivate dal **neuroectoderma**, poi come derivata dal **mesoderma** in quanto fagocita mononucleato. La seconda è la versione corretta, ed è quella che la pagina successiva conferma facendola derivare dai progenitori mieloidi |
| `teoria-nervoso-145` | dice che gli astrociti che invadono il sito di lesione "si riattivano e diventano **neurotrofici**", e nella frase successiva che la cicatrice gliale che formano "impedisce fisicamente e chimicamente la ricrescita degli assoni". Classicamente l'astrocita reattivo produce molecole **inibitorie** per la crescita assonale |
| (nessuna carta) | a pagina 4 una microfotografia è didascalizzata "colon" ma mostra tessuto adiposo e vasi: non ne è stata fatta una carta di riconoscimento |

Casi risolti senza tag, perché il refuso è evidente e non c'è dubbio di contenuto:

- la sbobina scrive adiposo "multicolore" per multiloculare (`lab-connettivi-030`);
- a pagine 145 e 146 scrive "piastre **ipofisarie**" per piastre **epifisarie**
  (`teoria-cartilagine-049` e `056`). La stessa dispensa usa il termine giusto a
  pagina 138, dove le definisce "regioni di cartilagine collocate tra le epifisi
  e la diafisi", a pagina 144 e nella didascalia della figura di pagina 146;
- a pagine 151, 152 e 153 scrive "canale trasversale di **Voorman**" per canale
  di **Volkmann**. La stessa dispensa usa il nome giusto a pagina 160, dove
  intitola un paragrafo `Canali di Havers e canali di Volkmann`, e nelle figure
  delle pagine 158, 159 e 160, che lo portano stampato sopra. Resta invece la
  segnalazione `teoria-osso-049`, che non riguarda il **nome** ma la **cosa**;
- a pagina 152 scrive "scheletro inferiore dei vertebrati" per scheletro dei
  **vertebrati inferiori** (`teoria-osso-045`): è un'inversione di parole, ed è
  segnalata in corsivo sulla carta senza tag;
- a pagina 164 intitola un paragrafo "Gli **osteoclasti** come meccanorecettori",
  ma il paragrafo parla per intero degli **osteociti**, come tutto il resto del
  capitolo. È un lapsus di intestazione e non tocca il contenuto;
- a pagina 232 scrive che l'assone del motoneurone dell'arco riflesso "esce dalla
  parte del **cranio** del midollo spinale": lo schema della stessa pagina lo
  chiama `Assone della cellula del **corno anteriore**`, che è la via d'uscita
  attesa (`teoria-nervoso-039`);
- a pagina 242 scrive "recettori accoppiati a **dendriti**" dove a pagina 245
  scrive correttamente "recettori legati alla **proteina G**"
  (`teoria-nervoso-092`);
- a pagina 254 scrive "degenerazione **Welleriana**" per degenerazione
  **walleriana**, da Augustus Waller (`teoria-nervoso-137`).

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

**`extract.py` buttava via figure vere scambiandole per icone. Risolto il
2026-08-11, scrivendo il mazzo 15.** `is_artifact()` scartava ogni immagine con
**un lato sotto `MIN_USEFUL_PX`**, che valeva **200**: su tutta la Teoria ne
perdeva 25 e sul Laboratorio 17. Il sintomo era che una pagina **mostrava** una
figura che `images.jsonl` non elencava affatto, senza nessun avviso.

**La soglia è ora a 100 px.** La modifica è stata fatta test-first, e i due test
nuovi in `tests/test_extract.py` descrivono dove cade il confine e perché:

- `test_keeps_a_small_micrograph_crop`: `is_artifact(122, 122)` e
  `is_artifact(874, 156)` devono essere `False`. 122x122 è il più piccolo
  ritaglio di striscio delle due sbobine (un leucocita fra gli eritrociti,
  `lab_p070_4342`), 874x156 è lo schema dell'eritropoiesi di pagina 197;
- `test_flags_a_formula_rendered_as_an_image`: `is_artifact(282, 56)` deve
  restare `True`. È la **formula dell'apertura numerica** di pagina 54,
  renderizzata come immagine: larga abbastanza ma alta quanto una riga.

Sotto i 100 px restano solo le **icone** (le più grandi sono 35x25, nel
Laboratorio) e le **due formule** di pagina 54 della Teoria. La suite è passata
da 151 a **153 test**.

L'estrazione rigenerata dà **486 immagini** per la Teoria (erano 463) e **235**
per il Laboratorio (erano 222). **I due pacchetti non sono cambiati il giorno
della modifica**: 1301 carte / 302 immagini e 673 carte / 120 immagini,
esattamente come prima, perché `build_apkg` impacchetta solo le immagini
**referenziate** dalle carte. (I numeri di oggi, molto più alti, sono al punto
1: sono cresciuti scrivendo i capitoli, non abbassando la soglia.)

**Le figure recuperate, e dove sono finite** (il follow-up è **chiuso**: tutte e
quindici sono state guardate e decise):

| Dove | Figure | Stato |
|---|---|---|
| p. 7 (mazzo 02), p. 13 (03), p. 42 (06), p. 53, 56, 57 ×2, 58 (07), p. 125 (12), p. 148 (13) | 10 | **chiuse**, con **una carta nuova, otto figure su carte esistenti e due scarti**: vedi qui sotto |
| p. 16, 19 ×2, 21 (mazzo 04) | 4 | **recuperate davvero**: il 04 le ha guardate una per una e le ha usate tutte e quattro |
| p. 165 (mazzo 14) | 1 | **falso positivo**, vedi qui sotto |

*Attenzione*: una stesura precedente di questo piano dava tutte e quindici per
"in capitoli già scritti". Non era così: quattro stavano in un capitolo ancora
da fare, ed è quello che le ha usate.

**Le dieci, una per una.** Le prime quattro erano già state campionate chiudendo
il progetto; le altre sei sono state guardate dopo, insieme alle pagine
renderizzate che le contengono. L'esito è **più basso di quanto il piano
lasciasse sperare**, ma non nullo:

| File | Che cos'è | Dove è finita |
|---|---|---|
| `teoria_p148_1016` (329x161) | il **disco intervertebrale** in sezione longitudinale, con i richiami muti `V`, `NP`, `AF` | **carta nuova sul fronte**, `teoria-cartilagine-071`: è l'unica delle dieci a valerne una |
| `teoria_p007_21` (226x173) | micrografia di **cripte intestinali in Alcian blu**, **senza alcuna etichetta** | **fronte** di `teoria-colorazioni-033` |
| `teoria_p013_46` (186x156) | **sezione trasversale di nervo**, **senza alcuna etichetta** | **fronte** di `teoria-nervoso-002` |
| `teoria_p042_279` (165x411) | ME delle **interdigitazioni laterali**, didascalia del libro **stampata sopra** | **retro** di `teoria-epiteli-122` |
| `teoria_p057_406` (342x148) | schema del **campo chiaro**, `Source`/`Translucent Sample`/`Detector` stampati sopra | **retro** di `teoria-microscopia-066` |
| `teoria_p057_408` (338x196) | cellule vive in **campo chiaro e contrasto di fase**, titolo stampato sopra | **retro** di `teoria-microscopia-072` |
| `teoria_p058_417` (460x182) | i due **spettri** di eccitazione ed emissione, etichette stampate sopra | **retro** di `teoria-microscopia-080` (Stokes shift) |
| `teoria_p125_906` (232x196) | micrografia di **macrofagi**, scritta `Macrofagi` **stampata sopra** | **retro** di `teoria-connettivi-109` |
| `teoria_p053_371` (678x112) | la **formula** `M_tot = M_obiettivo × M_oculari` | **scartata**: non è una figura |
| `teoria_p056_398` (1200x132) | la **tabella** degli spessori del coprioggetto | **scartata**: il testo del `07` la copre già |

Due delle dieci **non sono figure**, ed è lo stesso caso che il test
`test_flags_a_formula_rendered_as_an_image` descrive: larghe abbastanza ma alte
quanto una riga. La soglia a 100 px non le prende perché hanno **entrambi** i
lati sopra i 100. L'euristica del **rapporto d'aspetto** ha funzionato: le due
più allungate (6,05 e 9,09) sono gli scarti, e le tre meno allungate (1,18,
1,19, 1,31) sono le tre micrografie senza etichette.

**Perché una sola carta nuova, e non tre.** Il criterio delle immagini decide
dove va la figura, non se serva una carta: sei delle otto figure usate
illustrano un fatto che una carta **già copriva**, e per quelle la cosa giusta è
attaccare l'immagine, non scriverne una nuova. Due casi meritano di essere
ricordati perché la decisione non era obbligata:

- `teoria_p007_21` era data da questo piano per «una carta nuova, sul fronte».
  Non lo è diventata: `teoria-colorazioni-033` era **già** una carta
  `tipo::riconoscimento` («che cosa si colora di blu e che cosa di rosso?») a cui
  mancava solo la cosa da riconoscere. Una carta nuova ne sarebbe stata una
  **parafrasi**, cioè esattamente il doppione che il validatore **non**
  intercetta, perché blocca solo le domande identiche. Stesso ragionamento per
  `teoria_p013_46` e `teoria-nervoso-002`;
- `teoria_p042_279` sembra la figura di `teoria-epiteli-095`, che parla di
  interdigitazioni, e invece no: la `095` descrive quelle del dominio **basale**,
  mentre la figura sta a pagina 42 sotto il titolo «Specializzazioni morfologiche
  della superficie **laterale**». È andata su `teoria-epiteli-122`, che è la
  carta di quel paragrafo.

Un'ultima osservazione, che vale se un giorno si toccasse il clip path: la
figura di pagina 42 è uno dei casi in cui **la pagina mostra meno del file**. Il
documento ritaglia via la striscia di didascalia `Figura 5.24 ■ Interdigitazioni
laterali della membrana plasmatica`, che sulla pagina non si vede e nel file c'è.
È il motivo per cui va sul retro e non sul fronte: quello che conta è **il file
che finisce sulla carta**, non quello che si vede sulla pagina.

**Il bilancio dell'abbassamento della soglia si può ora chiudere del tutto.** Ha
fruttato in tre capitoli su quattro: otto figure al `15` (fra cui lo schema
dell'eritropoiesi e cinque strisci da fronte), quattro al `04` (fra cui lo
schema delle tre modalità di divisione con i loro contesti biologici, la figura
più utile di quel mazzo) e **otto sparse** nei capitoli già scritti, di cui però
**una sola** ha prodotto una carta. Al `14` non ha fruttato niente, perché la
sua unica candidata non era una figura. La lezione, per una prossima modifica
degli strumenti: **recuperare figure in un capitolo ancora da scrivere rende
molto più che recuperarle in uno già scritto**, perché lì il testo ha già una
carta per ogni fatto e alla figura resta solo il ruolo di illustrazione.

**La quindicesima non era una figura.** `teoria_p165_1091` (301x138) è stata
guardata scrivendo il mazzo 14 ed è uno dei **rettangoli colorati sovrapposti**
allo schema dell'osteoclasto di pagina 165, quello blu che marca la regione
basolaterale: il file estratto è un rettangolo **nero con il bordo blu**, e la
correlazione con la pagina è −0,49. È stata scartata. Il capitolo 14 **non ha
guadagnato nulla** dall'abbassamento della soglia: ci si aspettava il contrario,
e vale la pena ricordarlo prima di ricontrollare gli altri capitoli.

Per ritrovare le immagini che una soglia scarta, il modo è questo (con `< 100`
al posto di `< 200` per verificare che cosa resta fuori oggi):

```sh
./venv/bin/python -c "
import pymupdf
d = pymupdf.open('\$DL/Istologia 5th gen-combinato.pdf')
seen = set()
for pno in range(1, d.page_count + 1):
    for info in d[pno - 1].get_images(full=True):
        x = info[0]
        if x in seen: continue
        seen.add(x)
        r = d.extract_image(x)
        w, h = r['width'], r['height']
        if (w < 200 or h < 200) and w >= 100 and h >= 100:
            print(f'p{pno} xref{x} {w}x{h}')"
```

**Il capitolo più colpito era di gran lunga il `15 - Il sangue`**, con **otto**
figure perse fra pagina 177 e pagina 198, perché le sue illustrazioni sono
ritagli piccoli di striscio: fra queste lo **schema dell'eritropoiesi** e cinque
strisci senza etichette, cioè materiale da **fronte**. È il motivo per cui la
soglia è stata abbassata proprio lì, e non prima.

**Abbassare la soglia è additivo e non rompe niente di pubblicato**, ed è la
differenza con la trappola del clip path qui sotto: il nome del file è
`teoria_pNNN_XREF.jpg`, quindi rigenerare **aggiunge** file senza rinominare né
modificare quelli esistenti, e nessuna carta già consegnata a Pietro cambia. Il
clip path invece cambierebbe il **contenuto** di file già referenziati, e andava
perciò fatto prima di scrivere le carte, **non dopo**. È l'unica modifica a
`extract.py` mai fatta, ed è ormai troppo tardi perché convenga: vedi la
raccomandazione in fondo a questo punto e a quello 4.

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

**Lo stesso sbobinatore ricompare nel capitolo 17**: alle pagine 222-226 sono
altre nove finestre di Safari, riconoscibili a colpo d'occhio perché hanno tutte
la **stessa dimensione, 1600x1041**, e la stessa fila di schede in alto. Se in un
capitolo compaiono più file estratti con dimensioni identiche e correlazione
prossima a zero, sono quasi certamente questo caso. **Nel 18 non ricompare**,
benché il capitolo segua immediatamente il 17: gli sbobinatori sono altri e le
loro figure sono quasi tutte scansioni di libro, tanto che il controllo del clip
path sulle pagine 227-256 ha segnalato **due placement su 47**, nessuno dei
quali è una finestra di browser. Prima di scartarli **guardali
comunque**: fra quelli del 17 c'era lo schema riassuntivo per il riconoscimento
dei vetrini annunciato da un `[N.d.S.]`, cioè materiale d'esame che nel testo
estratto non compare affatto e che è stato recuperato leggendolo dallo
screenshot. Si scarta l'immagine, non il contenuto.

**Nei mazzi 04 e 05 non ricompare**, e il controllo sulle pagine 16-27 non ha
segnalato **nemmeno un placement su 22**, con correlazione minima 0,96: è
l'esito migliore di tutta la Teoria, e chiude il conto. Su tutto il progetto il
problema si è concentrato in **due soli sbobinatori**, quelli dell'`08` e del
`17`.

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
fonti, quindi andava fatto prima di scrivere le carte, non dopo.

**Ora è dopo, e la raccomandazione è di non farlo.** Il perché sta in fondo al
punto 4, sotto "Il progetto è finito": le carte ci sono tutte, le ventuno figure
che il clip path recupererebbe sono già state scartate a ragion veduta, e il
loro contenuto, dove valeva qualcosa, è stato trascritto a mano.
