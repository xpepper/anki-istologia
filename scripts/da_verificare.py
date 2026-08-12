"""Elenco delle carte da portare al libro, generato dalle carte stesse.

La lista delle segnalazioni esiste gia in tre posti che non vanno tenuti
allineati a mano: il tag `da-verificare` in Anki, la nota in fondo alla carta
e la tabella del punto 5 di PLAN.md. Questo script produce il quarto, il solo
che serva a Pietro col libro davanti, e lo ricava dalle carte: cosi quando una
segnalazione si chiude togliendo il tag, la riga sparisce da sola e il
documento non puo mentire.
"""

import argparse
import re
from pathlib import Path

from scripts.validate import load_cards

FLAG = "da-verificare"

# La sbobina ha due punti dubbi su cui non e stata scritta nessuna carta,
# quindi nessun tag li porta: senza questa costante il documento generato
# sarebbe piu povero dell'elenco del punto 5 di PLAN.md, da cui vengono.
WITHOUT_CARD = [
    (
        "Laboratorio p. 4",
        "Una microfotografia e didascalizzata *colon* ma mostra tessuto adiposo "
        "e vasi: non ne e stata fatta una carta di riconoscimento.",
    ),
    (
        "Laboratorio p. 70",
        "`lab_p070_4344.jpg` e un ritaglio con un solo leucocita fra gli "
        "eritrociti, non identificabile con certezza.",
    ),
]

NOTE_OPENS = "<i>"


def _to_markdown(html):
    text = re.sub(r"</?(?:b|strong)>", "**", html)
    text = re.sub(r"</?(?:i|em)>", "", text)
    text = re.sub(r"<li>\s*", "; ", text)
    text = re.sub(r"<br\s*/?>", " ", text)
    text = re.sub(r"</?[a-zA-Z]+[^>]*>", "", text)
    return re.sub(r"\s+", " ", text).strip(" ;")


def note_of(card):
    """La spiegazione di cosa non torna, cosi come sta gia sulla carta.

    Sul cloze e il campo `extra`. Sul basic la segnalazione comincia dove si
    apre il corsivo e arriva in fondo al `back`: quello che la precede e la
    risposta, non la segnalazione. Va presa **tutta la coda** e non i soli
    blocchi <i>, per due motivi che le carte mostrano davvero: il corsivo si
    chiude e riapre attorno a ogni parola in grassetto (teoria-sangue-030, dove
    il C4 e il C2 andrebbero persi), e a volte in corsivo c'e solo l'etichetta
    mentre la spiegazione prosegue in tondo (lab-linfoide-022).

    Dove il corsivo manca del tutto, l'affermazione dubbia e la risposta stessa.
    """
    if card["type"] == "cloze":
        return _to_markdown(card.get("extra", ""))

    back = card.get("back", "")
    opens = back.find(NOTE_OPENS)
    return _to_markdown(back[opens:] if opens != -1 else back)


def select_flagged(cards):
    return [card for card in cards if FLAG in card.get("tags", [])]


def as_markdown(cards):
    flagged = select_flagged(cards)
    by_deck = {}
    for card in flagged:
        by_deck.setdefault(card["deck"], []).append(card)

    lines = [
        "# Carte da verificare sul libro",
        "",
        f"**{len(flagged)} carte**, piu {len(WITHOUT_CARD)} punti su cui non e stata "
        "scritta nessuna carta.",
        "",
        "Sono i punti in cui la sbobina dice qualcosa che non torna. La convenzione "
        "del progetto e non correggere mai in silenzio: la carta riporta quello che "
        "dice la sbobina, spiega cosa non quadra e porta il tag `da-verificare`, e la "
        "decisione resta tua.",
        "",
        "In Anki le ritrovi tutte con la ricerca `tag:da-verificare`.",
        "",
        "> Questo file e **generato dalle carte**: le modifiche a mano vengono "
        "sovrascritte. Una riga sparisce quando la sua carta perde il tag, cioe "
        "quando la segnalazione e chiusa. Per rigenerarlo:",
        ">",
        "> ```sh",
        "> ./venv/bin/python -m scripts.da_verificare --cards cards --out DA_VERIFICARE.md",
        "> ```",
        "",
    ]

    for deck in sorted(by_deck):
        lines.append(f"## {deck}")
        lines.append("")
        for card in sorted(by_deck[deck], key=lambda c: c["id"]):
            source = card.get("source", "")
            lines.append(f"**`{card['id']}`** — {source}")
            lines.append("")
            lines.append(note_of(card))
            lines.append("")

    lines.append("## Senza carta")
    lines.append("")
    lines.append(
        "Due punti dubbi che non hanno prodotto una carta, quindi nessun tag li "
        "porta e in Anki non si trovano."
    )
    lines.append("")
    for source, note in WITHOUT_CARD:
        lines.append(f"**{source}**")
        lines.append("")
        lines.append(note)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cards", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    cards = load_cards(args.cards)
    text = as_markdown(cards)
    Path(args.out).write_text(text, encoding="utf-8")
    print(f"{args.out}: {len(select_flagged(cards))} carte da verificare")


if __name__ == "__main__":
    main()
