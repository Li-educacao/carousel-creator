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
from pcb_autoplacer.placer.constraints import resolve_overlaps, validate_placement


def snap_to_grid(value: float, grid: float = DEFAULT_GRID_MM) -> float:
    """Snap a coordinate to the nearest grid point."""
    return round(value / grid) * grid


def calculate_board_size(
    components: list[Component],
    footprints: dict[str, FootprintDef],
    target_fill_ratio: float = 0.25,
    min_size: float = 30.0,
    grid: float = 5.0,
    logo_space_mm: tuple[float, float] = (15.0, 7.0),
) -> tuple[float, float]:
    """Calculate optimal board size based on component areas.

    Uses a fill ratio target (25% = plenty of routing space) and finds the
    largest component to set a minimum dimension. Reserves space for an
    optional logo. Returns (width, height) rounded up to the nearest grid (5mm).

    Args:
        components: List of components to place
        footprints: Resolved footprint definitions keyed by ref
        target_fill_ratio: Target component area / board area (0.25 = 25%)
        min_size: Minimum board dimension in mm
        grid: Round up dimensions to this grid (mm)
        logo_space_mm: (width, height) in mm reserved for logo on the board
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

    # Add logo area to total before calculating required board area
    logo_area = logo_space_mm[0] * logo_space_mm[1]
    total_area += logo_area

    # Required board area based on fill ratio
    required_area = total_area / target_fill_ratio

    # Use a 4:3 aspect ratio (wider boards work better for grid placement)
    aspect = 4.0 / 3.0
    width_est = math.sqrt(required_area * aspect)
    height_est = required_area / width_est

    # Content height: tallest component + logo + margin between them
    max_content_height = max_h + logo_space_mm[1] + 2.0

    # Ensure the board fits the widest component + margins
    width = max(width_est, max_w + 10.0, logo_space_mm[0] + 10.0, min_size)
    height = max(height_est, max_content_height + 10.0, min_size)

    # Round up to grid
    width = math.ceil(width / grid) * grid
    height = math.ceil(height / grid) * grid

    return width, height


def auto_size_board(
    components: list[Component],
    nets: list[Net],
    footprints: dict[str, FootprintDef],
    logo_space_mm: tuple[float, float] = (15.0, 7.0),
    target_fill_ratio: float = 0.25,
    min_size: float = 30.0,
    max_iterations: int = 10,
) -> tuple[BoardConfig, list[PlacedComponent]]:
    """Auto-calculate board size and place components iteratively.

    Estimates board size via calculate_board_size(), generates a fallback
    grid placement, validates it, and grows the board by 5mm per axis if
    placement is invalid. Repeats up to max_iterations times.

    Returns:
        (board_config, placed_components)
    """
    width, height = calculate_board_size(
        components, footprints,
        target_fill_ratio=target_fill_ratio,
        min_size=min_size,
        logo_space_mm=logo_space_mm,
    )

    for _ in range(max_iterations):
        board = BoardConfig(width_mm=width, height_mm=height)
        ai_placements = fallback_placement(components, footprints, board)
        placed = apply_placement(components, nets, footprints, ai_placements, board)

        # Resolve overlaps by pushing components apart (500 iterations)
        placed, remaining = resolve_overlaps(placed, board, max_iterations=500)
        result = validate_placement(placed, board)

        if result["valid"]:
            return board, placed

        # Grow board (more width than height for better grid packing)
        width += 5.0
        height += 5.0

    # Return last attempt even if not fully valid
    return board, placed


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
    Sorts largest-first for better packing. Uses visual bbox centers to avoid
    offset-related overlaps.
    """
    # Sort by footprint area (largest first) for better grid packing
    def _comp_area(comp: Component) -> float:
        fp = footprints.get(comp.ref)
        return (fp.bbox_width * fp.bbox_height) if fp else 25.0

    sorted_comps = sorted(components, key=_comp_area, reverse=True)

    placements = []
    margin = board.edge_clearance_mm + 2.0
    x_cursor = margin
    y_cursor = margin
    row_height = 0.0
    spacing = 2.5  # mm between components

    for comp in sorted_comps:
        fp = footprints.get(comp.ref)
        w = fp.bbox_width if fp else 5.0
        h = fp.bbox_height if fp else 5.0
        ox = fp.bbox_offset_x if fp else 0.0
        oy = fp.bbox_offset_y if fp else 0.0

        # Check if component fits in current row
        if x_cursor + w + spacing > board.width_mm - margin:
            x_cursor = margin
            y_cursor += row_height + spacing
            row_height = 0.0

        # Place at visual center, then subtract offset to get origin position
        # (apply_placement adds board.origin, so we work in local coords)
        visual_cx = x_cursor + w / 2
        visual_cy = y_cursor + h / 2
        origin_x = visual_cx - ox
        origin_y = visual_cy - oy

        placements.append({
            "ref": comp.ref,
            "x": snap_to_grid(origin_x),
            "y": snap_to_grid(origin_y),
            "rotation": 0,
            "layer": "F.Cu",
        })

        x_cursor += w + spacing
        row_height = max(row_height, h)

    return placements
