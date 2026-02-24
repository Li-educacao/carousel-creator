"""FreeRouting integration — headless auto-routing via subprocess."""
from __future__ import annotations
import subprocess
import shutil
from pathlib import Path

from rich.console import Console

from pcb_autoplacer.config import FREEROUTING_JAR

console = Console()


class FreeRoutingError(Exception):
    """Error running FreeRouting."""


def find_java() -> str:
    """Find Java executable."""
    java = shutil.which("java")
    if java:
        return java
    # Common macOS locations
    candidates = [
        "/usr/bin/java",
        "/opt/homebrew/bin/java",
        "/Library/Java/JavaVirtualMachines/*/Contents/Home/bin/java",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    raise FreeRoutingError("Java not found. Install JDK: brew install openjdk")


def route(dsn_path: Path, output_dir: Path | None = None, timeout_sec: int = 300) -> Path:
    """Run FreeRouting headless auto-routing on a DSN file.

    Args:
        dsn_path: Path to input .dsn file
        output_dir: Directory for output files. Defaults to dsn_path's directory.
        timeout_sec: Maximum routing time in seconds

    Returns:
        Path to the generated .ses file
    """
    if not FREEROUTING_JAR.exists():
        raise FreeRoutingError(f"FreeRouting JAR not found at {FREEROUTING_JAR}")

    # Resolve to absolute paths — FreeRouting Java requires absolute paths
    dsn_path = dsn_path.resolve()

    if not dsn_path.exists():
        raise FreeRoutingError(f"DSN file not found: {dsn_path}")

    if output_dir is None:
        output_dir = dsn_path.parent
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    ses_path = output_dir / dsn_path.with_suffix(".ses").name

    # Patch DSN with proper net classes before routing
    from pcb_autoplacer.routing.dsn_patcher import patch_dsn_net_classes
    console.print("[cyan]Patching DSN with net class trace widths...[/cyan]")
    patch_dsn_net_classes(dsn_path)

    java = find_java()

    console.print(f"[cyan]Running FreeRouting on {dsn_path.name}...[/cyan]")
    console.print("[dim]This may take a few minutes for complex boards.[/dim]")

    cmd = [
        java, "-jar", str(FREEROUTING_JAR),
        "-de", str(dsn_path),        # input DSN
        "-do", str(ses_path),        # output SES
        "-mp", "20",                 # max passes
        "-oit",                      # optimize intermediate traces
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            cwd=str(output_dir),
        )
    except subprocess.TimeoutExpired:
        raise FreeRoutingError(f"FreeRouting timed out after {timeout_sec}s")

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise FreeRoutingError(f"FreeRouting failed (exit {result.returncode}): {stderr}")

    if not ses_path.exists():
        # FreeRouting might use a different naming convention
        possible = list(output_dir.glob("*.ses"))
        if possible:
            ses_path = possible[0]
        else:
            raise FreeRoutingError("FreeRouting completed but no .ses file was generated")

    console.print(f"[green]Routing complete: {ses_path.name}[/green]")
    return ses_path
