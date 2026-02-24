"""Claude Code CLI wrapper for AI-powered PCB analysis."""
from __future__ import annotations
import json
import os
import subprocess

from rich.console import Console

from pcb_autoplacer.ai.schemas import ANALYSIS_SCHEMA, PLACEMENT_SCHEMA
from pcb_autoplacer.ai.prompts import build_analysis_prompt, build_placement_prompt
from pcb_autoplacer.models import Component, Net, FootprintDef

console = Console()


class ClaudeCLIError(Exception):
    """Error calling Claude CLI."""


def _call_claude(full_prompt: str, schema: dict, model: str = "sonnet") -> dict:
    """Call Claude Code CLI with structured JSON output.

    Uses stdin pipe to avoid OS argument length limits with large prompts.

    Args:
        full_prompt: Complete prompt text (instructions + netlist data)
        schema: JSON schema for --json-schema flag
        model: Model to use (sonnet, haiku, opus)

    Returns:
        Parsed structured output dict matching the schema
    """
    schema_json = json.dumps(schema)
    cmd = [
        "claude", "-p", "-",
        "--output-format", "json",
        "--json-schema", schema_json,
        "--model", model,
        "--max-turns", "3",
    ]

    # Remove CLAUDECODE env var to allow running from within a Claude Code session
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    try:
        result = subprocess.run(
            cmd,
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=600,
            env=env,
        )
    except subprocess.TimeoutExpired:
        raise ClaudeCLIError("Claude CLI timed out after 600s")
    except FileNotFoundError:
        raise ClaudeCLIError("Claude CLI not found. Install: npm install -g @anthropic-ai/claude-code")

    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise ClaudeCLIError(f"Claude CLI failed (exit {result.returncode}): {stderr}")

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise ClaudeCLIError(f"Failed to parse Claude CLI output as JSON: {e}")

    # --json-schema puts the structured data in "structured_output"
    if isinstance(output, dict) and "structured_output" in output:
        return output["structured_output"]

    # Fallback: try "result" field (may contain JSON string)
    if isinstance(output, dict) and "result" in output:
        result_text = output["result"]
        if isinstance(result_text, str):
            try:
                return json.loads(result_text)
            except json.JSONDecodeError:
                pass
        if isinstance(result_text, dict):
            return result_text

    raise ClaudeCLIError(f"Unexpected Claude CLI output format: {list(output.keys()) if isinstance(output, dict) else type(output)}")


def analyze_circuit(
    components: list[Component],
    nets: list[Net],
    footprints: dict[str, FootprintDef],
) -> dict:
    """Analyze circuit and identify critical paths, power/ground nets.

    Returns dict matching ANALYSIS_SCHEMA.
    """
    full_prompt = build_analysis_prompt(components, nets, footprints)

    console.print("[cyan]Analyzing circuit with Claude...[/cyan]")
    result = _call_claude(full_prompt, ANALYSIS_SCHEMA)
    console.print(f"[green]Circuit type: {result.get('circuit_type', 'unknown')}[/green]")

    return result


def generate_placement(
    components: list[Component],
    nets: list[Net],
    footprints: dict[str, FootprintDef],
    board_width: float = 50.0,
    board_height: float = 50.0,
) -> dict:
    """Generate component placement using Claude AI.

    Returns dict matching PLACEMENT_SCHEMA.
    """
    full_prompt = build_placement_prompt(components, nets, footprints, board_width, board_height)

    console.print(f"[cyan]Generating placement for {len(components)} components on {board_width}x{board_height}mm board...[/cyan]")
    result = _call_claude(full_prompt, PLACEMENT_SCHEMA, model="opus")
    console.print(f"[green]Placement generated: {len(result.get('placements', []))} components placed[/green]")

    return result
