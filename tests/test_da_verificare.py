from scripts.da_verificare import as_markdown, note_of, select_flagged


def basic(**overrides):
    card = {
        "id": "lab-epiteli-031",
        "type": "basic",
        "deck": "Istologia::Laboratorio::02 - Tessuti epiteliali",
        "front": "Che cosa riveste la sierosa?",
        "back": "Il mesotelio.",
        "tags": ["fonte::lab", "da-verificare"],
        "source": "Laboratorio p. 8",
    }
    card.update(overrides)
    return card


def cloze(**overrides):
    card = {
        "id": "teoria-osso-049",
        "type": "cloze",
        "deck": "Istologia::Teoria::14 - Tessuto osseo",
        "text": "I canalicoli collegano le {{c1::lacune}}.",
        "extra": "La sbobina li chiama canali di Voorman.",
        "tags": ["fonte::teoria", "da-verificare"],
        "source": "5th gen p. 151",
    }
    card.update(overrides)
    return card


def test_takes_only_the_flagged_cards():
    flagged = select_flagged([basic(), basic(id="lab-epiteli-032", tags=["fonte::lab"])])

    assert [card["id"] for card in flagged] == ["lab-epiteli-031"]


def test_the_note_of_a_cloze_is_its_extra_field():
    assert note_of(cloze()) == "La sbobina li chiama canali di Voorman."


def test_the_note_of_a_basic_card_is_the_italic_block_at_the_end():
    """La convenzione del punto 3: sul basic la segnalazione sta in corsivo in
    fondo al back, preceduta dalla risposta vera, che qui non serve."""
    card = basic(back="Il mesotelio.<br><br><i>Attenzione: la sbobina dice altro.</i>")

    assert note_of(card) == "Attenzione: la sbobina dice altro."


def test_a_basic_card_without_italics_falls_back_to_the_whole_back():
    """Due carte sono fatte cosi: l'affermazione dubbia e la risposta stessa,
    quindi non c'e una nota da separare e va riportato tutto."""
    card = basic(back="La giunzione miotendinea e formata da cartilagine ialina.")

    assert note_of(card) == "La giunzione miotendinea e formata da cartilagine ialina."


def test_the_note_keeps_the_emphasis_as_markdown():
    card = basic(back="X.<br><br><i>La sbobina scrive <b>Cowper</b> per Littre.</i>")

    assert note_of(card) == "La sbobina scrive **Cowper** per Littre."


def test_the_note_keeps_the_bold_words_that_interrupt_the_italics():
    """Il corsivo si chiude e riapre attorno a ogni parola in grassetto: unire
    i soli blocchi <i> perderebbe le parole in mezzo, che sono il contenuto
    della segnalazione (il C4 e il C2 di teoria-sangue-030)."""
    card = basic(back="C1 attiva C2.<br><br><i>Il C1 taglia prima il </i><b>C4</b><i> e poi il </i><b>C2</b><i>.</i>")

    assert note_of(card) == "Il C1 taglia prima il **C4** e poi il **C2**."


def test_the_note_keeps_what_follows_an_italic_label():
    """Su alcune carte il corsivo e solo l'etichetta e la spiegazione prosegue
    in tondo, come su lab-linfoide-022."""
    card = basic(back="Un tessuto trofico.<br><br><i>Da verificare:</i> il timo e un <b>organo</b>.")

    assert note_of(card) == "Da verificare: il timo e un **organo**."


def test_the_document_groups_by_deck_in_course_order():
    text = as_markdown([cloze(), basic()])

    lab = text.index("Istologia::Laboratorio::02 - Tessuti epiteliali")
    teoria = text.index("Istologia::Teoria::14 - Tessuto osseo")
    assert lab < teoria


def test_every_entry_carries_its_id_and_its_page():
    text = as_markdown([basic()])

    assert "`lab-epiteli-031`" in text
    assert "Laboratorio p. 8" in text


def test_the_document_counts_the_open_notes():
    assert "2 carte" in as_markdown([cloze(), basic()])
