#!/usr/bin/env python3
"""KiCad Bridge — runs under KiCad's Python 3.9 for pcbnew operations.

Usage:
    kicad_bridge.py export-dsn <board.kicad_pcb> <output.dsn>
    kicad_bridge.py import-ses <board.kicad_pcb> <routed.ses>
"""
import sys
import os


def _setup_net_classes(board) -> None:
    """Configure net classes with proper trace widths before DSN export.

    AC mains nets get 1.0mm traces, power nets 0.5mm, signal 0.25mm.
    """
    import pcbnew

    # Classify nets by name
    ac_keywords = ("LINE", "NEUT", "AC", "MAINS", "PS1-AC")
    power_keywords = ("+5V", "+3V3", "VCC", "VDD", "GND")

    settings = board.GetDesignSettings()

    # Set default net class trace width
    default_nc = settings.GetDefaultNetclass()
    default_nc.SetTraceWidth(pcbnew.FromMM(0.25))
    default_nc.SetViaDiameter(pcbnew.FromMM(0.45))
    default_nc.SetViaDrill(pcbnew.FromMM(0.2))
    default_nc.SetClearance(pcbnew.FromMM(0.2))

    # Apply per-net trace widths via net info
    netinfo = board.GetNetInfo()
    for net in board.GetNetInfo().NetsByName():
        name = net
        upper = name.upper()

        net_item = netinfo.GetNetItem(name)
        if net_item is None:
            continue

        nc = net_item.GetNetClass()
        if any(kw in upper for kw in ac_keywords):
            # AC mains: 1.0mm trace
            nc.SetTraceWidth(pcbnew.FromMM(1.0))
            nc.SetViaDiameter(pcbnew.FromMM(0.8))
            nc.SetViaDrill(pcbnew.FromMM(0.4))
            nc.SetClearance(pcbnew.FromMM(0.5))
        elif any(kw in upper for kw in power_keywords):
            # Power: 0.5mm trace
            nc.SetTraceWidth(pcbnew.FromMM(0.5))
            nc.SetViaDiameter(pcbnew.FromMM(0.6))
            nc.SetViaDrill(pcbnew.FromMM(0.3))
            nc.SetClearance(pcbnew.FromMM(0.3))


def export_dsn(pcb_path: str, dsn_path: str) -> None:
    """Export a .kicad_pcb to Specctra DSN format."""
    try:
        import pcbnew
    except ImportError:
        print("ERROR: pcbnew not available. This script must run under KiCad's Python.", file=sys.stderr)
        sys.exit(1)

    pcb_path = os.path.abspath(pcb_path)
    dsn_path = os.path.abspath(dsn_path)

    board = pcbnew.LoadBoard(pcb_path)
    if board is None:
        print(f"ERROR: Failed to load board: {pcb_path}", file=sys.stderr)
        sys.exit(1)

    # Set trace widths per net type before DSN export
    try:
        _setup_net_classes(board)
        print("OK: Net classes configured (AC=1.0mm, Power=0.5mm, Signal=0.25mm)")
    except Exception as e:
        print(f"WARNING: Could not setup net classes: {e}", file=sys.stderr)

    ok = pcbnew.ExportSpecctraDSN(board, dsn_path)
    if not ok:
        print(f"ERROR: Failed to export DSN: {dsn_path}", file=sys.stderr)
        sys.exit(1)

    print(f"OK: Exported DSN to {dsn_path}")


def import_ses(pcb_path: str, ses_path: str) -> None:
    """Import a Specctra SES (routed) file back into .kicad_pcb."""
    try:
        import pcbnew
    except ImportError:
        print("ERROR: pcbnew not available. This script must run under KiCad's Python.", file=sys.stderr)
        sys.exit(1)

    pcb_path = os.path.abspath(pcb_path)
    ses_path = os.path.abspath(ses_path)

    board = pcbnew.LoadBoard(pcb_path)
    if board is None:
        print(f"ERROR: Failed to load board: {pcb_path}", file=sys.stderr)
        sys.exit(1)

    ok = pcbnew.ImportSpecctraSES(board, ses_path)
    if not ok:
        print(f"ERROR: Failed to import SES: {ses_path}", file=sys.stderr)
        sys.exit(1)

    board.Save(pcb_path)
    print(f"OK: Imported SES and saved board to {pcb_path}")


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "export-dsn":
        if len(sys.argv) != 4:
            print("Usage: kicad_bridge.py export-dsn <board.kicad_pcb> <output.dsn>", file=sys.stderr)
            sys.exit(1)
        export_dsn(sys.argv[2], sys.argv[3])

    elif command == "import-ses":
        if len(sys.argv) != 4:
            print("Usage: kicad_bridge.py import-ses <board.kicad_pcb> <routed.ses>", file=sys.stderr)
            sys.exit(1)
        import_ses(sys.argv[2], sys.argv[3])

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
