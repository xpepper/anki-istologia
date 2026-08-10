"""Da quiz estratti a carte Anki.

Deterministico apposta: le domande sono decine e ricopiarle a mano
introdurrebbe errori proprio dove la carta deve essere affidabile.
"""

import argparse
import html
import json

from scripts.quiz import extract_quiz


def cards_from_quiz(questions, deck, prefix, tags, source):
    cards = []
    for item in questions:
        # Senza opzioni e una domanda aperta; senza risposta segnata non
        # sapremmo cosa mettere sul retro. In entrambi i casi meglio nessuna
        # carta che una carta inaffidabile.
        if not item["options"] or not item["answers"]:
            continue

        options = "".join(f"<li>{html.escape(o['text'])}</li>" for o in item["options"])
        answers = "".join(f"<li><b>{html.escape(a)}</b></li>" for a in item["answers"])
        plural = "Risposte corrette" if len(item["answers"]) > 1 else "Risposta corretta"

        cards.append(
            {
                "id": f"{prefix}-{item['number']:03d}",
                "type": "basic",
                "deck": deck,
                "front": f"{html.escape(item['question'])}<ul>{options}</ul>",
                "back": f"{plural}:<ul>{answers}</ul>",
                "tags": list(tags) + ["tipo::quiz"],
                "source": source,
            }
        )
    return cards


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--from-page", type=int, required=True)
    parser.add_argument("--to-page", type=int, required=True)
    parser.add_argument("--deck", required=True)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--tags", nargs="+", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    questions = extract_quiz(args.pdf, args.from_page, args.to_page)
    cards = cards_from_quiz(questions, args.deck, args.prefix, args.tags, args.source)
    skipped = [q["number"] for q in questions if not q["options"] or not q["answers"]]

    with open(args.out, "w", encoding="utf-8") as handle:
        for card in cards:
            handle.write(json.dumps(card, ensure_ascii=False) + "\n")
    print(f"{args.out}: {len(cards)} carte da {len(questions)} domande")
    if skipped:
        print(f"  saltate (aperte o senza risposta segnata), da scrivere a mano: {skipped}")


if __name__ == "__main__":
    main()
