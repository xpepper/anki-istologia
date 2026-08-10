"""Stadio D, prima meta: controllare le carte prima di costruire il pacchetto.

Meglio un errore qui che una carta rotta scoperta durante un ripasso.
"""

import argparse
import json
import re
import sys
from pathlib import Path

CARD_TYPES = ("basic", "cloze")
COMMON_FIELDS = ("id", "type", "deck")
TYPE_FIELDS = {"basic": ("front", "back"), "cloze": ("text",)}
IMAGE_SIDES = ("front", "back")

VALID_DELETION = re.compile(r"\{\{c(\d+)::[^{}]+?(?:::[^{}]+?)?\}\}")
ANY_BRACES = re.compile(r"\{\{.*?\}\}")


def validate_cards(cards, media_dir):
    """Lista di messaggi di errore, vuota se le carte sono a posto."""
    media_dir = Path(media_dir)
    errors = []
    seen_ids = set()
    seen_questions = set()

    for card in cards:
        name = card.get("id") or "(carta senza id)"

        card_type = card.get("type")
        if not card_type:
            errors.append(f"{name}: campo 'type' mancante")
            continue
        if card_type not in CARD_TYPES:
            errors.append(f"{name}: 'type' sconosciuto: {card_type!r}, attesi {CARD_TYPES}")
            continue

        for field in COMMON_FIELDS + TYPE_FIELDS[card_type]:
            value = card.get(field)
            if value is None:
                errors.append(f"{name}: campo '{field}' mancante")
            elif not str(value).strip():
                errors.append(f"{name}: campo '{field}' vuoto")

        if card_type == "cloze" and card.get("text"):
            errors.extend(_cloze_errors(name, card["text"]))

        card_id = card.get("id")
        if card_id:
            if card_id in seen_ids:
                errors.append(f"{name}: id duplicato")
            seen_ids.add(card_id)

        question = card.get("front") or card.get("text")
        if question and card.get("deck"):
            key = (card["deck"], " ".join(str(question).split()))
            if key in seen_questions:
                errors.append(f"{name}: domanda duplicata nello stesso mazzo")
            seen_questions.add(key)

        for image in card.get("images", []):
            if not (media_dir / image).exists():
                errors.append(f"{name}: immagine assente dal disco: {image}")

        side = card.get("image_side")
        if side is not None and side not in IMAGE_SIDES:
            errors.append(f"{name}: 'image_side' non valido: {side!r}, attesi {IMAGE_SIDES}")

    return errors


def _cloze_errors(name, text):
    deletions = VALID_DELETION.findall(text)
    malformed = [
        match for match in ANY_BRACES.findall(text) if not VALID_DELETION.fullmatch(match)
    ]
    if malformed:
        return [f"{name}: cloze malformato: {malformed[0]}"]
    if not deletions:
        return [f"{name}: carta cloze senza alcuna eliminazione {{{{c1::...}}}}"]
    if "1" not in deletions:
        return [f"{name}: le eliminazioni cloze non partono da c1"]
    return []


def load_cards(cards_dir):
    cards = []
    for path in sorted(Path(cards_dir).rglob("*.jsonl")):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if line.strip():
                try:
                    cards.append(json.loads(line))
                except json.JSONDecodeError as error:
                    raise SystemExit(f"{path}:{number}: JSON non valido: {error}")
    return cards


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cards", required=True)
    parser.add_argument("--media", required=True)
    args = parser.parse_args()

    cards = load_cards(args.cards)
    errors = validate_cards(cards, args.media)
    for error in errors:
        print(f"  ERRORE {error}")
    print(f"{len(cards)} carte controllate, {len(errors)} errori")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
