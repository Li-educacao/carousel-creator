"""Domain models for PCB Autoplacer."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Pad:
    """A pad on a footprint."""
    number: str          # "1", "2", "A1", etc.
    pad_type: str        # "smd", "thru_hole", "np_thru_hole"
    shape: str           # "rect", "circle", "oval", "roundrect", "custom"
    x: float = 0.0      # relative to footprint origin, mm
    y: float = 0.0
    width: float = 0.0   # mm
    height: float = 0.0  # mm
    drill: float = 0.0   # mm, 0 for SMD
    layers: list[str] = field(default_factory=list)  # ["F.Cu", "F.Paste", "F.Mask"]
    net_number: int = 0
    net_name: str = ""

@dataclass
class FootprintDef:
    """Parsed footprint definition from .kicad_mod."""
    name: str            # e.g. "R_0805_2012Metric"
    library: str = ""    # e.g. "Resistor_SMD"
    description: str = ""
    pads: list[Pad] = field(default_factory=list)
    bbox_width: float = 0.0   # bounding box mm
    bbox_height: float = 0.0
    bbox_offset_x: float = 0.0  # center of bbox relative to footprint origin
    bbox_offset_y: float = 0.0
    is_smd: bool = True

@dataclass
class Component:
    """A component from the netlist."""
    ref: str             # "R1", "C1", "U1"
    value: str           # "10k", "100nF", "STM32F103"
    footprint: str       # "Resistor_SMD:R_0805_2012Metric"
    library: str = ""    # footprint library name
    footprint_name: str = ""  # footprint name within library
    description: str = ""
    properties: dict[str, str] = field(default_factory=dict)

@dataclass
class NetNode:
    """A connection point in a net."""
    ref: str             # component reference "R1"
    pin: str             # pin number/name "1"

@dataclass
class Net:
    """A named net connecting component pins."""
    code: int            # net number
    name: str            # "/VCC", "GND", "Net-(R1-Pad1)"
    nodes: list[NetNode] = field(default_factory=list)

@dataclass
class PlacedComponent:
    """A component with placement coordinates."""
    ref: str
    value: str
    footprint: str
    x: float             # mm, board coordinates
    y: float             # mm
    rotation: float = 0.0   # degrees
    layer: str = "F.Cu"     # "F.Cu" or "B.Cu"
    footprint_def: FootprintDef | None = None
    ref_offset: tuple[float, float] | None = None  # (dx, dy) override for Reference label
    hide_value: bool = False  # hide Value label to reduce visual clutter

@dataclass
class BoardConfig:
    """Board configuration for generation."""
    width_mm: float = 50.0
    height_mm: float = 50.0
    origin_x: float = 100.0   # KiCad board origin
    origin_y: float = 100.0
    layers: int = 2
    edge_clearance_mm: float = 1.0

@dataclass
class PlacementGroup:
    """Group of related components for placement strategy."""
    name: str                    # "power", "decoupling", "signal"
    refs: list[str] = field(default_factory=list)
    priority: int = 0           # higher = place first
    keep_together: bool = True
    near_ref: str = ""          # place near this reference

@dataclass
class PlacementStrategy:
    """AI-generated placement strategy."""
    board_width_mm: float = 50.0
    board_height_mm: float = 50.0
    groups: list[PlacementGroup] = field(default_factory=list)
    placements: list[dict] = field(default_factory=list)  # [{ref, x, y, rotation, layer}]
    reasoning: str = ""
