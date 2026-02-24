"""JSON schemas for Claude CLI structured output."""

# Schema for circuit analysis — Claude describes what it sees
ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "circuit_type": {
            "type": "string",
            "description": "Type of circuit: power_supply, microcontroller, amplifier, sensor, motor_driver, mixed"
        },
        "critical_paths": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Path name like 'power_input', 'high_speed_clock'"},
                    "nets": {"type": "array", "items": {"type": "string"}, "description": "Net names in this path"},
                    "priority": {"type": "string", "enum": ["high", "medium", "low"]},
                    "trace_width_mm": {"type": "number", "description": "Recommended trace width"}
                },
                "required": ["name", "nets", "priority", "trace_width_mm"]
            }
        },
        "power_nets": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Net names that carry power (VCC, VDD, 3V3, 5V, etc.)"
        },
        "ground_nets": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Net names that are ground (GND, AGND, DGND, etc.)"
        }
    },
    "required": ["circuit_type", "critical_paths", "power_nets", "ground_nets"]
}

# Schema for placement strategy — Claude decides where to put components
PLACEMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "board_width_mm": {
            "type": "number",
            "description": "Recommended board width in mm"
        },
        "board_height_mm": {
            "type": "number",
            "description": "Recommended board height in mm"
        },
        "placements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ref": {"type": "string", "description": "Component reference like R1, U1"},
                    "x": {"type": "number", "description": "X position in mm from board origin"},
                    "y": {"type": "number", "description": "Y position in mm from board origin"},
                    "rotation": {"type": "number", "description": "Rotation in degrees (0, 90, 180, 270)"},
                    "layer": {"type": "string", "enum": ["F.Cu", "B.Cu"], "description": "Component layer"}
                },
                "required": ["ref", "x", "y", "rotation", "layer"]
            }
        },
        "reasoning": {
            "type": "string",
            "description": "Brief explanation of placement strategy"
        }
    },
    "required": ["board_width_mm", "board_height_mm", "placements", "reasoning"]
}
