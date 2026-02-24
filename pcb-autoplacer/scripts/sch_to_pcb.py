#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Converte esquematico KiCad (.kicad_sch) em PCB completo.

Entry point B: Esquematico existente → kicad-cli export netlist → .net → PCB

Usage:
    PYTHONPATH=src python3 scripts/sch_to_pcb.py output-NOME/circuito.kicad_sch
    PYTHONPATH=src python3 scripts/sch_to_pcb.py meu-projeto.kicad_sch --output-dir output-NOME
    PYTHONPATH=src python3 scripts/sch_to_pcb.py meu-projeto.kicad_sch --no-logo --fill-ratio 0.30
"""
import argparse
import subprocess
import sys
from pathlib import Path

from pcb_autoplacer.config import KICAD_CLI
from rich.console import Console

# Importa o pipeline compartilhado
sys.path.insert(0, str(Path(__file__).parent))
from place_auto import run_auto_pipeline

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Convert KiCad schematic (.kicad_sch) to PCB.",
    )
    parser.add_argument("schematic", type=Path, help="Path to .kicad_sch file")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Output directory (default: same as schematic)")
    parser.add_argument("--logo-width", type=float, default=15.0,
                        help="Logo width in mm (default: 15)")
    parser.add_argument("--no-logo", action="store_true",
                        help="Disable logo space reservation")
    parser.add_argument("--min-size", type=float, default=30.0,
                        help="Minimum board dimension in mm (default: 30)")
    parser.add_argument("--fill-ratio", type=float, default=0.25,
                        help="Target fill ratio (default: 0.25)")
    args = parser.parse_args()

    sch_path = args.schematic
    if not sch_path.exists():
        console.print(f"[red]Schematic not found: {sch_path}[/red]")
        sys.exit(1)

    output_dir = args.output_dir or sch_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Gerar .net via kicad-cli
    netlist_path = output_dir / sch_path.with_suffix(".net").name
    console.print(f"[cyan]Generating netlist from {sch_path.name}...[/cyan]")

    result = subprocess.run(
        [str(KICAD_CLI), "sch", "export", "netlist",
         "--output", str(netlist_path), str(sch_path)],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0 or not netlist_path.exists():
        console.print(f"[red]Failed to generate netlist:[/red]")
        console.print(f"[red]{result.stderr.strip()}[/red]")
        sys.exit(1)

    console.print(f"  [green]Netlist generated: {netlist_path}[/green]")

    # 2. Rodar pipeline auto-placement
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
