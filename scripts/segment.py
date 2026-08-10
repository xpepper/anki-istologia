"""Stadio B: dividere il materiale estratto in sezioni di lavoro.

Ogni sezione corrisponde a un sottomazzo e all'unita di lavoro dello stadio C:
titolo, capitolo di appartenenza, intervallo di pagine, testo e immagini.

La gerarchia non viene dai marcatori di lezione, che nelle sbobine sono
irregolari, ma dalle dimensioni di font raccolte nello stadio A: i titoli piu
grandi sono i capitoli, quelli intermedi le sezioni.
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path

DEFAULT_MAX_TIER = 2
INTRO_TITLE = "(inizio documento)"


def heading_tiers(pages):
    """Da dimensione di font a livello gerarchico, 1 = il piu grande."""
    sizes = sorted(
        {block["size"] for page in pages for block in page["blocks"] if block["heading"] > 0},
        reverse=True,
    )
    return {size: tier for tier, size in enumerate(sizes, start=1)}


def slugify(text):
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")[:50] or "sezione"


def split_sections(pages, tiers, max_tier=DEFAULT_MAX_TIER):
    sections = []
    current = None
    chapter = ""

    def start(title, tier, size, page):
        section = {
            "title": title,
            "tier": tier,
            "size": size,
            "chapter": chapter,
            "page_start": page,
            "page_end": page,
            "_parts": [],
        }
        sections.append(section)
        return section

    for page in pages:
        for block in page["blocks"]:
            tier = tiers.get(block["size"]) if block["heading"] > 0 else None
            is_split_point = tier is not None and tier <= max_tier

            if is_split_point:
                title = " ".join(block["text"].split())
                # Un titolo spezzato su due blocchi: stessa dimensione e nessun
                # testo in mezzo. Va ricucito, altrimenti nascono sezioni tronche.
                if current is not None and not current["_parts"] and current["size"] == block["size"]:
                    current["title"] = f"{current['title']} {title}".strip()
                    current["page_end"] = page["page"]
                else:
                    current = start(title, tier, block["size"], page["page"])
                if current["tier"] == 1:
                    chapter = current["title"]
                    current["chapter"] = chapter
                continue

            if current is None:
                current = start(INTRO_TITLE, max_tier + 1, None, page["page"])
            current["_parts"].append(block["text"])
            current["page_end"] = page["page"]

    for index, section in enumerate(sections):
        section["id"] = f"{index:03d}-{slugify(section['title'])}"
        section["text"] = "\n\n".join(section.pop("_parts"))
    return sections


def images_for_section(section, images):
    return [
        image["file"]
        for image in images
        if section["page_start"] <= image["page"] <= section["page_end"]
    ]


def segment(build_dir, max_tier=DEFAULT_MAX_TIER):
    build_dir = Path(build_dir)
    pages = _read_jsonl(build_dir / "pages.jsonl")
    images = _read_jsonl(build_dir / "images.jsonl")
    by_file = {image["file"]: image for image in images}

    tiers = heading_tiers(pages)
    sections = split_sections(pages, tiers, max_tier)
    for section in sections:
        section["images"] = [
            {
                "file": name,
                "page": by_file[name]["page"],
                "caption": by_file[name]["caption"],
            }
            for name in images_for_section(section, images)
        ]

    with open(build_dir / "sections.jsonl", "w", encoding="utf-8") as handle:
        for section in sections:
            handle.write(json.dumps(section, ensure_ascii=False) + "\n")

    words = sum(len(section["text"].split()) for section in sections)
    print(f"{build_dir}: {len(sections)} sezioni, {words} parole, livelli {tiers}")
    return sections


def _read_jsonl(path):
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", required=True, help="es. build/lab")
    parser.add_argument("--max-tier", type=int, default=DEFAULT_MAX_TIER)
    args = parser.parse_args()
    segment(args.build, args.max_tier)


if __name__ == "__main__":
    main()
