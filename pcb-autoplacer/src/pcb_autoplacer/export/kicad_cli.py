"""KiCad CLI integration — DRC, Gerber export, Drill files."""
from __future__ import annotations
import json
import subprocess
from pathlib import Path

from rich.console import Console

from pcb_autoplacer.config import KICAD_CLI

console = Console()


class KiCadCLIError(Exception):
    """Error running kicad-cli."""


def _run_kicad_cli(args: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    """Run a kicad-cli command."""
    if not KICAD_CLI.exists():
        raise KiCadCLIError(f"kicad-cli not found at {KICAD_CLI}")

    cmd = [str(KICAD_CLI)] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise KiCadCLIError(f"kicad-cli timed out after {timeout}s")

    return result


def run_drc(pcb_path: Path, output_path: Path | None = None) -> dict:
    """Run Design Rule Check on a .kicad_pcb file.

    Args:
        pcb_path: Path to .kicad_pcb file
        output_path: Path for JSON DRC report. Defaults to pcb_path with .drc.json suffix.

    Returns:
        DRC report dict with violations
    """
    if output_path is None:
        output_path = pcb_path.with_suffix(".drc.json")

    console.print(f"[cyan]Running DRC on {pcb_path.name}...[/cyan]")

    result = _run_kicad_cli([
        "pcb", "drc",
        "--output", str(output_path),
        "--format", "json",
        "--severity-all",
        str(pcb_path),
    ])

    # kicad-cli drc returns exit code based on violations found
    # Read the report regardless
    if output_path.exists():
        report = json.loads(output_path.read_text())
    else:
        report = {"violations": [], "unconnected_items": [], "schematic_parity": []}

    violations = report.get("violations", [])
    unconnected = report.get("unconnected_items", [])

    error_count = len(violations)
    warning_count = len(unconnected)

    if error_count == 0 and warning_count == 0:
        console.print("[green]DRC passed — no violations[/green]")
    else:
        console.print(f"[yellow]DRC: {error_count} violations, {warning_count} unconnected[/yellow]")
        for v in violations[:5]:
            desc = v.get("description", "unknown")
            console.print(f"  [red]• {desc}[/red]")

    return report


def export_gerbers(pcb_path: Path, output_dir: Path) -> list[Path]:
    """Export Gerber files for JLCPCB fabrication.

    Args:
        pcb_path: Path to .kicad_pcb file
        output_dir: Directory for Gerber output

    Returns:
        List of generated Gerber file paths
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[cyan]Exporting Gerbers to {output_dir}...[/cyan]")

    # Export copper + mask + silk + edge cuts
    result = _run_kicad_cli([
        "pcb", "export", "gerbers",
        "--output", str(output_dir) + "/",
        "--layers", "F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,F.Paste,B.Paste,Edge.Cuts",
        "--use-drill-file-origin",
        "--no-protel-ext",
        str(pcb_path),
    ])

    if result.returncode != 0:
        console.print(f"[yellow]Gerber export warnings: {result.stderr.strip()}[/yellow]")

    # Export drill files
    _run_kicad_cli([
        "pcb", "export", "drill",
        "--output", str(output_dir) + "/",
        "--format", "excellon",
        "--excellon-units", "mm",
        "--generate-map",
        "--map-format", "gerberx2",
        "--use-drill-file-origin",
        str(pcb_path),
    ])

    generated = list(output_dir.glob("*"))
    console.print(f"[green]Generated {len(generated)} files in {output_dir}[/green]")

    # Rename for JLCPCB conventions
    _rename_for_jlcpcb(output_dir, pcb_path.stem)

    return generated


def _rename_for_jlcpcb(output_dir: Path, board_name: str) -> None:
    """Rename Gerber/Drill files to JLCPCB naming conventions.

    JLCPCB expects:
    - *-F_Cu.gtl (or .gbr) → top copper
    - *-B_Cu.gbl → bottom copper
    - *-F_SilkS.gto → top silk
    - *-B_SilkS.gbo → bottom silk
    - *-F_Mask.gts → top mask
    - *-B_Mask.gbs → bottom mask
    - *-Edge_Cuts.gm1 → outline
    - *.drl → drill file
    """
    # JLCPCB accepts KiCad's default naming, so we mainly ensure
    # the files are present. Rename only if needed.
    renames = {
        "-F_Cu.gbr": "-F_Cu.gtl",
        "-B_Cu.gbr": "-B_Cu.gbl",
        "-F_SilkS.gbr": "-F_SilkS.gto",
        "-B_SilkS.gbr": "-B_SilkS.gbo",
        "-F_Mask.gbr": "-F_Mask.gts",
        "-B_Mask.gbr": "-B_Mask.gbs",
        "-F_Paste.gbr": "-F_Paste.gtp",
        "-B_Paste.gbr": "-B_Paste.gbp",
        "-Edge_Cuts.gbr": "-Edge_Cuts.gm1",
    }

    for old_suffix, new_suffix in renames.items():
        old_file = output_dir / f"{board_name}{old_suffix}"
        if old_file.exists():
            new_file = output_dir / f"{board_name}{new_suffix}"
            old_file.rename(new_file)
