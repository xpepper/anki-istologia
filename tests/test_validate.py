import pytest

from scripts.validate import validate_cards


@pytest.fixture
def media(tmp_path):
    (tmp_path / "lab_p042_1.jpg").write_bytes(b"jpeg")
    return tmp_path


def basic(**overrides):
    card = {
        "id": "lab-epiteli-001",
        "type": "basic",
        "deck": "Istologia::Laboratorio::02 - Tessuti epiteliali",
        "front": "Da cosa e nutrito il tessuto epiteliale?",
        "back": "Per diffusione dal connettivo sottostante, non essendo vascolarizzato.",
        "tags": ["fonte::lab"],
        "source": "Laboratorio p. 6",
    }
    card.update(overrides)
    return card


def cloze(**overrides):
    card = {
        "id": "lab-epiteli-002",
        "type": "cloze",
        "deck": "Istologia::Laboratorio::02 - Tessuti epiteliali",
        "text": "La membrana basale e costituita da {{c1::collagene}} e {{c2::glicoproteine}}.",
        "tags": ["fonte::lab"],
        "source": "Laboratorio p. 6",
    }
    card.update(overrides)
    return card


class TestAcceptsValidCards:
    def test_a_well_formed_basic_card_passes(self, media):
        assert validate_cards([basic()], media) == []

    def test_a_well_formed_cloze_card_passes(self, media):
        assert validate_cards([cloze()], media) == []

    def test_a_card_referencing_an_existing_image_passes(self, media):
        assert validate_cards([basic(images=["lab_p042_1.jpg"])], media) == []


class TestRequiredFields:
    @pytest.mark.parametrize("field", ["id", "type", "deck", "front", "back"])
    def test_reports_a_missing_field_on_a_basic_card(self, field, media):
        card = basic()
        del card[field]
        assert any(field in error for error in validate_cards([card], media))

    def test_reports_a_missing_text_on_a_cloze_card(self, media):
        card = cloze()
        del card["text"]
        assert any("text" in error for error in validate_cards([card], media))

    def test_reports_an_empty_field(self, media):
        assert any("front" in error for error in validate_cards([basic(front="  ")], media))

    def test_reports_an_unknown_card_type(self, media):
        assert any("type" in error for error in validate_cards([basic(type="image")], media))


class TestClozeSyntax:
    def test_reports_a_cloze_card_with_no_deletion(self, media):
        card = cloze(text="La membrana basale e costituita da collagene.")
        assert any("cloze" in error.lower() for error in validate_cards([card], media))

    def test_reports_a_malformed_deletion(self, media):
        card = cloze(text="La membrana basale contiene {{c1:collagene}}.")
        assert any("cloze" in error.lower() for error in validate_cards([card], media))

    def test_reports_deletion_numbering_that_does_not_start_at_one(self, media):
        card = cloze(text="Contiene {{c2::collagene}}.")
        assert any("c1" in error for error in validate_cards([card], media))

    def test_accepts_a_deletion_carrying_a_hint(self, media):
        card = cloze(text="Contiene {{c1::collagene::proteina fibrosa}}.")
        assert validate_cards([card], media) == []


class TestIdentity:
    def test_reports_two_cards_sharing_an_id(self, media):
        assert any("id" in error for error in validate_cards([basic(), basic()], media))

    def test_reports_the_same_question_asked_twice_in_one_deck(self, media):
        duplicate = basic(id="lab-epiteli-009")
        assert any("duplicat" in error.lower() for error in validate_cards([basic(), duplicate], media))

    def test_allows_the_same_question_in_different_decks(self, media):
        other = basic(id="lab-osso-001", deck="Istologia::Laboratorio::07 - Tessuto osseo")
        assert validate_cards([basic(), other], media) == []


class TestMedia:
    def test_reports_an_image_missing_from_disk(self, media):
        card = basic(images=["lab_p999_7.jpg"])
        assert any("lab_p999_7.jpg" in error for error in validate_cards([card], media))

    def test_reports_an_image_side_that_is_not_front_or_back(self, media):
        card = basic(images=["lab_p042_1.jpg"], image_side="sopra")
        assert any("image_side" in error for error in validate_cards([card], media))


class TestErrorMessages:
    def test_an_error_names_the_card_it_belongs_to(self, media):
        errors = validate_cards([basic(front="")], media)
        assert "lab-epiteli-001" in errors[0]
