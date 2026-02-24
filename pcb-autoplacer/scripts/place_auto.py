#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Universal auto-placement script — calculates board size from netlist.

Usage:
    PYTHONPATH=src python3 scripts/place_auto.py output-NOME/circuito.net
    PYTHONPATH=src python3 scripts/place_auto.py output-NOME/circuito.net --output-dir output-NOME
    PYTHONPATH=src python3 scripts/place_auto.py output-NOME/circuito.net --no-logo --fill-ratio 0.30
"""
import argparse
import sys
from pathlib import Path

from pcb_autoplacer.parsers.netlist import parse_netlist
from pcb_autoplacer.parsers.footprint import load_footprint
from pcb_autoplacer.placer.engine import auto_size_board
from pcb_autoplacer.placer.constraints import validate_placement
from pcb_autoplacer.generators.kicad_pcb import generate_pcb
from rich.console import Console
from rich.table import Table

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Auto-size board and place components from a KiCad netlist.",
    )
    parser.add_argument("netlist", type=Path, help="Path to .net netlist file")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Output directory (default: same as netlist)")
    parser.add_argument("--logo-width", type=float, default=15.0,
                        help="Logo width in mm (default: 15)")
    parser.add_argument("--no-logo", action="store_true",
                        help="Disable logo space reservation")
    parser.add_argument("--min-size", type=float, default=30.0,
                        help="Minimum board dimension in mm (default: 30)")
    parser.add_argument("--fill-ratio", type=float, default=0.25,
                        help="Target fill ratio (default: 0.25)")
    args = parser.parse_args()

    netlist_path = args.netlist
    if not netlist_path.exists():
        console.print(f"[red]Netlist not found: {netlist_path}[/red]")
        sys.exit(1)

    output_dir = args.output_dir or netlist_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "board.kicad_pcb"

    # Logo space reservation
    logo_height = args.logo_width * 0.47  # ~aspect ratio from Lawteck logo
    logo_space = (0.0, 0.0) if args.no_logo else (args.logo_width, logo_height)

    # 1. Parse netlist
    console.print("[cyan]Parsing netlist...[/cyan]")
    components, nets = parse_netlist(netlist_path)

    # 2. Load footprints
    console.print("[cyan]Loading footprints...[/cyan]")
    footprints = {}
    missing_fps = []
    for comp in components:
        fp = load_footprint(comp.footprint)
        if fp:
            footprints[comp.ref] = fp
        else:
            missing_fps.append(f"{comp.ref} ({comp.footprint})")

    console.print(f"  {len(components)} components, {len(nets)} nets, "
                  f"{len(footprints)} footprints resolved")
    if missing_fps:
        console.print(f"  [yellow]Missing footprints: {', '.join(missing_fps[:10])}"
                      f"{'...' if len(missing_fps) > 10 else ''}[/yellow]")

    # 3. Auto-size board + place components
    console.print("[cyan]Calculating board size and placing components...[/cyan]")
    board, placed = auto_size_board(
        components, nets, footprints,
        logo_space_mm=logo_space,
        target_fill_ratio=args.fill_ratio,
        min_size=args.min_size,
    )

    # 4. Validate
    validation = validate_placement(placed, board)

    # 5. Generate PCB
    generate_pcb(placed, nets, board, output_path)

    # 6. Summary
    comp_area = sum(
        footprints[c.ref].bbox_width * footprints[c.ref].bbox_height
        for c in components if c.ref in footprints
    )
    board_area = board.width_mm * board.height_mm
    fill = comp_area / board_area * 100 if board_area > 0 else 0

    console.print()
    table = Table(title="Auto-Placement Summary")
    table.add_column("Metric", style="bold")
    table.add_column("Value")
    table.add_row("Board size", f"{board.width_mm:.0f} x {board.height_mm:.0f} mm")
    table.add_row("Board area", f"{board_area:.0f} mm²")
    table.add_row("Component area", f"{comp_area:.0f} mm²")
    table.add_row("Fill ratio", f"{fill:.1f}%")
    table.add_row("Components placed", str(len(placed)))
    table.add_row("Logo space", f"{logo_space[0]:.0f} x {logo_space[1]:.1f} mm"
                  if not args.no_logo else "disabled")
    table.add_row("Overlaps", str(len(validation["overlaps"])))
    table.add_row("Boundary violations", str(len(validation["boundary_violations"])))
    table.add_row("Valid", "[green]YES[/green]" if validation["valid"]
                  else "[red]NO[/red]")
    console.print(table)

    if validation["overlaps"]:
        console.print(f"\n[yellow]Overlapping pairs: "
                      f"{', '.join(f'{a}-{b}' for a, b in validation['overlaps'][:10])}"
                      f"[/yellow]")
    if validation["boundary_violations"]:
        console.print(f"[yellow]Out of bounds: "
                      f"{', '.join(validation['boundary_violations'][:10])}[/yellow]")

    console.print(f"\n[green bold]PCB generated: {output_path}[/green bold]")
    if not args.no_logo:
        console.print(f"[dim]Logo position suggestion: bottom-right area of the board[/dim]")


if __name__ == "__main__":
    main()
