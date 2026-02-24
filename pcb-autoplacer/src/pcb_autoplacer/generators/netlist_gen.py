#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera arquivo .net (KiCad netlist S-expression) a partir de dados JSON."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from pcb_autoplacer.generators.sexpr_writer import Quoted, serialize, write_sexpr_file


def generate_netlist(
    components: list[dict],
    output_path: Path,
    project: str = "sketch",
) -> Path:
    """Gera um arquivo .net a partir de componentes com mapeamento pin→net.

    Args:
        components: Lista de dicts com {ref, value, footprint, pins: {pin_num: net_name}}
        output_path: Caminho para o arquivo .net de saida
        project: Nome do projeto (aparece no header)

    Returns:
        Path do arquivo gerado
    """
    # 1. Deduzir nets a partir dos pins dos componentes
    net_pins: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for comp in components:
        for pin_num, net_name in comp.get("pins", {}).items():
            net_pins[net_name].append((comp["ref"], str(pin_num)))

    # 2. Atribuir net codes sequenciais (1-based)
    net_codes: dict[str, int] = {}
    code = 1
    for net_name in sorted(net_pins.keys()):
        net_codes[net_name] = code
        code += 1

    # 3. Montar S-expression tree
    tree: list = ["export", ["version", Quoted("E")]]

    # Design section
    tree.append([
        "design",
        ["source", Quoted(project)],
        ["tool", Quoted("pcb-autoplacer netlist_gen")],
    ])

    # Components section
    comp_section: list = ["components"]
    for comp in components:
        comp_node: list = [
            "comp",
            ["ref", Quoted(comp["ref"])],
            ["value", Quoted(comp.get("value", ""))],
            ["footprint", Quoted(comp["footprint"])],
        ]
        if comp.get("description"):
            comp_node.append(["description", Quoted(comp["description"])])
        comp_section.append(comp_node)
    tree.append(comp_section)

    # Nets section
    nets_section: list = ["nets",
                          ["net", ["code", "0"], ["name", Quoted("")]]]
    for net_name in sorted(net_pins.keys(), key=lambda n: net_codes[n]):
        net_code = net_codes[net_name]
        net_node: list = [
            "net",
            ["code", str(net_code)],
            ["name", Quoted(net_name)],
        ]
        for ref, pin in sorted(net_pins[net_name]):
            net_node.append([
                "node",
                ["ref", Quoted(ref)],
                ["pin", Quoted(pin)],
            ])
        nets_section.append(net_node)
    tree.append(nets_section)

    # 4. Escrever arquivo
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_sexpr_file(tree, output_path)

    return output_path


def load_circuit_json(json_path: Path) -> tuple[list[dict], str]:
    """Carrega JSON de circuito e retorna (components, project_name)."""
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    project = data.get("project", "sketch")
    components = data.get("components", [])
    return components, project
