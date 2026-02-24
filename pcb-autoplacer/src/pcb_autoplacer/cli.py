"""PCB Autoplacer CLI — automated PCB layout pipeline."""
from __future__ import annotations
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer(
    name="pcb-autoplacer",
    help="Automated PCB layout: schematic → placement → routing → Gerbers",
    no_args_is_help=True,
)
console = Console()


def _resolve_netlist(schematic: Path) -> Path:
    """Find or generate the .net netlist file for a schematic."""
    # KiCad 9 stores netlist as .net alongside .kicad_sch
    net_path = schematic.with_suffix(".net")
    if net_path.exists():
        return net_path

    # Try to generate via kicad-cli
    from pcb_autoplacer.config import KICAD_CLI
    import subprocess

    console.print(f"[cyan]Generating netlist from {schematic.name}...[/cyan]")
    result = subprocess.run(
        [str(KICAD_CLI), "sch", "export", "netlist",
         "--output", str(net_path), str(schematic)],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0 or not net_path.exists():
        console.print(f"[red]Failed to generate netlist: {result.stderr.strip()}[/red]")
        raise typer.Exit(1)

    console.print(f"[green]Netlist generated: {net_path.name}[/green]")
    return net_path


def _load_netlist(schematic: Path):
    """Load and parse netlist, resolve footprints."""
    from pcb_autoplacer.parsers.netlist import parse_netlist
    from pcb_autoplacer.parsers.footprint import load_footprint

    net_path = _resolve_netlist(schematic)
    components, nets = parse_netlist(net_path)

    # Resolve footprints
    footprints = {}
    for comp in components:
        fp = load_footprint(comp.footprint)
        if fp:
            footprints[comp.ref] = fp

    return components, nets, footprints


@app.command()
def parse(
    schematic: Annotated[Path, typer.Argument(help="Path to .kicad_sch or .net file")],
):
    """Parse schematic/netlist and show component & net summary."""
    if not schematic.exists():
        console.print(f"[red]File not found: {schematic}[/red]")
        raise typer.Exit(1)

    components, nets, footprints = _load_netlist(schematic)

    # Components table
    table = Table(title=f"Components ({len(components)})")
    table.add_column("Ref", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Footprint")
    table.add_column("Size (mm)")
    table.add_column("Type")

    for comp in sorted(components, key=lambda c: c.ref):
        fp = footprints.get(comp.ref)
        size = f"{fp.bbox_width:.1f}x{fp.bbox_height:.1f}" if fp else "?"
        fp_type = "SMD" if (fp and fp.is_smd) else "THT" if fp else "?"
        table.add_row(comp.ref, comp.value, comp.footprint_name, size, fp_type)

    console.print(table)

    # Nets summary
    console.print(f"\n[bold]Nets: {len(nets)}[/bold]")
    for net in sorted(nets, key=lambda n: n.code)[:20]:
        if net.code == 0 or not net.nodes:
            continue
        nodes = ", ".join(f"{n.ref}.{n.pin}" for n in net.nodes)
        console.print(f"  [dim]{net.name}:[/dim] {nodes}")
    if len(nets) > 20:
        console.print(f"  [dim]... and {len(nets) - 20} more nets[/dim]")

    console.print(f"\n[green]Footprints resolved: {len(footprints)}/{len(components)}[/green]")


@app.command()
def analyze(
    schematic: Annotated[Path, typer.Argument(help="Path to .kicad_sch or .net file")],
):
    """Analyze circuit with AI and show placement strategy."""
    if not schematic.exists():
        console.print(f"[red]File not found: {schematic}[/red]")
        raise typer.Exit(1)

    components, nets, footprints = _load_netlist(schematic)

    from pcb_autoplacer.ai.claude_cli import analyze_circuit

    analysis = analyze_circuit(components, nets, footprints)

    console.print(Panel(f"[bold]Circuit Type:[/bold] {analysis.get('circuit_type', 'unknown')}"))

    # Critical paths
    paths = analysis.get("critical_paths", [])
    if paths:
        table = Table(title="Critical Paths")
        table.add_column("Name")
        table.add_column("Priority")
        table.add_column("Trace Width")
        table.add_column("Nets")
        for p in paths:
            table.add_row(
                p["name"],
                p["priority"],
                f"{p['trace_width_mm']}mm",
                ", ".join(p["nets"][:3]),
            )
        console.print(table)

    # Power/Ground nets
    power = analysis.get("power_nets", [])
    ground = analysis.get("ground_nets", [])
    if power:
        console.print(f"[yellow]Power nets:[/yellow] {', '.join(power)}")
    if ground:
        console.print(f"[blue]Ground nets:[/blue] {', '.join(ground)}")


@app.command()
def place(
    schematic: Annotated[Path, typer.Argument(help="Path to .kicad_sch or .net file")],
    output: Annotated[Path, typer.Option("-o", "--output", help="Output .kicad_pcb path")] = Path("board.kicad_pcb"),
    width: Annotated[Optional[float], typer.Option("-w", "--width", help="Board width in mm (auto if omitted)")] = None,
    height: Annotated[Optional[float], typer.Option("-h", "--height", help="Board height in mm (auto if omitted)")] = None,
    no_ai: Annotated[bool, typer.Option("--no-ai", help="Use grid fallback instead of AI")] = False,
):
    """Generate .kicad_pcb with AI-powered component placement."""
    if not schematic.exists():
        console.print(f"[red]File not found: {schematic}[/red]")
        raise typer.Exit(1)

    from pcb_autoplacer.models import BoardConfig
    from pcb_autoplacer.placer.engine import apply_placement, fallback_placement, calculate_board_size
    from pcb_autoplacer.placer.constraints import validate_placement, resolve_overlaps
    from pcb_autoplacer.generators.kicad_pcb import generate_pcb

    components, nets, footprints = _load_netlist(schematic)

    # Auto-size board if dimensions not specified
    if width is None or height is None:
        auto_w, auto_h = calculate_board_size(components, footprints)
        width = width or auto_w
        height = height or auto_h
        console.print(f"[cyan]Auto-sized board: {width:.0f}x{height:.0f}mm[/cyan]")

    board = BoardConfig(width_mm=width, height_mm=height)

    if no_ai:
        console.print("[yellow]Using grid fallback placement (--no-ai)[/yellow]")
        ai_placements = fallback_placement(components, footprints, board)
    else:
        from pcb_autoplacer.ai.claude_cli import generate_placement
        result = generate_placement(components, nets, footprints, width, height)
        ai_placements = result.get("placements", [])
        if result.get("reasoning"):
            console.print(Panel(result["reasoning"], title="Placement Strategy"))

    placed = apply_placement(components, nets, footprints, ai_placements, board)

    # Check for overlaps before resolving
    pre_validation = validate_placement(placed, board)
    pre_overlaps = len(pre_validation["overlaps"])

    if pre_overlaps > 0:
        console.print(f"[yellow]Found {pre_overlaps} overlapping pairs — resolving...[/yellow]")
        placed, remaining = resolve_overlaps(placed, board)
        if remaining == 0:
            console.print("[green]All overlaps resolved![/green]")
        else:
            console.print(f"[yellow]{remaining} overlaps remaining after resolution[/yellow]")

    # Final validation
    validation = validate_placement(placed, board)
    if validation["boundary_violations"]:
        console.print(f"[yellow]Warning: {len(validation['boundary_violations'])} components outside board[/yellow]")

    # Generate PCB
    generate_pcb(placed, nets, board, output)
    console.print(f"\n[green bold]PCB generated: {output}[/green bold]")
    console.print(f"  Components: {len(placed)}, Board: {width}x{height}mm")


@app.command()
def route(
    pcb: Annotated[Path, typer.Argument(help="Path to .kicad_pcb file")],
    timeout: Annotated[int, typer.Option("--timeout", help="Routing timeout in seconds")] = 300,
):
    """Auto-route PCB using FreeRouting."""
    if not pcb.exists():
        console.print(f"[red]File not found: {pcb}[/red]")
        raise typer.Exit(1)

    from pcb_autoplacer.routing.bridge import export_dsn, import_ses
    from pcb_autoplacer.routing.freerouting import route as freeroute

    work_dir = pcb.parent
    dsn_path = work_dir / pcb.with_suffix(".dsn").name

    # Export DSN
    export_dsn(pcb, dsn_path)

    # Route
    ses_path = freeroute(dsn_path, timeout_sec=timeout)

    # Import SES back
    import_ses(pcb, ses_path)

    console.print(f"\n[green bold]Routing complete: {pcb}[/green bold]")


@app.command()
def drc(
    pcb: Annotated[Path, typer.Argument(help="Path to .kicad_pcb file")],
):
    """Run Design Rule Check on a PCB file."""
    if not pcb.exists():
        console.print(f"[red]File not found: {pcb}[/red]")
        raise typer.Exit(1)

    from pcb_autoplacer.export.kicad_cli import run_drc

    report = run_drc(pcb)
    violations = report.get("violations", [])
    unconnected = report.get("unconnected_items", [])

    if not violations and not unconnected:
        console.print("[green bold]DRC PASSED — zero violations[/green bold]")
    else:
        raise typer.Exit(1)


@app.command()
def export(
    pcb: Annotated[Path, typer.Argument(help="Path to .kicad_pcb file")],
    output: Annotated[Path, typer.Option("-o", "--output", help="Output directory for Gerbers")] = Path("./gerbers"),
):
    """Export Gerber + Drill files for JLCPCB fabrication."""
    if not pcb.exists():
        console.print(f"[red]File not found: {pcb}[/red]")
        raise typer.Exit(1)

    from pcb_autoplacer.export.kicad_cli import export_gerbers

    files = export_gerbers(pcb, output)
    console.print(f"\n[green bold]Gerbers ready: {output}[/green bold]")
    console.print(f"  Files: {len(files)}")
    console.print("  Upload to https://cart.jlcpcb.com/quote")


@app.command()
def run(
    schematic: Annotated[Path, typer.Argument(help="Path to .kicad_sch file")],
    output: Annotated[Path, typer.Option("-o", "--output", help="Output directory")] = Path("./output"),
    width: Annotated[float, typer.Option("-w", "--width", help="Board width mm")] = 50.0,
    height: Annotated[float, typer.Option("-h", "--height", help="Board height mm")] = 50.0,
    no_ai: Annotated[bool, typer.Option("--no-ai", help="Skip AI, use grid placement")] = False,
    skip_route: Annotated[bool, typer.Option("--skip-route", help="Skip auto-routing")] = False,
    skip_drc: Annotated[bool, typer.Option("--skip-drc", help="Skip DRC check")] = False,
):
    """Full pipeline: parse → analyze → place → route → DRC → export."""
    if not schematic.exists():
        console.print(f"[red]File not found: {schematic}[/red]")
        raise typer.Exit(1)

    output.mkdir(parents=True, exist_ok=True)
    pcb_path = output / "board.kicad_pcb"
    gerber_dir = output / "gerbers"

    from pcb_autoplacer.models import BoardConfig
    from pcb_autoplacer.placer.engine import apply_placement, fallback_placement
    from pcb_autoplacer.placer.constraints import validate_placement, resolve_overlaps
    from pcb_autoplacer.generators.kicad_pcb import generate_pcb

    # Step 1: Parse
    console.print(Panel("[bold]Step 1/6: Parsing schematic[/bold]"))
    components, nets, footprints = _load_netlist(schematic)
    console.print(f"  {len(components)} components, {len(nets)} nets, {len(footprints)} footprints resolved")

    # Step 2: Analyze + Place
    console.print(Panel("[bold]Step 2/6: Generating placement[/bold]"))
    board = BoardConfig(width_mm=width, height_mm=height)

    if no_ai:
        ai_placements = fallback_placement(components, footprints, board)
    else:
        from pcb_autoplacer.ai.claude_cli import generate_placement
        result = generate_placement(components, nets, footprints, width, height)
        ai_placements = result.get("placements", [])
        if result.get("reasoning"):
            console.print(f"  Strategy: {result['reasoning'][:100]}...")

    placed = apply_placement(components, nets, footprints, ai_placements, board)

    # Resolve overlaps
    pre_validation = validate_placement(placed, board)
    if pre_validation["overlaps"]:
        console.print(f"  [yellow]{len(pre_validation['overlaps'])} overlaps found — resolving...[/yellow]")
        placed, remaining = resolve_overlaps(placed, board)
        if remaining == 0:
            console.print("  [green]All overlaps resolved![/green]")
        else:
            console.print(f"  [yellow]{remaining} overlaps remaining[/yellow]")

    # Step 3: Generate PCB
    console.print(Panel("[bold]Step 3/6: Generating PCB file[/bold]"))
    generate_pcb(placed, nets, board, pcb_path)
    console.print(f"  [green]Generated: {pcb_path}[/green]")

    # Step 4: Route
    if not skip_route:
        console.print(Panel("[bold]Step 4/6: Auto-routing[/bold]"))
        try:
            from pcb_autoplacer.routing.bridge import export_dsn, import_ses
            from pcb_autoplacer.routing.freerouting import route as freeroute

            dsn_path = output / "board.dsn"
            export_dsn(pcb_path, dsn_path)
            ses_path = freeroute(dsn_path, output_dir=output)
            import_ses(pcb_path, ses_path)
        except Exception as e:
            console.print(f"  [yellow]Routing failed: {e}[/yellow]")
            console.print("  [yellow]PCB generated without routing. Route manually in KiCad.[/yellow]")
    else:
        console.print(Panel("[bold]Step 4/6: Routing SKIPPED[/bold]"))

    # Step 5: DRC
    if not skip_drc:
        console.print(Panel("[bold]Step 5/6: Design Rule Check[/bold]"))
        try:
            from pcb_autoplacer.export.kicad_cli import run_drc
            run_drc(pcb_path)
        except Exception as e:
            console.print(f"  [yellow]DRC failed: {e}[/yellow]")
    else:
        console.print(Panel("[bold]Step 5/6: DRC SKIPPED[/bold]"))

    # Step 6: Export Gerbers
    console.print(Panel("[bold]Step 6/6: Exporting Gerbers[/bold]"))
    try:
        from pcb_autoplacer.export.kicad_cli import export_gerbers
        export_gerbers(pcb_path, gerber_dir)
    except Exception as e:
        console.print(f"  [yellow]Gerber export failed: {e}[/yellow]")

    # Summary
    console.print()
    console.print(Panel.fit(
        f"[bold green]Pipeline complete![/bold green]\n\n"
        f"  PCB: {pcb_path}\n"
        f"  Gerbers: {gerber_dir}\n"
        f"  Board: {width}x{height}mm, {len(placed)} components\n\n"
        f"  Next: Open {pcb_path.name} in KiCad to review",
        title="PCB Autoplacer",
    ))


if __name__ == "__main__":
    app()
