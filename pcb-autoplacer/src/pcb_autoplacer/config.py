"""PCB Autoplacer configuration — KiCad paths and JLCPCB design rules."""
from __future__ import annotations
import os
from pathlib import Path
from dataclasses import dataclass, field

# KiCad paths (macOS)
KICAD_APP = Path("/Applications/KiCad/KiCad.app")
KICAD_CLI = KICAD_APP / "Contents/MacOS/kicad-cli"
KICAD_PYTHON = KICAD_APP / "Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9"
KICAD_FOOTPRINT_LIBS = Path(os.path.expanduser("~/Documents/KiCad/9.0/footprints"))
KICAD_SYSTEM_FOOTPRINTS = KICAD_APP / "Contents/SharedSupport/footprints"

# FreeRouting
FREEROUTING_JAR = Path(os.path.expanduser(
    "~/Documents/KiCad/9.0/3rdparty/plugins/app_freerouting_kicad-plugin/jar/freerouting-2.1.0.jar"
))

# Grid
DEFAULT_GRID_MM = 0.5
FINE_GRID_MM = 0.25

@dataclass
class JLCPCBRules:
    """JLCPCB 2-layer design rules."""
    min_trace_width_mm: float = 0.2
    min_clearance_mm: float = 0.2
    min_via_diameter_mm: float = 0.45
    min_via_drill_mm: float = 0.2
    board_thickness_mm: float = 1.6
    copper_weight_oz: float = 1.0
    default_trace_width_mm: float = 0.25
    power_trace_width_mm: float = 0.5
    min_annular_ring_mm: float = 0.125  # (0.45 - 0.2) / 2
    edge_clearance_mm: float = 0.3
    silk_line_width_mm: float = 0.15
    silk_text_size_mm: float = 1.0

JLCPCB = JLCPCBRules()
