"""Prompt templates for Claude CLI PCB analysis."""
from __future__ import annotations
from pcb_autoplacer.models import Component, Net, FootprintDef


def format_component_table(components: list[Component], footprints: dict[str, FootprintDef]) -> str:
    """Format components as a readable table for the AI prompt."""
    lines = ["| Ref | Value | Footprint | Size (mm) | Type |"]
    lines.append("|-----|-------|-----------|-----------|------|")
    for c in components:
        fp = footprints.get(c.ref)
        size = f"{fp.bbox_width:.1f}x{fp.bbox_height:.1f}" if fp else "?"
        fp_type = "SMD" if (fp and fp.is_smd) else "THT" if fp else "?"
        lines.append(f"| {c.ref} | {c.value} | {c.footprint_name} | {size} | {fp_type} |")
    return "\n".join(lines)


def format_net_graph(nets: list[Net]) -> str:
    """Format nets as connection graph for the AI prompt."""
    lines = []
    for net in nets:
        if not net.nodes or net.code == 0:
            continue
        node_strs = [f"{n.ref}.{n.pin}" for n in net.nodes]
        lines.append(f"  {net.name}: {' \u2194 '.join(node_strs)}")
    return "\n".join(lines)


def build_analysis_prompt(
    components: list[Component],
    nets: list[Net],
    footprints: dict[str, FootprintDef],
) -> str:
    """Build the circuit analysis prompt."""
    comp_table = format_component_table(components, footprints)
    net_graph = format_net_graph(nets)

    return f"""You are an expert PCB design engineer. Analyze this circuit and identify critical paths and power nets.

## Components
{comp_table}

## Net Connections
{net_graph}

## Instructions
1. Identify the circuit type (power supply, microcontroller, amplifier, sensor, motor driver, or mixed)
2. Identify critical signal paths that need short/controlled traces
3. Identify power nets (VCC, VDD, 3V3, 5V, etc.) and ground nets (GND, AGND, etc.)
4. For each critical path, recommend trace width based on current/signal requirements

Use JLCPCB 2-layer rules: min trace 0.2mm, min clearance 0.2mm, default 0.25mm, power 0.5mm."""


def _classify_ac_dc(
    components: list[Component],
    nets: list[Net],
) -> tuple[set[str], set[str], set[str]]:
    """Classify components into AC-side, DC-side, and isolation boundary."""
    ac_nets = set()
    dc_nets = set()

    for net in nets:
        name_upper = net.name.upper()
        if any(kw in name_upper for kw in ("LINE", "NEUT", "AC", "MAINS")):
            ac_nets.add(net.name)
        elif any(kw in name_upper for kw in ("+5V", "+3V3", "+3.3V", "VCC", "VDD", "GND")):
            dc_nets.add(net.name)

    ref_nets: dict[str, set[str]] = {}
    for net in nets:
        for node in net.nodes:
            ref_nets.setdefault(node.ref, set()).add(net.name)

    ac_refs = set()
    dc_refs = set()
    isolation_refs = set()

    for comp in components:
        comp_nets = ref_nets.get(comp.ref, set())
        has_ac = bool(comp_nets & ac_nets)
        has_dc = bool(comp_nets & dc_nets)
        is_opto = comp.ref.startswith("U") and "817" in comp.value
        is_converter = "HLK" in comp.value or "converter" in comp.footprint.lower()

        if is_opto:
            isolation_refs.add(comp.ref)
        elif is_converter:
            isolation_refs.add(comp.ref)
        elif has_ac and not has_dc:
            ac_refs.add(comp.ref)
        elif has_dc and not has_ac:
            dc_refs.add(comp.ref)
        elif has_ac and has_dc:
            isolation_refs.add(comp.ref)
        else:
            dc_refs.add(comp.ref)

    return ac_refs, dc_refs, isolation_refs


def build_placement_prompt(
    components: list[Component],
    nets: list[Net],
    footprints: dict[str, FootprintDef],
    board_width: float,
    board_height: float,
) -> str:
    """Build the placement prompt with circuit understanding and PCB best practices."""
    ac_refs, dc_refs, iso_refs = _classify_ac_dc(components, nets)

    size_lines = []
    total_area = 0.0
    for c in sorted(components, key=lambda x: x.ref):
        fp = footprints.get(c.ref)
        w = fp.bbox_width if fp else 3.0
        h = fp.bbox_height if fp else 3.0
        total_area += w * h
        fp_type = "SMD" if (fp and fp.is_smd) else "THT"
        domain = "AC" if c.ref in ac_refs else "ISO" if c.ref in iso_refs else "DC"
        size_lines.append(f"  {c.ref:6s}  {w:5.1f} x {h:4.1f} mm  {fp_type:3s}  [{domain:3s}]  {c.value}")
    sizes = "\n".join(size_lines)

    adjacency_lines = []
    for net in nets:
        if not net.nodes or net.code == 0:
            continue
        refs = sorted(set(n.ref for n in net.nodes))
        if len(refs) >= 2:
            adjacency_lines.append(f"  {net.name}: {' — '.join(refs)}")
    adjacency = "\n".join(adjacency_lines)

    return f"""You are an expert PCB layout engineer. Place ALL {len(components)} components on a {board_width:.0f}x{board_height:.0f}mm board.

## COMPONENTS (Ref, Size WxH, Mount, Domain, Value)
{sizes}

## CONNECTIONS (components on same net must be close)
{adjacency}

## DOMAINS
- AC HIGH VOLTAGE ({', '.join(sorted(ac_refs)) or 'none'}): LEFT side of board
- Isolation barrier ({', '.join(sorted(iso_refs)) or 'none'}): CENTER, bridges AC↔DC
- DC LOW VOLTAGE ({', '.join(sorted(dc_refs)) or 'none'}): RIGHT side of board
Signal flow: AC INPUT (left) → ISOLATION (center) → DC/MCU (right)

## COORDINATE SYSTEM
- (0,0) = top-left. X right, Y down. All mm, snap to 0.5mm grid.
- (x,y) = CENTER of component. Body occupies [x-W/2, x+W/2] x [y-H/2, y+H/2].
- Valid: x in [W/2+2, {board_width:.0f}-W/2-2], y in [H/2+2, {board_height:.0f}-H/2-2].

## RULES (MANDATORY — violating these makes the board unusable)

1. NO OVERLAPS: Gap >= 1.5mm between any two component bodies. Before placing each component, verify it doesn't collide with ALL previously placed components.

2. STAY IN BOUNDS: Full component body inside board with 2mm edge margin.

3. AC/DC ISOLATION: 6mm minimum gap between AC and DC zones. Optocouplers/converter form the boundary.

4. DECOUPLING: Caps C6, C7 within 3mm of U3 power pins.

5. CONNECTORS: J1, J2, J3 at left board edge (AC input side).

6. LEDs: D5-D8 in a visible row near bottom or right edge, with series resistors adjacent.

7. ALIGNMENT: SMD passives in neat rows/columns. THT components on grid.

8. ROTATION: 0 or 90 degrees only.

## STRATEGY
1. PS1 (biggest: ~31x17mm) → top-left area
2. AC connectors J2, J3 → left edge near PS1 inputs
3. F1, RV1, C4 → between connectors and PS1
4. R4 (22mm long) → horizontal, below PS1 as AC/DC divider
5. U1, U2 (optocouplers) → center column, isolation boundary
6. U3 (ATtiny85, 9x9mm) → right-center with C6, C7 adjacent
7. D5-D8 + series resistors → bottom row
8. SW1 → near U3, accessible edge
9. Remaining passives → organized around their connected ICs

Provide x,y for ALL {len(components)} components. Verify no overlaps."""
