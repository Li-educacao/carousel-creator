"""Parse KiCad .net (netlist) files into Component and Net domain objects."""
from __future__ import annotations

from pathlib import Path

from pcb_autoplacer.models import Component, Net, NetNode
from pcb_autoplacer.parsers import sexpr


def parse_netlist(path: Path) -> tuple[list[Component], list[Net]]:
    """Parse a KiCad .net file and return (components, nets).

    The netlist S-expression structure expected:

        (export (version D)
          (components
            (comp (ref R1) (value 10k)
                  (footprint Resistor_SMD:R_0805_2012Metric)
                  (property (name "key") (value "val")) ...)
            ...)
          (nets
            (net (code 0) (name ""))
            (net (code 1) (name "GND")
                 (node (ref R1) (pin 1)) ...)
            ...))

    Net code 0 (unconnected) is filtered out.
    """
    text = path.read_text(encoding="utf-8")
    tree = sexpr.parse(text)

    # Root node should be 'export'
    if not isinstance(tree, list) or not tree or tree[0] != "export":
        raise ValueError(f"Expected 'export' root in netlist, got: {tree[0] if tree else 'empty'}")

    components = _parse_components(tree)
    nets = _parse_nets(tree)
    return components, nets


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_components(export_tree: list) -> list[Component]:
    """Extract all <comp> entries from the <components> section."""
    components_node = sexpr.find_node(export_tree, "components")
    if components_node is None:
        return []

    result: list[Component] = []
    for comp_node in sexpr.find_nodes(components_node, "comp"):
        ref = sexpr.get_value(comp_node, "ref")
        value = sexpr.get_value(comp_node, "value")
        footprint_str = sexpr.get_value(comp_node, "footprint")
        description = sexpr.get_value(comp_node, "description")

        # Split "Library:FootprintName" into parts
        library = ""
        footprint_name = ""
        if ":" in footprint_str:
            library, footprint_name = footprint_str.split(":", 1)
        else:
            footprint_name = footprint_str

        # Collect arbitrary <property> entries
        properties: dict[str, str] = {}
        for prop_node in sexpr.find_nodes(comp_node, "property"):
            prop_name = sexpr.get_value(prop_node, "name")
            prop_value = sexpr.get_value(prop_node, "value")
            if prop_name:
                properties[prop_name] = prop_value

        result.append(Component(
            ref=ref,
            value=value,
            footprint=footprint_str,
            library=library,
            footprint_name=footprint_name,
            description=description,
            properties=properties,
        ))

    return result


def _parse_nets(export_tree: list) -> list[Net]:
    """Extract all <net> entries from the <nets> section, skipping code 0."""
    nets_node = sexpr.find_node(export_tree, "nets")
    if nets_node is None:
        return []

    result: list[Net] = []
    for net_node in sexpr.find_nodes(nets_node, "net"):
        code_str = sexpr.get_value(net_node, "code", "0")
        try:
            code = int(code_str)
        except ValueError:
            code = 0

        # Skip the unconnected net
        if code == 0:
            continue

        name = sexpr.get_value(net_node, "name")

        nodes: list[NetNode] = []
        for node_item in sexpr.find_nodes(net_node, "node"):
            n_ref = sexpr.get_value(node_item, "ref")
            n_pin = sexpr.get_value(node_item, "pin")
            if n_ref:
                nodes.append(NetNode(ref=n_ref, pin=n_pin))

        result.append(Net(code=code, name=name, nodes=nodes))

    return result
