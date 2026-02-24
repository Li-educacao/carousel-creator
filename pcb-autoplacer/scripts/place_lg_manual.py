#!/usr/bin/env python3
"""Manual precision placement for Simulador Evaporadora LG — Compact Edition.

Board: 80x55mm (optimized from 100x80mm), 3 zones, commercial-grade layout.

Design principles:
- Compact: minimum viable board size with safe routing space
- Organized: clear AC/ISO/DC zones, aligned rows/columns
- Centered: content centered vertically, balanced distribution
- Commercial: neat, professional appearance

IMPORTANT: Positions defined as VISUAL CENTER. The script auto-converts to
footprint pin-1 origin using bbox_offset from parsed .kicad_mod files.
"""
from pathlib import Path
from pcb_autoplacer.parsers.netlist import parse_netlist
from pcb_autoplacer.parsers.footprint import load_footprint
from pcb_autoplacer.models import BoardConfig, PlacedComponent
from pcb_autoplacer.placer.engine import apply_placement
from pcb_autoplacer.placer.constraints import validate_placement
from pcb_autoplacer.generators.kicad_pcb import generate_pcb
from rich.console import Console
from rich.table import Table

console = Console()

BOARD_W = 80.0
BOARD_H = 55.0

# ┌──────────────────────── 80mm ─────────────────────────────────┐
# │ AC ZONE(3-22)│  ISOLATION(22-54)  │  DC ZONE(56-78)          │
# │              │                    │                          │  55mm
# │ J2  F1       │      PS1           │  C6 C7  U3    Q1        │
# │ J3  RV1      │   (HLK-PM01)      │  C3 C5       R8 R9      │
# │ J1  C4       │                    │              R11        │
# │     D9       │  D3                │  R6 R7                  │
# │     R14  D6  │     R4 (13K 3W)   │        SW1              │
# │              │  R5  U1            │                          │
# │              │      U2            │  D5  D7  D8             │
# │              │                    │  R15 R12 R13            │
# └──────────────────────────────────────────────────────────────┘

VISUAL_CENTERS = {
    # ===== ZONA AC (x=3-22) — Alta tensão, borda esquerda =====
    # Conectores empilhados na borda esquerda
    "J2":  (5.0,   7.0,  0),     # LINE input        (3.9x3.9)
    "J3":  (5.0,  14.0,  0),     # NEUTRAL           (3.9x3.9)
    "J1":  (5.0,  21.0,  0),     # Output conn       (3.9x3.9)

    # Proteção ao lado dos conectores
    "F1":  (15.0,  7.0,  0),     # Fuse 250mA        (6.5x1.4)
    "RV1": (15.0, 14.0,  0),     # MOV varistor      (9.3x3.4)
    "C4":  (15.0, 21.0,  0),     # Safety cap 470pF  (9.5x2.0)

    # Zener + LED AC com resistor série
    "D9":  (10.0, 27.0,  0),     # Zener BZV55B68    (4.8x1.7)
    "R14": (12.0, 32.0,  0),     # R 100K 1W         (11.8x1.6)
    "D6":  (22.0, 32.0,  0),     # LED red AC        (4.3x1.8)

    # ===== ZONA ISOLAÇÃO (x=22-54) — PS1 + Optocouplers =====
    # PS1 Hi-Link no topo central (maior componente)
    "PS1": (38.0, 13.0,  0),     # HLK-PM01          (30.8x17.0)

    # Diodo de proteção e resistor longo abaixo do PS1
    "D3":  (25.0, 27.0,  0),     # 1N4007W           (2.8x1.8)
    "R4":  (38.0, 27.0,  0),     # 13K 3W            (21.9x1.6)

    # Optocouplers — barreira de isolação galvânica
    "R5":  (28.0, 34.0,  0),     # 1.2K (opto bias)  (1.6x1.0)
    "U1":  (37.0, 37.0,  0),     # PC817 opto #1     (9.2x4.1)
    "U2":  (37.0, 45.0,  0),     # PC817 opto #2     (9.2x4.1)

    # ===== ZONA DC (x=56-78) — MCU + Periféricos =====
    # Caps desacoplamento em coluna alinhada
    "C6":  (58.0,  8.0,  0),     # 100uF eletrolítico (4.1x1.6)
    "C7":  (58.0, 12.0,  0),     # 100nF decoupling   (2.0x1.4)
    "C3":  (58.0, 16.0,  0),     # 100nF              (2.0x1.4)
    "C5":  (58.0, 20.0,  0),     # 1nF                (2.0x1.4)

    # U3 ATtiny85 — MCU principal
    "U3":  (67.0, 12.0,  0),     # ATtiny85 DIP-8     (9.2x9.2)

    # Circuito do transistor em coluna alinhada (x=74 for edge clearance)
    "Q1":  (74.0,  8.0,  0),     # FMMT491 SOT-23     (3.0x2.6)
    "R8":  (74.0, 12.0,  0),     # 1.2K               (2.0x1.4)
    "R9":  (74.0, 16.0,  0),     # 680Ω               (2.0x1.4)
    "R11": (74.0, 20.0,  0),     # 2K                  (2.0x1.4)

    # Pullups/divisores perto do MCU
    "R6":  (67.0, 26.0,  0),     # 5.1K               (2.0x1.4)
    "R7":  (67.0, 30.0,  0),     # 10K                 (2.0x1.4)

    # Botão perto do MCU, acessível
    "SW1": (74.0, 28.0,  0),     # Push 6mm            (8.5x6.5)

    # ===== LEDs + Resistores série (fila inferior) =====
    # LEDs em fila alinhada
    "D5":  (58.0, 40.0,  0),     # LED green           (4.3x1.8)
    "D7":  (66.0, 40.0,  0),     # LED red             (4.3x1.8)
    "D8":  (74.0, 40.0,  0),     # LED green           (4.3x1.8)

    # Resistores série alinhados abaixo dos LEDs
    "R15": (60.0, 46.0,  0),     # 1K (série D5)       (11.8x1.6)
    "R12": (70.0, 46.0,  0),     # 1K (série D7)       (2.0x1.4)
    "R13": (74.0, 46.0,  0),     # 2K (série D8)       (2.0x1.4)
}


# Label position overrides: ref → {"ref_offset": (dx, dy), "hide_value": bool}
# Offsets are relative to bbox center. Positive dx=right, positive dy=down.
# Strategy: alternate above/below/lateral to avoid overlaps in dense zones.
LABEL_CONFIG = {
    # ===== AC ZONE — connectors + protection =====
    # J1/J2/J3 stacked: labels to the right
    "J2":  {"ref_offset": (3.5, 0.0), "hide_value": True},
    "J3":  {"ref_offset": (3.5, 0.0), "hide_value": True},
    "J1":  {"ref_offset": (3.5, 0.0), "hide_value": True},
    # Protection row: labels above (spaced from connectors)
    "F1":  {"ref_offset": (0.0, -2.0), "hide_value": True},
    "RV1": {"ref_offset": (0.0, -3.0), "hide_value": True},
    "C4":  {"ref_offset": (0.0, -2.5), "hide_value": True},
    # D9/R14/D6: staggered
    "D9":  {"ref_offset": (-3.5, 0.0), "hide_value": True},
    "R14": {"ref_offset": (0.0, -2.0), "hide_value": True},
    "D6":  {"ref_offset": (0.0, -2.0), "hide_value": True},

    # ===== ISOLATION ZONE — PS1 + optocouplers =====
    "PS1": {"ref_offset": (0.0, -10.0), "hide_value": True},
    "D3":  {"ref_offset": (-2.5, 0.0), "hide_value": True},
    "R4":  {"ref_offset": (0.0, -2.0), "hide_value": True},  # long resistor
    "R5":  {"ref_offset": (-2.0, 0.0), "hide_value": True},
    "U1":  {"ref_offset": (-6.0, 0.0), "hide_value": True},
    "U2":  {"ref_offset": (-6.0, 0.0), "hide_value": True},

    # ===== DC ZONE — caps column (x=58) =====
    # C6/C7/C3/C5 stacked tight (4mm spacing): alternate left/right
    "C6":  {"ref_offset": (-3.0, 0.0), "hide_value": True},
    "C7":  {"ref_offset": (3.0, 0.0), "hide_value": True},
    "C3":  {"ref_offset": (-3.0, 0.0), "hide_value": True},
    "C5":  {"ref_offset": (3.0, 0.0), "hide_value": True},

    # U3 ATtiny85 — label above (large DIP-8)
    "U3":  {"ref_offset": (0.0, -6.5), "hide_value": True},

    # Transistor column (x=74): Q1/R8/R9/R11 stacked tight
    "Q1":  {"ref_offset": (3.0, 0.0), "hide_value": True},
    "R8":  {"ref_offset": (3.0, 0.0), "hide_value": True},
    "R9":  {"ref_offset": (3.0, 0.0), "hide_value": True},
    "R11": {"ref_offset": (3.0, 0.0), "hide_value": True},

    # Pullups near MCU
    "R6":  {"ref_offset": (-3.0, 0.0), "hide_value": True},
    "R7":  {"ref_offset": (-3.0, 0.0), "hide_value": True},

    # Switch — label above
    "SW1": {"ref_offset": (0.0, -5.0), "hide_value": True},

    # ===== LEDs row (y=40) + series resistors (y=46) =====
    "D5":  {"ref_offset": (0.0, -2.5), "hide_value": True},
    "D7":  {"ref_offset": (0.0, -2.5), "hide_value": True},
    "D8":  {"ref_offset": (0.0, -2.5), "hide_value": True},
    "R15": {"ref_offset": (0.0, 2.5), "hide_value": True},
    "R12": {"ref_offset": (0.0, 2.5), "hide_value": True},
    "R13": {"ref_offset": (0.0, 2.5), "hide_value": True},
}


def main():
    netlist_path = Path("output-lg/evaporadora-lg.net")
    output_path = Path("output-lg/board.kicad_pcb")

    console.print("[cyan]Parsing netlist...[/cyan]")
    components, nets = parse_netlist(netlist_path)
    footprints = {}
    for comp in components:
        fp = load_footprint(comp.footprint)
        if fp:
            footprints[comp.ref] = fp

    console.print(f"  {len(components)} components, {len(nets)} nets")

    # Check all components have placements
    placed_refs = set(VISUAL_CENTERS.keys())
    all_refs = {c.ref for c in components}
    missing = all_refs - placed_refs
    if missing:
        console.print(f"[red]MISSING placements for: {', '.join(sorted(missing))}[/red]")
        return

    # Convert visual centers → pin-1 origins, apply label config
    ai_placements = []
    for ref, (vcx, vcy, rot) in VISUAL_CENTERS.items():
        fp = footprints.get(ref)
        ox, oy = (fp.bbox_offset_x, fp.bbox_offset_y) if fp else (0.0, 0.0)
        placement = {
            "ref": ref,
            "x": vcx - ox,
            "y": vcy - oy,
            "rotation": rot,
            "layer": "F.Cu",
        }
        label_cfg = LABEL_CONFIG.get(ref)
        if label_cfg:
            if "ref_offset" in label_cfg:
                placement["ref_offset"] = label_cfg["ref_offset"]
            if label_cfg.get("hide_value"):
                placement["hide_value"] = True
        ai_placements.append(placement)

    board = BoardConfig(width_mm=BOARD_W, height_mm=BOARD_H)
    placed = apply_placement(components, nets, footprints, ai_placements, board)
    validation = validate_placement(placed, board)

    if validation["overlaps"]:
        console.print(f"\n[red bold]OVERLAPS: {len(validation['overlaps'])} pairs[/red bold]")
        for ref_a, ref_b in validation["overlaps"]:
            fp_a, fp_b = footprints.get(ref_a), footprints.get(ref_b)
            sz_a = f"{fp_a.bbox_width:.1f}x{fp_a.bbox_height:.1f}" if fp_a else "?"
            sz_b = f"{fp_b.bbox_width:.1f}x{fp_b.bbox_height:.1f}" if fp_b else "?"
            va, vb = VISUAL_CENTERS[ref_a], VISUAL_CENTERS[ref_b]
            console.print(f"  {ref_a} ({sz_a} @{va[0]},{va[1]}) ↔ {ref_b} ({sz_b} @{vb[0]},{vb[1]})")
    else:
        console.print("\n[green bold]ZERO overlaps![/green bold]")

    if validation["boundary_violations"]:
        console.print(f"[red]BOUNDARY: {', '.join(validation['boundary_violations'])}[/red]")
    else:
        console.print("[green]All within bounds[/green]")

    # Stats
    comp_area = sum((footprints[c.ref].bbox_width * footprints[c.ref].bbox_height)
                    for c in components if c.ref in footprints)
    board_area = BOARD_W * BOARD_H
    fill = comp_area / board_area * 100
    console.print(f"\n[bold]Board: {BOARD_W:.0f}x{BOARD_H:.0f}mm ({board_area:.0f}mm²)[/bold]")
    console.print(f"[bold]Fill ratio: {fill:.1f}% ({comp_area:.0f}mm² / {board_area:.0f}mm²)[/bold]")

    generate_pcb(placed, nets, board, output_path)
    console.print(f"\n[green bold]PCB generated: {output_path}[/green bold]")
    console.print(f"  {len(placed)} components, Valid: {validation['valid']}")


if __name__ == "__main__":
    main()
