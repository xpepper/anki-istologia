# Mazzi Anki di Istologia dalle sbobine

Data: 2026-08-10
Stato: approvato

## Obiettivo

Trasformare due sbobine di Istologia (A.A. 2024/2025) in mazzi Anki `.apkg` pronti da
importare, ad alta densita di copertura e con le immagini dei vetrini incluse.

## Materiale sorgente

| | `Istologia 5th gen-combinato.pdf` | `Istologia Laboratorio combinato.pdf` |
|---|---|---|
| Pagine | 256 | 106 |
| Parole | ~98.400 | ~24.500 |
| Livello di testo | presente ed estraibile | presente ed estraibile |
| Immagini uniche | 488 (292 MB) | 239 (281 MB) |
| Particolarita | | contiene sezioni "Domande e risposte dei quiz" |

Entrambi i file sono in `/Users/pietrodibello/Downloads/`. Non vengono modificati:
il progetto li tratta come sola lettura.

## Decisioni prese

1. **Consegna in `.apkg`** costruiti con genanki, non file di testo da importare a mano.
2. **Mix di carte Base e Cloze**: domanda/risposta per definizioni, funzioni e confronti;
   cloze per elenchi, sequenze e dettagli interni a una frase.
3. **Alta densita**: copertura sistematica del contenuto, stima 1.200-1.800 carte totali.
4. **Immagini incluse fin da subito**, con triage per categoria (sotto).
5. **Laboratorio per primo**, perche e piu corto e contiene i quiz gia pronti: permette di
   correggere lo stile delle carte prima di investire sulle 256 pagine di teoria.

## Architettura

### Struttura

```
anki-istologia/
  scripts/     estrazione, segmentazione, validazione, build
  build/       artefatti generati (git-ignored)
  cards/       le carte, in JSONL, una carta per riga
  dist/        i .apkg finali (git-ignored)
  tests/       test del pipeline
```

`build/` e `dist/` sono ignorati da git: sono rigenerabili dagli script e dal contenuto di
`cards/`. Quello che va versionato e il lavoro intellettuale, cioe le carte e gli script.

### Stadio A: estrazione

`scripts/extract.py` produce, per ogni PDF:

- `build/<fonte>/pages.jsonl`: una riga per pagina con il testo e, per ogni blocco, la
  dimensione e il peso del font. Le informazioni sul font servono a ricostruire la gerarchia
  dei titoli, che nel testo piatto andrebbe persa.
- `build/<fonte>/images/<fonte>_p<pagina>_<xref>.jpg`: immagini ridimensionate a max 1000px
  e ricodificate in JPEG q78. Misurato su un campione di 120 immagini: 573 MB complessivi
  scendono a circa 52 MB, dimensione accettabile per un mazzo Anki e per la sincronizzazione.
- `build/<fonte>/images.jsonl`: per ogni immagine, pagina di origine, dimensioni e il testo
  circostante, che nelle sbobine funge da didascalia.

I nomi dei file immagine sono deterministici, cosi rieseguire l'estrazione non cambia i
riferimenti gia scritti nelle carte.

### Stadio B: segmentazione

`scripts/segment.py` produce `build/<fonte>/sections.jsonl`, dividendo il materiale in unita
di lezione e sezioni tramite:

- i marcatori `SBOBINATORI:` e `data lezione:` che separano le lezioni
- la gerarchia dei titoli ricavata dalle dimensioni di font dello stadio A

Ogni sezione porta con se: identificativo, titolo, livello, pagine coperte, testo e immagini
associate. Una sezione e l'unita di lavoro dello stadio C e corrisponde a un sottomazzo.

### Stadio C: scrittura delle carte

Questo stadio non e automatizzabile: e lettura e comprensione del contenuto, fatta sezione
per sezione. Per ogni sezione: leggere il testo, guardare le immagini di quelle pagine,
scrivere le carte in `cards/<mazzo>/<NNN>-<slug>.jsonl`.

**Triage delle immagini.** Ogni immagine finisce in una di tre categorie:

| Categoria | Trattamento | Motivo |
|---|---|---|
| Microfotografia senza etichette | immagine sul **fronte**, carta di riconoscimento | la domanda "che tessuto e?" ha senso solo se la risposta non e visibile |
| Schema con etichette gia stampate | immagine sul **retro** di una carta testuale | l'etichetta nell'immagine rivelerebbe la risposta |
| Icona, logo, artefatto di layout | scartata | nessun valore didattico |

**Schema di una carta** (una riga JSONL):

```json
{
  "id": "hash stabile del contenuto",
  "type": "basic",
  "deck": "Istologia::Laboratorio::02 - Tessuti epiteliali",
  "front": "...",
  "back": "...",
  "text": "... {{c1::...}} ...",
  "extra": "...",
  "images": ["lab_p42_280.jpg"],
  "image_side": "front",
  "tags": ["fonte::lab", "argomento::epiteli", "tipo::riconoscimento"],
  "source": "Laboratorio p. 42"
}
```

`front`/`back` valgono per `type: basic`; `text`/`extra` per `type: cloze`.

### Stadio D: validazione e build

`scripts/validate.py` verifica:

- presenza dei campi obbligatori per il tipo di carta
- sintassi cloze: ogni carta cloze contiene almeno un `{{c1::...}}` ben formato
- assenza di duplicati sul fronte
- esistenza sul disco di ogni file immagine referenziato
- HTML ben formato nei campi

`scripts/build_apkg.py` trasforma JSONL e media in `.apkg`.

## Formato delle note

Due tipi di nota personalizzati, con ID di modello fissi nel codice:

| Tipo | Campi |
|---|---|
| `Istologia Base` | Fronte, Retro, Immagine, Fonte |
| `Istologia Cloze` | Testo, Note, Immagine, Fonte |

Il campo **Fonte** riporta sempre documento e pagina (es. `5th gen p. 42`), cosi ogni carta
resta tracciabile all'originale quando qualcosa non torna.

**GUID deterministici.** Il GUID di ogni nota deriva da un hash del suo contenuto. E il
dettaglio che conta di piu nell'uso quotidiano: rigenerando i mazzi dopo una correzione e
reimportandoli, Anki aggiorna le carte esistenti invece di duplicarle, e lo storico di
ripetizione non va perso.

## Mazzi e tag

```
Istologia::Teoria::01 - Tecniche istologiche
Istologia::Teoria::02 - Microscopia
...
Istologia::Laboratorio::01 - Colorazioni
...
Istologia::Laboratorio::Quiz
```

Tag su tre assi indipendenti:

- `fonte::teoria`, `fonte::lab`
- `argomento::epiteli`, `argomento::connettivo`, ...
- `tipo::riconoscimento`, `tipo::definizione`, `tipo::classificazione`

I tag permettono selezioni trasversali (per esempio solo il riconoscimento dei vetrini)
senza dover riorganizzare i mazzi.

## Fedelta alla fonte

Le sbobine sono trascrizioni redatte da studenti e possono contenere errori.

**Regola: restare fedeli alla sbobina, senza correggere in silenzio.** Se un passaggio
sembra sbagliato o ambiguo, la carta viene comunque prodotta, ma con tag `da-verificare` e
una nota nel campo Note o Retro. Cosi il dubbio e visibile e verificabile sul libro, invece
di restare nascosto fino all'esame.

## Verifica

- test automatici sulle parti deterministiche: regole del validatore, parsing dei cloze,
  stabilita dei GUID, compressione delle immagini
- test end-to-end: costruire un `.apkg`, riaprirlo leggendo il database sqlite interno,
  verificare numero di note e presenza dei media
- controllo umano: import del primo mazzo in Anki e feedback sullo stile delle carte

## Consegna incrementale

Il volume e reale: circa 1.200-1.800 carte da 123.000 parole, piu il triage di 727 immagini.
E un lavoro di piu sessioni. Per questo la consegna e incrementale:

1. **Milestone 1**: pipeline completa piu tutto il Laboratorio (106 pagine, quiz inclusi).
   Import e feedback sullo stile.
2. **Milestone 2**: applicazione del feedback, poi la Teoria in circa 8 blocchi, con `.apkg`
   aggiornato e commit a ogni blocco.

## Rischi

| Rischio | Mitigazione |
|---|---|
| Errori presenti nella sbobina propagati nelle carte | tag `da-verificare`, campo Fonte con la pagina |
| Peso dei media eccessivo | ridimensionamento a 1000px e JPEG q78, misurato a ~52 MB |
| Reimport che duplica le carte e azzera lo storico | GUID deterministici derivati dal contenuto |
| Volume che rende il lavoro interminabile | consegna a blocchi, ognuno usabile da solo |
