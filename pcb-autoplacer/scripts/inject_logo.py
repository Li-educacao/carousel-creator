#!/usr/bin/env python3
"""Inject Lawteck logo into a KiCad PCB as silkscreen footprint."""
from __future__ import annotations

import argparse
import io
import uuid
from pathlib import Path

import cairosvg
import numpy as np
from PIL import Image, ImageFilter


DEFAULT_SVG = "/Users/lawhander/Downloads/lawteck vector.svg"
DEFAULT_WIDTH = 15.0  # mm
DEFAULT_POS = (120.0, 148.0)
DEFAULT_LAYER = "F.SilkS"

# SVG crop region (in 2048x2048 viewbox coords) — main logo area
SVG_CROP_Y = (640, 1420)
SVG_CROP_X = (100, 1980)
BRIGHTNESS_THRESHOLD = 160
RENDER_SIZE = 2000
DOWNSAMPLE_W = 400
SCANLINE_BLOCK = 2


def svg_to_polygons(svg_path: str, target_width_mm: float) -> tuple[list, float, float]:
    """Convert SVG logo to list of (x1, y1, x2, y2) rectangles in mm, centered at origin."""
    png_data = cairosvg.svg2png(url=svg_path, output_width=RENDER_SIZE, output_height=RENDER_SIZE)
    img = Image.open(io.BytesIO(png_data)).convert("RGBA")
    arr = np.array(img)

    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    brightness = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
    mask = brightness < BRIGHTNESS_THRESHOLD

    s = RENDER_SIZE / 2048
    y0, y1 = int(SVG_CROP_Y[0] * s), int(SVG_CROP_Y[1] * s)
    x0, x1 = int(SVG_CROP_X[0] * s), int(SVG_CROP_X[1] * s)
    cropped = mask[y0:y1, x0:x1]

    mono = Image.fromarray((cropped.astype(np.uint8) * 255), mode="L")
    mono = mono.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))

    scale = DOWNSAMPLE_W / mono.width
    target_h = int(mono.height * scale)
    small = mono.resize((DOWNSAMPLE_W, target_h), Image.LANCZOS)
    bitmap = np.array(small) > 128

    phys_w = target_width_mm
    phys_h = phys_w * target_h / DOWNSAMPLE_W
    px_to_mm = phys_w / DOWNSAMPLE_W
    cx, cy = DOWNSAMPLE_W / 2, target_h / 2

    rects = []
    for y in range(0, target_h, SCANLINE_BLOCK):
        row = bitmap[y]
        in_run = False
        start = 0
        for x in range(DOWNSAMPLE_W):
            if row[x] and not in_run:
                start = x
                in_run = True
            elif not row[x] and in_run:
                rects.append((
                    (start - cx) * px_to_mm, (y - cy) * px_to_mm,
                    (x - cx) * px_to_mm, (y + SCANLINE_BLOCK - cy) * px_to_mm,
                ))
                in_run = False
        if in_run:
            rects.append((
                (start - cx) * px_to_mm, (y - cy) * px_to_mm,
                (DOWNSAMPLE_W - cx) * px_to_mm, (y + SCANLINE_BLOCK - cy) * px_to_mm,
            ))

    return rects, phys_w, phys_h


def build_footprint_text(rects: list, phys_h: float, pos: tuple, layer: str) -> str:
    """Build KiCad PCB inline footprint text for the logo."""
    uid = lambda: str(uuid.uuid4())
    px, py = pos

    lines = []
    lines.append(f'\t(footprint "Lawteck_Logo"')
    lines.append(f'\t\t(layer "{layer}")')
    lines.append(f'\t\t(uuid "{uid()}")')
    lines.append(f'\t\t(at {px} {py})')
    lines.append(f'\t\t(property "Reference" "LOGO"')
    lines.append(f'\t\t\t(at 0 {-phys_h/2 - 1:.2f})')
    lines.append(f'\t\t\t(layer "{layer}")')
    lines.append(f'\t\t\t(hide yes)')
    lines.append(f'\t\t\t(uuid "{uid()}")')
    lines.append(f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))')
    lines.append(f'\t\t)')
    lines.append(f'\t\t(property "Value" "Lawteck"')
    lines.append(f'\t\t\t(at 0 {phys_h/2 + 1:.2f})')
    lines.append(f'\t\t\t(layer "F.Fab")')
    lines.append(f'\t\t\t(hide yes)')
    lines.append(f'\t\t\t(uuid "{uid()}")')
    lines.append(f'\t\t\t(effects (font (size 1 1) (thickness 0.15)))')
    lines.append(f'\t\t)')

    for mx1, my1, mx2, my2 in rects:
        lines.append(f'\t\t(fp_poly')
        lines.append(f'\t\t\t(pts')
        lines.append(f'\t\t\t\t(xy {mx1:.4f} {my1:.4f})')
        lines.append(f'\t\t\t\t(xy {mx2:.4f} {my1:.4f})')
        lines.append(f'\t\t\t\t(xy {mx2:.4f} {my2:.4f})')
        lines.append(f'\t\t\t\t(xy {mx1:.4f} {my2:.4f})')
        lines.append(f'\t\t\t)')
        lines.append(f'\t\t\t(stroke (width 0) (type solid))')
        lines.append(f'\t\t\t(fill solid)')
        lines.append(f'\t\t\t(layer "{layer}")')
        lines.append(f'\t\t\t(uuid "{uid()}")')
        lines.append(f'\t\t)')

    lines.append(f'\t)')
    return '\n'.join(lines)


def inject_into_board(board_path: str, footprint_text: str) -> None:
    """Inject logo footprint into .kicad_pcb file, before the zone section."""
    board = Path(board_path).read_text(encoding="utf-8")

    # Remove existing logo if present
    if "Lawteck_Logo" in board:
        import re
        board = re.sub(r'\t\(footprint "Lawteck_Logo".*?\n\t\)', '', board, flags=re.DOTALL)
        board = re.sub(r'\n{3,}', '\n\n', board)  # clean extra blank lines

    # Insert before zone or before last closing paren
    zone_idx = board.find('\t(zone\n')
    if zone_idx > 0:
        board = board[:zone_idx] + footprint_text + '\n' + board[zone_idx:]
    else:
        last = board.rfind(')')
        board = board[:last] + '\n' + footprint_text + '\n' + board[last:]

    Path(board_path).write_text(board, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Inject Lawteck logo into KiCad PCB")
    parser.add_argument("--board", required=True, help="Path to .kicad_pcb file")
    parser.add_argument("--svg", default=DEFAULT_SVG, help="Path to SVG logo")
    parser.add_argument("--width", type=float, default=DEFAULT_WIDTH, help="Logo width in mm")
    parser.add_argument("--position", default=f"{DEFAULT_POS[0]},{DEFAULT_POS[1]}",
                        help="X,Y position on board (mm)")
    parser.add_argument("--layer", default=DEFAULT_LAYER, help="Target layer")
    args = parser.parse_args()

    pos = tuple(float(v) for v in args.position.split(","))

    print(f"Converting {args.svg}...")
    rects, phys_w, phys_h = svg_to_polygons(args.svg, args.width)
    print(f"  {len(rects)} polygons, {phys_w:.1f} x {phys_h:.1f} mm")

    fp_text = build_footprint_text(rects, phys_h, pos, args.layer)

    print(f"Injecting into {args.board}...")
    inject_into_board(args.board, fp_text)
    print(f"Done! Logo at ({pos[0]}, {pos[1]}) on {args.layer}")


if __name__ == "__main__":
    main()
