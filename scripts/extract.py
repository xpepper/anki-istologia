"""Stadio A: da PDF a testo per pagina e immagini compresse.

Produce, sotto build/<source_id>/:
  pages.jsonl   una riga per pagina: testo e blocchi con info di font
  images/       le immagini, ridimensionate e ricodificate in JPEG
  images.jsonl  una riga per immagine: pagina, dimensioni, didascalia

Le info di font servono allo stadio B: nel testo piatto la gerarchia dei
titoli andrebbe persa, ed e proprio quella che divide il materiale in lezioni.
"""

import argparse
import io
import json
import statistics
from pathlib import Path

import pymupdf
from PIL import Image

MAX_PX = 1000
JPEG_QUALITY = 78
MIN_USEFUL_PX = 100
MAX_CAPTION_GAP = 60.0


def image_filename(source_id, page, xref):
    """Nome deterministico: rieseguire l'estrazione non rompe i riferimenti
    gia scritti nelle carte. La pagina e zero-padded per ordinare in lettura."""
    return f"{source_id}_p{page:03d}_{xref}.jpg"


def compress_image(raw, max_px=MAX_PX, quality=JPEG_QUALITY):
    """Ridimensiona a max_px sul lato lungo e ricodifica in JPEG."""
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    if max(img.size) > max_px:
        img.thumbnail((max_px, max_px), Image.LANCZOS)
    out = io.BytesIO()
    img.save(out, "JPEG", quality=quality, optimize=True)
    return out.getvalue()


def is_artifact(width, height, min_px=MIN_USEFUL_PX):
    """Icone, loghi e strisce di layout: nessun valore didattico.

    La soglia sta a 100 px e non piu alta perche le figure del sangue sono
    ritagli piccoli di striscio: a 200 px se ne perdevano otto solo fra le
    pagine 177 e 198. Sotto i 100 px restano icone (21x17) e formule
    renderizzate come immagine (282x56), che una figura vera non e mai.
    """
    return width < min_px or height < min_px


def heading_level(size, bold, body_size):
    """0 = testo normale, 1..3 = titoli dal piu grande al piu piccolo.

    Le sbobine non hanno stili nominati, quindi il livello si deduce dal
    rapporto con la dimensione di corpo prevalente nel documento.
    """
    if size < body_size * 0.98:
        return 0
    ratio = size / body_size
    if ratio >= 1.45:
        return 1
    if ratio >= 1.15:
        return 2
    if bold:
        return 3
    return 0


def caption_for_image(image_bbox, blocks, max_gap=MAX_CAPTION_GAP):
    """Il testo che fa da didascalia, cercato prima sotto e poi sopra.

    Nelle sbobine la didascalia sta quasi sempre subito sotto la figura.
    """
    _, top, _, bottom = image_bbox

    def horizontally_overlaps(bbox):
        return bbox[0] < image_bbox[2] and bbox[2] > image_bbox[0]

    below, above = [], []
    for block in blocks:
        bbox = block["bbox"]
        if not block["text"].strip() or not horizontally_overlaps(bbox):
            continue
        if bbox[1] >= bottom:
            below.append((bbox[1] - bottom, block["text"]))
        elif bbox[3] <= top:
            above.append((top - bbox[3], block["text"]))

    for candidates in (below, above):
        near = [(gap, text) for gap, text in candidates if gap <= max_gap]
        if near:
            return min(near)[1].strip()
    return ""


def _page_blocks(page):
    """Blocchi di testo con la dimensione di font dominante e il peso."""
    blocks = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        spans = [span for line in block["lines"] for span in line["spans"]]
        text = "".join(
            "".join(span["text"] for span in line["spans"]) + "\n" for line in block["lines"]
        ).strip()
        if not text:
            continue
        # La dimensione dominante e quella che copre piu caratteri: un titolo
        # seguito da una nota piccola resta classificato come titolo.
        by_size = {}
        for span in spans:
            by_size[round(span["size"], 1)] = by_size.get(round(span["size"], 1), 0) + len(
                span["text"]
            )
        size = max(by_size.items(), key=lambda kv: kv[1])[0]
        bold = any("bold" in span["font"].lower() for span in spans)
        blocks.append({"text": text, "size": size, "bold": bold, "bbox": tuple(block["bbox"])})
    return blocks


def _body_size(pages):
    """Dimensione di font prevalente, pesata sui caratteri."""
    weighted = []
    for blocks in pages:
        for block in blocks:
            weighted.extend([block["size"]] * len(block["text"]))
    return statistics.median(weighted) if weighted else 10.0


def extract(pdf_path, source_id, out_dir):
    out_dir = Path(out_dir)
    (out_dir / "images").mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf_path)

    all_blocks = [_page_blocks(page) for page in doc]
    body_size = _body_size(all_blocks)

    pages, images, seen_xrefs = [], [], set()
    for index, page in enumerate(doc):
        page_no = index + 1
        blocks = all_blocks[index]
        for block in blocks:
            block["heading"] = heading_level(block["size"], block["bold"], body_size)
        pages.append(
            {
                "page": page_no,
                "text": "\n\n".join(block["text"] for block in blocks),
                "blocks": blocks,
            }
        )

        for info in page.get_images(full=True):
            xref = info[0]
            if xref in seen_xrefs:
                continue
            seen_xrefs.add(xref)
            raw = doc.extract_image(xref)
            if is_artifact(raw["width"], raw["height"]):
                continue
            try:
                data = compress_image(raw["image"])
            except Exception as error:  # immagini in spazi colore esotici
                print(f"  ! salto xref {xref} a p.{page_no}: {error}")
                continue
            name = image_filename(source_id, page_no, xref)
            (out_dir / "images" / name).write_bytes(data)
            rects = page.get_image_rects(xref)
            bbox = tuple(rects[0]) if rects else (0.0, 0.0, 0.0, 0.0)
            images.append(
                {
                    "file": name,
                    "page": page_no,
                    "width": raw["width"],
                    "height": raw["height"],
                    "bytes": len(data),
                    "caption": caption_for_image(bbox, blocks) if rects else "",
                }
            )

    _write_jsonl(out_dir / "pages.jsonl", pages)
    _write_jsonl(out_dir / "images.jsonl", images)
    doc.close()

    total_mb = sum(image["bytes"] for image in images) / 1e6
    print(f"{source_id}: {len(pages)} pagine, {len(images)} immagini, {total_mb:.1f} MB media")
    print(f"  dimensione di corpo rilevata: {body_size}")
    return {"pages": len(pages), "images": len(images), "media_mb": total_mb}


def _write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--source-id", required=True, help="teoria | lab")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    extract(args.pdf, args.source_id, args.out)


if __name__ == "__main__":
    main()
