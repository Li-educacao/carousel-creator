"""Parse KiCad .kicad_mod footprint files into FootprintDef domain objects."""
from __future__ import annotations

from pathlib import Path

from pcb_autoplacer.config import KICAD_FOOTPRINT_LIBS, KICAD_SYSTEM_FOOTPRINTS
from pcb_autoplacer.models import FootprintDef, Pad
from pcb_autoplacer.parsers import sexpr


def parse_footprint(path: Path) -> FootprintDef:
    """Parse a .kicad_mod file into a FootprintDef.

    KiCad footprint structure:

        (footprint "R_0805_2012Metric"
          (version ...)
          (generator ...)
          (layer "F.Cu")
          (descr "Resistor SMD ...")
          (pad "1" smd roundrect
               (at -0.9125 0)
               (size 1.025 1.4)
               (layers "F.Cu" "F.Paste" "F.Mask") ...)
          (pad "2" smd roundrect
               (at 0.9125 0)
               (size 1.025 1.4)
               (layers "F.Cu" "F.Paste" "F.Mask") ...))
    """
    text = path.read_text(encoding="utf-8")
    tree = sexpr.parse(text)

    if not isinstance(tree, list) or not tree or tree[0] != "footprint":
        raise ValueError(
            f"Expected 'footprint' root in {path.name}, got: {tree[0] if tree else 'empty'}"
        )

    # Name is the second element (string)
    name = tree[1] if len(tree) > 1 and isinstance(tree[1], str) else path.stem
    description = sexpr.get_value(tree, "descr")

    pads = _parse_pads(tree)

    # Bounding box from pad extents (half-size in each direction from pad centre)
    bbox_width, bbox_height, bbox_offset_x, bbox_offset_y = _compute_bbox(pads)

    # Classify as SMD if at least one SMD pad exists (and no thru-hole pads);
    # if there are thru-hole pads the footprint is not SMD.
    has_smd = any(p.pad_type == "smd" for p in pads)
    has_thru = any(p.pad_type == "thru_hole" for p in pads)
    is_smd = has_smd and not has_thru

    return FootprintDef(
        name=name,
        library="",  # caller may fill in after resolve_footprint
        description=description,
        pads=pads,
        bbox_width=bbox_width,
        bbox_height=bbox_height,
        bbox_offset_x=bbox_offset_x,
        bbox_offset_y=bbox_offset_y,
        is_smd=is_smd,
    )


def resolve_footprint(footprint_str: str) -> Path | None:
    """Resolve a 'Library:Footprint' string to an actual .kicad_mod file path.

    Searches KICAD_SYSTEM_FOOTPRINTS first, then KICAD_FOOTPRINT_LIBS (user
    libraries).  Returns the first match as a Path, or None if not found.

    Example:
        resolve_footprint('Resistor_SMD:R_0805_2012Metric')
        → Path('/Applications/KiCad/KiCad.app/.../Resistor_SMD.pretty/R_0805_2012Metric.kicad_mod')
    """
    if ":" not in footprint_str:
        return None

    library, name = footprint_str.split(":", 1)
    filename = f"{name}.kicad_mod"
    pretty_dir = f"{library}.pretty"

    for base in (KICAD_SYSTEM_FOOTPRINTS, KICAD_FOOTPRINT_LIBS):
        candidate = base / pretty_dir / filename
        if candidate.is_file():
            return candidate

    return None


def load_footprint(footprint_str: str) -> FootprintDef | None:
    """Resolve and parse a footprint string.

    Returns a FootprintDef with the library field populated, or None if the
    .kicad_mod file cannot be found. Falls back to built-in definitions for
    common JLCPCB/standard packages.
    """
    path = resolve_footprint(footprint_str)
    if path is None:
        # Try fallback for common packages
        return _fallback_footprint(footprint_str)

    fp = parse_footprint(path)

    # Populate the library name from the footprint string
    if ":" in footprint_str:
        fp.library = footprint_str.split(":", 1)[0]

    return fp


# Common SMD/THT packages with known dimensions and pad layouts.
# Sizes from IPC-7351 nominal land patterns.
_FALLBACK_PACKAGES: dict[str, dict] = {
    "C_0805": {
        "bbox": (2.0, 1.4), "is_smd": True,
        "pads": [
            Pad(number="1", pad_type="smd", shape="roundrect", x=-0.91, y=0, width=1.02, height=1.4, layers=["F.Cu", "F.Paste", "F.Mask"]),
            Pad(number="2", pad_type="smd", shape="roundrect", x=0.91, y=0, width=1.02, height=1.4, layers=["F.Cu", "F.Paste", "F.Mask"]),
        ],
    },
    "R_0805": {
        "bbox": (2.0, 1.4), "is_smd": True,
        "pads": [
            Pad(number="1", pad_type="smd", shape="roundrect", x=-0.91, y=0, width=1.02, height=1.4, layers=["F.Cu", "F.Paste", "F.Mask"]),
            Pad(number="2", pad_type="smd", shape="roundrect", x=0.91, y=0, width=1.02, height=1.4, layers=["F.Cu", "F.Paste", "F.Mask"]),
        ],
    },
    "R_0603": {
        "bbox": (1.6, 1.0), "is_smd": True,
        "pads": [
            Pad(number="1", pad_type="smd", shape="roundrect", x=-0.75, y=0, width=0.8, height=1.0, layers=["F.Cu", "F.Paste", "F.Mask"]),
            Pad(number="2", pad_type="smd", shape="roundrect", x=0.75, y=0, width=0.8, height=1.0, layers=["F.Cu", "F.Paste", "F.Mask"]),
        ],
    },
    "C_0603": {
        "bbox": (1.6, 1.0), "is_smd": True,
        "pads": [
            Pad(number="1", pad_type="smd", shape="roundrect", x=-0.75, y=0, width=0.8, height=1.0, layers=["F.Cu", "F.Paste", "F.Mask"]),
            Pad(number="2", pad_type="smd", shape="roundrect", x=0.75, y=0, width=0.8, height=1.0, layers=["F.Cu", "F.Paste", "F.Mask"]),
        ],
    },
    "D_SOD-123FL": {
        "bbox": (2.8, 1.8), "is_smd": True,
        "pads": [
            Pad(number="1", pad_type="smd", shape="roundrect", x=-1.18, y=0, width=0.91, height=1.22, layers=["F.Cu", "F.Paste", "F.Mask"]),
            Pad(number="2", pad_type="smd", shape="roundrect", x=1.18, y=0, width=0.91, height=1.22, layers=["F.Cu", "F.Paste", "F.Mask"]),
        ],
    },
    "Q_SOT-23": {
        "bbox": (3.0, 2.6), "is_smd": True,
        "pads": [
            Pad(number="1", pad_type="smd", shape="roundrect", x=-1.0, y=1.1, width=0.9, height=0.8, layers=["F.Cu", "F.Paste", "F.Mask"]),
            Pad(number="2", pad_type="smd", shape="roundrect", x=1.0, y=1.1, width=0.9, height=0.8, layers=["F.Cu", "F.Paste", "F.Mask"]),
            Pad(number="3", pad_type="smd", shape="roundrect", x=0, y=-1.1, width=0.9, height=0.8, layers=["F.Cu", "F.Paste", "F.Mask"]),
        ],
    },
}


def _fallback_footprint(footprint_str: str) -> FootprintDef | None:
    """Return a built-in FootprintDef for common packages not found on disk."""
    if ":" not in footprint_str:
        return None

    library, name = footprint_str.split(":", 1)

    pkg = _FALLBACK_PACKAGES.get(name)
    if pkg is None:
        return None

    return FootprintDef(
        name=name,
        library=library,
        pads=list(pkg["pads"]),
        bbox_width=pkg["bbox"][0],
        bbox_height=pkg["bbox"][1],
        is_smd=pkg["is_smd"],
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_pads(footprint_tree: list) -> list[Pad]:
    """Parse all pad nodes inside the footprint tree."""
    pads: list[Pad] = []

    for pad_node in sexpr.find_nodes(footprint_tree, "pad"):
        # (pad "1" smd roundrect (at ...) (size ...) (drill ...) (layers ...))
        # Positional atoms: index 1 = number, 2 = type, 3 = shape
        number = _atom_at(pad_node, 1, "")
        pad_type = _atom_at(pad_node, 2, "smd")
        shape = _atom_at(pad_node, 3, "rect")

        # (at x y [rotation])
        x, y = 0.0, 0.0
        at_node = sexpr.find_node(pad_node, "at")
        if at_node and len(at_node) >= 3:
            x = _float(at_node[1])
            y = _float(at_node[2])

        # (size width height)
        width, height = 0.0, 0.0
        size_node = sexpr.find_node(pad_node, "size")
        if size_node and len(size_node) >= 3:
            width = _float(size_node[1])
            height = _float(size_node[2])

        # (drill diameter) — circle drill; (drill oval w h) for oval
        drill = 0.0
        drill_node = sexpr.find_node(pad_node, "drill")
        if drill_node and len(drill_node) >= 2:
            # First sub-element may be "oval" keyword; skip it
            drill_val_idx = 1
            if isinstance(drill_node[1], str) and drill_node[1] == "oval":
                drill_val_idx = 2
            if len(drill_node) > drill_val_idx:
                drill = _float(drill_node[drill_val_idx])

        # (layers "F.Cu" "F.Paste" "F.Mask")
        layers: list[str] = []
        layers_node = sexpr.find_node(pad_node, "layers")
        if layers_node:
            layers = [item for item in layers_node[1:] if isinstance(item, str)]

        pads.append(Pad(
            number=number,
            pad_type=pad_type,
            shape=shape,
            x=x,
            y=y,
            width=width,
            height=height,
            drill=drill,
            layers=layers,
        ))

    return pads


def _compute_bbox(pads: list[Pad]) -> tuple[float, float, float, float]:
    """Return (width, height, offset_x, offset_y) bounding box covering all pad extents.

    offset_x/y is the center of the bbox relative to the footprint origin (0,0).
    For symmetric footprints this is (0,0); for asymmetric ones (e.g. DIP with
    pin 1 at origin) the offset shifts the visual rectangle to match the pads.
    """
    if not pads:
        return 0.0, 0.0, 0.0, 0.0

    min_x = min(p.x - p.width / 2 for p in pads)
    max_x = max(p.x + p.width / 2 for p in pads)
    min_y = min(p.y - p.height / 2 for p in pads)
    max_y = max(p.y + p.height / 2 for p in pads)

    width = max_x - min_x
    height = max_y - min_y
    offset_x = (min_x + max_x) / 2
    offset_y = (min_y + max_y) / 2

    return width, height, offset_x, offset_y


def _atom_at(node: list, index: int, default: str) -> str:
    """Return the string atom at position index, or default."""
    if index < len(node) and isinstance(node[index], str):
        return node[index]
    return default


def _float(value: str | float | int) -> float:
    """Safely convert a token to float, returning 0.0 on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
