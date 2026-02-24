#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analisa imagem de circuito via Claude Vision API.

Envia foto/desenho de circuito para Claude e retorna descricao estruturada
compativel com SchematicBuilder.build_from_dict().

Dependencia: pip install anthropic
Requer: ANTHROPIC_API_KEY no environment
"""

import base64
import json
import os
import sys
from pathlib import Path


CIRCUIT_ANALYSIS_PROMPT = """Analyze this circuit image and return a structured JSON description.

You MUST return ONLY valid JSON (no markdown, no explanation). The JSON must follow this exact schema:

{
    "components": [
        {
            "type": "resistor|capacitor|diode|led|optocoupler|ic",
            "ref": "R1",
            "value": "10k",
            "x": 100,
            "y": 50,
            "angle": 0,
            "footprint": "Resistor_SMD:R_0805_2012Metric"
        }
    ],
    "connections": [
        {"from": [100, 53.81], "to": [120, 53.81]}
    ],
    "power_rails": [
        {"name": "+5V", "x": 100, "y": 30},
        {"name": "GND", "x": 100, "y": 80}
    ],
    "labels": [
        {"text": "INPUT", "x": 70, "y": 50, "angle": 180, "shape": "input"}
    ],
    "junctions": [
        {"x": 100, "y": 50}
    ],
    "notes": "Brief description of the circuit"
}

RULES:
1. Use KiCad schematic coordinates: X grows rightward, Y grows downward
2. Space components ~25-30 units apart horizontally, ~20-25 vertically
3. Start placement at approximately x=80, y=50
4. Resistor/capacitor pin spacing is 3.81 units from center (7.62 total)
5. For horizontal resistors use angle=90, vertical use angle=0
6. Use standard KiCad footprints:
   - Resistors: "Resistor_SMD:R_0805_2012Metric" (or R_0603, R_1206)
   - Capacitors: "Capacitor_SMD:C_0805_2012Metric"
   - Diodes: "Diode_SMD:D_SOD-123"
   - LEDs: "LED_SMD:LED_0805_2012Metric"
   - Optocouplers: "Package_DIP:DIP-4_W7.62mm"
   - ICs: use appropriate DIP or SMD package
7. Wire connections must align with component pin positions
8. Every net must connect to something (no floating wires)
9. Include power rails (VCC/+5V/+3V3/+12V and GND) for all power connections
10. Label signal inputs/outputs with global labels

For ICs, provide the KiCad lib_id (e.g., "Timer:NE555", "Amplifier_Operational:LM358").
If unsure about exact lib_id, use a reasonable guess and note it.

Identify ALL components visible in the image. If values are not readable, estimate reasonable values."""


MANUAL_TEMPLATE = {
    "components": [
        {"type": "resistor", "ref": "R1", "value": "10k", "x": 100, "y": 50, "angle": 0},
    ],
    "connections": [
        {"from": [100, 53.81], "to": [130, 53.81]},
    ],
    "power_rails": [
        {"name": "+5V", "x": 100, "y": 40},
        {"name": "GND", "x": 100, "y": 70},
    ],
    "labels": [],
    "junctions": [],
    "notes": "Preencha manualmente com os componentes do circuito",
}


def _get_media_type(image_path):
    """Detecta media type pela extensao."""
    ext = Path(image_path).suffix.lower()
    types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return types.get(ext, "image/jpeg")


def analyze_circuit_image(image_path, model="claude-sonnet-4-20250514"):
    """Analisa imagem de circuito via Claude Vision API.

    Args:
        image_path: caminho da imagem (JPG, PNG, etc)
        model: modelo Claude a usar (default: sonnet para custo/velocidade)

    Returns:
        dict com descricao estruturada do circuito (compativel com build_from_dict)
    """
    image_path = Path(image_path)
    if not image_path.exists():
        print(f"  X Imagem nao encontrada: {image_path}")
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ! ANTHROPIC_API_KEY nao definida no environment")
        print("  ! Gerando template JSON para preenchimento manual...")
        return _fallback_manual(image_path)

    try:
        import anthropic
    except ImportError:
        print("  X SDK anthropic nao instalado. Execute:")
        print("    pip install anthropic")
        print("  ! Gerando template JSON para preenchimento manual...")
        return _fallback_manual(image_path)

    # Encode image
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
    media_type = _get_media_type(image_path)

    print(f"  >> Enviando imagem para Claude Vision ({model})...")

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": CIRCUIT_ANALYSIS_PROMPT,
                    },
                ],
            }
        ],
    )

    response_text = message.content[0].text.strip()

    # Strip markdown code fences if present
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        # Remove first and last lines (```json and ```)
        lines = [l for l in lines if not l.strip().startswith("```")]
        response_text = "\n".join(lines)

    try:
        circuit_desc = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"  X Erro ao parsear JSON da resposta: {e}")
        print(f"  Resposta bruta salva em _claude_response.txt")
        Path("_claude_response.txt").write_text(response_text)
        sys.exit(1)

    # Validacao basica
    if "components" not in circuit_desc:
        print("  X Resposta nao contem 'components'")
        sys.exit(1)

    n_comp = len(circuit_desc.get("components", []))
    n_conn = len(circuit_desc.get("connections", []))
    n_pwr = len(circuit_desc.get("power_rails", []))
    print(f"  << {n_comp} componentes, {n_conn} conexoes, {n_pwr} power rails detectados")

    return circuit_desc


def _fallback_manual(image_path):
    """Gera template JSON para preenchimento manual quando API nao disponivel."""
    template = MANUAL_TEMPLATE.copy()
    template["notes"] = f"Template gerado de: {image_path.name} — preencha manualmente"

    template_path = Path(image_path).with_suffix(".circuit.json")
    with open(template_path, "w") as f:
        json.dump(template, f, indent=2)

    print(f"  >> Template salvo em: {template_path}")
    print(f"  >> Edite o arquivo e re-execute com:")
    print(f"     python3 scripts/photo_to_pcb.py {template_path} --from-json --project nome")
    return template
