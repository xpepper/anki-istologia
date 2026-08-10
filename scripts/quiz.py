"""Estrarre i quiz delle sbobine, comprese le risposte corrette.

Le risposte corrette non sono nel testo. Le sbobine usano due convenzioni
diverse, a seconda della lezione:

- quiz sul ghiandolare endocrino: la casella accanto alla risposta e spuntata
- quiz sui connettivi e sul nervoso: le caselle restano vuote e la risposta
  corretta e in grassetto

Le caselle sono disegni vettoriali e nel testo estratto spariscono del tutto.
Vengono quindi ritrovate come rettangoli di circa 10x10 pt, il che identifica
anche quali righe sono opzioni: il testo non produce mai rettangoli. Lo stato
della casella si legge poi dall'inchiostro al suo interno.
"""

import argparse
import json
import re

import pymupdf

QUESTION_START = re.compile(r"^\d+\)")
ZERO_WIDTH = "​"
PAGE_FURNITURE = {"Giovanni Profaizer"}
BOLD_FLAG = 1 << 4
BULLETS = {"●", "•", "○", "◦", "▪", "-"}

# I titoli di sezione misurano 14-16 pt, il corpo del testo 10,5-11.
TITLE_MIN_PT = 12

CHECKBOX_MIN_PT = 8
CHECKBOX_MAX_PT = 13
CHECKBOX_SQUARENESS_PT = 1.5
CHECKBOX_MAX_GAP_PT = 30

# Misurati sulle pagine di quiz: caselle vuote 0,328-0,353, spuntate
# 0,415-0,433. Fra i due valori non si decide, si segnala.
EMPTY_MAX = 0.38
CHECKED_MIN = 0.40

RENDER_DPI = 300


class AmbiguousCheckbox(Exception):
    """Casella la cui quantita di inchiostro non e ne vuota ne spuntata."""


def is_question_start(text):
    return bool(QUESTION_START.match(text.replace(ZERO_WIDTH, "").strip()))


def is_noise(text):
    """Intestazione di pagina e numero di pagina, che non fanno parte del quiz."""
    stripped = text.replace(ZERO_WIDTH, "").strip()
    return not stripped or stripped.isdigit() or stripped in PAGE_FURNITURE


def is_bullet(text):
    """Marcatore di elenco isolato: la riga vera e propria e quella dopo."""
    return text.replace(ZERO_WIDTH, "").strip() in BULLETS


def is_bold_span(span):
    return "bold" in span["font"].lower() or bool(span["flags"] & BOLD_FLAG)


def is_title(span):
    """Titolo della sezione quiz, da scartare.

    Dove le domande non sono numerate il titolo e attaccato alla prima domanda
    e nient'altro lo separa da essa. Lo si riconosce perche e in grassetto ed e
    piu grande del corpo del testo: le domande numerate del quiz sui connettivi
    sono anch'esse in grassetto, ma della misura del corpo.
    """
    return is_bold_span(span) and span["size"] >= TITLE_MIN_PT


def is_checkbox_rect(width, height):
    return (
        CHECKBOX_MIN_PT < width < CHECKBOX_MAX_PT
        and abs(width - height) < CHECKBOX_SQUARENESS_PT
    )


def checkbox_for_span(span_bbox, boxes, max_gap=CHECKBOX_MAX_GAP_PT):
    """La casella che precede la riga, se c'e: e cio che rende la riga un'opzione."""
    x0, y0, _, y1 = span_bbox
    for box in boxes:
        horizontally_before = 0 <= x0 - box[2] <= max_gap
        vertically_aligned = box[1] < y1 and box[3] > y0
        if horizontally_before and vertically_aligned:
            return box
    return None


def checkbox_state(ink_fraction):
    if ink_fraction < EMPTY_MAX:
        return False
    if ink_fraction > CHECKED_MIN:
        return True
    raise AmbiguousCheckbox(
        f"inchiostro {ink_fraction:.4f} fra {EMPTY_MAX} e {CHECKED_MIN}: "
        "casella da controllare a mano"
    )


def option_is_checked(ink_fraction, bold):
    """Vera se l'opzione e segnata come corretta, con una delle due convenzioni.

    Il grassetto risolve anche una casella che sarebbe altrimenti ambigua.
    """
    if bold:
        return True
    return checkbox_state(ink_fraction)


def group_questions(lines):
    questions = []
    pending = []
    for line in lines:
        text = line["text"].replace(ZERO_WIDTH, "").strip()
        if line["kind"] == "question":
            pending = []
            number, _, body = text.partition(")")
            questions.append(
                {"number": int(number), "question": body.strip(), "options": [], "answers": []}
            )
        elif line["kind"] == "option":
            if pending and (not questions or questions[-1]["options"]):
                # Quarta convenzione: la domanda non e numerata, e solo il
                # testo che precede il blocco di opzioni. Senza testo in
                # attesa siamo invece dentro una domanda gia aperta, di cui
                # le opzioni proseguono dalla pagina precedente.
                questions.append(
                    {
                        "number": len(questions) + 1,
                        "question": " ".join(pending),
                        "options": [],
                        "answers": [],
                    }
                )
            pending = []
            if not questions:
                continue
            questions[-1]["options"].append({"text": text, "checked": line["checked"]})
            if line["checked"]:
                questions[-1]["answers"].append(text)
        elif not questions or questions[-1]["options"]:
            # Fuori da una domanda aperta: potrebbe essere l'inizio della
            # prossima domanda non numerata, lo si sapra alla prima opzione.
            pending.append(text)
        else:
            # Domanda numerata gia aperta ma ancora senza opzioni: numero e
            # testo sono span separati, e una domanda lunga si spezza su piu
            # span ancora.
            questions[-1]["question"] = f"{questions[-1]['question']} {text}".strip()
    return questions


def _ink_fraction(page, rect):
    pixmap = page.get_pixmap(dpi=RENDER_DPI, clip=pymupdf.Rect(rect))
    samples, channels = pixmap.samples, pixmap.n
    dark = sum(1 for index in range(0, len(samples), channels) if samples[index] < 128)
    return dark / (pixmap.width * pixmap.height)


def read_page(page):
    """Righe della pagina, classificate in domande, opzioni e testo libero."""
    boxes = [
        tuple(drawing["rect"])
        for drawing in page.get_drawings()
        if is_checkbox_rect(drawing["rect"].width, drawing["rect"].height)
    ]

    lines = []
    after_bullet = False
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if is_noise(span["text"]):
                    continue
                text = span["text"].replace(ZERO_WIDTH, "").strip()

                if is_bullet(text):
                    after_bullet = True
                    continue

                box = checkbox_for_span(span["bbox"], boxes)
                if is_question_start(span["text"]):
                    lines.append({"kind": "question", "text": text})
                elif box is not None:
                    lines.append(
                        {
                            "kind": "option",
                            "text": text,
                            "checked": option_is_checked(
                                _ink_fraction(page, box), is_bold_span(span)
                            ),
                        }
                    )
                elif after_bullet:
                    # Terza convenzione: nessuna casella, solo punto elenco.
                    # Qui la risposta corretta e segnata unicamente dal grassetto.
                    lines.append(
                        {"kind": "option", "text": text, "checked": is_bold_span(span)}
                    )
                elif not is_title(span):
                    lines.append({"kind": "text", "text": text})
                after_bullet = False
    return lines


def extract_quiz(pdf_path, first_page, last_page):
    doc = pymupdf.open(pdf_path)
    lines = []
    for number in range(first_page, last_page + 1):
        lines.extend(read_page(doc[number - 1]))
    doc.close()

    questions = group_questions(lines)
    unanswered = [q["number"] for q in questions if not q["answers"]]
    if unanswered:
        print(f"  ATTENZIONE domande senza risposta segnata: {unanswered}")
    return questions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--from-page", type=int, required=True)
    parser.add_argument("--to-page", type=int, required=True)
    args = parser.parse_args()

    questions = extract_quiz(args.pdf, args.from_page, args.to_page)
    print(json.dumps(questions, ensure_ascii=False, indent=1))
    print(f"\n{len(questions)} domande estratte", flush=True)


if __name__ == "__main__":
    main()
