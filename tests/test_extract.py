import io
import random

from PIL import Image

from scripts.extract import (
    caption_for_image,
    compress_image,
    heading_level,
    image_filename,
    is_artifact,
)


def make_png(width, height):
    """A noisy image, so byte sizes behave like the real micrographs.

    A flat colour would compress to almost nothing as PNG and could come out
    *larger* as JPEG, which would make the size assertions meaningless.
    """
    random.seed(width * height)
    noise = bytes(random.getrandbits(8) for _ in range(width * height * 3))
    buf = io.BytesIO()
    Image.frombytes("RGB", (width, height), noise).save(buf, "PNG")
    return buf.getvalue()


class TestImageFilename:
    def test_encodes_source_page_and_xref(self):
        assert image_filename("lab", 42, 280) == "lab_p042_280.jpg"

    def test_pads_page_so_names_sort_in_reading_order(self):
        names = sorted([image_filename("lab", 9, 1), image_filename("lab", 100, 1)])
        assert names == ["lab_p009_1.jpg", "lab_p100_1.jpg"]

    def test_is_stable_across_calls(self):
        assert image_filename("teoria", 7, 55) == image_filename("teoria", 7, 55)


class TestCompressImage:
    def test_returns_jpeg(self):
        out = compress_image(make_png(1200, 900))
        assert Image.open(io.BytesIO(out)).format == "JPEG"

    def test_scales_longest_side_down_to_the_limit(self):
        out = compress_image(make_png(2500, 1250), max_px=1000)
        assert Image.open(io.BytesIO(out)).size == (1000, 500)

    def test_does_not_upscale_images_already_smaller(self):
        out = compress_image(make_png(300, 200), max_px=1000)
        assert Image.open(io.BytesIO(out)).size == (300, 200)

    def test_shrinks_a_large_photographic_image(self):
        raw = make_png(2000, 2000)
        assert len(compress_image(raw)) < len(raw)

    def test_handles_images_with_transparency(self):
        buf = io.BytesIO()
        Image.new("RGBA", (400, 400), (10, 20, 30, 128)).save(buf, "PNG")
        assert Image.open(io.BytesIO(compress_image(buf.getvalue()))).mode == "RGB"


class TestIsArtifact:
    def test_flags_tiny_images(self):
        assert is_artifact(80, 80) is True

    def test_flags_images_thin_in_one_dimension(self):
        assert is_artifact(1500, 30) is True

    def test_keeps_a_real_micrograph(self):
        assert is_artifact(760, 480) is False

    def test_keeps_a_small_micrograph_crop(self):
        """Gli strisci di sangue sono ritagli piccoli, non icone.

        Il piu piccolo delle sbobine e 121x126 (un leucocita fra gli
        eritrociti); il capitolo sul sangue ne ha otto fra 122x122 e 874x156.
        """
        assert is_artifact(122, 122) is False
        assert is_artifact(874, 156) is False

    def test_flags_a_formula_rendered_as_an_image(self):
        """Una striscia di testo (la formula dell'apertura numerica, p. 54):

        larga abbastanza, ma alta quanto una riga.
        """
        assert is_artifact(282, 56) is True


class TestHeadingLevel:
    BODY = 10.0

    def test_body_text_is_level_zero(self):
        assert heading_level(size=10.0, bold=False, body_size=self.BODY) == 0

    def test_much_larger_text_is_a_top_level_heading(self):
        assert heading_level(size=16.0, bold=True, body_size=self.BODY) == 1

    def test_moderately_larger_text_is_a_subheading(self):
        assert heading_level(size=12.5, bold=True, body_size=self.BODY) == 2

    def test_bold_at_body_size_is_the_deepest_heading(self):
        assert heading_level(size=10.0, bold=True, body_size=self.BODY) == 3

    def test_smaller_than_body_is_never_a_heading(self):
        assert heading_level(size=8.0, bold=True, body_size=self.BODY) == 0


class TestCaptionForImage:
    IMAGE = (100.0, 200.0, 400.0, 500.0)

    def test_prefers_the_text_block_just_below_the_image(self):
        blocks = [
            {"text": "testo sopra", "bbox": (100.0, 150.0, 400.0, 190.0)},
            {"text": "Vetrino di colon, Ematossilina-Eosina.", "bbox": (100.0, 510.0, 400.0, 540.0)},
        ]
        assert caption_for_image(self.IMAGE, blocks) == "Vetrino di colon, Ematossilina-Eosina."

    def test_falls_back_to_the_block_above_when_nothing_follows(self):
        blocks = [{"text": "testo sopra", "bbox": (100.0, 150.0, 400.0, 190.0)}]
        assert caption_for_image(self.IMAGE, blocks) == "testo sopra"

    def test_ignores_blocks_too_far_away_to_be_a_caption(self):
        blocks = [{"text": "altra sezione", "bbox": (100.0, 780.0, 400.0, 800.0)}]
        assert caption_for_image(self.IMAGE, blocks) == ""

    def test_returns_empty_string_when_the_page_has_no_text(self):
        assert caption_for_image(self.IMAGE, []) == ""
