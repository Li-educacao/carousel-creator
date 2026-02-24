"""KiCad Bridge manager — subprocess calls to kicad_bridge.py."""
from __future__ import annotations
import subprocess
from pathlib import Path

from rich.console import Console

from pcb_autoplacer.config import KICAD_PYTHON

console = Console()

# Path to the bridge script (relative to package root)
BRIDGE_SCRIPT = Path(__file__).parent.parent.parent.parent / "scripts" / "kicad_bridge.py"


class BridgeError(Exception):
    """Error in KiCad bridge operation."""


def export_dsn(pcb_path: Path, dsn_path: Path) -> Path:
    """Export .kicad_pcb to Specctra DSN format using KiCad's Python.

    Args:
        pcb_path: Path to .kicad_pcb file
        dsn_path: Output .dsn file path

    Returns:
        Path to the generated .dsn file
    """
    if not KICAD_PYTHON.exists():
        raise BridgeError(f"KiCad Python not found at {KICAD_PYTHON}")

    if not BRIDGE_SCRIPT.exists():
        raise BridgeError(f"Bridge script not found at {BRIDGE_SCRIPT}")

    console.print(f"[cyan]Exporting DSN: {pcb_path.name} → {dsn_path.name}[/cyan]")

    result = subprocess.run(
        [str(KICAD_PYTHON), str(BRIDGE_SCRIPT), "export-dsn", str(pcb_path), str(dsn_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode != 0:
        raise BridgeError(f"DSN export failed: {result.stderr.strip()}")

    if not dsn_path.exists():
        raise BridgeError(f"DSN file was not created: {dsn_path}")

    console.print(f"[green]DSN exported: {dsn_path}[/green]")
    return dsn_path


def import_ses(pcb_path: Path, ses_path: Path) -> Path:
    """Import Specctra SES (routed traces) back into .kicad_pcb.

    Args:
        pcb_path: Path to .kicad_pcb file (will be modified in-place)
        ses_path: Path to .ses file from FreeRouting

    Returns:
        Path to the updated .kicad_pcb file
    """
    if not KICAD_PYTHON.exists():
        raise BridgeError(f"KiCad Python not found at {KICAD_PYTHON}")

    if not ses_path.exists():
        raise BridgeError(f"SES file not found: {ses_path}")

    console.print(f"[cyan]Importing SES: {ses_path.name} → {pcb_path.name}[/cyan]")

    result = subprocess.run(
        [str(KICAD_PYTHON), str(BRIDGE_SCRIPT), "import-ses", str(pcb_path), str(ses_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode != 0:
        raise BridgeError(f"SES import failed: {result.stderr.strip()}")

    console.print(f"[green]SES imported into {pcb_path.name}[/green]")
    return pcb_path
