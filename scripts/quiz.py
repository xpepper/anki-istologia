"""Estrarre i quiz delle sbobine, comprese le risposte corrette.

Le risposte corrette sono segnate con caselle spuntate, che sono disegni
vettoriali: nel testo estratto spariscono del tutto, e una domanda a scelta
multipla senza risposta non serve a niente.

Lo stato della casella si legge quindi rendendo la piccola area a sinistra di
ogni opzione e misurandone l'inchiostro. Sulle pagine di quiz del Laboratorio i
due gruppi sono ben separati: caselle vuote intorno a 0,074-0,080 e caselle
spuntate intorno a 0,101-0,108.
"""

import argparse
import json
import re

import pymupdf

QUESTION_START = re.compile(r"^\d+\)")
ZERO_WIDTH = "​"
PAGE_FURNITURE = {"Giovanni Profaizer"}

# Fra i due valori non si decide: si segnala.
EMPTY_MAX = 0.085
CHECKED_MIN = 0.095

CHECKBOX_OFFSET = 20
CHECKBOX_MARGIN = 4
RENDER_DPI = 300


class AmbiguousCheckbox(Exception):
    """Casella la cui quantita di inchiostro non e ne vuota ne spuntata."""


def is_question_start(text):
    return bool(QUESTION_START.match(text.replace(ZERO_WIDTH, "").strip()))


def is_noise(text):
    """Intestazione di pagina e numero di pagina, che non fanno parte del quiz."""
    stripped = text.replace(ZERO_WIDTH, "").strip()
    return not stripped or stripped.isdigit() or stripped in PAGE_FURNITURE


def checkbox_state(ink_fraction):
    if ink_fraction < EMPTY_MAX:
        return False
    if ink_fraction > CHECKED_MIN:
        return True
    raise AmbiguousCheckbox(
        f"inchiostro {ink_fraction:.4f} fra {EMPTY_MAX} e {CHECKED_MIN}: "
        "casella da controllare a mano"
    )


def group_questions(lines):
    questions = []
    for line in lines:
        text = line["text"].replace(ZERO_WIDTH, "").strip()
        if line["kind"] == "question":
            number, _, body = text.partition(")")
            questions.append(
                {"number": int(number), "question": body.strip(), "options": [], "answers": []}
            )
        elif not questions:
            continue
        elif line["kind"] == "option":
            questions[-1]["options"].append({"text": text, "checked": line["checked"]})
            if line["checked"]:
                questions[-1]["answers"].append(text)
        elif not questions[-1]["options"]:
            # Numero e testo della domanda sono span separati, e una domanda
            # lunga si spezza su piu span ancora. Il testo dopo la prima
            # opzione non appartiene piu alla domanda.
            questions[-1]["question"] = f"{questions[-1]['question']} {text}".strip()
    return questions


def _ink_fraction(page, span_bbox):
    x0, y0, _, y1 = span_bbox
    clip = pymupdf.Rect(x0 - CHECKBOX_OFFSET, y0 - 2, x0 - CHECKBOX_MARGIN, y1 + 2)
    pixmap = page.get_pixmap(dpi=RENDER_DPI, clip=clip)
    samples, channels = pixmap.samples, pixmap.n
    dark = sum(1 for index in range(0, len(samples), channels) if samples[index] < 128)
    return dark / (pixmap.width * pixmap.height)


def read_page(page):
    """Righe della pagina, gia classificate in domande e opzioni."""
    lines = []
    for block in page.get_text("dict")["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                text = span["text"].replace(ZERO_WIDTH, "").strip()
                if is_noise(span["text"]):
                    continue
                if is_question_start(span["text"]):
                    lines.append({"kind": "question", "text": text})
                elif span["text"].startswith(ZERO_WIDTH):
                    lines.append(
                        {
                            "kind": "option",
                            "text": text,
                            "checked": checkbox_state(_ink_fraction(page, span["bbox"])),
                        }
                    )
                else:
                    lines.append({"kind": "text", "text": text})
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
