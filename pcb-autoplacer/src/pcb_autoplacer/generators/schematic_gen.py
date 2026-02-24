#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gerador de esquematicos KiCad 9 a partir de descricao estruturada.

Extraido e generalizado do generate_consul_schematic.py.
Suporta: resistor, capacitor, optocoupler, diode, IC generico, power, wire, glabel, text.
"""

import uuid


def uid():
    return str(uuid.uuid4())


# ── KiCad 9 lib_symbols embutidos ─────────────────────────────────────

LIB_SYMBOLS_REGISTRY = {
    "Device:R": """
    (symbol "Device:R"
      (pin_numbers hide)
      (pin_names (offset 0))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "R"
        (at 2.032 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "R"
        (at 0 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" ""
        (at -1.778 0 90)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" "~"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (symbol "R_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54)
          (stroke (width 0) (type default))
          (fill (type none))
        )
      )
      (symbol "R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 0 -3.81 90) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    )""",

    "Device:C": """
    (symbol "Device:C"
      (pin_numbers hide)
      (pin_names (offset 0.254))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "C"
        (at 0.635 2.54 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )
      (property "Value" "C"
        (at 0.635 -2.54 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )
      (property "Footprint" ""
        (at 0.9652 -3.81 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" "~"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (symbol "C_0_1"
        (polyline
          (pts (xy -2.032 -0.762) (xy 2.032 -0.762))
          (stroke (width 0.508) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy -2.032 0.762) (xy 2.032 0.762))
          (stroke (width 0.508) (type default))
          (fill (type none))
        )
      )
      (symbol "C_1_1"
        (pin passive line (at 0 3.81 270) (length 2.794)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 0 -3.81 90) (length 2.794)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    )""",

    "Device:D": """
    (symbol "Device:D"
      (pin_numbers hide)
      (pin_names (offset 1.016) hide)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "D"
        (at 0 2.54 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "D"
        (at 0 -2.54 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" "~"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (symbol "D_0_1"
        (polyline
          (pts (xy -1.27 1.27) (xy -1.27 -1.27))
          (stroke (width 0.254) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 1.27 0) (xy -1.27 0))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 1.27 1.27) (xy 1.27 -1.27) (xy -1.27 0) (xy 1.27 1.27))
          (stroke (width 0.254) (type default))
          (fill (type none))
        )
      )
      (symbol "D_1_1"
        (pin passive line (at -3.81 0 0) (length 2.54)
          (name "K" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 3.81 0 180) (length 2.54)
          (name "A" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    )""",

    "Device:LED": """
    (symbol "Device:LED"
      (pin_numbers hide)
      (pin_names (offset 1.016) hide)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "D"
        (at 0 2.54 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "LED"
        (at 0 -2.54 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" "~"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (symbol "LED_0_1"
        (polyline
          (pts (xy -1.27 -1.27) (xy -1.27 1.27))
          (stroke (width 0.254) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy -1.27 0) (xy 1.27 0))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27))
          (stroke (width 0.254) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy -3.048 -0.762) (xy -4.572 -2.286))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy -1.778 -0.762) (xy -3.302 -2.286))
          (stroke (width 0) (type default))
          (fill (type none))
        )
      )
      (symbol "LED_1_1"
        (pin passive line (at -3.81 0 0) (length 2.54)
          (name "K" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 3.81 0 180) (length 2.54)
          (name "A" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    )""",

    "Isolator:PC817": """
    (symbol "Isolator:PC817"
      (pin_names (offset 1.016))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "U"
        (at -3.81 6.35 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )
      (property "Value" "PC817"
        (at -3.81 -6.35 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )
      (property "Footprint" "Package_DIP:DIP-4_W7.62mm"
        (at -3.81 -8.89 0)
        (effects (font (size 1.27 1.27) (italic yes)) (justify left) (hide yes))
      )
      (property "Datasheet" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (symbol "PC817_0_1"
        (rectangle (start -3.81 5.08) (end 3.81 -5.08)
          (stroke (width 0.254) (type default))
          (fill (type background))
        )
        (polyline
          (pts (xy -2.286 -1.27) (xy -1.27 -1.27) (xy -1.27 1.27) (xy -0.254 1.27))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy -0.254 -1.27) (xy -2.286 -1.27))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy -0.254 -1.27) (xy -0.254 1.27))
          (stroke (width 0.254) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 0.508 -0.762) (xy 0.508 -2.286))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 0.762 0.508) (xy 1.524 1.016))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 0.762 1.524) (xy 1.524 2.032))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 2.286 -2.54) (xy 0.508 -2.286) (xy 0.762 -1.524))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 0.508 2.286) (xy 0.508 0.762) (xy 2.286 2.54))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 1.524 1.016) (xy 1.016 1.016) (xy 1.27 1.524) (xy 1.524 1.016))
          (stroke (width 0) (type default))
          (fill (type outline))
        )
        (polyline
          (pts (xy 1.524 2.032) (xy 1.016 2.032) (xy 1.27 2.54) (xy 1.524 2.032))
          (stroke (width 0) (type default))
          (fill (type outline))
        )
      )
      (symbol "PC817_1_1"
        (pin passive line (at -6.35 2.54 0) (length 2.54)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at -6.35 -2.54 0) (length 2.54)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 6.35 -2.54 180) (length 2.54)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "3" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 6.35 2.54 180) (length 2.54)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "4" (effects (font (size 1.27 1.27))))
        )
      )
    )""",
}

# Power symbols (generated on demand)
POWER_SYMBOL_TEMPLATE = {
    "supply": """
    (symbol "power:{name}"
      (power)
      (pin_names (offset 0))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "#PWR"
        (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Value" "{name}"
        (at 0 3.556 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (symbol "{name}_0_1"
        (polyline
          (pts (xy -0.762 1.27) (xy 0 2.54))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 0 0) (xy 0 2.54))
          (stroke (width 0) (type default))
          (fill (type none))
        )
        (polyline
          (pts (xy 0 2.54) (xy 0.762 1.27))
          (stroke (width 0) (type default))
          (fill (type none))
        )
      )
      (symbol "{name}_1_1"
        (pin power_in line (at 0 0 90) (length 0)
          (name "{name}" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
      )
    )""",

    "GND": """
    (symbol "power:GND"
      (power)
      (pin_names (offset 0))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "#PWR"
        (at 0 -6.35 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Value" "GND"
        (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (symbol "GND_0_1"
        (polyline
          (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
          (stroke (width 0) (type default))
          (fill (type none))
        )
      )
      (symbol "GND_1_1"
        (pin power_in line (at 0 0 270) (length 0)
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
      )
    )""",
}


class SchematicBuilder:
    """Constroi esquematico KiCad 9 com layout limpo e legivel.

    Uso generico — aceita componentes via metodos individuais ou via dict.
    """

    def __init__(self):
        self.elements = []
        self.pwr_num = 1
        self.instances = []
        self.used_libs = set()      # lib_ids usados (para gerar lib_symbols)
        self.used_powers = set()    # power names usados
        self.root_uuid = uid()

    def _track_instance(self, sym_uuid, ref):
        self.instances.append((sym_uuid, ref))

    def resistor(self, ref, value, x, y, angle=0, footprint="Resistor_SMD:R_0805_2012Metric"):
        """Resistor com labels afastados e legiveis."""
        u = uid()
        self._track_instance(u, ref)
        self.used_libs.add("Device:R")

        if angle == 0:  # vertical
            rx, ry = x - 5, y
            vx, vy = x + 5, y
        else:  # 90 = horizontal
            rx, ry = x, y - 4.5
            vx, vy = x, y + 4.5

        self.elements.append(f"""
    (symbol
      (lib_id "Device:R")
      (at {x} {y} {angle})
      (unit 1)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (dnp no)
      (uuid "{u}")
      (property "Reference" "{ref}"
        (at {rx} {ry} 0)
        (effects (font (size 1.4 1.4)))
      )
      (property "Value" "{value}"
        (at {vx} {vy} 0)
        (effects (font (size 1.4 1.4)))
      )
      (property "Footprint" "{footprint}"
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{self.root_uuid}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")
        return u

    def capacitor(self, ref, value, x, y, footprint="Capacitor_SMD:C_0805_2012Metric"):
        """Capacitor vertical com labels a direita."""
        u = uid()
        self._track_instance(u, ref)
        self.used_libs.add("Device:C")

        self.elements.append(f"""
    (symbol
      (lib_id "Device:C")
      (at {x} {y} 0)
      (unit 1)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (dnp no)
      (uuid "{u}")
      (property "Reference" "{ref}"
        (at {x + 5} {y - 2} 0)
        (effects (font (size 1.4 1.4)) (justify left))
      )
      (property "Value" "{value}"
        (at {x + 5} {y + 2} 0)
        (effects (font (size 1.4 1.4)) (justify left))
      )
      (property "Footprint" "{footprint}"
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{self.root_uuid}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")
        return u

    def diode(self, ref, value, x, y, angle=0, footprint="Diode_SMD:D_SOD-123"):
        """Diodo generico (Device:D)."""
        u = uid()
        self._track_instance(u, ref)
        self.used_libs.add("Device:D")

        self.elements.append(f"""
    (symbol
      (lib_id "Device:D")
      (at {x} {y} {angle})
      (unit 1)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (dnp no)
      (uuid "{u}")
      (property "Reference" "{ref}"
        (at {x} {y - 4} 0)
        (effects (font (size 1.4 1.4)))
      )
      (property "Value" "{value}"
        (at {x} {y + 4} 0)
        (effects (font (size 1.4 1.4)))
      )
      (property "Footprint" "{footprint}"
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{self.root_uuid}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")
        return u

    def led(self, ref, value, x, y, angle=0, footprint="LED_SMD:LED_0805_2012Metric"):
        """LED (Device:LED)."""
        u = uid()
        self._track_instance(u, ref)
        self.used_libs.add("Device:LED")

        self.elements.append(f"""
    (symbol
      (lib_id "Device:LED")
      (at {x} {y} {angle})
      (unit 1)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (dnp no)
      (uuid "{u}")
      (property "Reference" "{ref}"
        (at {x} {y - 4} 0)
        (effects (font (size 1.4 1.4)))
      )
      (property "Value" "{value}"
        (at {x} {y + 4} 0)
        (effects (font (size 1.4 1.4)))
      )
      (property "Footprint" "{footprint}"
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{self.root_uuid}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")
        return u

    def optocoupler(self, ref, value, x, y, footprint="Package_DIP:DIP-4_W7.62mm"):
        """PC817 com labels acima e abaixo."""
        u = uid()
        self._track_instance(u, ref)
        self.used_libs.add("Isolator:PC817")

        self.elements.append(f"""
    (symbol
      (lib_id "Isolator:PC817")
      (at {x} {y} 0)
      (unit 1)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (dnp no)
      (uuid "{u}")
      (property "Reference" "{ref}"
        (at {x} {y - 9} 0)
        (effects (font (size 1.6 1.6)))
      )
      (property "Value" "{value}"
        (at {x} {y + 9} 0)
        (effects (font (size 1.6 1.6)))
      )
      (property "Footprint" "{footprint}"
        (at {x} {y + 12} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{self.root_uuid}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")
        pins = {
            "anode":     (x - 6.35, y - 2.54),
            "cathode":   (x - 6.35, y + 2.54),
            "emitter":   (x + 6.35, y + 2.54),
            "collector": (x + 6.35, y - 2.54),
        }
        return pins

    def ic(self, ref, lib_id, value, x, y, footprint, pins_map=None, angle=0):
        """IC generico — qualquer simbolo KiCad.

        pins_map: dict opcional {pin_name: (abs_x, abs_y)} para retornar posicoes.
        NOTA: lib_symbol para ICs custom deve ser adicionado manualmente via add_lib_symbol().
        """
        u = uid()
        self._track_instance(u, ref)
        self.used_libs.add(lib_id)

        self.elements.append(f"""
    (symbol
      (lib_id "{lib_id}")
      (at {x} {y} {angle})
      (unit 1)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (dnp no)
      (uuid "{u}")
      (property "Reference" "{ref}"
        (at {x} {y - 9} 0)
        (effects (font (size 1.6 1.6)))
      )
      (property "Value" "{value}"
        (at {x} {y + 9} 0)
        (effects (font (size 1.6 1.6)))
      )
      (property "Footprint" "{footprint}"
        (at {x} {y + 12} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{self.root_uuid}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")
        return pins_map or u

    def power(self, name, x, y):
        """Simbolo de alimentacao (+3V3, +5V, GND, +12V, etc)."""
        u = uid()
        ref = f"#PWR{self.pwr_num:02d}"
        self.pwr_num += 1
        self._track_instance(u, ref)
        self.used_powers.add(name)

        val_y = y - 2.5 if name != "GND" else y + 4

        self.elements.append(f"""
    (symbol
      (lib_id "power:{name}")
      (at {x} {y} 0)
      (unit 1)
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (dnp no)
      (uuid "{u}")
      (property "Reference" "{ref}"
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Value" "{name}"
        (at {x} {val_y} 0)
        (effects (font (size 1.4 1.4)))
      )
      (property "Footprint" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{self.root_uuid}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")

    def wire(self, x1, y1, x2, y2):
        self.elements.append(f"""
    (wire
      (pts (xy {x1} {y1}) (xy {x2} {y2}))
      (stroke (width 0) (type default))
      (uuid "{uid()}")
    )""")

    def junction(self, x, y):
        self.elements.append(f"""
    (junction (at {x} {y}) (diameter 0) (color 0 0 0 0)
      (uuid "{uid()}")
    )""")

    def glabel(self, text, x, y, angle=0, shape="input"):
        self.elements.append(f"""
    (global_label "{text}"
      (shape {shape})
      (at {x} {y} {angle})
      (effects (font (size 1.4 1.4)))
      (uuid "{uid()}")
      (property "Intersheetrefs" "${{INTERSHEET_REFS}}"
        (at 0 0 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
    )""")

    def text(self, content, x, y, size=2.0):
        self.elements.append(f"""
    (text "{content}"
      (exclude_from_sim no)
      (at {x} {y} 0)
      (effects (font (size {size} {size})))
      (uuid "{uid()}")
    )""")

    def add_lib_symbol(self, lib_id, sexpr):
        """Registra lib_symbol custom (para ICs que nao estao no registry)."""
        LIB_SYMBOLS_REGISTRY[lib_id] = sexpr
        self.used_libs.add(lib_id)

    def get_elements(self):
        return "\n".join(self.elements)

    def get_lib_symbols(self):
        """Gera bloco (lib_symbols ...) apenas com simbolos usados."""
        parts = []
        for lib_id in sorted(self.used_libs):
            if lib_id in LIB_SYMBOLS_REGISTRY:
                parts.append(LIB_SYMBOLS_REGISTRY[lib_id])

        for pwr_name in sorted(self.used_powers):
            if pwr_name == "GND":
                parts.append(POWER_SYMBOL_TEMPLATE["GND"])
            else:
                parts.append(POWER_SYMBOL_TEMPLATE["supply"].replace("{name}", pwr_name))

        return f"""  (lib_symbols\n{"".join(parts)}\n  )"""

    def get_sheet_instances(self):
        return """
  (sheet_instances
    (path "/"
      (page "1")
    )
  )"""

    def to_kicad_sch(self, generator_name="schematic_gen"):
        """Gera o arquivo .kicad_sch completo como string."""
        return f"""(kicad_sch
  (version 20231120)
  (generator "{generator_name}")
  (generator_version "1.0")
  (uuid "{self.root_uuid}")
  (paper "A4")
{self.get_lib_symbols()}
{self.get_elements()}
{self.get_sheet_instances()}
)"""

    def save(self, output_path, generator_name="schematic_gen"):
        """Salva o esquematico em arquivo."""
        content = self.to_kicad_sch(generator_name)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path


def build_from_dict(circuit_desc):
    """Constroi esquematico a partir de descricao estruturada (dict/JSON).

    Formato esperado:
    {
        "components": [
            {"type": "resistor", "ref": "R1", "value": "10k", "x": 100, "y": 50, "angle": 0},
            {"type": "capacitor", "ref": "C1", "value": "100nF", "x": 120, "y": 50},
            {"type": "diode", "ref": "D1", "value": "1N4148", "x": 140, "y": 50},
            {"type": "led", "ref": "D2", "value": "RED", "x": 140, "y": 70},
            {"type": "optocoupler", "ref": "U1", "value": "PC817", "x": 160, "y": 50},
            {"type": "ic", "ref": "U2", "value": "NE555", "x": 180, "y": 50,
             "lib_id": "Timer:NE555", "footprint": "Package_DIP:DIP-8_W7.62mm"},
        ],
        "connections": [
            {"from": [100, 50], "to": [120, 50]},
        ],
        "power_rails": [
            {"name": "+5V", "x": 100, "y": 40},
            {"name": "GND", "x": 100, "y": 60},
        ],
        "labels": [
            {"text": "INPUT", "x": 80, "y": 50, "angle": 180, "shape": "input"},
        ],
        "notes": "Circuito de teste"
    }
    """
    s = SchematicBuilder()

    # Component dispatch table
    comp_methods = {
        "resistor": lambda c: s.resistor(
            c["ref"], c["value"], c["x"], c["y"],
            angle=c.get("angle", 0),
            footprint=c.get("footprint", "Resistor_SMD:R_0805_2012Metric"),
        ),
        "capacitor": lambda c: s.capacitor(
            c["ref"], c["value"], c["x"], c["y"],
            footprint=c.get("footprint", "Capacitor_SMD:C_0805_2012Metric"),
        ),
        "diode": lambda c: s.diode(
            c["ref"], c["value"], c["x"], c["y"],
            angle=c.get("angle", 0),
            footprint=c.get("footprint", "Diode_SMD:D_SOD-123"),
        ),
        "led": lambda c: s.led(
            c["ref"], c["value"], c["x"], c["y"],
            angle=c.get("angle", 0),
            footprint=c.get("footprint", "LED_SMD:LED_0805_2012Metric"),
        ),
        "optocoupler": lambda c: s.optocoupler(
            c["ref"], c["value"], c["x"], c["y"],
            footprint=c.get("footprint", "Package_DIP:DIP-4_W7.62mm"),
        ),
        "ic": lambda c: s.ic(
            c["ref"], c["lib_id"], c["value"], c["x"], c["y"],
            footprint=c["footprint"],
            angle=c.get("angle", 0),
        ),
    }

    # Place components
    for comp in circuit_desc.get("components", []):
        ctype = comp.get("type", "").lower()
        if ctype in comp_methods:
            comp_methods[ctype](comp)
        else:
            print(f"  WARNING: tipo desconhecido '{ctype}' para {comp.get('ref', '?')}")

    # Draw wires
    for conn in circuit_desc.get("connections", []):
        pts = conn.get("from", conn.get("points", []))
        end = conn.get("to")
        if pts and end:
            s.wire(pts[0], pts[1], end[0], end[1])
        elif "points" in conn:
            # Multi-point wire: list of [x, y] pairs
            points = conn["points"]
            for i in range(len(points) - 1):
                s.wire(points[i][0], points[i][1], points[i+1][0], points[i+1][1])

    # Place power rails
    for pwr in circuit_desc.get("power_rails", []):
        s.power(pwr["name"], pwr["x"], pwr["y"])

    # Place labels
    for lbl in circuit_desc.get("labels", []):
        s.glabel(
            lbl["text"], lbl["x"], lbl["y"],
            angle=lbl.get("angle", 0),
            shape=lbl.get("shape", "input"),
        )

    # Place junctions
    for junc in circuit_desc.get("junctions", []):
        s.junction(junc["x"], junc["y"])

    # Title text
    if circuit_desc.get("notes"):
        s.text(circuit_desc["notes"], 60, 180, 2.5)

    return s
