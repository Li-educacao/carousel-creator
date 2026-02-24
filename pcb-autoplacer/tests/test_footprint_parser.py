"""Tests for the footprint parser."""
from pathlib import Path
from pcb_autoplacer.parsers.footprint import parse_footprint

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseFootprint:
    def test_r0805(self):
        fp = parse_footprint(FIXTURES / "r0805.kicad_mod")

        assert fp.name == "R_0805_2012Metric"
        assert "0805" in fp.description or "2012" in fp.description
        assert len(fp.pads) == 2
        assert fp.is_smd is True

    def test_pad_details(self):
        fp = parse_footprint(FIXTURES / "r0805.kicad_mod")

        pad1 = next(p for p in fp.pads if p.number == "1")
        assert pad1.pad_type == "smd"
        assert pad1.shape == "roundrect"
        assert abs(pad1.x - (-0.9125)) < 0.01
        assert abs(pad1.y) < 0.01
        assert abs(pad1.width - 1.025) < 0.01
        assert abs(pad1.height - 1.4) < 0.01
        assert "F.Cu" in pad1.layers

    def test_bounding_box(self):
        fp = parse_footprint(FIXTURES / "r0805.kicad_mod")
        # Bounding box should encompass both pads
        assert fp.bbox_width > 0
        assert fp.bbox_height > 0
        # Width should be at least the distance between pads
        assert fp.bbox_width >= 1.8  # 0.9125 * 2 approx
