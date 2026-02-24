#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry Point B: Schematic (.kicad_sch) -> PCB completo.

Exporta netlist via kicad-cli e executa o pipeline completo.

Uso:
  python3 scripts/sch_to_pcb.py circuito.kicad_sch [--project nome]
  python3 scripts/sch_to_pcb.py output-consul/consul_comm_circuit.kicad_sch --project test-consul
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
SCRIPTS_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPTS_DIR.parent


def log(emoji, msg):
    print(f"  {emoji} {msg}")


def main():
    parser = argparse.ArgumentParser(
        description="Schematic -> PCB: exporta netlist e executa pipeline completo"
    )
    parser.add_argument("schematic", help="Caminho do .kicad_sch")
    parser.add_argument("--project", help="Nome do projeto (default: nome do arquivo)")
    parser.add_argument("--fill-ratio", type=float, default=0.30,
                        help="Target fill ratio (default 0.30)")
    parser.add_argument("--logo-width", type=float, default=12,
                        help="Largura da logo em mm (default 12)")
    parser.add_argument("--no-logo", action="store_true",
                        help="Pula injecao da logo")
    parser.add_argument("--skip-route", action="store_true",
                        help="Pula autoroute")
    args = parser.parse_args()

    sch_path = Path(args.schematic).resolve()
    if not sch_path.exists():
        log("X", f"Schematic nao encontrado: {sch_path}")
        sys.exit(1)

    if not sch_path.suffix == ".kicad_sch":
        log("X", f"Arquivo deve ser .kicad_sch, recebido: {sch_path.suffix}")
        sys.exit(1)

    # Project name
    project_name = args.project or sch_path.stem.replace("_", "-")

    # Output directory
    output_dir = PROJECT_DIR / f"output-{project_name}"
    output_dir.mkdir(exist_ok=True)

    netlist_path = output_dir / "circuit.net"

    print("=" * 60)
    print(f"  SCH -> PCB Pipeline")
    print(f"  Schematic: {sch_path.name}")
    print(f"  Project:   {project_name}")
    print(f"  Output:    {output_dir}")
    print("=" * 60)

    # ── Step 1: Export Netlist via kicad-cli ──
    print(f"\n[1/2] Export netlist via kicad-cli")
    print("=" * 60)

    result = subprocess.run(
        [KICAD_CLI, "sch", "export", "netlist",
         "-o", str(netlist_path),
         str(sch_path)],
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        log("X", f"kicad-cli falhou: {result.stderr}")
        sys.exit(1)

    if not netlist_path.exists():
        log("X", f"Netlist nao foi gerado em {netlist_path}")
        sys.exit(1)

    size_kb = netlist_path.stat().st_size / 1024
    log("OK", f"Netlist gerado: {netlist_path.name} ({size_kb:.1f}KB)")

    # ── Step 2: Run pipeline ──
    print(f"\n[2/2] Executando pipeline completo")
    print("=" * 60)

    # Import run_pipeline function
    sys.path.insert(0, str(SCRIPTS_DIR))
    from run_pipeline import run_pipeline

    result = run_pipeline(
        str(netlist_path),
        fill_ratio=args.fill_ratio,
        logo_width=args.logo_width,
        no_logo=args.no_logo,
        skip_route=args.skip_route,
    )

    return result


if __name__ == "__main__":
    main()
