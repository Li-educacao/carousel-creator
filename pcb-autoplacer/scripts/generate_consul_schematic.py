#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera esquematico KiCad 9 do circuito de comunicacao Consul 12k/18k.

Circuito de isolacao galvanica entre uC SMD (3.3V) e uC DIP (5V)
usando dois optoacopladores (ISO802 e ISO801).
"""

import os
import uuid


ROOT_UUID = str(uuid.uuid4())


def uid():
    return str(uuid.uuid4())


# ── KiCad 9 S-expression builders ────────────────────────────────────

class SchematicBuilder:
    """Constroi esquematico KiCad 9 com layout limpo e legivel."""

    def __init__(self):
        self.elements = []
        self.pwr_num = 1
        self.instances = []  # (uuid, reference) para section final

    def _track_instance(self, sym_uuid, ref):
        self.instances.append((sym_uuid, ref))

    def resistor(self, ref, value, x, y, angle=0):
        """Resistor com labels afastados e legiveis."""
        u = uid()
        self._track_instance(u, ref)

        if angle == 0:  # vertical
            rx, ry = x - 5, y      # ref a esquerda
            vx, vy = x + 5, y      # value a direita
        else:  # 90 = horizontal
            rx, ry = x, y - 4.5    # ref acima
            vx, vy = x, y + 4.5    # value abaixo

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
      (property "Footprint" "Resistor_SMD:R_0805_2012Metric"
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{ROOT_UUID}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")
        return u

    def capacitor(self, ref, value, x, y):
        """Capacitor vertical com labels a direita."""
        u = uid()
        self._track_instance(u, ref)

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
      (property "Footprint" "Capacitor_SMD:C_0805_2012Metric"
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{ROOT_UUID}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")
        return u

    def optocoupler(self, ref, value, x, y):
        """PC817 com labels acima e abaixo, bem afastados."""
        u = uid()
        self._track_instance(u, ref)

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
      (property "Footprint" "Package_DIP:DIP-4_W7.62mm"
        (at {x} {y + 12} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Datasheet" ""
        (at {x} {y} 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (instances
        (project ""
          (path "/{ROOT_UUID}"
            (reference "{ref}")
            (unit 1)
          )
        )
      )
    )""")
        # Pin positions (absolute)
        pins = {
            "anode":     (x - 6.35, y - 2.54),  # pin 1
            "cathode":   (x - 6.35, y + 2.54),  # pin 2
            "emitter":   (x + 6.35, y + 2.54),  # pin 3
            "collector": (x + 6.35, y - 2.54),  # pin 4
        }
        return pins

    def power(self, name, x, y):
        """Simbolo de alimentacao (+3V3, +5V, GND)."""
        u = uid()
        ref = f"#PWR{self.pwr_num:02d}"
        self.pwr_num += 1
        self._track_instance(u, ref)

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
          (path "/{ROOT_UUID}"
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

    def get_elements(self):
        return "\n".join(self.elements)

    def get_sheet_instances(self):
        return f"""
  (sheet_instances
    (path "/"
      (page "1")
    )
  )"""


# ── Esquematico principal ────────────────────────────────────────────

def build():
    s = SchematicBuilder()

    # ══════════════════════════════════════════════════════════════════
    #  CANAL 1 — ISO802: uC SMD Pin19 (TX) --> uC DIP Pin20 (RX)
    # ══════════════════════════════════════════════════════════════════
    #
    #            +3.3V                              +5V
    #              |                                  |
    #            [R671]                             [R821]
    #            390R                               4.7k
    #              |                                  |
    #  uC_SMD_19 --+---[R672 2k]---pin1    pin4------+---[R820 100R]---uC_DIP_20
    #                               |        |       |
    #                              LED      COLL    [C1]
    #                               |        |       |
    #                             pin2     pin3------+
    #                               |        |
    #                              GND      GND
    #
    # ══════════════════════════════════════════════════════════════════

    # Constantes de posicao — Canal 1
    SIG1_Y = 55         # linha de sinal horizontal
    OPTO1_X = 130       # centro do optoacoplador
    OPTO1_Y = SIG1_Y

    # ── U1 (ISO802) ──
    pins1 = s.optocoupler("U1", "ISO802", OPTO1_X, OPTO1_Y)
    anode1 = pins1["anode"]       # (123.65, 52.46)
    cathode1 = pins1["cathode"]   # (123.65, 57.54)
    emitter1 = pins1["emitter"]   # (136.35, 57.54)
    collector1 = pins1["collector"]  # (136.35, 52.46)

    # ── R672 (2k) horizontal: signal_node → Anode ──
    R672_X = anode1[0] - 16       # 107.65
    R672_Y = anode1[1]            # 52.46
    s.resistor("R672", "2k", R672_X, R672_Y, 90)
    # Fio: R672 pino direito → anode
    s.wire(R672_X + 3.81, R672_Y, anode1[0], anode1[1])

    # Signal node (esquerda do R672)
    SIG1_NODE_X = R672_X - 3.81   # ~103.84
    SIG1_NODE_Y = R672_Y

    # ── R671 (390R) vertical: +3.3V pull-up → signal_node ──
    R671_X = SIG1_NODE_X
    R671_Y = SIG1_NODE_Y - 18     # ~34.46, bem acima
    s.resistor("R671", "390R", R671_X, R671_Y, 0)
    # Fio: R671 pino inferior → signal node
    s.wire(R671_X, R671_Y + 3.81, SIG1_NODE_X, SIG1_NODE_Y)
    # +3.3V no topo do R671
    s.power("+3V3", R671_X, R671_Y - 3.81)

    # Junction no signal node
    s.junction(SIG1_NODE_X, SIG1_NODE_Y)

    # ── Label uC_SMD_Pin19 (far left) ──
    LBL1_X = SIG1_NODE_X - 18
    s.wire(LBL1_X, SIG1_NODE_Y, SIG1_NODE_X, SIG1_NODE_Y)
    s.glabel("uC_SMD_Pin19", LBL1_X, SIG1_NODE_Y, 180, "output")

    # ── Cathode (pin 2) → GND ──
    GND1_Y = cathode1[1] + 8
    s.wire(cathode1[0], cathode1[1], cathode1[0], GND1_Y)
    s.power("GND", cathode1[0], GND1_Y)

    # ── Collector (pin 4) — node de bifurcacao ──
    COLL1_NODE_X = collector1[0] + 8
    COLL1_NODE_Y = collector1[1]
    s.wire(collector1[0], collector1[1], COLL1_NODE_X, COLL1_NODE_Y)
    s.junction(COLL1_NODE_X, COLL1_NODE_Y)

    # ── R821 (4.7k) vertical: +5V pull-up → collector ──
    R821_X = COLL1_NODE_X
    R821_Y = COLL1_NODE_Y - 18
    s.resistor("R821", "4.7k", R821_X, R821_Y, 0)
    s.wire(R821_X, R821_Y + 3.81, COLL1_NODE_X, COLL1_NODE_Y)
    s.power("+5V", R821_X, R821_Y - 3.81)

    # ── R820 (100R) horizontal: collector → uC_DIP_Pin20 ──
    R820_X = COLL1_NODE_X + 18
    R820_Y = COLL1_NODE_Y
    s.resistor("R820", "100R", R820_X, R820_Y, 90)
    s.wire(COLL1_NODE_X, COLL1_NODE_Y, R820_X - 3.81, R820_Y)

    # Label uC_DIP_Pin20 (far right)
    LBL2_X = R820_X + 3.81 + 10
    s.wire(R820_X + 3.81, R820_Y, LBL2_X, R820_Y)
    s.glabel("uC_DIP_Pin20", LBL2_X, R820_Y, 0, "input")

    # ── Emitter (pin 3) → GND ──
    GND2_Y = emitter1[1] + 8
    s.wire(emitter1[0], emitter1[1], emitter1[0], GND2_Y)
    s.power("GND", emitter1[0], GND2_Y)

    # ── C1 (100nF) filtro entre pin 4 (collector) e pin 3 (emitter) ──
    C1_X = COLL1_NODE_X + 8
    C1_Y = OPTO1_Y
    s.capacitor("C1", "100nF", C1_X, C1_Y)
    # Fio coletor → C1 topo
    s.wire(COLL1_NODE_X, COLL1_NODE_Y, C1_X, COLL1_NODE_Y)
    s.wire(C1_X, COLL1_NODE_Y, C1_X, C1_Y - 3.81)
    # Fio emissor → C1 base
    s.wire(emitter1[0], emitter1[1], C1_X, emitter1[1])
    s.wire(C1_X, emitter1[1], C1_X, C1_Y + 3.81)
    s.junction(emitter1[0], emitter1[1])
    s.junction(COLL1_NODE_X, COLL1_NODE_Y)

    # ══════════════════════════════════════════════════════════════════
    #  CANAL 2 — ISO801: uC DIP Pin21 (TX) --> uC SMD Pin18 (RX)
    # ══════════════════════════════════════════════════════════════════
    #
    #              +5V                             +3.3V
    #               |                                |
    #             [R819]                           [R670]
    #             4.7k                             4.7k
    #               |                                |
    #  uC_DIP_21 --+---[R818 390R]--pin1   pin4-----+-------uC_SMD_18
    #                                |       |       |
    #                               LED    COLL    [C670]
    #                                |       |       |
    #                              pin2    pin3------+
    #                                |       |
    #                               GND     GND
    #
    # ══════════════════════════════════════════════════════════════════

    SIG2_Y = 140
    OPTO2_X = 130
    OPTO2_Y = SIG2_Y

    # ── U2 (ISO801) ──
    pins2 = s.optocoupler("U2", "ISO801", OPTO2_X, OPTO2_Y)
    anode2 = pins2["anode"]
    cathode2 = pins2["cathode"]
    emitter2 = pins2["emitter"]
    collector2 = pins2["collector"]

    # ── R818 (390R) horizontal: signal → Anode ──
    R818_X = anode2[0] - 16
    R818_Y = anode2[1]
    s.resistor("R818", "390R", R818_X, R818_Y, 90)
    s.wire(R818_X + 3.81, R818_Y, anode2[0], anode2[1])

    SIG2_NODE_X = R818_X - 3.81
    SIG2_NODE_Y = R818_Y

    # ── R819 (4.7k) vertical: +5V pull-up → signal ──
    R819_X = SIG2_NODE_X
    R819_Y = SIG2_NODE_Y - 18
    s.resistor("R819", "4.7k", R819_X, R819_Y, 0)
    s.wire(R819_X, R819_Y + 3.81, SIG2_NODE_X, SIG2_NODE_Y)
    s.power("+5V", R819_X, R819_Y - 3.81)

    s.junction(SIG2_NODE_X, SIG2_NODE_Y)

    # ── Label uC_DIP_Pin21 ──
    LBL3_X = SIG2_NODE_X - 18
    s.wire(LBL3_X, SIG2_NODE_Y, SIG2_NODE_X, SIG2_NODE_Y)
    s.glabel("uC_DIP_Pin21", LBL3_X, SIG2_NODE_Y, 180, "output")

    # ── Cathode → GND ──
    GND3_Y = cathode2[1] + 8
    s.wire(cathode2[0], cathode2[1], cathode2[0], GND3_Y)
    s.power("GND", cathode2[0], GND3_Y)

    # ── Collector node ──
    COLL2_NODE_X = collector2[0] + 8
    COLL2_NODE_Y = collector2[1]
    s.wire(collector2[0], collector2[1], COLL2_NODE_X, COLL2_NODE_Y)
    s.junction(COLL2_NODE_X, COLL2_NODE_Y)

    # ── R670 (4.7k) vertical: +3.3V → collector ──
    R670_X = COLL2_NODE_X
    R670_Y = COLL2_NODE_Y - 18
    s.resistor("R670", "4.7k", R670_X, R670_Y, 0)
    s.wire(R670_X, R670_Y + 3.81, COLL2_NODE_X, COLL2_NODE_Y)
    s.power("+3V3", R670_X, R670_Y - 3.81)

    # ── C670 (100nF) filtro no coletor ──
    C670_X = COLL2_NODE_X + 8
    C670_Y = OPTO2_Y
    s.capacitor("C670", "100nF", C670_X, C670_Y)
    s.wire(COLL2_NODE_X, COLL2_NODE_Y, C670_X, COLL2_NODE_Y)
    s.wire(C670_X, COLL2_NODE_Y, C670_X, C670_Y - 3.81)
    s.wire(emitter2[0], emitter2[1], C670_X, emitter2[1])
    s.wire(C670_X, emitter2[1], C670_X, C670_Y + 3.81)
    s.junction(emitter2[0], emitter2[1])
    s.junction(COLL2_NODE_X, COLL2_NODE_Y)

    # ── Label uC_SMD_Pin18 (far right) ──
    LBL4_X = COLL2_NODE_X + 22
    s.wire(COLL2_NODE_X, COLL2_NODE_Y, LBL4_X, COLL2_NODE_Y)
    s.glabel("uC_SMD_Pin18", LBL4_X, COLL2_NODE_Y, 0, "input")

    # ── Emitter → GND ──
    GND4_Y = emitter2[1] + 8
    s.wire(emitter2[0], emitter2[1], emitter2[0], GND4_Y)
    s.power("GND", emitter2[0], GND4_Y)

    # ══════════════════════════════════════════════════════════════════
    #  TITULO
    # ══════════════════════════════════════════════════════════════════

    s.text("CIRCUITO DE COMUNICACAO - uC DIP x uC SMD", 60, 175, 3.5)
    s.text("Condensadora Consul 12k / 18k", 80, 183, 2.2)
    s.text("Isolacao galvanica 3.3V <-> 5V via optoacopladores", 70, 190, 1.8)

    return s


# ── Embedded lib symbols ─────────────────────────────────────────────

LIB_SYMBOLS = """
  (lib_symbols
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
    )
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
    )
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
    )
    (symbol "power:+3V3"
      (power)
      (pin_names (offset 0))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "#PWR"
        (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Value" "+3V3"
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
      (symbol "+3V3_0_1"
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
      (symbol "+3V3_1_1"
        (pin power_in line (at 0 0 90) (length 0)
          (name "+3V3" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
      )
    )
    (symbol "power:+5V"
      (power)
      (pin_names (offset 0))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "#PWR"
        (at 0 -3.81 0)
        (effects (font (size 1.27 1.27)) (hide yes))
      )
      (property "Value" "+5V"
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
      (symbol "+5V_0_1"
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
      (symbol "+5V_1_1"
        (pin power_in line (at 0 0 90) (length 0)
          (name "+5V" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
      )
    )
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
    )
  )
"""


def main():
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output-consul")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "consul_comm_circuit.kicad_sch")

    s = build()

    content = f"""(kicad_sch
  (version 20231120)
  (generator "consul_comm_generator")
  (generator_version "3.0")
  (uuid "{ROOT_UUID}")
  (paper "A4")
{LIB_SYMBOLS}
{s.get_elements()}
{s.get_sheet_instances()}
)"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Esquematico gerado: {output_path}")
    print()
    print("Componentes (11):")
    print("  U1   ISO802   Opto canal 1: SMD TX -> DIP RX")
    print("  U2   ISO801   Opto canal 2: DIP TX -> SMD RX")
    print("  R671 390R     Pull-up 3.3V (sinal uC SMD Pin19)")
    print("  R672 2k       Serie anodo ISO802")
    print("  R821 4.7k     Pull-up 5V (coletor ISO802)")
    print("  R820 100R     Serie uC DIP Pin20")
    print("  R819 4.7k     Pull-up 5V (sinal uC DIP Pin21)")
    print("  R818 390R     Serie anodo ISO801")
    print("  R670 4.7k     Pull-up 3.3V (coletor ISO801)")
    print("  C1   100nF    Filtro pinos 3-4 ISO802")
    print("  C670 100nF    Filtro coletor ISO801")


if __name__ == "__main__":
    main()
