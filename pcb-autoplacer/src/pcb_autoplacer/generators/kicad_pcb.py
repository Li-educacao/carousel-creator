"""KiCad PCB file generator — assembles complete .kicad_pcb."""
from __future__ import annotations

import uuid
from pathlib import Path

from pcb_autoplacer.generators.board_setup import (
    generate_board_outline,
    generate_general,
    generate_ground_zone,
    generate_header,
    generate_layers,
    generate_net_classes,
    generate_nets,
    generate_setup,
)
from pcb_autoplacer.generators.sexpr_writer import Quoted, serialize, write_sexpr_file
from pcb_autoplacer.models import BoardConfig, FootprintDef, Net, Pad, PlacedComponent


def generate_pcb(
    placed: list[PlacedComponent],
    nets: list[Net],
    board: BoardConfig,
    output_path: Path,
) -> Path:
    """Generate a complete .kicad_pcb file."""
    tree = generate_header()
    tree.append(generate_general(board))
    tree.append(generate_layers())
    tree.append(generate_setup())

    # Net declarations
    net_entries: list[tuple[int, str]] = [(0, "")]
    for net in nets:
        if net.code > 0:
            net_entries.append((net.code, net.name))
    for net_node in generate_nets(net_entries):
        tree.append(net_node)

    # Board outline
    for outline_element in generate_board_outline(board):
        tree.append(outline_element)

    # Footprints
    net_map = {net.name: net.code for net in nets}
    for comp in placed:
        fp_tree = _build_footprint_tree(comp, net_map)
        tree.append(fp_tree)

    # Ground plane zone on B.Cu
    gnd_net = next((n for n in nets if n.name == "GND"), None)
    if gnd_net:
        zone = generate_ground_zone(board, gnd_net.code, gnd_net.name, "B.Cu")
        tree.append(zone)

    write_sexpr_file(tree, output_path)
    return output_path


def _build_footprint_tree(comp: PlacedComponent, net_map: dict[str, int]) -> list:
    """Build S-expression tree for a single placed footprint."""
    fp_def = comp.footprint_def

    # Determine bounding box for visual elements
    # ox/oy shifts the rectangle center to match actual pad positions
    if fp_def:
        hw = fp_def.bbox_width / 2
        hh = fp_def.bbox_height / 2
        ox = fp_def.bbox_offset_x
        oy = fp_def.bbox_offset_y
    else:
        hw, hh = 1.5, 1.5  # default 3x3mm for unknown
        ox, oy = 0.0, 0.0

    tree: list = ["footprint", comp.footprint,
                  ["layer", comp.layer],
                  ["uuid", str(uuid.uuid4())],
                  ["at", f"{comp.x:.4f}", f"{comp.y:.4f}", f"{comp.rotation:.0f}"]]

    # Reference property — use custom offset if provided, else default above bbox
    if comp.ref_offset:
        ref_x, ref_y = comp.ref_offset
    else:
        ref_x, ref_y = ox, oy - hh - 1.0
    tree.append(["property", "Reference", comp.ref,
                 ["at", f"{ref_x:.2f}", f"{ref_y:.2f}"],
                 ["layer", "F.SilkS"],
                 ["uuid", str(uuid.uuid4())],
                 ["effects", ["font", ["size", "0.8", "0.8"], ["thickness", "0.12"]]]])

    # Value property — optionally hidden to reduce clutter
    val_node = ["property", "Value", comp.value,
                ["at", f"{ox:.2f}", f"{oy + hh + 1.0:.2f}"],
                ["layer", "F.Fab"],
                ["uuid", str(uuid.uuid4())],
                ["effects", ["font", ["size", "0.8", "0.8"], ["thickness", "0.12"]]]]
    if comp.hide_value:
        val_node.append("hide")
    tree.append(val_node)

    # Courtyard rectangle (makes component visible in KiCad)
    crt_margin = 0.25
    tree.append(["fp_rect",
                 ["start", f"{ox - hw - crt_margin:.4f}", f"{oy - hh - crt_margin:.4f}"],
                 ["end", f"{ox + hw + crt_margin:.4f}", f"{oy + hh + crt_margin:.4f}"],
                 ["stroke", ["width", "0.05"], ["type", "solid"]],
                 ["fill", "none"],
                 ["layer", "F.CrtYd"],
                 ["uuid", str(uuid.uuid4())]])

    # Fabrication layer outline
    tree.append(["fp_rect",
                 ["start", f"{ox - hw:.4f}", f"{oy - hh:.4f}"],
                 ["end", f"{ox + hw:.4f}", f"{oy + hh:.4f}"],
                 ["stroke", ["width", "0.1"], ["type", "solid"]],
                 ["fill", "none"],
                 ["layer", "F.Fab"],
                 ["uuid", str(uuid.uuid4())]])

    # Silkscreen outline (slightly larger)
    silk_margin = 0.12
    tree.append(["fp_rect",
                 ["start", f"{ox - hw - silk_margin:.4f}", f"{oy - hh - silk_margin:.4f}"],
                 ["end", f"{ox + hw + silk_margin:.4f}", f"{oy + hh + silk_margin:.4f}"],
                 ["stroke", ["width", "0.12"], ["type", "solid"]],
                 ["fill", "none"],
                 ["layer", "F.SilkS"],
                 ["uuid", str(uuid.uuid4())]])

    # Pads with net assignments
    if fp_def:
        for pad in fp_def.pads:
            pad_tree = _build_pad_tree(pad, net_map)
            tree.append(pad_tree)

    return tree


def _build_pad_tree(pad: Pad, net_map: dict[str, int]) -> list:
    """Build S-expression tree for a single pad."""
    tree: list = ["pad", Quoted(pad.number), pad.pad_type, pad.shape,
                  ["at", f"{pad.x:.4f}", f"{pad.y:.4f}"],
                  ["size", f"{pad.width:.4f}", f"{pad.height:.4f}"]]

    if pad.drill > 0:
        tree.append(["drill", f"{pad.drill:.4f}"])

    # Layers
    if pad.layers:
        layer_node: list = ["layers"] + pad.layers
        tree.append(layer_node)

    # Net assignment
    if pad.net_name and pad.net_name in net_map:
        tree.append(["net", str(net_map[pad.net_name]), pad.net_name])

    tree.append(["uuid", str(uuid.uuid4())])

    return tree
