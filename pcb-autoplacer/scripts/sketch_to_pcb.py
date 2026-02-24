#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Converte JSON de circuito (sketch) em PCB completo.

Entry point A: Foto desenhada a mao → Claude Vision → JSON → .net → PCB

Usage:
    PYTHONPATH=src python3 scripts/sketch_to_pcb.py output-NOME/circuit.json
    PYTHONPATH=src python3 scripts/sketch_to_pcb.py output-NOME/circuit.json --output-dir output-NOME
    PYTHONPATH=src python3 scripts/sketch_to_pcb.py output-NOME/circuit.json --no-logo --fill-ratio 0.30
    PYTHONPATH=src python3 scripts/sketch_to_pcb.py output-NOME/circuit.json --gen-sch
"""
import argparse
import sys
from pathlib import Path

from pcb_autoplacer.generators.netlist_gen import generate_netlist, load_circuit_json
from pcb_autoplacer.generators.schematic_gen import generate_schematic
from rich.console import Console

# Importa o pipeline compartilhado
sys.path.insert(0, str(Path(__file__).parent))
from place_auto import run_auto_pipeline

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Convert circuit JSON (from sketch/photo) to PCB.",
    )
    parser.add_argument("json_file", type=Path, help="Path to circuit JSON file")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Output directory (default: same as JSON)")
    parser.add_argument("--logo-width", type=float, default=15.0,
                        help="Logo width in mm (default: 15)")
    parser.add_argument("--no-logo", action="store_true",
                        help="Disable logo space reservation")
    parser.add_argument("--min-size", type=float, default=30.0,
                        help="Minimum board dimension in mm (default: 30)")
    parser.add_argument("--fill-ratio", type=float, default=0.25,
                        help="Target fill ratio (default: 0.25)")
    parser.add_argument("--gen-sch", action="store_true",
                        help="Also generate .kicad_sch schematic for visual validation")
    args = parser.parse_args()

    json_path = args.json_file
    if not json_path.exists():
        console.print(f"[red]JSON file not found: {json_path}[/red]")
        sys.exit(1)

    output_dir = args.output_dir or json_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Carregar JSON
    console.print(f"[cyan]Loading circuit JSON: {json_path.name}[/cyan]")
    components, project = load_circuit_json(json_path)
    console.print(f"  Project: {project}")
    console.print(f"  Components: {len(components)}")

    # Contar nets
    net_names = set()
    for comp in components:
        for net_name in comp.get("pins", {}).values():
            net_names.add(net_name)
    console.print(f"  Nets: {len(net_names)}")

    # 2. Gerar .kicad_sch (opcional — para validacao visual)
    if args.gen_sch:
        sch_path = output_dir / f"{project}.kicad_sch"
        console.print(f"\n[cyan]Generating schematic: {sch_path.name}[/cyan]")
        generate_schematic(components, sch_path, project=project)
        console.print(f"  [green]Schematic generated: {sch_path}[/green]")
        console.print(f"  [dim]Open in KiCad to validate visually: open {sch_path}[/dim]")

    # 3. Gerar .net
    netlist_path = output_dir / f"{project}.net"
    console.print(f"\n[cyan]Generating netlist: {netlist_path.name}[/cyan]")
    generate_netlist(components, netlist_path, project=project)
    console.print(f"  [green]Netlist generated: {netlist_path}[/green]")

    # 4. Rodar pipeline auto-placement
    console.print()
    run_auto_pipeline(
        netlist_path=netlist_path,
        output_dir=output_dir,
        logo_width=args.logo_width,
        no_logo=args.no_logo,
        min_size=args.min_size,
        fill_ratio=args.fill_ratio,
    )


if __name__ == "__main__":
    main()
