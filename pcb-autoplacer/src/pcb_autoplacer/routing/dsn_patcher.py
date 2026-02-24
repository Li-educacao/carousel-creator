"""DSN net class patcher — rewrites FreeRouting class definitions with proper trace widths."""
from __future__ import annotations

import re
from pathlib import Path

from rich.console import Console

console = Console()

# Net classification rules (keywords → class)
AC_KEYWORDS = ("LINE", "NEUT", "AC", "MAINS", "PS1-AC")
POWER_KEYWORDS = ("+5V", "+3V3", "+3.3V", "VCC", "VDD", "GND")

# Trace widths in DSN units (um). KiCad DSN: 200 = 0.2mm, 1000 = 1.0mm
AC_WIDTH = 1000        # 1.0mm
AC_CLEARANCE = 500     # 0.5mm
AC_VIA = "Via[0-1]_800:400_um"

POWER_WIDTH = 500      # 0.5mm
POWER_CLEARANCE = 300  # 0.3mm
POWER_VIA = "Via[0-1]_600:300_um"

SIGNAL_WIDTH = 250     # 0.25mm
SIGNAL_CLEARANCE = 200 # 0.2mm
SIGNAL_VIA = "Via[0-1]_450:200_um"


def classify_net(name: str) -> str:
    """Classify a net name into AC_Mains, Power, or Signal."""
    upper = name.upper()
    if any(kw in upper for kw in AC_KEYWORDS):
        return "AC_Mains"
    if any(kw in upper for kw in POWER_KEYWORDS):
        return "Power"
    return "Signal"


def patch_dsn_net_classes(dsn_path: Path) -> Path:
    """Rewrite DSN class section to split nets by trace width requirements.

    Replaces the single 'kicad_default' class with AC_Mains, Power, and Signal
    classes, each with appropriate trace widths.

    Returns:
        Path to the patched DSN file (same file, modified in-place).
    """
    text = dsn_path.read_text(encoding="utf-8")

    # Find the class section: (class kicad_default ... )
    # Match from "(class kicad_default" to its closing paren
    class_pattern = re.compile(
        r'(\s*\(class kicad_default\s+)(.*?)(\s*\(circuit.*?\)\s*\(rule.*?\)\s*\))',
        re.DOTALL,
    )
    match = class_pattern.search(text)
    if not match:
        console.print("[yellow]Warning: Could not find kicad_default class in DSN[/yellow]")
        return dsn_path

    # Extract all net names from the class
    net_names_str = match.group(2)
    # Parse net names — could be bare words or quoted strings
    net_names = re.findall(r'"([^"]+)"|(\S+)', net_names_str)
    nets = [quoted or bare for quoted, bare in net_names]

    # Classify nets
    ac_nets = []
    power_nets = []
    signal_nets = []
    for net in nets:
        cls = classify_net(net)
        if cls == "AC_Mains":
            ac_nets.append(net)
        elif cls == "Power":
            power_nets.append(net)
        else:
            signal_nets.append(net)

    console.print(f"  [cyan]AC Mains nets ({len(ac_nets)}):[/cyan] {', '.join(ac_nets)}")
    console.print(f"  [yellow]Power nets ({len(power_nets)}):[/yellow] {', '.join(power_nets)}")
    console.print(f"  [dim]Signal nets ({len(signal_nets)}):[/dim] {len(signal_nets)} nets")

    # Build via definitions for the structure section
    via_defs = set()
    via_defs.add(AC_VIA)
    via_defs.add(POWER_VIA)
    via_defs.add(SIGNAL_VIA)

    # Add via padstack definitions to library if not present
    # FreeRouting needs padstack definitions for non-default vias
    # We'll add them to the structure section

    # Build replacement class sections
    def _format_nets(net_list: list[str]) -> str:
        parts = []
        for n in net_list:
            if re.search(r'[\s()\-{}/~]', n):
                parts.append(f'"{n}"')
            else:
                parts.append(n)
        return " ".join(parts)

    def _build_class(name: str, net_list: list[str], width: int, clearance: int, via: str) -> str:
        if not net_list:
            return ""
        nets_str = _format_nets(net_list)
        return f"""    (class {name} {nets_str}
      (circuit
        (use_via "{via}")
      )
      (rule
        (width {width})
        (clearance {clearance})
      )
    )"""

    classes = []
    if ac_nets:
        classes.append(_build_class("AC_Mains", ac_nets, AC_WIDTH, AC_CLEARANCE, AC_VIA))
    if power_nets:
        classes.append(_build_class("Power", power_nets, POWER_WIDTH, POWER_CLEARANCE, POWER_VIA))
    if signal_nets:
        classes.append(_build_class("Signal", signal_nets, SIGNAL_WIDTH, SIGNAL_CLEARANCE, SIGNAL_VIA))

    new_classes = "\n".join(classes)

    # Replace the old class section
    # Find the full class block including its closing paren
    full_class_pattern = re.compile(
        r'\s*\(class kicad_default\s+.*?\(rule\s*\n?\s*\(width \d+\)\s*\n?\s*\(clearance \d+\)\s*\n?\s*\)\s*\)',
        re.DOTALL,
    )
    full_match = full_class_pattern.search(text)
    if not full_match:
        console.print("[yellow]Warning: Could not match full class block[/yellow]")
        return dsn_path

    text = text[:full_match.start()] + "\n" + new_classes + text[full_match.end():]

    # Also add via padstack definitions to the library section if needed
    # FreeRouting needs padstacks for custom vias
    for via_name in [AC_VIA, POWER_VIA, SIGNAL_VIA]:
        if via_name not in text:
            # Parse via dimensions from name: Via[0-1]_D:d_um
            via_match = re.match(r'Via\[0-1\]_(\d+):(\d+)_um', via_name)
            if via_match:
                diameter = int(via_match.group(1))
                drill = int(via_match.group(2))
                padstack = f"""    (padstack "{via_name}"
      (shape
        (circle F.Cu {diameter})
      )
      (shape
        (circle B.Cu {diameter})
      )
      (attach off)
    )"""
                # Insert before closing of library section
                lib_end = text.rfind("  )\n  (network")
                if lib_end > 0:
                    text = text[:lib_end] + padstack + "\n" + text[lib_end:]

    # Add via references to structure section
    for via_name in [AC_VIA, POWER_VIA, SIGNAL_VIA]:
        via_ref = f'    (via "{via_name}")'
        if via_ref not in text:
            # Insert after existing via line
            existing_via = re.search(r'(\s*\(via "[^"]+"\))', text)
            if existing_via:
                text = text[:existing_via.end()] + "\n" + via_ref + text[existing_via.end():]

    dsn_path.write_text(text, encoding="utf-8")
    console.print(f"[green]DSN patched with net classes: AC={AC_WIDTH/1000:.1f}mm, Power={POWER_WIDTH/1000:.1f}mm, Signal={SIGNAL_WIDTH/1000:.2f}mm[/green]")
    return dsn_path
