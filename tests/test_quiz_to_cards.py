from scripts.quiz_to_cards import cards_from_quiz

DECK = "Istologia::Laboratorio::Quiz"


def question(**overrides):
    item = {
        "number": 2,
        "question": "Quali cellule producono calcitonina nella tiroide?",
        "options": [
            {"text": "Cellule follicolari", "checked": False},
            {"text": "Cellule parafollicolari", "checked": True},
        ],
        "answers": ["Cellule parafollicolari"],
    }
    item.update(overrides)
    return item


def build(items, **kwargs):
    options = {
        "deck": DECK,
        "prefix": "lab-quiz-endocrino",
        "tags": ["fonte::lab", "argomento::endocrino"],
        "source": "Laboratorio p. 40-43",
    }
    options.update(kwargs)
    return cards_from_quiz(items, **options)


class TestFront:
    def test_shows_the_question(self):
        assert "Quali cellule producono calcitonina" in build([question()])[0]["front"]

    def test_lists_every_option(self):
        front = build([question()])[0]["front"]
        assert "Cellule follicolari" in front and "Cellule parafollicolari" in front

    def test_does_not_reveal_which_option_is_correct(self):
        """Se il fronte marcasse la risposta la carta non chiederebbe nulla."""
        assert "<b>" not in build([question()])[0]["front"]

    def test_escapes_html_special_characters(self):
        item = question(options=[{"text": "H&E <forte>", "checked": True}], answers=["H&E <forte>"])
        assert "&amp;" in build([item])[0]["front"] and "<forte>" not in build([item])[0]["front"]


class TestBack:
    def test_carries_the_correct_answer(self):
        assert "Cellule parafollicolari" in build([question()])[0]["back"]

    def test_lists_all_the_correct_answers_when_there_are_several(self):
        item = question(
            question="Quali NON hanno dotto escretore?",
            options=[
                {"text": "Tiroide", "checked": True},
                {"text": "Pancreas esocrino", "checked": False},
                {"text": "Ipofisi", "checked": True},
            ],
            answers=["Tiroide", "Ipofisi"],
        )
        back = build([item])[0]["back"]
        assert "Tiroide" in back and "Ipofisi" in back and "Pancreas esocrino" not in back


class TestSelection:
    def test_skips_open_questions_that_have_no_options(self):
        assert build([question(options=[], answers=[])]) == []

    def test_skips_a_question_whose_answer_was_never_marked(self):
        """Meglio nessuna carta che una carta senza risposta."""
        item = question(options=[{"text": "Cellule follicolari", "checked": False}], answers=[])
        assert build([item]) == []


class TestCardShape:
    def test_builds_a_basic_card(self):
        assert build([question()])[0]["type"] == "basic"

    def test_derives_a_stable_id_from_the_question_number(self):
        assert build([question()])[0]["id"] == "lab-quiz-endocrino-002"

    def test_puts_the_card_in_the_requested_deck(self):
        assert build([question()])[0]["deck"] == DECK

    def test_tags_the_card_as_a_quiz_question(self):
        assert "tipo::quiz" in build([question()])[0]["tags"]

    def test_keeps_the_tags_it_was_given(self):
        assert "argomento::endocrino" in build([question()])[0]["tags"]

    def test_records_the_source(self):
        assert build([question()])[0]["source"] == "Laboratorio p. 40-43"
