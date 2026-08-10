from scripts.segment import heading_tiers, images_for_section, split_sections


def block(text, size, heading):
    return {"text": text, "size": size, "bold": True, "heading": heading, "bbox": (0, 0, 1, 1)}


def body(text):
    return {"text": text, "size": 10.5, "bold": False, "heading": 0, "bbox": (0, 0, 1, 1)}


def page(number, blocks):
    return {"page": number, "text": "", "blocks": blocks}


class TestHeadingTiers:
    def test_ranks_distinct_heading_sizes_largest_first(self):
        pages = [page(1, [block("A", 18.0, 1), block("B", 16.0, 1), block("C", 14.0, 2)])]
        assert heading_tiers(pages) == {18.0: 1, 16.0: 2, 14.0: 3}

    def test_ignores_body_text_sizes(self):
        pages = [page(1, [block("A", 18.0, 1), body("corpo")])]
        assert heading_tiers(pages) == {18.0: 1}

    def test_returns_empty_mapping_when_there_are_no_headings(self):
        assert heading_tiers([page(1, [body("solo corpo")])]) == {}


class TestSplitSections:
    TIERS = {18.0: 1, 16.0: 2, 14.0: 3}

    def test_starts_a_new_section_at_each_heading_within_the_depth_limit(self):
        pages = [
            page(1, [block("TESSUTI EPITELIALI", 18.0, 1), body("intro")]),
            page(2, [block("Caratteristiche", 16.0, 1), body("dettaglio")]),
        ]
        sections = split_sections(pages, self.TIERS, max_tier=2)
        assert [s["title"] for s in sections] == ["TESSUTI EPITELIALI", "Caratteristiche"]

    def test_does_not_split_on_headings_deeper_than_the_limit(self):
        pages = [
            page(1, [block("TESSUTI", 18.0, 1), body("intro")]),
            page(1, [block("sottotitolo", 14.0, 2), body("dettaglio")]),
        ]
        assert len(split_sections(pages, self.TIERS, max_tier=2)) == 1

    def test_carries_the_chapter_title_down_into_its_sections(self):
        pages = [
            page(1, [block("TESSUTI EPITELIALI", 18.0, 1)]),
            page(2, [block("Caratteristiche", 16.0, 1), body("x")]),
        ]
        assert split_sections(pages, self.TIERS)[1]["chapter"] == "TESSUTI EPITELIALI"

    def test_keeps_the_deeper_headings_inside_the_section_text(self):
        pages = [
            page(1, [block("TESSUTI", 18.0, 1), block("sottotitolo", 14.0, 2), body("dettaglio")]),
        ]
        assert "sottotitolo" in split_sections(pages, self.TIERS)[0]["text"]

    def test_records_the_page_range_a_section_spans(self):
        pages = [
            page(3, [block("TESSUTI", 18.0, 1), body("a")]),
            page(4, [body("b")]),
            page(5, [body("c"), block("Altro", 18.0, 1)]),
        ]
        first = split_sections(pages, self.TIERS)[0]
        assert (first["page_start"], first["page_end"]) == (3, 5)

    def test_merges_a_title_broken_across_two_blocks(self):
        pages = [
            page(4, [block("Colorazione di uno striscio di", 16.0, 1), block("sangue", 16.0, 1)]),
        ]
        sections = split_sections(pages, self.TIERS)
        assert [s["title"] for s in sections] == ["Colorazione di uno striscio di sangue"]

    def test_text_before_the_first_heading_becomes_its_own_section(self):
        pages = [page(1, [body("frontespizio"), block("TESSUTI", 18.0, 1)])]
        sections = split_sections(pages, self.TIERS)
        assert sections[0]["title"] == "(inizio documento)"
        assert "frontespizio" in sections[0]["text"]

    def test_gives_every_section_a_unique_identifier(self):
        pages = [
            page(1, [block("Ripetuto", 16.0, 1), body("a")]),
            page(2, [block("Ripetuto", 16.0, 1), body("b")]),
        ]
        ids = [s["id"] for s in split_sections(pages, self.TIERS)]
        assert len(set(ids)) == 2


class TestImagesForSection:
    IMAGES = [
        {"file": "lab_p002_1.jpg", "page": 2},
        {"file": "lab_p004_2.jpg", "page": 4},
        {"file": "lab_p009_3.jpg", "page": 9},
    ]

    def test_selects_images_inside_the_page_range(self):
        section = {"page_start": 2, "page_end": 4}
        assert images_for_section(section, self.IMAGES) == ["lab_p002_1.jpg", "lab_p004_2.jpg"]

    def test_returns_nothing_when_the_range_holds_no_images(self):
        assert images_for_section({"page_start": 5, "page_end": 8}, self.IMAGES) == []
