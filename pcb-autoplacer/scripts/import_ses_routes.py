#!/usr/bin/env python3
"""Import Specctra SES routes into an existing .kicad_pcb file.

Reads wire segments and vias from board.ses, converts coordinates
from SES units (um*10 = 0.1µm) to mm, and appends them as
(segment ...) and (via ...) elements to the .kicad_pcb.
"""
import re
import uuid
from pathlib import Path


def parse_ses_routes(ses_path: Path) -> tuple[list[dict], list[dict]]:
    """Parse wire segments and vias from a .ses file.

    Returns (segments, vias).
    """
    text = ses_path.read_text()

    # Resolution: "um 10" → 0.1µm units. To convert to mm: value / (1000 * 10)
    res_match = re.search(r'\(resolution\s+um\s+(\d+)\)', text)
    divisor = int(res_match.group(1)) if res_match else 10
    scale = 1.0 / (1000.0 * divisor)

    segments = []
    vias = []

    # Extract the (network_out ...) block
    net_out_match = re.search(r'\(network_out\s*\n(.*)\n\s*\)\s*\n\s*\)\s*\n\s*\)', text, re.DOTALL)
    if not net_out_match:
        print("ERROR: Could not find (network_out ...) block")
        return segments, vias

    net_out = net_out_match.group(1)

    # Split into net blocks: find each (net NAME ...)
    # Use a simple state machine approach
    current_net = None
    depth = 0
    i = 0

    # Find all (net ...) blocks with a simpler regex
    # Each net: (net NAME\n  (wire ...)\n  ...\n)
    # Net names: quoted "Net-(D3-Pad2)" or bare +5V, GND, LINE
    net_pattern = re.compile(r'\(net\s+("(?:[^"\\]|\\.)*"|[A-Za-z0-9_+./-]+)')
    wire_pattern = re.compile(r'\(path\s+(\S+)\s+(\d+)\s*\n([\s\d\n-]+)\)')
    via_pattern = re.compile(r'\(via\s+"([^"]+)"\s+(-?\d+)\s+(-?\d+)')

    # Find all net names and their positions
    net_starts = [(m.start(), m.group(1)) for m in net_pattern.finditer(net_out)]

    for idx, (start, net_name) in enumerate(net_starts):
        # Get the text for this net block (until next net or end)
        if idx + 1 < len(net_starts):
            end = net_starts[idx + 1][0]
        else:
            end = len(net_out)
        block = net_out[start:end]

        # Remove surrounding quotes if present, keep {slash} as-is (matches PCB net names)
        clean_name = net_name.strip('"')

        # Find all wire paths in this net block
        for wire in wire_pattern.finditer(block):
            layer = wire.group(1)
            width_raw = int(wire.group(2))
            width_mm = width_raw * scale
            coords_text = wire.group(3).strip()
            nums = [int(x) for x in coords_text.split()]

            # Pairs of (x, y) → consecutive segments
            for j in range(0, len(nums) - 2, 2):
                x1 = nums[j] * scale
                y1 = -nums[j + 1] * scale  # SES Y is negated vs KiCad
                x2 = nums[j + 2] * scale
                y2 = -nums[j + 3] * scale
                segments.append({
                    "layer": layer, "width": width_mm,
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "net_name": clean_name,
                })

        # Find all vias
        for via in via_pattern.finditer(block):
            vx = int(via.group(2)) * scale
            vy = -int(via.group(3)) * scale
            vias.append({"x": vx, "y": vy, "net_name": clean_name})

    return segments, vias


def build_net_map(pcb_text: str) -> dict[str, int]:
    """Extract net name → net number mapping from .kicad_pcb."""
    net_map = {}
    for m in re.finditer(r'\(net\s+(\d+)\s+"([^"]*?)"\)', pcb_text):
        net_map[m.group(2)] = int(m.group(1))
    return net_map


def inject_routes(pcb_path: Path, segments: list[dict], vias: list[dict]) -> None:
    """Inject segments and vias into .kicad_pcb before the closing paren."""
    pcb_text = pcb_path.read_text()
    net_map = build_net_map(pcb_text)

    # Debug: show available nets
    unmatched = set()
    for seg in segments:
        if seg["net_name"] not in net_map:
            unmatched.add(seg["net_name"])
    if unmatched:
        print(f"  WARNING: {len(unmatched)} nets not found in PCB: {sorted(unmatched)[:5]}...")
        print(f"  Available nets: {sorted(net_map.keys())[:10]}...")

    lines = []
    lines.append("")

    for seg in segments:
        net_num = net_map.get(seg["net_name"], 0)
        lines.append(
            f'  (segment (start {seg["x1"]:.4f} {seg["y1"]:.4f})'
            f' (end {seg["x2"]:.4f} {seg["y2"]:.4f})'
            f' (width {seg["width"]:.4f})'
            f' (layer "{seg["layer"]}")'
            f' (net {net_num})'
            f' (uuid "{uuid.uuid4()}"))'
        )

    for v in vias:
        net_num = net_map.get(v["net_name"], 0)
        lines.append(
            f'  (via (at {v["x"]:.4f} {v["y"]:.4f})'
            f' (size 0.6) (drill 0.3)'
            f' (layers "F.Cu" "B.Cu")'
            f' (net {net_num})'
            f' (uuid "{uuid.uuid4()}"))'
        )

    route_block = "\n".join(lines) + "\n"

    # Insert before the final closing paren
    last_paren = pcb_text.rfind(")")
    new_text = pcb_text[:last_paren] + route_block + pcb_text[last_paren:]
    pcb_path.write_text(new_text)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Import Specctra SES routes into .kicad_pcb")
    parser.add_argument("ses", help="Caminho do arquivo .ses")
    parser.add_argument("pcb", help="Caminho do arquivo .kicad_pcb")
    args = parser.parse_args()

    ses_path = Path(args.ses)
    pcb_path = Path(args.pcb)

    if not ses_path.exists():
        print(f"ERROR: SES not found: {ses_path}")
        return
    if not pcb_path.exists():
        print(f"ERROR: PCB not found: {pcb_path}")
        return

    print(f"Parsing SES: {ses_path}")
    segments, vias = parse_ses_routes(ses_path)
    print(f"  {len(segments)} segments, {len(vias)} vias")

    if not segments and not vias:
        print("ERROR: No routes found in SES!")
        return

    print(f"Injecting into: {pcb_path}")
    inject_routes(pcb_path, segments, vias)
    print(f"Done! {len(segments)} segments + {len(vias)} vias injected.")


if __name__ == "__main__":
    main()
