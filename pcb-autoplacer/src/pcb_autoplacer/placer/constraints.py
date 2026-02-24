"""Placement constraints — overlap detection, boundary checks, anti-overlap."""
from __future__ import annotations

import math
from dataclasses import dataclass

from pcb_autoplacer.config import DEFAULT_GRID_MM
from pcb_autoplacer.models import BoardConfig, FootprintDef, PlacedComponent


@dataclass
class BBox:
    """Axis-aligned bounding box."""

    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def width(self) -> float:
        return self.x_max - self.x_min

    @property
    def height(self) -> float:
        return self.y_max - self.y_min

    def overlaps(self, other: BBox, clearance: float = 0.0) -> bool:
        """Check if this bbox overlaps another, with optional clearance."""
        return not (
            self.x_max + clearance <= other.x_min
            or other.x_max + clearance <= self.x_min
            or self.y_max + clearance <= other.y_min
            or other.y_max + clearance <= self.y_min
        )


def get_component_bbox(comp: PlacedComponent) -> BBox:
    """Get the bounding box of a placed component in board coordinates."""
    fp = comp.footprint_def
    if fp:
        w, h = fp.bbox_width, fp.bbox_height
        ox, oy = fp.bbox_offset_x, fp.bbox_offset_y
    else:
        w, h = 3.0, 3.0  # default for unknown footprints
        ox, oy = 0.0, 0.0

    # Handle rotation (simplified — only 0/90/180/270)
    rot = comp.rotation % 360
    if rot in (90, 270):
        w, h = h, w
        ox, oy = -oy, ox
    if rot in (180,):
        ox, oy = -ox, -oy

    half_w = w / 2
    half_h = h / 2

    return BBox(
        x_min=comp.x + ox - half_w,
        y_min=comp.y + oy - half_h,
        x_max=comp.x + ox + half_w,
        y_max=comp.y + oy + half_h,
    )


def check_overlaps(
    placed: list[PlacedComponent],
    clearance_mm: float = 0.25,
) -> list[tuple[str, str]]:
    """Check for overlapping components.

    Returns list of (ref1, ref2) pairs that overlap.
    """
    overlaps = []
    bboxes = [(comp, get_component_bbox(comp)) for comp in placed]

    for i in range(len(bboxes)):
        for j in range(i + 1, len(bboxes)):
            comp_a, bbox_a = bboxes[i]
            comp_b, bbox_b = bboxes[j]
            if bbox_a.overlaps(bbox_b, clearance_mm):
                overlaps.append((comp_a.ref, comp_b.ref))

    return overlaps


def check_boundary(
    placed: list[PlacedComponent],
    board: BoardConfig,
    margin_mm: float = 0.5,
) -> list[str]:
    """Check which components are outside the board boundary.

    Returns list of refs that violate the boundary.
    """
    violations = []

    x_min = board.origin_x + margin_mm
    y_min = board.origin_y + margin_mm
    x_max = board.origin_x + board.width_mm - margin_mm
    y_max = board.origin_y + board.height_mm - margin_mm

    board_bbox = BBox(x_min, y_min, x_max, y_max)

    for comp in placed:
        bbox = get_component_bbox(comp)
        if (
            bbox.x_min < board_bbox.x_min
            or bbox.y_min < board_bbox.y_min
            or bbox.x_max > board_bbox.x_max
            or bbox.y_max > board_bbox.y_max
        ):
            violations.append(comp.ref)

    return violations


def resolve_overlaps(
    placed: list[PlacedComponent],
    board: BoardConfig,
    clearance_mm: float = 0.5,
    max_iterations: int = 200,
    grid: float = DEFAULT_GRID_MM,
) -> tuple[list[PlacedComponent], int]:
    """Push overlapping components apart iteratively.

    Uses a repulsion-based approach: for each overlapping pair, compute the
    minimum translation vector (MTV) and push both components in opposite
    directions. Also clamps components to stay within board boundaries.

    Returns:
        (adjusted placed list, remaining overlap count)
    """
    for iteration in range(max_iterations):
        bboxes = [(comp, get_component_bbox(comp)) for comp in placed]
        moves: dict[str, list[tuple[float, float]]] = {c.ref: [] for c in placed}

        overlap_count = 0
        for i in range(len(bboxes)):
            for j in range(i + 1, len(bboxes)):
                comp_a, bbox_a = bboxes[i]
                comp_b, bbox_b = bboxes[j]
                if not bbox_a.overlaps(bbox_b, clearance_mm):
                    continue

                overlap_count += 1

                # Compute overlap amounts on each axis
                ox = min(bbox_a.x_max, bbox_b.x_max) - max(bbox_a.x_min, bbox_b.x_min) + clearance_mm
                oy = min(bbox_a.y_max, bbox_b.y_max) - max(bbox_a.y_min, bbox_b.y_min) + clearance_mm

                # Push along the axis with smallest overlap (minimum translation)
                cx_a = (bbox_a.x_min + bbox_a.x_max) / 2
                cx_b = (bbox_b.x_min + bbox_b.x_max) / 2
                cy_a = (bbox_a.y_min + bbox_a.y_max) / 2
                cy_b = (bbox_b.y_min + bbox_b.y_max) / 2

                if ox < oy:
                    # Push horizontally
                    sign = 1.0 if cx_a < cx_b else -1.0
                    push = ox / 2 + 0.1
                    moves[comp_a.ref].append((-sign * push, 0))
                    moves[comp_b.ref].append((sign * push, 0))
                else:
                    # Push vertically
                    sign = 1.0 if cy_a < cy_b else -1.0
                    push = oy / 2 + 0.1
                    moves[comp_a.ref].append((0, -sign * push))
                    moves[comp_b.ref].append((0, sign * push))

        if overlap_count == 0:
            break

        # Apply accumulated moves
        for comp in placed:
            if not moves[comp.ref]:
                continue
            dx = sum(m[0] for m in moves[comp.ref])
            dy = sum(m[1] for m in moves[comp.ref])
            comp.x = _snap(comp.x + dx, grid)
            comp.y = _snap(comp.y + dy, grid)

        # Clamp to board boundaries
        _clamp_to_board(placed, board, grid)

    final_overlaps = len(check_overlaps(placed, clearance_mm))
    return placed, final_overlaps


def _snap(value: float, grid: float) -> float:
    """Snap coordinate to grid."""
    return round(value / grid) * grid


def _clamp_to_board(
    placed: list[PlacedComponent],
    board: BoardConfig,
    grid: float,
    margin: float = 1.0,
) -> None:
    """Clamp all components to stay within board boundaries."""
    for comp in placed:
        bbox = get_component_bbox(comp)
        hw = (bbox.x_max - bbox.x_min) / 2
        hh = (bbox.y_max - bbox.y_min) / 2

        x_min = board.origin_x + margin + hw
        x_max = board.origin_x + board.width_mm - margin - hw
        y_min = board.origin_y + margin + hh
        y_max = board.origin_y + board.height_mm - margin - hh

        comp.x = _snap(max(x_min, min(x_max, comp.x)), grid)
        comp.y = _snap(max(y_min, min(y_max, comp.y)), grid)


def validate_placement(
    placed: list[PlacedComponent],
    board: BoardConfig,
) -> dict:
    """Run all placement validations.

    Returns:
        {"overlaps": [(ref1, ref2), ...], "boundary_violations": [ref, ...], "valid": bool}
    """
    overlaps = check_overlaps(placed)
    boundary = check_boundary(placed, board)

    return {
        "overlaps": overlaps,
        "boundary_violations": boundary,
        "valid": len(overlaps) == 0 and len(boundary) == 0,
    }
