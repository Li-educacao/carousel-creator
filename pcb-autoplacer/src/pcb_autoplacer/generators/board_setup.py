"""Board setup generator — layers, stackup, design rules, outline for KiCad 9."""
from __future__ import annotations

import uuid

from pcb_autoplacer.config import JLCPCB
from pcb_autoplacer.generators.sexpr_writer import Quoted
from pcb_autoplacer.models import BoardConfig


def generate_header() -> list:
    """Generate kicad_pcb header (KiCad 9 format)."""
    return ["kicad_pcb", ["version", "20241229"], ["generator", "pcbnew"],
            ["generator_version", Quoted("9.0")]]


def generate_general(board: BoardConfig) -> list:
    """Generate general section."""
    return ["general",
            ["thickness", str(JLCPCB.board_thickness_mm)],
            ["legacy_teardrops", "no"]]


def generate_layers() -> list:
    """Generate 2-layer stackup layer definitions (KiCad 9 IDs)."""
    return ["layers",
            ["0", "F.Cu", "signal"],
            ["2", "B.Cu", "signal"],
            ["9", "F.Adhes", "user", "F.Adhesive"],
            ["11", "B.Adhes", "user", "B.Adhesive"],
            ["13", "F.Paste", "user"],
            ["15", "B.Paste", "user"],
            ["5", "F.SilkS", "user", "F.Silkscreen"],
            ["7", "B.SilkS", "user", "B.Silkscreen"],
            ["1", "F.Mask", "user"],
            ["3", "B.Mask", "user"],
            ["17", "Dwgs.User", "user", "User.Drawings"],
            ["19", "Cmts.User", "user", "User.Comments"],
            ["21", "Eco1.User", "user", "User.Eco1"],
            ["23", "Eco2.User", "user", "User.Eco2"],
            ["25", "Edge.Cuts", "user"],
            ["27", "Margin", "user"],
            ["31", "F.CrtYd", "user", "F.Courtyard"],
            ["29", "B.CrtYd", "user", "B.Courtyard"],
            ["35", "F.Fab", "user"],
            ["33", "B.Fab", "user"]]


def generate_setup() -> list:
    """Generate design rules setup section for JLCPCB (KiCad 9 format)."""
    return ["setup",
            ["stackup",
             ["layer", "F.SilkS", ["type", "Top Silk Screen"]],
             ["layer", "F.Paste", ["type", "Top Solder Paste"]],
             ["layer", "F.Mask", ["type", "Top Solder Mask"], ["thickness", "0.01"]],
             ["layer", "F.Cu", ["type", "copper"], ["thickness", "0.035"]],
             ["layer", "dielectric 1", ["type", "core"], ["thickness", "1.51"],
              ["material", "FR4"], ["epsilon_r", "4.5"], ["loss_tangent", "0.02"]],
             ["layer", "B.Cu", ["type", "copper"], ["thickness", "0.035"]],
             ["layer", "B.Mask", ["type", "Bottom Solder Mask"], ["thickness", "0.01"]],
             ["layer", "B.Paste", ["type", "Bottom Solder Paste"]],
             ["layer", "B.SilkS", ["type", "Bottom Silk Screen"]],
             ["copper_finish", "None"],
             ["dielectric_constraints", "no"]],
            ["pad_to_mask_clearance", "0"],
            ["allow_soldermask_bridges_in_footprints", "no"],
            ["tenting", "front", "back"],
            ["pcbplotparams",
             ["layerselection", "0x00000000_00000000_55555555_5755f5ff"],
             ["plot_on_all_layers_selection", "0x00000000_00000000_00000000_00000000"],
             ["disableapertmacros", "no"],
             ["usegerberextensions", "no"],
             ["usegerberattributes", "yes"],
             ["usegerberadvancedattributes", "yes"],
             ["creategerberjobfile", "yes"],
             ["dashed_line_dash_ratio", "12.000000"],
             ["dashed_line_gap_ratio", "3.000000"],
             ["svgprecision", "4"],
             ["plotframeref", "no"],
             ["mode", "1"],
             ["useauxorigin", "no"],
             ["hpglpennumber", "1"],
             ["hpglpenspeed", "20"],
             ["hpglpendiameter", "15.000000"],
             ["pdf_front_fp_property_popups", "yes"],
             ["pdf_back_fp_property_popups", "yes"],
             ["pdf_metadata", "yes"],
             ["pdf_single_document", "no"],
             ["dxfpolygonmode", "yes"],
             ["dxfimperialunits", "no"],
             ["dxfusepcbnewfont", "yes"],
             ["psnegative", "no"],
             ["psa4output", "no"],
             ["plotreference", "yes"],
             ["plotvalue", "yes"],
             ["plotfptext", "yes"],
             ["plotinvisibletext", "no"],
             ["sketchpadsonfab", "no"],
             ["subtractmaskfromsilk", "no"],
             ["outputformat", "1"],
             ["mirror", "no"],
             ["drillshape", "0"],
             ["scaleselection", "1"],
             ["outputdirectory", "gerbers"]]]


def generate_nets(net_names: list[tuple[int, str]]) -> list[list]:
    """Generate net declarations.

    Args:
        net_names: List of (code, name) tuples, e.g. [(0, ""), (1, "GND"), ...]

    Returns:
        List of net S-expression nodes.
    """
    result = []
    for code, name in net_names:
        result.append(["net", str(code), name])
    return result


def generate_board_outline(board: BoardConfig) -> list[list]:
    """Generate board outline as edge cuts rectangle."""
    x0 = board.origin_x
    y0 = board.origin_y
    x1 = board.origin_x + board.width_mm
    y1 = board.origin_y + board.height_mm

    lines = []
    corners = [
        (x0, y0, x1, y0),
        (x1, y0, x1, y1),
        (x1, y1, x0, y1),
        (x0, y1, x0, y0),
    ]
    for sx, sy, ex, ey in corners:
        lines.append(["gr_line",
                      ["start", f"{sx:.4f}", f"{sy:.4f}"],
                      ["end", f"{ex:.4f}", f"{ey:.4f}"],
                      ["stroke", ["width", "0.1"], ["type", "solid"]],
                      ["layer", "Edge.Cuts"],
                      ["uuid", _uuid()]])
    return lines


def generate_net_classes(nets: list[tuple[int, str]]) -> list[list]:
    """Generate net class assignments based on net function.

    Net classes control trace width, clearance, and via size per net.
    Classification:
      - AC_MAINS:  LINE, NEUT, AC nets → 1.0mm trace, 0.5mm clearance
      - Power:     +5V, VCC, GND       → 0.5mm trace, 0.3mm clearance
      - Signal:    everything else      → 0.25mm trace, 0.2mm clearance
    """
    # Classify nets
    ac_nets = []
    power_nets = []
    signal_nets = []

    for code, name in nets:
        if code == 0 or not name:
            continue
        upper = name.upper()
        if any(kw in upper for kw in ("LINE", "NEUT", "AC", "MAINS", "PS1-AC")):
            ac_nets.append(name)
        elif any(kw in upper for kw in ("+5V", "+3V3", "VCC", "VDD", "GND")):
            power_nets.append(name)
        else:
            signal_nets.append(name)

    result = []

    # Default net class (Signal)
    result.append(["net_class", "Default",
                   ["trace_width", "0.25"],
                   ["clearance", "0.2"],
                   ["via_diameter", "0.45"],
                   ["via_drill", "0.2"],
                   ["microvia_diameter", "0.3"],
                   ["microvia_drill", "0.1"]])

    # AC Mains class
    if ac_nets:
        node = ["net_class", "AC_Mains",
                ["trace_width", "1.0"],
                ["clearance", "0.5"],
                ["via_diameter", "0.8"],
                ["via_drill", "0.4"],
                ["microvia_diameter", "0.3"],
                ["microvia_drill", "0.1"]]
        for name in ac_nets:
            node.append(["add_net", name])
        result.append(node)

    # Power class
    if power_nets:
        node = ["net_class", "Power",
                ["trace_width", "0.5"],
                ["clearance", "0.3"],
                ["via_diameter", "0.6"],
                ["via_drill", "0.3"],
                ["microvia_diameter", "0.3"],
                ["microvia_drill", "0.1"]]
        for name in power_nets:
            node.append(["add_net", name])
        result.append(node)

    return result


def generate_ground_zone(
    board: BoardConfig, net_code: int, net_name: str, layer: str = "B.Cu",
) -> list:
    """Generate a copper zone (ground plane) covering the board area.

    The zone polygon is inset from the board edge by ``board.edge_clearance_mm``.
    KiCad will fill the zone automatically (Fill All Zones / key B).
    """
    margin = board.edge_clearance_mm
    x1 = board.origin_x + margin
    y1 = board.origin_y + margin
    x2 = board.origin_x + board.width_mm - margin
    y2 = board.origin_y + board.height_mm - margin

    return [
        "zone",
        ["net", str(net_code)],
        ["net_name", net_name],
        ["layer", layer],
        ["uuid", _uuid()],
        ["name", "GND_PLANE"],
        ["hatch", "edge", "0.508"],
        ["connect_pads", ["clearance", "0.5"]],
        ["min_thickness", "0.25"],
        ["fill", "yes", ["thermal_gap", "0.5"], ["thermal_bridge_width", "0.5"]],
        ["polygon", ["pts",
            ["xy", f"{x1:.4f}", f"{y1:.4f}"],
            ["xy", f"{x2:.4f}", f"{y1:.4f}"],
            ["xy", f"{x2:.4f}", f"{y2:.4f}"],
            ["xy", f"{x1:.4f}", f"{y2:.4f}"],
        ]],
    ]


def _uuid() -> str:
    """Generate a random UUID for KiCad elements."""
    return str(uuid.uuid4())
