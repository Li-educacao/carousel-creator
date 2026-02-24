"""S-expression writer — serialize Python lists to KiCad format."""
from __future__ import annotations


class Quoted(str):
    """Marker class to force quoting in S-expression output."""
    pass


def serialize(tree: list, indent: int = 0) -> str:
    """Serialize a nested list to S-expression string with proper formatting.

    ['footprint', 'R_0805', ['at', '1.0', '2.0']]
    → '(footprint "R_0805"\n  (at 1.0 2.0)\n)'
    """
    if not tree:
        return "()"

    has_sublists = any(isinstance(item, list) for item in tree)

    if not has_sublists:
        # Simple node — single line
        atoms = [_format_atom(item) for item in tree]
        return "(" + " ".join(atoms) + ")"

    # Complex node — tag on first line, children indented
    tag = _format_atom(tree[0])
    inline_atoms = []
    children = []

    for item in tree[1:]:
        if isinstance(item, list):
            children.append(item)
        else:
            inline_atoms.append(_format_atom(item))

    # Build first line: (tag atom1 atom2
    first_line = "(" + tag
    if inline_atoms:
        first_line += " " + " ".join(inline_atoms)

    if not children:
        return first_line + ")"

    parts = [first_line]

    child_indent = indent + 2
    prefix = " " * child_indent
    for child in children:
        parts.append(prefix + serialize(child, child_indent))

    parts.append(" " * indent + ")")
    return "\n".join(parts)


_KICAD_KEYWORDS = frozenset({
    # S-expression tags (never appear as values, but just in case)
    "kicad_pcb", "footprint", "pad", "net", "layers", "layer", "at", "size",
    "drill", "property", "effects", "font", "thickness", "stroke", "fill",
    "start", "end", "fp_rect", "fp_line", "fp_circle", "fp_arc", "fp_poly",
    "fp_text", "gr_line", "gr_rect", "gr_circle", "gr_arc", "gr_poly",
    "general", "setup", "stackup", "pcbplotparams", "uuid", "version",
    "generator", "generator_version", "paper", "tenting",
    # Boolean-like keywords
    "yes", "no",
    # Layer types
    "signal", "user", "power", "mixed", "jumper",
    # Pad types
    "smd", "thru_hole", "np_thru_hole", "connect",
    # Pad shapes
    "rect", "oval", "circle", "roundrect", "trapezoid", "custom",
    # Stroke/fill keywords
    "none", "solid", "dash", "dot", "dash_dot", "dash_dot_dot", "default",
    # Tenting keywords
    "front", "back",
    # Other bare keywords
    "hide", "locked", "unlocked", "type", "width", "height",
    "pintype", "pinfunction", "embedded_fonts",
    "legacy_teardrops", "pad_to_mask_clearance",
    "allow_soldermask_bridges_in_footprints",
    "copper_finish", "dielectric_constraints",
    "roundrect_rratio", "offset", "xyz", "scale", "model",
    "material", "epsilon_r", "loss_tangent", "descr", "tags",
    # Net class keywords
    "net_class", "trace_width", "clearance", "via_diameter", "via_drill",
    "microvia_diameter", "microvia_drill", "add_net",
    # Zone / ground plane keywords
    "zone", "polygon", "pts", "xy", "connect_pads", "min_thickness",
    "thermal_gap", "thermal_bridge_width", "hatch", "edge",
    "net_name", "name",
    # Plot params (bare keyword names)
    "layerselection", "plot_on_all_layers_selection",
    "disableapertmacros", "usegerberextensions", "usegerberattributes",
    "usegerberadvancedattributes", "creategerberjobfile",
    "dashed_line_dash_ratio", "dashed_line_gap_ratio", "svgprecision",
    "plotframeref", "mode", "useauxorigin", "hpglpennumber", "hpglpenspeed",
    "hpglpendiameter", "pdf_front_fp_property_popups",
    "pdf_back_fp_property_popups", "pdf_metadata", "pdf_single_document",
    "dxfpolygonmode", "dxfimperialunits", "dxfusepcbnewfont",
    "psnegative", "psa4output", "plotreference", "plotvalue", "plotfptext",
    "plotinvisibletext", "sketchpadsonfab", "subtractmaskfromsilk",
    "outputformat", "mirror", "drillshape", "scaleselection", "outputdirectory",
})


def _format_atom(value) -> str:
    """Format a single atom for S-expression output.

    KiCad 9 format rules:
    - Numbers stay unquoted: 1.6, 0, 20241229
    - Known keywords stay unquoted: yes, no, signal, smd, rect, etc.
    - Everything else gets quoted: layer names, net names, refs, values, UUIDs
    """
    s = str(value)

    # Empty string → ""
    if not s:
        return '""'

    # Explicitly marked for quoting
    if isinstance(value, Quoted):
        return f'"{s}"'

    # Numbers stay unquoted
    try:
        float(s)
        return s
    except ValueError:
        pass

    # Hex values stay unquoted (layerselection etc.)
    if s.startswith("0x"):
        return s

    # Known KiCad keywords stay unquoted
    if s in _KICAD_KEYWORDS:
        return s

    # Everything else gets quoted
    return f'"{s}"'


def write_sexpr_file(tree: list, path) -> None:
    """Write S-expression tree to a file."""
    from pathlib import Path

    text = serialize(tree)
    Path(path).write_text(text + "\n", encoding="utf-8")
