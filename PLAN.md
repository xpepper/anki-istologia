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

## 2. Stato al 2026-08-10

**673 note**, 120 immagini, 151 test verdi. **Il Laboratorio è finito**: tutte
e 106 le pagine sono coperte. Resta solo la Teoria.

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

**Non iniziata.** Nessun file in `cards/teoria/`.

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
| `argomento::` | `colorazioni`, `epiteli`, `ghiandole`, `endocrino`, `connettivi`, `cartilagine`, `osso`, `sangue`, `linfoide`, `muscolare`, `nervoso` |
| `tipo::` | `definizione`, `classificazione`, `elenco`, `sequenza`, `riconoscimento`, `confronto`, `quiz` |
| segnalazione | `da-verificare` |

Riusa i valori esistenti prima di inventarne di nuovi: i tag servono a Pietro per
studiare in trasversale, e un sinonimo in più rompe la selezione.

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

Resta la sola Teoria. L'ordine dei suoi capitoli è ancora da scegliere: vale il
criterio usato finora, consegnare valore prima e lasciare i capitoli lunghi
quando le convenzioni sono rodate.

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

Non iniziata: 111 sezioni, 98.000 parole, 463 immagini. I 15 capitoli sono:

| Pagine | Capitolo |
|---|---|
| 7 | Colorazioni istochimiche |
| 24 | Applicazioni terapeutiche delle cellule staminali |
| 28 | Tessuti epiteliali |
| 49 | Concetti base di microscopia |
| 60 | Epitelio di rivestimento |
| 85 | Epiteli ghiandolari |
| 86 | Ghiandole esocrine |
| 97 | Ghiandole endocrine |
| 111 | Tessuti connettivi |
| 137 | Tessuti connettivi di sostegno |
| 149 | Tessuto osseo |
| 177 | Il sangue |
| 198 | Sistema linfatico |
| 208 | Tessuto muscolare striato scheletrico |
| 227 | Il tessuto nervoso |

Le pagine indicate sono quelle del titolo di capitolo; l'estensione reale di ogni
sezione sta in `build/teoria/sections.jsonl`.

Attenzione: la teoria ripete argomenti già coperti dal Laboratorio, ma da un
punto di vista diverso (meccanismi invece che riconoscimento al vetrino). Non è
duplicazione da evitare, sono due tagli complementari. Il validatore blocca solo
i duplicati esatti dentro lo stesso mazzo.

### Ritmo di consegna

Un capitolo per volta: scrivere le carte, `build_apkg` (che valida), commit.
Ogni capitolo committato è un incremento che Pietro può già importare.

---

## 5. Segnalazioni `da-verificare` già trovate

Tredici carte taggate, più due figure scartate senza produrre carta. Vale la pena
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

**Le sezioni si sovrappongono ai bordi.** `images_for_section` assegna per
intervallo di pagine, quindi una figura a cavallo di due sezioni compare in
entrambe. Va scelta a giudizio, non usata due volte.
