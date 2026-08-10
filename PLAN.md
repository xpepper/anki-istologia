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

./venv/bin/python -m pytest tests/ -q          # atteso: 138 passed
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
```

---

## 2. Stato al 2026-08-10

**329 note**, 34 immagini, 138 test verdi.

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
| `08c-quiz-nervoso.jsonl` | 24 | generato, pagine 92-95 |

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
il caso d'uso per cui il guid è costruito così.

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
| `argomento::` | `colorazioni`, `epiteli`, `ghiandole`, `endocrino`, `connettivi`, `nervoso` |
| `tipo::` | `definizione`, `classificazione`, `elenco`, `sequenza`, `riconoscimento`, `confronto`, `quiz` |
| segnalazione | `da-verificare` |

Riusa i valori esistenti prima di inventarne di nuovi: i tag servono a Pietro per
studiare in trasversale, e un sinonimo in più rompe la selezione.

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

L'ordine è pensato per consegnare valore prima e per lasciare i capitoli lunghi
quando le convenzioni sono ormai rodate.

### Laboratorio

| # | Lavoro | Sezione | Pagine | Parole | Note |
|---|---|---|---|---|---|
| 1 | Tessuto osseo | 019 | 57-76 | 4.260 | il più lungo, conviene spezzarlo |
| 2 | Tessuto muscolare | 020 | 76-78 | 585 | |
| 3 | Tessuto nervoso e SNP | 021-022 | 78-92 | 3.700 | |
| 4 | Embriologia | 024-025 | 96-98 | 706 | |
| 5 | Modellini embriologia | 026 | 98-106 | 2.088 | |
| 6 | Tonsilla palatina | 027 | 106 | 230 | |

Il tessuto osseo è il capitolo più lungo del Laboratorio e conviene aprirlo a
inizio sessione, quando c'è contesto disponibile per leggerlo tutto e guardare
le sue 29 immagini.

I quiz del Laboratorio sono **tutti fatti**. Se ne emergessero altri, il
generatore gestisce già le tre convenzioni di marcatura.

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

Quattro carte taggate, più una figura scartata senza produrre carta. Vale la pena
rileggerle prima di scriverne di nuove, per calibrare quanto è alta l'asticella.

| Carta | Cosa non torna |
|---|---|
| `lab-epiteli-031` | la sbobina scrive cavità "portorie", termine inesistente, con ogni probabilità per cavità sierose |
| `lab-esocrino-033` | porta le ghiandole di Cowper come esempio di ghiandola intraepiteliale; le bulbouretrali non lo sono, l'esempio atteso sono le ghiandole di Littré |
| `lab-endocrino-014` | attribuisce il testosterone ai tubuli seminiferi invece che alle cellule di Leydig, gli estrogeni al corpo luteo invece del progesterone, e classifica il corpo luteo fra le interstiziali dopo averlo messo fra quelle a cordoni solidi |
| `lab-connettivi-037` | descrive la giunzione miotendinea come formata da cartilagine ialina; è classicamente un'interdigitazione fra membrana delle fibre muscolari e collagene, la fibrocartilagine sta semmai all'entesi |
| (nessuna carta) | a pagina 4 una microfotografia è didascalizzata "colon" ma mostra tessuto adiposo e vasi: non ne è stata fatta una carta di riconoscimento |

Casi risolti senza tag, perché il refuso è evidente e non c'è dubbio di contenuto:
la sbobina scrive adiposo "multicolore" per multiloculare (`lab-connettivi-030`).

---

## 6. Trappole note

**Le didascalie estratte sono inaffidabili.** `caption_for_image` prende il blocco
di testo più vicino sotto la figura, che spesso è prosa qualsiasi. Su 222 immagini
del Laboratorio solo 94 hanno una didascalia, e non tutte sono corrette. Servono
come indizio, non come verità: guarda l'immagine.

**Le risposte dei quiz non sono nel testo.** Sono marcate graficamente, in tre
modi diversi a seconda della lezione. `scripts/quiz.py` le gestisce tutte e tre e
solleva `AmbiguousCheckbox` invece di indovinare quando il segnale non è chiaro.
Se una nuova sezione di quiz esce con zero risposte, quasi certamente usa una
quarta convenzione: renderizza la pagina e guardala prima di modificare le soglie.

**Il validatore considera l'immagine parte della domanda.** Molte carte di
riconoscimento hanno lo stesso fronte ("Che epitelio è questo?") e sono distinte
solo dalla figura. Se compare un errore di domanda duplicata su carte che hanno
davvero immagini diverse, il bug è altrove.

**La cwd della shell si resetta fra un comando e l'altro.** Usa percorsi assoluti
o prefissa `cd /Users/pietrodibello/tools/anki-istologia &&`.

**Le sezioni si sovrappongono ai bordi.** `images_for_section` assegna per
intervallo di pagine, quindi una figura a cavallo di due sezioni compare in
entrambe. Va scelta a giudizio, non usata due volte.
