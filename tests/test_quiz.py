import pytest

from scripts.quiz import (
    AmbiguousCheckbox,
    checkbox_for_span,
    checkbox_state,
    group_questions,
    is_bold_span,
    is_bullet,
    is_checkbox_rect,
    is_noise,
    is_question_start,
    is_title,
    option_is_checked,
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
        assert checkbox_state(0.33) is False

    def test_high_ink_means_checked(self):
        assert checkbox_state(0.43) is True

    def test_a_value_in_the_grey_band_is_refused_rather_than_guessed(self):
        """Una casella incerta va segnalata: tirare a indovinare qui produce
        una carta che insegna la risposta sbagliata."""
        with pytest.raises(AmbiguousCheckbox):
            checkbox_state(0.39)

    def test_the_band_edges_are_themselves_ambiguous(self):
        with pytest.raises(AmbiguousCheckbox):
            checkbox_state(0.38)
        with pytest.raises(AmbiguousCheckbox):
            checkbox_state(0.40)


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


class TestOptionIsChecked:
    """Le sbobine usano due convenzioni diverse per segnare la risposta: la
    casella spuntata nel quiz endocrino, il grassetto in quello sui connettivi."""

    def test_an_inked_checkbox_marks_the_answer(self):
        assert option_is_checked(ink_fraction=0.43, bold=False) is True

    def test_bold_text_marks_the_answer_even_with_an_empty_checkbox(self):
        assert option_is_checked(ink_fraction=0.33, bold=True) is True

    def test_plain_text_with_an_empty_checkbox_is_not_the_answer(self):
        assert option_is_checked(ink_fraction=0.33, bold=False) is False

    def test_bold_settles_a_checkbox_that_would_be_ambiguous(self):
        assert option_is_checked(ink_fraction=0.39, bold=True) is True

    def test_an_ambiguous_checkbox_without_bold_is_still_refused(self):
        with pytest.raises(AmbiguousCheckbox):
            option_is_checked(ink_fraction=0.39, bold=False)


class TestIsBoldSpan:
    def test_detects_bold_from_the_font_name(self):
        assert is_bold_span({"font": "Nunito-Bold", "flags": 4}) is True

    def test_detects_bold_from_the_flags(self):
        assert is_bold_span({"font": "Nunito", "flags": 20}) is True

    def test_regular_text_is_not_bold(self):
        assert is_bold_span({"font": "Nunito-Regular", "flags": 4}) is False


class TestIsTitle:
    """Il titolo della sezione ("QUIZ", "Domande e risposte del quiz finale")
    e in grassetto e piu grande del corpo del testo. Va scartato: dove le
    domande non sono numerate niente segnerebbe altrimenti che il titolo non
    fa parte della prima domanda."""

    def test_recognises_the_quiz_heading(self):
        assert is_title({"font": "Nunito-Bold", "flags": 20, "size": 14.0}) is True

    def test_a_bold_question_in_the_body_text_is_not_a_title(self):
        """Nel quiz sui connettivi le domande numerate sono in grassetto."""
        assert is_title({"font": "Nunito-Bold", "flags": 20, "size": 11.0}) is False

    def test_plain_body_text_is_not_a_title(self):
        assert is_title({"font": "Nunito", "flags": 4, "size": 10.5}) is False


class TestIsBullet:
    """Terza convenzione, nel quiz sul nervoso: niente caselle, opzioni con
    punto elenco e risposta in grassetto."""

    @pytest.mark.parametrize("text", ["●", "•", "○", "▪", "-"])
    def test_recognises_the_list_markers_used(self, text):
        assert is_bullet(text) is True

    def test_recognises_a_marker_carrying_a_zero_width_space(self):
        assert is_bullet("●​") is True

    @pytest.mark.parametrize("text", ["Nuclei centrali", "1)", "-5 mm"])
    def test_rejects_real_content(self, text):
        assert is_bullet(text) is False


class TestIsCheckboxRect:
    def test_accepts_the_ten_point_square_used_in_the_sbobine(self):
        assert is_checkbox_rect(10.1, 10.1) is True

    def test_rejects_the_wide_bands_of_the_page_layout(self):
        assert is_checkbox_rect(507.0, 19.0) is False

    def test_rejects_a_rectangle_that_is_not_square(self):
        assert is_checkbox_rect(10.1, 4.0) is False

    def test_rejects_a_square_far_from_the_expected_size(self):
        assert is_checkbox_rect(3.0, 3.0) is False


class TestCheckboxForSpan:
    """La casella a sinistra e cio che rende una riga un'opzione: il testo non
    produce mai rettangoli, quindi il segnale non si confonde con la domanda."""

    BOX = (66.9, 200.0, 77.0, 210.0)
    SPAN = (100.0, 199.0, 300.0, 211.0)

    def test_finds_the_box_just_left_of_the_option(self):
        assert checkbox_for_span(self.SPAN, [self.BOX]) == self.BOX

    def test_ignores_a_box_too_far_to_the_left(self):
        far = (10.0, 200.0, 20.1, 210.0)
        assert checkbox_for_span(self.SPAN, [far]) is None

    def test_ignores_a_box_on_another_line(self):
        other_line = (66.9, 400.0, 77.0, 410.0)
        assert checkbox_for_span(self.SPAN, [other_line]) is None

    def test_ignores_a_box_to_the_right(self):
        right = (320.0, 200.0, 330.1, 210.0)
        assert checkbox_for_span(self.SPAN, [right]) is None

    def test_a_question_line_has_no_box_and_stays_a_question(self):
        assert checkbox_for_span((35.4, 199.0, 300.0, 211.0), [self.BOX]) is None


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


class TestUnnumberedQuestions:
    """Quarta convenzione, nel quiz finale sui connettivi specializzati: le
    domande non portano il marcatore "N)". L'unico segnale che una riga di
    testo e una domanda e che subito dopo comincia un blocco di opzioni."""

    LINES = [
        {"kind": "text", "text": "Quali cellule riassorbono l'osso?"},
        {"kind": "option", "text": "Osteoblasti", "checked": False},
        {"kind": "option", "text": "Osteoclasti", "checked": True},
        {"kind": "text", "text": "Qual e la componente minerale della matrice?"},
        {"kind": "option", "text": "Idrossiapatite", "checked": True},
    ]

    def test_reads_the_text_before_the_options_as_the_question(self):
        assert [q["question"] for q in group_questions(self.LINES)] == [
            "Quali cellule riassorbono l'osso?",
            "Qual e la componente minerale della matrice?",
        ]

    def test_numbers_them_in_reading_order(self):
        assert [q["number"] for q in group_questions(self.LINES)] == [1, 2]

    def test_collects_the_options_under_their_question(self):
        assert [len(q["options"]) for q in group_questions(self.LINES)] == [2, 1]

    def test_lists_the_correct_answers(self):
        assert [q["answers"] for q in group_questions(self.LINES)] == [
            ["Osteoclasti"],
            ["Idrossiapatite"],
        ]

    def test_joins_a_question_broken_over_two_spans(self):
        lines = [
            {"kind": "text", "text": "Quale dei seguenti tessuti protegge"},
            {"kind": "text", "text": "il sistema nervoso centrale?"},
            {"kind": "option", "text": "Tessuto osseo", "checked": True},
        ]
        question = group_questions(lines)[0]
        assert question["question"] == "Quale dei seguenti tessuti protegge il sistema nervoso centrale?"

    def test_options_continuing_on_the_next_page_stay_with_their_question(self):
        """Fra le ultime opzioni di una pagina e le prime della successiva non
        c'e testo: aprire li una domanda nuova le staccherebbe dalla loro."""
        lines = [
            {"kind": "text", "text": "Quali sono le componenti del sangue?"},
            {"kind": "option", "text": "Plasma", "checked": True},
            {"kind": "option", "text": "Eritrociti", "checked": True},
        ]
        assert len(group_questions(lines)) == 1
        assert len(group_questions(lines)[0]["options"]) == 2
