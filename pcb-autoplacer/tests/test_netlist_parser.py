"""Tests for the netlist parser."""
from pathlib import Path
from pcb_autoplacer.parsers.netlist import parse_netlist

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseNetlist:
    def test_components(self):
        components, nets = parse_netlist(FIXTURES / "simple.net")
        assert len(components) == 5

        refs = {c.ref for c in components}
        assert refs == {"U1", "R1", "R2", "C1", "C2"}

        u1 = next(c for c in components if c.ref == "U1")
        assert u1.value == "STM32F103C8T6"
        assert u1.footprint == "Package_QFP:LQFP-48_7x7mm_P0.5mm"
        assert u1.library == "Package_QFP"
        assert u1.footprint_name == "LQFP-48_7x7mm_P0.5mm"

    def test_nets(self):
        components, nets = parse_netlist(FIXTURES / "simple.net")
        # Net 0 (unconnected) should be filtered out
        named_nets = [n for n in nets if n.code > 0]
        assert len(named_nets) == 5

        gnd = next(n for n in nets if n.name == "GND")
        assert gnd.code == 1
        assert len(gnd.nodes) == 3

        vcc = next(n for n in nets if n.name == "VCC")
        assert len(vcc.nodes) == 4
        vcc_refs = {node.ref for node in vcc.nodes}
        assert "U1" in vcc_refs
        assert "R1" in vcc_refs

    def test_net_nodes(self):
        _, nets = parse_netlist(FIXTURES / "simple.net")
        nrst = next(n for n in nets if n.name == "NRST")
        assert len(nrst.nodes) == 2
        node_refs = [(n.ref, n.pin) for n in nrst.nodes]
        assert ("U1", "7") in node_refs
        assert ("R1", "2") in node_refs
