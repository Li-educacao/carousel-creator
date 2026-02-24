"""Tests for the PCB generator and S-expression writer."""
from pathlib import Path
from pcb_autoplacer.generators.sexpr_writer import serialize
from pcb_autoplacer.generators.board_setup import (
    generate_header, generate_general, generate_layers, generate_board_outline,
)
from pcb_autoplacer.models import BoardConfig, PlacedComponent, FootprintDef, Pad, Net, NetNode
from pcb_autoplacer.placer.constraints import BBox, check_overlaps, check_boundary, get_component_bbox


class TestSexprWriter:
    def test_simple_keyword(self):
        result = serialize(["layer", "signal"])
        assert result == "(layer signal)"

    def test_quoted_layer_name(self):
        result = serialize(["layer", "F.Cu"])
        assert result == '(layer "F.Cu")'

    def test_nested(self):
        result = serialize(["footprint", "R_0805", ["layer", "F.Cu"]])
        assert '(footprint "R_0805"' in result
        assert '(layer "F.Cu")' in result

    def test_quoted_strings(self):
        result = serialize(["property", "hello world"])
        assert '"hello world"' in result

    def test_numbers(self):
        result = serialize(["at", "1.5", "-2.3"])
        assert "(at 1.5 -2.3)" == result

    def test_net_quoted(self):
        result = serialize(["net", "1", "GND"])
        assert result == '(net 1 "GND")'

    def test_keywords_unquoted(self):
        from pcb_autoplacer.generators.sexpr_writer import Quoted
        result = serialize(["pad", Quoted("1"), "smd", "rect"])
        assert result == '(pad "1" smd rect)'


class TestBoardSetup:
    def test_header(self):
        header = generate_header()
        assert header[0] == "kicad_pcb"

    def test_general(self):
        board = BoardConfig()
        general = generate_general(board)
        assert general[0] == "general"

    def test_layers(self):
        layers = generate_layers()
        assert layers[0] == "layers"
        # Should have F.Cu and B.Cu
        layer_names = [l[1] for l in layers[1:] if isinstance(l, list)]
        assert "F.Cu" in layer_names
        assert "B.Cu" in layer_names

    def test_board_outline(self):
        board = BoardConfig(width_mm=50, height_mm=30)
        outline = generate_board_outline(board)
        assert len(outline) == 4  # 4 lines for rectangle
        for line in outline:
            assert line[0] == "gr_line"


class TestConstraints:
    def test_bbox_overlap(self):
        b1 = BBox(0, 0, 5, 5)
        b2 = BBox(3, 3, 8, 8)
        assert b1.overlaps(b2) is True

    def test_bbox_no_overlap(self):
        b1 = BBox(0, 0, 5, 5)
        b2 = BBox(10, 10, 15, 15)
        assert b1.overlaps(b2) is False

    def test_bbox_clearance(self):
        b1 = BBox(0, 0, 5, 5)
        b2 = BBox(5.1, 0, 10, 5)
        assert b1.overlaps(b2) is False
        assert b1.overlaps(b2, clearance=0.2) is True

    def test_check_overlaps(self):
        fp = FootprintDef(name="test", bbox_width=4, bbox_height=4)
        comp1 = PlacedComponent(ref="R1", value="10k", footprint="test", x=5, y=5, footprint_def=fp)
        comp2 = PlacedComponent(ref="R2", value="10k", footprint="test", x=6, y=5, footprint_def=fp)
        comp3 = PlacedComponent(ref="R3", value="10k", footprint="test", x=20, y=20, footprint_def=fp)

        overlaps = check_overlaps([comp1, comp2, comp3])
        assert ("R1", "R2") in overlaps
        assert len(overlaps) == 1

    def test_check_boundary(self):
        board = BoardConfig(width_mm=50, height_mm=50)
        fp = FootprintDef(name="test", bbox_width=4, bbox_height=4)
        # Component outside board (board origin is 100,100)
        comp = PlacedComponent(ref="R1", value="10k", footprint="test", x=99, y=99, footprint_def=fp)
        violations = check_boundary([comp], board)
        assert "R1" in violations
