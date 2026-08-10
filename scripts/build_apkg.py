"""Stadio D, seconda meta: da carte JSONL a pacchetto .apkg."""

import argparse
import hashlib
import sys
from pathlib import Path

import genanki

from scripts.validate import load_cards, validate_cards

# Fissi per sempre: cambiarli farebbe apparire i tipi di nota come nuovi,
# e le carte gia studiate verrebbero reimportate come duplicati.
BASIC_MODEL_ID = 1789231001
CLOZE_MODEL_ID = 1789231002

CSS = """
.card {
  font-family: -apple-system, Helvetica, sans-serif;
  font-size: 19px;
  line-height: 1.5;
  text-align: left;
  color: #1a1a1a;
  background: #fdfdfd;
  padding: 16px;
}
.card img { max-width: 100%; height: auto; border-radius: 6px; margin-top: 10px; }
.media { margin-top: 12px; }
.fonte { margin-top: 18px; font-size: 13px; color: #888; }
ul, ol { margin: 6px 0 0 20px; padding: 0; }
li { margin-bottom: 4px; }
.cloze { font-weight: bold; color: #0b64c8; }
.nota { margin-top: 12px; font-size: 16px; color: #444; }
@media (prefers-color-scheme: dark) {
  .card { color: #eaeaea; background: #202124; }
  .fonte { color: #999; }
  .nota { color: #bbb; }
  .cloze { color: #6fb3ff; }
}
"""

BASIC_MODEL = genanki.Model(
    BASIC_MODEL_ID,
    "Istologia Base",
    fields=[
        {"name": "Fronte"},
        {"name": "Retro"},
        {"name": "ImmagineFronte"},
        {"name": "ImmagineRetro"},
        {"name": "Fonte"},
    ],
    templates=[
        {
            "name": "Domanda -> Risposta",
            "qfmt": "{{Fronte}}{{#ImmagineFronte}}<div class='media'>{{ImmagineFronte}}</div>"
            "{{/ImmagineFronte}}",
            "afmt": "{{FrontSide}}<hr id=answer>{{Retro}}"
            "{{#ImmagineRetro}}<div class='media'>{{ImmagineRetro}}</div>{{/ImmagineRetro}}"
            "{{#Fonte}}<div class='fonte'>{{Fonte}}</div>{{/Fonte}}",
        }
    ],
    css=CSS,
)

CLOZE_MODEL = genanki.Model(
    CLOZE_MODEL_ID,
    "Istologia Cloze",
    model_type=genanki.Model.CLOZE,
    fields=[
        {"name": "Testo"},
        {"name": "Note"},
        {"name": "Immagine"},
        {"name": "Fonte"},
    ],
    templates=[
        {
            "name": "Cloze",
            "qfmt": "{{cloze:Testo}}",
            "afmt": "{{cloze:Testo}}"
            "{{#Note}}<div class='nota'>{{Note}}</div>{{/Note}}"
            "{{#Immagine}}<div class='media'>{{Immagine}}</div>{{/Immagine}}"
            "{{#Fonte}}<div class='fonte'>{{Fonte}}</div>{{/Fonte}}",
        }
    ],
    css=CSS,
)


def note_guid(card_id):
    """Il guid dipende solo dall'id della carta.

    Correggere il testo di una carta gia studiata deve aggiornarla al
    reimport, non crearne una nuova azzerando lo storico di ripetizione.
    """
    return genanki.guid_for(card_id)


def render_images(files):
    return "".join(f'<img src="{name}">' for name in files)


def deck_id_for(name):
    """Id di mazzo stabile, derivato dal nome: due build producono lo stesso."""
    digest = hashlib.sha1(name.encode("utf-8")).hexdigest()[:12]
    return 1 << 30 | int(digest, 16) % (1 << 29)


def _note_for(card):
    images = card.get("images", [])
    rendered = render_images(images)
    source = card.get("source", "")
    tags = card.get("tags", [])

    if card["type"] == "cloze":
        return genanki.Note(
            model=CLOZE_MODEL,
            fields=[card["text"], card.get("extra", ""), rendered, source],
            tags=tags,
            guid=note_guid(card["id"]),
        )

    # Senza indicazione esplicita l'immagine va sulla risposta: e la scelta
    # sicura, perche una figura sulla domanda puo rivelare la risposta.
    on_front = card.get("image_side") == "front"
    return genanki.Note(
        model=BASIC_MODEL,
        fields=[
            card["front"],
            card["back"],
            rendered if on_front else "",
            "" if on_front else rendered,
            source,
        ],
        tags=tags,
        guid=note_guid(card["id"]),
    )


def build_package(cards, media_dir, out_path, package_name="Istologia"):
    media_dir = Path(media_dir)
    decks = {}
    used_media = set()

    for card in cards:
        name = card["deck"]
        if name not in decks:
            decks[name] = genanki.Deck(deck_id_for(name), name)
        decks[name].add_note(_note_for(card))
        used_media.update(card.get("images", []))

    package = genanki.Package(list(decks.values()))
    package.media_files = [str(media_dir / name) for name in sorted(used_media)]
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    package.write_to_file(out_path)
    return {"cards": len(cards), "decks": len(decks), "media": len(used_media)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cards", required=True)
    parser.add_argument("--media", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    cards = load_cards(args.cards)
    errors = validate_cards(cards, args.media)
    if errors:
        for error in errors:
            print(f"  ERRORE {error}")
        sys.exit(f"{len(errors)} errori: pacchetto non costruito")

    result = build_package(cards, args.media, args.out)
    size_mb = Path(args.out).stat().st_size / 1e6
    print(
        f"{args.out}: {result['cards']} carte, {result['decks']} mazzi, "
        f"{result['media']} immagini, {size_mb:.1f} MB"
    )


if __name__ == "__main__":
    main()
