#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline completo: Netlist -> PCB com trilhas, logo e gerbers.

Executa todos os passos do workflow automaticamente:
  1. Placement (place_auto.py)
  2. Export DSN (kicad_bridge.py)
  3. Autoroute (Freerouter)
  4. Import SES routes
  5. Inject logo Lawteck
  6. DRC
  7. Gerbers + Drill
  8. ZIP para fabricacao

Uso:
  python3 scripts/run_pipeline.py output-consul/consul_comm.net

Opcoes:
  --fill-ratio 0.30   Target fill ratio (default 0.30)
  --logo-width 12     Largura da logo em mm (default 12)
  --no-logo           Pula a injecao da logo
  --skip-route        Pula autoroute (gera board sem trilhas)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Paths
KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
KICAD_PYTHON = "/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3"
FREEROUTER_JAR = os.path.expanduser("~/Downloads/freerouting.jar")
LOGO_SVG = os.path.expanduser("~/Downloads/lawteck vector.svg")
SCRIPTS_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPTS_DIR.parent


def log(emoji, msg):
    print(f"  {emoji} {msg}")


def log_step(step, total, msg):
    print(f"\n[{step}/{total}] {msg}")
    print("=" * 60)


def run(cmd, timeout=120, check=True):
    """Executa comando e retorna stdout."""
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout,
        cwd=str(PROJECT_DIR),
        env={**os.environ, "PYTHONPATH": str(PROJECT_DIR / "src")}
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        log("X", f"Comando falhou (exit {result.returncode})")
        sys.exit(1)
    return result


def find_board_bounds(pcb_path):
    """Encontra os limites do board outline (Edge.Cuts)."""
    text = pcb_path.read_text()
    # Pega edge cuts
    edges = re.findall(
        r'\(gr_line\s+\(start ([\d.]+) ([\d.]+)\)\s+\(end ([\d.]+) ([\d.]+)\).*?Edge\.Cuts',
        text, re.DOTALL
    )
    if not edges:
        return None
    xs = [float(e[0]) for e in edges] + [float(e[2]) for e in edges]
    ys = [float(e[1]) for e in edges] + [float(e[3]) for e in edges]
    return min(xs), min(ys), max(xs), max(ys)


def main():
    parser = argparse.ArgumentParser(description="Pipeline completo: Netlist -> Gerbers")
    parser.add_argument("netlist", help="Caminho do netlist (.net)")
    parser.add_argument("--fill-ratio", type=float, default=0.30,
                        help="Target fill ratio (default 0.30)")
    parser.add_argument("--logo-width", type=float, default=12,
                        help="Largura da logo em mm (default 12)")
    parser.add_argument("--no-logo", action="store_true",
                        help="Pula injecao da logo")
    parser.add_argument("--skip-route", action="store_true",
                        help="Pula autoroute")
    args = parser.parse_args()

    netlist = Path(args.netlist)
    if not netlist.exists():
        log("X", f"Netlist nao encontrado: {netlist}")
        sys.exit(1)

    output_dir = netlist.parent
    board_pcb = output_dir / "board.kicad_pcb"
    board_dsn = output_dir / "board.dsn"
    board_ses = output_dir / "board.ses"
    gerbers_dir = output_dir / "gerbers"
    drc_report = output_dir / "drc-report.json"
    gerbers_zip = output_dir / "gerbers-jlcpcb.zip"

    total_steps = 9 if not args.skip_route else 7
    if args.no_logo:
        total_steps -= 1

    step = 0

    # ── Step 1: Placement ──
    step += 1
    log_step(step, total_steps, "Placement (auto-sizing board)")

    cmd = [
        sys.executable, str(SCRIPTS_DIR / "place_auto.py"),
        str(netlist),
        "--output-dir", str(output_dir),
        "--fill-ratio", str(args.fill_ratio),
    ]
    if not args.no_logo:
        cmd += ["--logo-width", str(args.logo_width)]
    else:
        cmd += ["--no-logo"]

    run(cmd)

    if not board_pcb.exists():
        log("X", "board.kicad_pcb nao foi gerado")
        sys.exit(1)

    # ── Step 2: Export DSN ──
    if not args.skip_route:
        step += 1
        log_step(step, total_steps, "Export DSN para Freerouter")

        run([
            KICAD_PYTHON, str(SCRIPTS_DIR / "kicad_bridge.py"),
            "export-dsn", str(board_pcb), str(board_dsn)
        ])

        # ── Step 3: Autoroute ──
        step += 1
        log_step(step, total_steps, "Autoroute (Freerouter)")

        if not Path(FREEROUTER_JAR).exists():
            log("!", f"Freerouter nao encontrado em {FREEROUTER_JAR}")
            log("!", "Baixe de: https://github.com/freerouting/freerouting/releases")
            log("!", "Pulando autoroute...")
        else:
            run([
                "java", "-jar", FREEROUTER_JAR,
                "-de", str(board_dsn),
                "-do", str(board_ses),
                "-mp", "20", "-mt", "1"
            ], timeout=300, check=False)

        # ── Step 4: Import SES routes ──
        if board_ses.exists():
            step += 1
            log_step(step, total_steps, "Import trilhas (SES)")

            # Import inline para evitar hardcoded paths
            sys.path.insert(0, str(SCRIPTS_DIR))
            from import_ses_routes import parse_ses_routes, inject_routes

            segments, vias = parse_ses_routes(board_ses)
            inject_routes(board_pcb, segments, vias)
            log("OK", f"{len(segments)} segments + {len(vias)} vias injetadas")
        else:
            log("!", "board.ses nao encontrado, pulando import")

    # ── Step 5: Logo ──
    if not args.no_logo:
        step += 1
        log_step(step, total_steps, "Injetar logo Lawteck")

        bounds = find_board_bounds(board_pcb)
        if bounds:
            bx1, by1, bx2, by2 = bounds
            board_w = bx2 - bx1
            board_h = by2 - by1
            # Logo no canto inferior direito
            logo_x = bx2 - args.logo_width / 2 - 2
            logo_y = by2 - 4
            log("OK", f"Board: {board_w:.0f}x{board_h:.0f}mm, logo em ({logo_x:.1f}, {logo_y:.1f})")
        else:
            logo_x, logo_y = 120, 148
            log("!", "Bounds nao encontrados, usando posicao default")

        if Path(LOGO_SVG).exists():
            run([
                sys.executable, str(SCRIPTS_DIR / "inject_logo.py"),
                "--board", str(board_pcb),
                "--svg", LOGO_SVG,
                "--width", str(args.logo_width),
                "--position", f"{logo_x:.1f},{logo_y:.1f}",
                "--layer", "F.SilkS"
            ])
        else:
            log("!", f"SVG nao encontrado: {LOGO_SVG}")

    # ── Step: Fill All Zones (ground plane) ──
    step += 1
    log_step(step, total_steps, "Fill All Zones (ground plane)")

    fill_result = run([
        KICAD_PYTHON, "-c",
        f"""
import pcbnew
board = pcbnew.LoadBoard('{board_pcb}')
filler = pcbnew.ZONE_FILLER(board)
zones = board.Zones()
filler.Fill(zones)
pcbnew.SaveBoard('{board_pcb}', board)
print(f'  Zones preenchidas: {{len(zones)}}')
"""
    ], check=False)
    log("OK", "Ground plane preenchido automaticamente (sem B manual)")

    # ── Step: DRC ──
    step += 1
    log_step(step, total_steps, "DRC (Design Rule Check)")

    run([
        KICAD_CLI, "pcb", "drc",
        "--severity-all", "--units", "mm", "--format", "json",
        "--output", str(drc_report),
        str(board_pcb)
    ], check=False)

    if drc_report.exists():
        with open(drc_report) as f:
            data = json.load(f)
        errors = sum(1 for v in data.get("violations", []) if v.get("severity") == "error")
        warnings = sum(1 for v in data.get("violations", []) if v.get("severity") == "warning")
        unconnected = len(data.get("unconnected_items", []))
        log("OK", f"Errors: {errors}  Warnings: {warnings}  Unconnected: {unconnected}")
        if errors > 0:
            log("!", "DRC tem erros! Verifique o board no KiCad")
        if unconnected > 0:
            log("!", f"{unconnected} itens desconectados")

    # ── Step 7: Gerbers + Drill ──
    step += 1
    log_step(step, total_steps, "Gerbers + Drill")

    gerbers_dir.mkdir(exist_ok=True)

    run([
        KICAD_CLI, "pcb", "export", "gerbers",
        "--layers", "F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
        "--subtract-soldermask",
        "--output", str(gerbers_dir) + "/",
        str(board_pcb)
    ])

    run([
        KICAD_CLI, "pcb", "export", "drill",
        "--format", "excellon",
        "--excellon-separate-th",
        "--excellon-units", "mm",
        "--generate-map", "--map-format", "gerberx2",
        "--output", str(gerbers_dir) + "/",
        str(board_pcb)
    ])

    # ── Step 8: ZIP ──
    step += 1
    log_step(step, total_steps, "ZIP para fabricacao")

    import glob
    gerber_files = (
        glob.glob(str(gerbers_dir / "*.gtl"))
        + glob.glob(str(gerbers_dir / "*.gbl"))
        + glob.glob(str(gerbers_dir / "*.gto"))
        + glob.glob(str(gerbers_dir / "*.gbo"))
        + glob.glob(str(gerbers_dir / "*.gts"))
        + glob.glob(str(gerbers_dir / "*.gbs"))
        + glob.glob(str(gerbers_dir / "*.gm1"))
        + glob.glob(str(gerbers_dir / "*.drl"))
    )

    if gerber_files:
        subprocess.run(
            ["zip", "-j", str(gerbers_zip)] + gerber_files,
            capture_output=True
        )
        size_kb = gerbers_zip.stat().st_size / 1024
        log("OK", f"{gerbers_zip.name} ({size_kb:.0f}KB, {len(gerber_files)} arquivos)")
    else:
        log("X", "Nenhum gerber encontrado!")

    # ── Resumo final ──
    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETO")
    print("=" * 60)
    print(f"  Board:   {board_pcb}")
    print(f"  Gerbers: {gerbers_zip}")
    print(f"  DRC:     {errors} errors, {warnings} warnings")
    print()
    print(f"  Proximo: abrir {board_pcb.name} no KiCad")
    print("           verificar visualmente (zones ja preenchidas)")
    print("=" * 60)


if __name__ == "__main__":
    main()
