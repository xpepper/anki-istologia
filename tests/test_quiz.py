import pytest

from scripts.quiz import (
    AmbiguousCheckbox,
    checkbox_state,
    group_questions,
    is_noise,
    is_question_start,
)


class TestIsNoise:
    @pytest.mark.parametrize("text", ["Giovanni Profaizer", "40", "  "])
    def test_discards_page_furniture(self, text):
        assert is_noise(text) is True

    @pytest.mark.parametrize("text", ["Tiroide", "Qual è l'unità funzionale?"])
    def test_keeps_real_content(self, text):
        assert is_noise(text) is False


class TestIsQuestionStart:
    @pytest.mark.parametrize("text", ["1)", "12)", "7)​"])
    def test_recognises_a_numbered_question_marker(self, text):
        assert is_question_start(text) is True

    @pytest.mark.parametrize("text", ["Tiroide", "a)", "", "1."])
    def test_rejects_anything_else(self, text):
        assert is_question_start(text) is False


class TestCheckboxState:
    def test_low_ink_means_empty(self):
        assert checkbox_state(0.074) is False

    def test_high_ink_means_checked(self):
        assert checkbox_state(0.104) is True

    def test_a_value_in_the_grey_band_is_refused_rather_than_guessed(self):
        """Una casella incerta va segnalata: tirare a indovinare qui produce
        una carta che insegna la risposta sbagliata."""
        with pytest.raises(AmbiguousCheckbox):
            checkbox_state(0.090)

    def test_the_band_edges_are_themselves_ambiguous(self):
        with pytest.raises(AmbiguousCheckbox):
            checkbox_state(0.085)
        with pytest.raises(AmbiguousCheckbox):
            checkbox_state(0.095)


class TestQuestionTextSpreadOverSpans:
    """Nel PDF il numero e il testo della domanda sono span separati: senza
    ricucirli le domande escono vuote."""

    LINES = [
        {"kind": "question", "text": "1)"},
        {"kind": "text", "text": "Quale ghiandola NON ha un dotto?"},
        {"kind": "option", "text": "Tiroide", "checked": True},
    ]

    def test_joins_the_text_that_follows_the_number(self):
        assert group_questions(self.LINES)[0]["question"] == "Quale ghiandola NON ha un dotto?"

    def test_joins_a_question_broken_over_two_spans(self):
        lines = [
            {"kind": "question", "text": "1)"},
            {"kind": "text", "text": "Quale ghiandola"},
            {"kind": "text", "text": "NON ha un dotto?"},
            {"kind": "option", "text": "Tiroide", "checked": True},
        ]
        assert group_questions(lines)[0]["question"] == "Quale ghiandola NON ha un dotto?"

    def test_ignores_text_appearing_after_the_options_started(self):
        lines = self.LINES + [{"kind": "text", "text": "didascalia di una figura"}]
        assert group_questions(lines)[0]["question"] == "Quale ghiandola NON ha un dotto?"

    def test_keeps_an_open_question_that_has_no_options(self):
        lines = [
            {"kind": "question", "text": "22)"},
            {"kind": "text", "text": "Elenca tutti i tessuti ghiandolari endocrini umani"},
        ]
        question = group_questions(lines)[0]
        assert question["question"] == "Elenca tutti i tessuti ghiandolari endocrini umani"
        assert question["options"] == []


class TestGroupQuestions:
    LINES = [
        {"kind": "question", "text": "1) Quale ghiandola NON ha un dotto?"},
        {"kind": "option", "text": "Tiroide", "checked": True},
        {"kind": "option", "text": "Pancreas esocrino", "checked": False},
        {"kind": "question", "text": "2) Chi produce calcitonina?"},
        {"kind": "option", "text": "Cellule parafollicolari", "checked": True},
    ]

    def test_collects_the_options_under_their_question(self):
        questions = group_questions(self.LINES)
        assert [len(q["options"]) for q in questions] == [2, 1]

    def test_strips_the_numbering_from_the_question_text(self):
        assert group_questions(self.LINES)[0]["question"] == "Quale ghiandola NON ha un dotto?"

    def test_keeps_the_question_number(self):
        assert [q["number"] for q in group_questions(self.LINES)] == [1, 2]

    def test_lists_the_correct_answers(self):
        assert group_questions(self.LINES)[0]["answers"] == ["Tiroide"]

    def test_supports_a_question_with_several_correct_answers(self):
        lines = [
            {"kind": "question", "text": "1) Quali NON hanno dotto?"},
            {"kind": "option", "text": "Tiroide", "checked": True},
            {"kind": "option", "text": "Pancreas esocrino", "checked": False},
            {"kind": "option", "text": "Ipofisi", "checked": True},
        ]
        assert group_questions(lines)[0]["answers"] == ["Tiroide", "Ipofisi"]

    def test_ignores_options_appearing_before_any_question(self):
        lines = [{"kind": "option", "text": "orfana", "checked": False}] + self.LINES
        assert len(group_questions(lines)) == 2

    def test_reports_a_question_left_without_any_correct_answer(self):
        lines = [
            {"kind": "question", "text": "1) Domanda senza risposta segnata"},
            {"kind": "option", "text": "A", "checked": False},
        ]
        assert group_questions(lines)[0]["answers"] == []
