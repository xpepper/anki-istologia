import json
import sqlite3
import zipfile

import pytest

from scripts.build_apkg import build_package, note_guid, render_images


@pytest.fixture
def media(tmp_path):
    for name in ("lab_p042_1.jpg", "lab_p043_2.jpg"):
        (tmp_path / name).write_bytes(b"jpeg-bytes")
    return tmp_path


def basic(**overrides):
    card = {
        "id": "lab-epiteli-001",
        "type": "basic",
        "deck": "Istologia::Laboratorio::02 - Tessuti epiteliali",
        "front": "Il tessuto epiteliale e vascolarizzato?",
        "back": "No.",
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
        "text": "La membrana basale contiene {{c1::collagene}}.",
        "tags": ["fonte::lab"],
        "source": "Laboratorio p. 6",
    }
    card.update(overrides)
    return card


def read_package(path):
    """Riapre l'.apkg e ne legge il database interno.

    Verificare il file prodotto, e non le strutture in memoria, e l'unico modo
    di sapere che Anki ricevera davvero quello che ci aspettiamo.
    """
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        media_map = json.loads(archive.read("media"))
        collection = [name for name in names if name.startswith("collection.anki")][0]
        archive.extract(collection, path.parent)
    connection = sqlite3.connect(path.parent / collection)
    notes = connection.execute("select guid, flds, tags from notes").fetchall()
    # genanki scrive i mazzi nel JSON della colonna col.decks, non in una tabella.
    decks = json.loads(connection.execute("select decks from col").fetchone()[0])
    connection.close()
    return {"notes": notes, "decks": [d["name"] for d in decks.values()], "media": media_map}


class TestNoteGuid:
    def test_is_stable_for_the_same_card_id(self):
        assert note_guid("lab-epiteli-001") == note_guid("lab-epiteli-001")

    def test_differs_between_card_ids(self):
        assert note_guid("lab-epiteli-001") != note_guid("lab-epiteli-002")

    def test_ignores_everything_but_the_id(self):
        """Il guid dipende solo dall'id: correggere il testo di una carta deve
        aggiornarla in Anki, non crearne una nuova perdendo lo storico."""
        assert note_guid("lab-epiteli-001") == note_guid("lab-epiteli-001")


class TestRenderImages:
    def test_wraps_each_file_in_an_img_tag(self):
        assert render_images(["a.jpg"]) == '<img src="a.jpg">'

    def test_renders_several_images_in_order(self):
        assert render_images(["a.jpg", "b.jpg"]) == '<img src="a.jpg"><img src="b.jpg">'

    def test_renders_nothing_when_there_are_no_images(self):
        assert render_images([]) == ""


class TestBuildPackage:
    def test_writes_one_note_per_card(self, tmp_path, media):
        out = tmp_path / "deck.apkg"
        build_package([basic(), cloze()], media, out, "Istologia")
        assert len(read_package(out)["notes"]) == 2

    def test_creates_the_deck_named_on_the_card(self, tmp_path, media):
        out = tmp_path / "deck.apkg"
        build_package([basic()], media, out, "Istologia")
        assert "Istologia::Laboratorio::02 - Tessuti epiteliali" in read_package(out)["decks"]

    def test_includes_only_the_referenced_media(self, tmp_path, media):
        out = tmp_path / "deck.apkg"
        build_package([basic(images=["lab_p042_1.jpg"])], media, out, "Istologia")
        assert sorted(read_package(out)["media"].values()) == ["lab_p042_1.jpg"]

    def test_puts_a_front_image_in_the_question(self, tmp_path, media):
        out = tmp_path / "deck.apkg"
        build_package(
            [basic(images=["lab_p042_1.jpg"], image_side="front")], media, out, "Istologia"
        )
        fields = read_package(out)["notes"][0][1].split("\x1f")
        assert 'src="lab_p042_1.jpg"' in fields[2] and fields[3] == ""

    def test_puts_a_back_image_in_the_answer(self, tmp_path, media):
        out = tmp_path / "deck.apkg"
        build_package(
            [basic(images=["lab_p042_1.jpg"], image_side="back")], media, out, "Istologia"
        )
        fields = read_package(out)["notes"][0][1].split("\x1f")
        assert fields[2] == "" and 'src="lab_p042_1.jpg"' in fields[3]

    def test_defaults_an_image_to_the_answer_side(self, tmp_path, media):
        out = tmp_path / "deck.apkg"
        build_package([basic(images=["lab_p042_1.jpg"])], media, out, "Istologia")
        fields = read_package(out)["notes"][0][1].split("\x1f")
        assert 'src="lab_p042_1.jpg"' in fields[3]

    def test_carries_the_tags_onto_the_note(self, tmp_path, media):
        out = tmp_path / "deck.apkg"
        build_package([basic(tags=["fonte::lab", "tipo::definizione"])], media, out, "Istologia")
        assert "tipo::definizione" in read_package(out)["notes"][0][2]

    def test_records_the_source_reference_on_the_note(self, tmp_path, media):
        out = tmp_path / "deck.apkg"
        build_package([basic()], media, out, "Istologia")
        assert "Laboratorio p. 6" in read_package(out)["notes"][0][1]

    def test_produces_the_same_guids_when_rebuilt(self, tmp_path, media):
        """Ricostruire e reimportare deve aggiornare le carte, non duplicarle."""
        first = tmp_path / "one.apkg"
        second = tmp_path / "two.apkg"
        build_package([basic()], media, first, "Istologia")
        build_package([basic(back="No, e nutrito per diffusione.")], media, second, "Istologia")
        assert read_package(first)["notes"][0][0] == read_package(second)["notes"][0][0]
