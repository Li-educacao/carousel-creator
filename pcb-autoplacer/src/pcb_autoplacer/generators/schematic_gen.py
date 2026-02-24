#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera arquivo .kicad_sch (esquematico KiCad 9) a partir de dados JSON.

Produz esquematico visual com simbolos genericos e net labels nas conexoes.
Util para validar circuitos extraidos de fotos antes de gerar o PCB.
"""
from __future__ import annotations

import uuid
from collections import defaultdict
from pathlib import Path


def _uuid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Embedded KiCad 9 symbol definitions (lib_symbols)
# Each returns a string block that goes inside (lib_symbols ...)
# ---------------------------------------------------------------------------

_LIB_SYMBOL_R = """
		(symbol "Device:R"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "R"
				(at 2.032 0 90)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "R"
				(at 0 0 90)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at -1.778 0 90)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Resistor"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "R_0_1"
				(rectangle
					(start -1.016 -2.54)
					(end 1.016 2.54)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "R_1_1"
				(pin passive line
					(at 0 3.81 270)
					(length 1.27)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -3.81 90)
					(length 1.27)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)"""

_LIB_SYMBOL_C = """
		(symbol "Device:C"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0.254)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "C"
				(at 0.635 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "C"
				(at 0.635 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Footprint" ""
				(at 0.9652 -3.81 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Unpolarized capacitor"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "C_0_1"
				(polyline
					(pts
						(xy -2.032 0.762) (xy 2.032 0.762)
					)
					(stroke
						(width 0.508)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy -2.032 -0.762) (xy 2.032 -0.762)
					)
					(stroke
						(width 0.508)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "C_1_1"
				(pin passive line
					(at 0 3.81 270)
					(length 2.794)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -3.81 90)
					(length 2.794)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)"""

_LIB_SYMBOL_LED = """
		(symbol "Device:LED"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 1.016)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "D"
				(at 0 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "LED"
				(at 0 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Light emitting diode"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "LED_0_1"
				(polyline
					(pts
						(xy -1.27 -1.27) (xy -1.27 1.27)
					)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy -1.27 0) (xy 1.27 0)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27)
					)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy -3.048 -0.762) (xy -4.572 -2.286) (xy -3.81 -2.286) (xy -4.572 -2.286) (xy -4.572 -1.524)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy -1.778 -0.762) (xy -3.302 -2.286) (xy -2.54 -2.286) (xy -3.302 -2.286) (xy -3.302 -1.524)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "LED_1_1"
				(pin passive line
					(at -3.81 0 0)
					(length 2.54)
					(name "K"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 3.81 0 180)
					(length 2.54)
					(name "A"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)"""

_LIB_SYMBOL_D = """
		(symbol "Device:D"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 1.016)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "D"
				(at 0 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "D"
				(at 0 -2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Diode"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "D_0_1"
				(polyline
					(pts
						(xy -1.27 1.27) (xy -1.27 -1.27)
					)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 1.27 0) (xy -1.27 0)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27)
					)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "D_1_1"
				(pin passive line
					(at -3.81 0 0)
					(length 2.54)
					(name "K"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 3.81 0 180)
					(length 2.54)
					(name "A"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)"""

_LIB_SYMBOL_Q_NPN = """
		(symbol "Device:Q_NPN_BCE"
			(pin_names
				(offset 0)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "Q"
				(at 5.08 1.905 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "Q_NPN_BCE"
				(at 5.08 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Footprint" ""
				(at 5.08 -1.905 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "NPN transistor, base/collector/emitter pin order"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "Q_NPN_BCE_0_1"
				(polyline
					(pts
						(xy 0.635 0.635) (xy 2.54 2.54)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0.635 -0.635) (xy 2.54 -2.54)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0.635 1.905) (xy 0.635 -1.905)
					)
					(stroke
						(width 0.508)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 1.27 -1.27) (xy 1.778 -1.524) (xy 1.524 -2.032) (xy 1.27 -1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type outline)
					)
				)
				(circle
					(center 1.27 0)
					(radius 2.8194)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "Q_NPN_BCE_1_1"
				(pin passive line
					(at -2.54 0 0)
					(length 3.175)
					(name "B"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 2.54 5.08 270)
					(length 2.54)
					(name "C"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 2.54 -5.08 90)
					(length 2.54)
					(name "E"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "3"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)"""

_LIB_SYMBOL_SW = """
		(symbol "Switch:SW_Push"
			(pin_names
				(offset 1.016)
				(hide yes)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "SW"
				(at 1.27 2.54 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "SW_Push"
				(at 0 -1.524 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Push button switch"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "SW_Push_0_1"
				(circle
					(center -2.032 0)
					(radius 0.508)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0 1.27) (xy 0 3.048)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 2.54 1.27) (xy -2.54 1.27)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(circle
					(center 2.032 0)
					(radius 0.508)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(pin passive line
					(at -5.08 0 0)
					(length 2.54)
					(name "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 5.08 0 180)
					(length 2.54)
					(name "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)"""

_LIB_SYMBOL_FUSE = """
		(symbol "Device:Fuse"
			(pin_numbers
				(hide yes)
			)
			(pin_names
				(offset 0)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(property "Reference" "F"
				(at 2.032 0 90)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "Fuse"
				(at 0 0 90)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" ""
				(at -1.778 0 90)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Datasheet" "~"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(property "Description" "Fuse"
				(at 0 0 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(hide yes)
				)
			)
			(symbol "Fuse_0_1"
				(rectangle
					(start -0.762 -2.54)
					(end 0.762 2.54)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type none)
					)
				)
				(polyline
					(pts
						(xy 0 2.54) (xy 0 -2.54)
					)
					(stroke
						(width 0)
						(type default)
					)
					(fill
						(type none)
					)
				)
			)
			(symbol "Fuse_1_1"
				(pin passive line
					(at 0 3.81 270)
					(length 1.27)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -3.81 90)
					(length 1.27)
					(name "~"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
			(embedded_fonts no)
		)"""


def _generic_ic_lib_symbol(lib_id: str, pin_count: int, ref_prefix: str = "U") -> str:
    """Gera lib_symbol generico para IC com N pinos (retangulo + pinos)."""
    half = pin_count // 2
    body_h = max(half * 2.54, 5.08)
    body_w = 7.62

    lines = [f'\t\t(symbol "{lib_id}"']
    lines.append('\t\t\t(pin_names\n\t\t\t\t(offset 1.016)\n\t\t\t)')
    lines.append('\t\t\t(exclude_from_sim no)\n\t\t\t(in_bom yes)\n\t\t\t(on_board yes)')
    lines.append(f'\t\t\t(property "Reference" "{ref_prefix}"\n'
                 f'\t\t\t\t(at 0 {body_h + 1.27:.2f} 0)\n'
                 '\t\t\t\t(effects\n\t\t\t\t\t(font\n\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)')
    lines.append(f'\t\t\t(property "Value" "{lib_id.split(":")[-1]}"\n'
                 f'\t\t\t\t(at 0 {-body_h - 1.27:.2f} 0)\n'
                 '\t\t\t\t(effects\n\t\t\t\t\t(font\n\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)')
    lines.append('\t\t\t(property "Footprint" ""\n\t\t\t\t(at 0 0 0)\n'
                 '\t\t\t\t(effects\n\t\t\t\t\t(font\n\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t)\n\t\t\t\t\t(hide yes)\n\t\t\t\t)\n\t\t\t)')
    lines.append('\t\t\t(property "Datasheet" "~"\n\t\t\t\t(at 0 0 0)\n'
                 '\t\t\t\t(effects\n\t\t\t\t\t(font\n\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t)\n\t\t\t\t\t(hide yes)\n\t\t\t\t)\n\t\t\t)')
    lines.append('\t\t\t(property "Description" "Generic IC"\n\t\t\t\t(at 0 0 0)\n'
                 '\t\t\t\t(effects\n\t\t\t\t\t(font\n\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t)\n\t\t\t\t\t(hide yes)\n\t\t\t\t)\n\t\t\t)')

    # Body rectangle
    lines.append(f'\t\t\t(symbol "{lib_id.split(":")[-1]}_0_1"')
    lines.append(f'\t\t\t\t(rectangle\n\t\t\t\t\t(start {-body_w / 2:.2f} {-body_h:.2f})\n'
                 f'\t\t\t\t\t(end {body_w / 2:.2f} {body_h:.2f})\n'
                 '\t\t\t\t\t(stroke\n\t\t\t\t\t\t(width 0.254)\n\t\t\t\t\t\t(type default)\n\t\t\t\t\t)\n'
                 '\t\t\t\t\t(fill\n\t\t\t\t\t\t(type background)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)')

    # Pins
    lines.append(f'\t\t\t(symbol "{lib_id.split(":")[-1]}_1_1"')
    for i in range(pin_count):
        pin_num = str(i + 1)
        if i < half:
            # Left side pins
            py = body_h - 2.54 * (i + 0.5)
            lines.append(f'\t\t\t\t(pin passive line\n'
                         f'\t\t\t\t\t(at {-body_w / 2 - 5.08:.2f} {py:.2f} 0)\n'
                         f'\t\t\t\t\t(length 5.08)\n'
                         f'\t\t\t\t\t(name "{pin_num}"\n'
                         '\t\t\t\t\t\t(effects\n\t\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t\t)\n\t\t\t\t\t\t)\n'
                         f'\t\t\t\t\t)\n\t\t\t\t\t(number "{pin_num}"\n'
                         '\t\t\t\t\t\t(effects\n\t\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t\t)\n\t\t\t\t\t\t)\n'
                         '\t\t\t\t\t)\n\t\t\t\t)')
        else:
            # Right side pins (bottom-up, mirrored DIP style)
            j = i - half
            py = -body_h + 2.54 * (j + 0.5)
            lines.append(f'\t\t\t\t(pin passive line\n'
                         f'\t\t\t\t\t(at {body_w / 2 + 5.08:.2f} {py:.2f} 180)\n'
                         f'\t\t\t\t\t(length 5.08)\n'
                         f'\t\t\t\t\t(name "{pin_num}"\n'
                         '\t\t\t\t\t\t(effects\n\t\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t\t)\n\t\t\t\t\t\t)\n'
                         f'\t\t\t\t\t)\n\t\t\t\t\t(number "{pin_num}"\n'
                         '\t\t\t\t\t\t(effects\n\t\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t\t)\n\t\t\t\t\t\t)\n'
                         '\t\t\t\t\t)\n\t\t\t\t)')

    lines.append('\t\t\t)\n\t\t\t(embedded_fonts no)\n\t\t)')
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Component type detection + pin geometry
# ---------------------------------------------------------------------------

# Maps ref prefix → (lib_id, pin endpoint positions relative to symbol origin)
# Pin positions: {pin_number: (x, y)} — where net label should be placed

_TWO_PIN_VERTICAL = {"1": (0.0, 3.81), "2": (0.0, -3.81)}
_TWO_PIN_HORIZONTAL = {"1": (-3.81, 0.0), "2": (3.81, 0.0)}

_KNOWN_SYMBOLS: dict[str, tuple[str, str, dict[str, tuple[float, float]]]] = {
    "R":   ("Device:R",           _LIB_SYMBOL_R,     _TWO_PIN_VERTICAL),
    "C":   ("Device:C",           _LIB_SYMBOL_C,     _TWO_PIN_VERTICAL),
    "F":   ("Device:Fuse",        _LIB_SYMBOL_FUSE,  _TWO_PIN_VERTICAL),
    "D":   ("Device:D",           _LIB_SYMBOL_D,     _TWO_PIN_HORIZONTAL),
    "LED": ("Device:LED",         _LIB_SYMBOL_LED,   _TWO_PIN_HORIZONTAL),
    "Q":   ("Device:Q_NPN_BCE",   _LIB_SYMBOL_Q_NPN,
            {"1": (-2.54, 0.0), "2": (2.54, 5.08), "3": (2.54, -5.08)}),
    "SW":  ("Switch:SW_Push",     _LIB_SYMBOL_SW,    _TWO_PIN_HORIZONTAL),
}


def _detect_type(ref: str) -> str:
    """Detecta tipo do componente pelo prefixo da referencia."""
    # Tenta prefixos mais longos primeiro (LED antes de L)
    for prefix in sorted(_KNOWN_SYMBOLS.keys(), key=len, reverse=True):
        if ref.upper().startswith(prefix):
            return prefix
    return "U"  # default: IC generico


def _get_symbol_info(
    comp: dict,
) -> tuple[str, str | None, dict[str, tuple[float, float]]]:
    """Retorna (lib_id, lib_symbol_def_or_None, pin_positions) para um componente."""
    comp_type = _detect_type(comp["ref"])

    if comp_type in _KNOWN_SYMBOLS:
        lib_id, lib_def, pin_pos = _KNOWN_SYMBOLS[comp_type]
        return lib_id, lib_def, pin_pos

    # IC generico: gerar dinamicamente
    pin_count = len(comp.get("pins", {}))
    if pin_count < 2:
        pin_count = 2
    # Round up to even
    if pin_count % 2 != 0:
        pin_count += 1

    lib_id = f"Autoplacer:{comp.get('value', 'IC')}"
    lib_def = _generic_ic_lib_symbol(lib_id, pin_count, ref_prefix=comp["ref"].rstrip("0123456789"))

    half = pin_count // 2
    body_h = max(half * 2.54, 5.08)
    body_w = 7.62
    pin_pos = {}
    for i in range(pin_count):
        pin_num = str(i + 1)
        if i < half:
            py = body_h - 2.54 * (i + 0.5)
            pin_pos[pin_num] = (-body_w / 2 - 5.08, py)
        else:
            j = i - half
            py = -body_h + 2.54 * (j + 0.5)
            pin_pos[pin_num] = (body_w / 2 + 5.08, py)

    return lib_id, lib_def, pin_pos


# ---------------------------------------------------------------------------
# Grid layout
# ---------------------------------------------------------------------------

_GRID = 2.54  # KiCad schematic grid (100mil = 2.54mm)
_COMP_SPACING_X = 30.0 * _GRID  # ~76mm between columns
_COMP_SPACING_Y = 15.0 * _GRID  # ~38mm between rows
_COLS = 4  # components per row


# ---------------------------------------------------------------------------
# Schematic generation
# ---------------------------------------------------------------------------

def generate_schematic(
    components: list[dict],
    output_path: Path,
    project: str = "sketch",
) -> Path:
    """Gera um arquivo .kicad_sch a partir de componentes JSON.

    Posiciona simbolos em grid e conecta com net labels.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    root_uuid = _uuid()

    # Collect lib_symbols and component info
    lib_symbols_used: dict[str, str] = {}  # lib_id → definition string
    comp_infos: list[tuple[dict, str, dict[str, tuple[float, float]]]] = []

    for comp in components:
        lib_id, lib_def, pin_pos = _get_symbol_info(comp)
        if lib_id not in lib_symbols_used and lib_def is not None:
            lib_symbols_used[lib_id] = lib_def
        comp_infos.append((comp, lib_id, pin_pos))

    # Build schematic text
    lines: list[str] = []
    lines.append('(kicad_sch')
    lines.append('\t(version 20250114)')
    lines.append('\t(generator "pcb-autoplacer")')
    lines.append('\t(generator_version "1.0")')
    lines.append(f'\t(uuid "{root_uuid}")')
    lines.append('\t(paper "A3")')

    # lib_symbols
    lines.append('\t(lib_symbols')
    for lib_def in lib_symbols_used.values():
        lines.append(lib_def)
    lines.append('\t)')

    # Place symbols on grid and collect net label positions
    net_labels: list[tuple[float, float, str]] = []  # (x, y, net_name)
    start_x = 40.0  # mm from left edge
    start_y = 40.0  # mm from top

    for idx, (comp, lib_id, pin_pos) in enumerate(comp_infos):
        col = idx % _COLS
        row = idx // _COLS
        cx = start_x + col * _COMP_SPACING_X
        cy = start_y + row * _COMP_SPACING_Y

        sym_uuid = _uuid()
        lines.append('\t(symbol')
        lines.append(f'\t\t(lib_id "{lib_id}")')
        lines.append(f'\t\t(at {cx:.2f} {cy:.2f} 0)')
        lines.append('\t\t(unit 1)')
        lines.append('\t\t(exclude_from_sim no)')
        lines.append('\t\t(in_bom yes)')
        lines.append('\t\t(on_board yes)')
        lines.append('\t\t(dnp no)')
        lines.append('\t\t(fields_autoplaced yes)')
        lines.append(f'\t\t(uuid "{sym_uuid}")')

        # Properties
        lines.append(f'\t\t(property "Reference" "{comp["ref"]}"')
        lines.append(f'\t\t\t(at {cx:.2f} {cy - 5.08:.2f} 0)')
        lines.append('\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)')

        lines.append(f'\t\t(property "Value" "{comp.get("value", "")}"')
        lines.append(f'\t\t\t(at {cx:.2f} {cy + 5.08:.2f} 0)')
        lines.append('\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)')

        lines.append(f'\t\t(property "Footprint" "{comp["footprint"]}"')
        lines.append(f'\t\t\t(at {cx:.2f} {cy:.2f} 0)')
        lines.append('\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(hide yes)\n\t\t\t)\n\t\t)')

        lines.append('\t\t(property "Datasheet" "~"')
        lines.append(f'\t\t\t(at {cx:.2f} {cy:.2f} 0)')
        lines.append('\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(hide yes)\n\t\t\t)\n\t\t)')

        lines.append('\t\t(property "Description" ""')
        lines.append(f'\t\t\t(at {cx:.2f} {cy:.2f} 0)')
        lines.append('\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(hide yes)\n\t\t\t)\n\t\t)')

        # Pin UUIDs
        pins = comp.get("pins", {})
        for pin_num in sorted(pins.keys(), key=lambda p: int(p) if p.isdigit() else 0):
            lines.append(f'\t\t(pin "{pin_num}"\n\t\t\t(uuid "{_uuid()}")\n\t\t)')

        # Instances
        lines.append(f'\t\t(instances\n\t\t\t(project "{project}"')
        lines.append(f'\t\t\t\t(path "/{root_uuid}"\n\t\t\t\t\t(reference "{comp["ref"]}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)')
        lines.append('\t)')

        # Collect net labels for this component's pins
        for pin_num, net_name in pins.items():
            if pin_num in pin_pos:
                px, py = pin_pos[pin_num]
                label_x = cx + px
                label_y = cy + py
                net_labels.append((label_x, label_y, net_name))

    # Net labels
    for lx, ly, net_name in net_labels:
        lines.append(f'\t(net_label "{net_name}"')
        lines.append(f'\t\t(at {lx:.2f} {ly:.2f} 0)')
        lines.append('\t\t(fields_autoplaced yes)')
        lines.append(f'\t\t(uuid "{_uuid()}")')
        lines.append('\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)')
        lines.append('\t)')

    # Sheet instances
    lines.append(f'\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)')
    lines.append(')')

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
