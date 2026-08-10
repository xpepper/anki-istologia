# Mazzi Anki di Istologia

Flash card generate dalle sbobine di Istologia e Laboratorio di Istologia, A.A. 2024/2025.

I mazzi pronti da importare stanno in `dist/`.

---

## 1. Installare Anki

Anki è gratuito su computer. Si scarica da un solo posto:

**https://apps.ankiweb.net**

**Windows.** Scarica il file `.exe` e installalo normalmente. Se Windows mostra un avviso
SmartScreen, scegli "Ulteriori informazioni" e poi "Esegui comunque": succede perché
l'installer non è firmato a pagamento, non perché ci sia un problema.

**macOS.** Il sito propone due versioni. Scegli quella giusta per il tuo Mac:

- **Apple Silicon** se hai un Mac con chip M1, M2, M3 o successivi
- **Intel** se hai un Mac più vecchio

Se non sai quale hai: menu Apple in alto a sinistra → "Informazioni su questo Mac" → guarda
la voce "Chip" o "Processore". Scaricato il `.dmg`, trascina Anki nella cartella Applicazioni.
Al primo avvio, se macOS blocca l'app, tasto destro sull'icona → "Apri".

**Sul telefono.** Utile per ripassare nei momenti morti, ma non indispensabile.

- **Android**: AnkiDroid, gratuito sul Play Store
- **iPhone e iPad**: AnkiMobile, a pagamento sull'App Store (è il modo con cui gli sviluppatori
  finanziano il progetto, visto che tutto il resto è gratis)

Per sincronizzare computer e telefono serve un account gratuito su https://ankiweb.net.
Crea l'account, poi in Anki premi **Sincronizza** e inserisci le credenziali.

---

## 2. Importare i mazzi

1. Apri Anki
2. **File → Importa**, oppure fai semplicemente doppio clic sul file `.apkg`
3. Scegli il file, per esempio `dist/Istologia-Laboratorio.apkg`
4. Conferma

I mazzi compaiono annidati sotto un mazzo padre `Istologia`. Clicca il `+` accanto al nome
per espandere e vedere i sottomazzi.

### Reimportare una versione aggiornata

Puoi reimportare lo stesso mazzo aggiornato tutte le volte che vuoi. Le carte che hai già
studiato **vengono aggiornate sul posto**, non duplicate, e il tuo storico di ripetizione
resta intatto. Le carte nuove si aggiungono e basta.

Questo funziona perché ogni carta porta un identificativo stabile. È il motivo per cui puoi
segnalare un errore e ricevere il mazzo corretto senza ricominciare da capo.

### "Ci sono solo 19 carte nuove, dove sono le altre?"

Ci sono tutte. Anki di default ti propone al massimo **20 carte nuove al giorno**: è un limite
di studio, non la dimensione del mazzo. Come alzarlo è spiegato qui sotto.

### Passare il mazzo a qualcun altro

Manda il file `.apkg` che trovi in `dist/` e basta. **Non contiene nessun progresso**: chi lo
importa parte da zero, con tutte le carte nuove e le statistiche vuote.

Non è una precauzione da prendere, è come è fatto il file. Il pacchetto viene costruito dai
file sorgente in `cards/`, non esportato da una collezione Anki, quindi dentro non c'è storico
di ripasso, non ci sono intervalli e nessuna carta porta statistiche.

**Non condividerlo esportandolo da Anki** (File → Esporta). Quella strada parte dalla tua
collezione e può includere le informazioni di programmazione: chi riceve il file si ritroverebbe
i tuoi intervalli al posto di un mazzo pulito, senza capire perché certe carte non gli vengono
mai proposte. Se per qualche motivo devi proprio esportare, togli la spunta alla casella sulle
informazioni di programmazione (scheduling).

---

## 3. Impostazioni consigliate

Si raggiungono dall'ingranaggio accanto al nome del mazzo → **Opzioni**.

Conviene impostarle sul mazzo padre `Istologia`: i sottomazzi ereditano la stessa
configurazione.

### Carte nuove al giorno

**Default: 20. Consigliato: 30-40 durante il corso.**

Attenzione al motivo per cui il default è basso. Ogni carta nuova genera ripassi per settimane:
come regola pratica, il carico di ripasso quotidiano si stabilizza intorno a **dieci volte** il
numero di carte nuove giornaliere. A 40 nuove al giorno vuol dire circa 400 ripassi al giorno
a regime. Parti da 30 e alza solo se regge.

### Ripassi massimi al giorno

**Default: 200. Consigliato: 9999.**

Questo è il tweak che fa più danno se lasciato com'è. Se i ripassi dovuti superano il limite,
Anki te ne nasconde una parte: tu credi di aver finito, ma l'arretrato cresce in silenzio e un
giorno ti ritrovi con settecento carte scadute. Meglio vedere sempre la verità.

### Seppellire i fratelli

**Da attivare: "Seppellisci nuovi fratelli" e "Seppellisci fratelli in ripasso".**

Un fratello è una carta generata dalla stessa nota. Molte carte di questi mazzi sono **cloze**,
e una sola frase con quattro buchi genera quattro carte. Senza questa opzione le vedi tutte lo
stesso giorno, ricordi la risposta dalla carta precedente e ti illudi di saperla. Con
l'opzione attiva, Anki rimanda le sorelle al giorno dopo.

Per queste carte è l'impostazione che incide di più sulla qualità dello studio.

### FSRS

**Da attivare, se non lo è già.**

FSRS è l'algoritmo di programmazione moderno di Anki, in fondo alle opzioni del mazzo. Rispetto
al vecchio algoritmo calcola gli intervalli sulla base dei tuoi dati reali e in genere riduce
il numero di ripassi a parità di ricordo. Se la tua versione di Anki ce l'ha già attivo, non
toccare nulla.

Lascia la ritenzione desiderata al valore di default (0,90). Alzarla a 0,95 fa esplodere il
carico di lavoro per un guadagno modesto: è una tentazione classica prima di un esame, e si
paga per settimane.

### Passaggi di apprendimento

**Default: `1m 10m`. Alternativa per la medicina: `15m 1d`.**

Rivedere una carta dieci minuti dopo averla vista serve a poco: la ricordi dalla memoria di
lavoro, non da quella a lungo termine. Con `15m 1d` la carta torna il giorno successivo, che
è dove si costruisce il ricordo vero. In cambio le carte nuove restano "in apprendimento" un
giorno in più.

### Sanguisughe (leech)

**Soglia 8, azione: "Tagga soltanto".**

Una sanguisuga è una carta che sbagli in continuazione. Il default la sospende e la fa sparire.
Meglio farsela taggare e basta, così te la ritrovi e puoi **riscriverla**: se sbagli una carta
otto volte, quasi sempre il problema è la carta, non la tua memoria. Di solito chiede troppe
cose insieme e va spezzata in due.

---

## 4. Come usare questi mazzi

### La regola che conta più di tutte

**Ripassa ogni giorno, anche poco.** Anki funziona presentandoti la carta poco prima che tu la
dimentichi. Saltare tre giorni non sposta il lavoro di tre giorni, lo accumula: le carte
scadute si sommano e il giorno che riapri l'app ne trovi centinaia. La maggior parte delle
persone che "ha provato Anki e non ha funzionato" ha smesso esattamente qui.

Meglio quindici minuti tutti i giorni che due ore la domenica.

### Prima i ripassi, poi le carte nuove

Se hai poco tempo, fai i ripassi e salta le carte nuove. I ripassi sono memoria che stai per
perdere, le carte nuove sono memoria che non hai ancora. Le prime valgono di più.

Se sei rimasto indietro, invece di arrancare azzera temporaneamente le carte nuove al giorno,
smaltisci l'arretrato, e poi riprendi.

### Rispondi onestamente

Se hai esitato, la risposta è **"Difficile"**, non "Buono". Se non l'avresti detta a un esame,
è **"Ancora"**. Barare con Anki funziona solo contro te stesso: l'algoritmo allunga gli
intervalli e tu arrivi all'esame convinto di sapere cose che non sai.

### Correggi le carte mentre studi

Premi **E** durante lo studio per modificare la carta che hai davanti. Se una carta è ambigua,
troppo lunga o ti fa sbagliare per come è scritta, riscrivila subito. Una carta che continui a
sbagliare va cambiata, non ripetuta.

### Studio mirato con i tag

Ogni carta di questi mazzi porta tre tipi di tag. Nella schermata **Sfoglia** puoi cercare così:

| Cerca questo | Per ottenere |
|---|---|
| `tag:tipo::riconoscimento` | solo le carte "che tessuto è questo?", ideali prima dell'esame pratico |
| `tag:tipo::classificazione` | solo le classificazioni |
| `tag:argomento::epiteli` | tutto quello che riguarda gli epiteli, teoria e laboratorio insieme |
| `tag:da-verificare` | i punti dubbi della sbobina, vedi sotto |
| `tag:non-trattato` | gli argomenti che la sbobina marca come non trattati nell'anno 2024/2025 |
| `deck:Istologia::Laboratorio tag:tipo::riconoscimento` | riconoscimento vetrini del solo Laboratorio |
| `is:due` | le carte che ti tocca ripassare |
| `prop:lapses>5` | le carte che sbagli più spesso, candidate a essere riscritte |

Per studiare una selezione senza sballare la programmazione: clicca il mazzo → **Studio
personalizzato** → "Studia per tag", oppure crea un mazzo filtrato dalla ricerca.

### Il tag `da-verificare`

Le sbobine sono trascrizioni fatte da studenti e ogni tanto contengono errori. Dove ho trovato
qualcosa che non torna **non ho corretto in silenzio**: la carta riporta quello che dice la
sbobina, ha il tag `da-verificare` e nelle note trovi cosa non quadra e cosa ci si aspetterebbe.

Prima dell'esame cerca `tag:da-verificare`, sono poche carte, e controllale sul libro. Così
decidi tu cosa studiare, invece di fidarti di una correzione fatta da me.

### Il tag `non-trattato`

Alcuni passaggi della sbobina hanno di fianco un riquadro "Argomento non trattato nell'anno
2024/2025". Le carte ci sono lo stesso, perché il materiale resta nella dispensa, ma portano
il tag `non-trattato` e te lo dicono in fondo alla risposta.

Se decidi di non studiarle, cerca `tag:non-trattato` nella schermata Sfoglia, selezionale
tutte e premi `-` per sospenderle in blocco.

### Il campo Fonte

In fondo a ogni risposta trovi il documento e la pagina da cui viene, per esempio
`Laboratorio p. 15`. Quando una carta non ti convince o vuoi il contesto completo, apri il PDF
a quella pagina invece di cercare a memoria.

### Scorciatoie da tastiera

| Tasto | Azione |
|---|---|
| `Spazio` | mostra la risposta, poi "Buono" |
| `1` `2` `3` `4` | Ancora, Difficile, Buono, Facile |
| `E` | modifica la carta corrente |
| `*` | segna la carta con una stella |
| `-` | sospendi la carta |
| `@` | segnala la carta come sanguisuga |

---

## 5. Rigenerare i mazzi

Serve solo se vuoi modificare le carte alla fonte.

```sh
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Stadio A: dai PDF a testo e immagini
./venv/bin/python scripts/extract.py --pdf "<percorso PDF>" --source-id lab --out build/lab

# Stadio B: dividere in sezioni
./venv/bin/python scripts/segment.py --build build/lab

# Stadio D: validare e costruire
./venv/bin/python -m scripts.build_apkg --cards cards/laboratorio \
    --media build/lab/images --out dist/Istologia-Laboratorio.apkg
```

Le carte sono file JSONL leggibili in `cards/`: una carta per riga. Modificando il testo e
ricostruendo, il reimport aggiorna le carte esistenti senza toccare il tuo storico.

I test si eseguono con `./venv/bin/python -m pytest tests/ -q`.

Il design del progetto e le ragioni delle scelte fatte stanno in
`docs/superpowers/specs/2026-08-10-anki-istologia-design.md`.

Lo stato di avanzamento, le convenzioni con cui sono scritte le carte e cosa resta
da fare stanno in `PLAN.md`.
