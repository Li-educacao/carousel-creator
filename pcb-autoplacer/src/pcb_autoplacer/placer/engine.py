"""Placement engine — applies AI strategy to components."""
from __future__ import annotations

import copy
import math

from pcb_autoplacer.config import DEFAULT_GRID_MM
from pcb_autoplacer.models import (
    BoardConfig,
    Component,
    FootprintDef,
    Net,
    NetNode,
    PlacedComponent,
)


def snap_to_grid(value: float, grid: float = DEFAULT_GRID_MM) -> float:
    """Snap a coordinate to the nearest grid point."""
    return round(value / grid) * grid


def calculate_board_size(
    components: list[Component],
    footprints: dict[str, FootprintDef],
    target_fill_ratio: float = 0.25,
    min_size: float = 30.0,
    grid: float = 5.0,
) -> tuple[float, float]:
    """Calculate optimal board size based on component areas.

    Uses a fill ratio target (25% = plenty of routing space) and finds the
    largest component to set a minimum dimension. Returns (width, height)
    rounded up to the nearest grid (5mm).

    Args:
        components: List of components to place
        footprints: Resolved footprint definitions keyed by ref
        target_fill_ratio: Target component area / board area (0.25 = 25%)
        min_size: Minimum board dimension in mm
        grid: Round up dimensions to this grid (mm)
    """
    total_area = 0.0
    max_w = 0.0
    max_h = 0.0

    for comp in components:
        fp = footprints.get(comp.ref)
        w = fp.bbox_width if fp else 3.0
        h = fp.bbox_height if fp else 3.0
        total_area += w * h
        max_w = max(max_w, w)
        max_h = max(max_h, h)

    # Required board area based on fill ratio
    required_area = total_area / target_fill_ratio

    # Start with a square board, then adjust
    side = math.sqrt(required_area)

    # Ensure the board is wide enough for the widest component + margins
    width = max(side, max_w + 10.0, min_size)
    height = max(required_area / width, max_h + 10.0, min_size)

    # Round up to grid
    width = math.ceil(width / grid) * grid
    height = math.ceil(height / grid) * grid

    return width, height


def apply_placement(
    components: list[Component],
    nets: list[Net],
    footprints: dict[str, FootprintDef],
    ai_placements: list[dict],
    board: BoardConfig,
) -> list[PlacedComponent]:
    """Apply AI-generated placements to components.

    Args:
        components: Parsed components from netlist
        nets: Parsed nets from netlist
        footprints: Resolved footprint definitions (keyed by ref)
        ai_placements: AI output [{ref, x, y, rotation, layer}, ...]
        board: Board configuration

    Returns:
        List of PlacedComponent with absolute board coordinates
    """
    # Index components by ref
    comp_map = {c.ref: c for c in components}

    # Build pad-to-net mapping: (ref, pin) → (net_code, net_name)
    pad_net_map: dict[tuple[str, str], tuple[int, str]] = {}
    for net in nets:
        for node in net.nodes:
            pad_net_map[(node.ref, node.pin)] = (net.code, net.name)

    # Build placement index from AI output
    ai_map = {p["ref"]: p for p in ai_placements}

    placed = []
    for comp in components:
        ai = ai_map.get(comp.ref)
        if not ai:
            continue

        # Snap coordinates to grid, offset by board origin
        x = snap_to_grid(ai["x"]) + board.origin_x
        y = snap_to_grid(ai["y"]) + board.origin_y
        rotation = float(ai.get("rotation", 0))
        layer = ai.get("layer", "F.Cu")

        # Get footprint definition and assign nets to pads
        fp_def = footprints.get(comp.ref)
        if fp_def:
            fp_def = _assign_pad_nets(fp_def, comp.ref, pad_net_map)

        placed.append(PlacedComponent(
            ref=comp.ref,
            value=comp.value,
            footprint=comp.footprint,
            x=x,
            y=y,
            rotation=rotation,
            layer=layer,
            footprint_def=fp_def,
            ref_offset=ai.get("ref_offset"),
            hide_value=ai.get("hide_value", False),
        ))

    return placed


def _assign_pad_nets(
    fp_def: FootprintDef,
    ref: str,
    pad_net_map: dict[tuple[str, str], tuple[int, str]],
) -> FootprintDef:
    """Assign net info to footprint pads based on netlist connections."""
    fp = copy.deepcopy(fp_def)
    for pad in fp.pads:
        key = (ref, pad.number)
        if key in pad_net_map:
            pad.net_number, pad.net_name = pad_net_map[key]
    return fp


def fallback_placement(
    components: list[Component],
    footprints: dict[str, FootprintDef],
    board: BoardConfig,
) -> list[dict]:
    """Simple grid-based fallback placement if AI is unavailable.

    Places components in a grid pattern with spacing based on component size.
    """
    placements = []
    x_cursor = board.edge_clearance_mm + 5.0
    y_cursor = board.edge_clearance_mm + 5.0
    row_height = 0.0

    for comp in components:
        fp = footprints.get(comp.ref)
        w = fp.bbox_width if fp else 5.0
        h = fp.bbox_height if fp else 5.0
        spacing = 2.0  # mm between components

        # Check if component fits in current row
        if x_cursor + w + spacing > board.width_mm - board.edge_clearance_mm:
            x_cursor = board.edge_clearance_mm + 5.0
            y_cursor += row_height + spacing
            row_height = 0.0

        placements.append({
            "ref": comp.ref,
            "x": snap_to_grid(x_cursor + w / 2),
            "y": snap_to_grid(y_cursor + h / 2),
            "rotation": 0,
            "layer": "F.Cu",
        })

        x_cursor += w + spacing
        row_height = max(row_height, h)

    return placements
