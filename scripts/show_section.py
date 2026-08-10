"""Stampa una sezione con le sue immagini: e la vista di lavoro dello stadio C."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", required=True)
    parser.add_argument("--id", required=True, help="prefisso dell'id di sezione, es. 004")
    parser.add_argument("--text-only", action="store_true")
    args = parser.parse_args()

    path = Path(args.build) / "sections.jsonl"
    sections = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    matches = [s for s in sections if s["id"].startswith(args.id)]
    if not matches:
        raise SystemExit(f"nessuna sezione con prefisso {args.id!r}")

    for section in matches:
        print(f"{'=' * 78}\n{section['id']} | {section['chapter']} > {section['title']}")
        print(f"pagine {section['page_start']}-{section['page_end']}\n{'=' * 78}")
        print(section["text"])
        if not args.text_only and section["images"]:
            print(f"\n--- immagini ({len(section['images'])}) ---")
            for image in section["images"]:
                print(f"  {image['file']} p.{image['page']} | {image['caption'][:90]}")


if __name__ == "__main__":
    main()
