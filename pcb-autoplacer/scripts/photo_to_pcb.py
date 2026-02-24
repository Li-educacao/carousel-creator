#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry Point A: Foto/imagem de circuito -> PCB completo.

Fluxo:
  1. Envia imagem para Claude Vision API
  2. Valida descricao estruturada (JSON)
  3. Gera .kicad_sch via SchematicBuilder
  4. Valida esquematico (ERC via kicad-cli)
  5. Exporta .net via kicad-cli
  6. Executa pipeline completo (placement -> routing -> gerbers)

Uso:
  python3 scripts/photo_to_pcb.py foto.jpg --project meu-circuito
  python3 scripts/photo_to_pcb.py circuito.circuit.json --from-json --project nome
  python3 scripts/photo_to_pcb.py foto.jpg --project nome --skip-validation

Dependencia: pip install anthropic
Requer: ANTHROPIC_API_KEY no environment (ou --from-json para pular IA)
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

KICAD_CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
SCRIPTS_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPTS_DIR.parent

# Ensure src is in path for pcb_autoplacer imports
sys.path.insert(0, str(PROJECT_DIR / "src"))
sys.path.insert(0, str(SCRIPTS_DIR))


def log(emoji, msg):
    print(f"  {emoji} {msg}")


# ── Validacao do circuit description (JSON) ───────────────────────────

def validate_circuit_desc(circuit_desc):
    """Valida descricao estruturada antes de gerar esquematico.

    Verifica:
    - Tem componentes (minimo 1)
    - Cada componente tem campos obrigatorios (type, ref, value, x, y)
    - Tipos de componente sao reconhecidos
    - Tem pelo menos 1 conexao ou power rail
    - Referencias nao estao duplicadas
    - Coordenadas sao numericas

    Returns:
        (ok: bool, errors: list[str], warnings: list[str])
    """
    errors = []
    warnings = []

    VALID_TYPES = {"resistor", "capacitor", "diode", "led", "optocoupler", "ic"}
    REQUIRED_FIELDS = {"type", "ref", "value", "x", "y"}
    IC_EXTRA_FIELDS = {"lib_id", "footprint"}

    # ── Componentes ──
    components = circuit_desc.get("components", [])
    if not components:
        errors.append("Nenhum componente encontrado (lista 'components' vazia)")
        return False, errors, warnings

    refs_seen = set()
    for i, comp in enumerate(components):
        prefix = f"components[{i}]"

        # Campos obrigatorios
        missing = REQUIRED_FIELDS - set(comp.keys())
        if missing:
            errors.append(f"{prefix}: campos obrigatorios ausentes: {missing}")
            continue

        # Tipo reconhecido
        ctype = comp.get("type", "").lower()
        if ctype not in VALID_TYPES:
            errors.append(f"{prefix}: tipo '{ctype}' desconhecido (validos: {VALID_TYPES})")

        # IC precisa de lib_id e footprint
        if ctype == "ic":
            missing_ic = IC_EXTRA_FIELDS - set(comp.keys())
            if missing_ic:
                errors.append(f"{prefix} (IC {comp.get('ref', '?')}): campos obrigatorios para IC ausentes: {missing_ic}")

        # Coordenadas numericas
        for field in ("x", "y"):
            val = comp.get(field)
            if val is not None and not isinstance(val, (int, float)):
                errors.append(f"{prefix}: '{field}' deve ser numerico, recebido: {type(val).__name__}")

        # Referencia duplicada
        ref = comp.get("ref", "")
        if ref in refs_seen:
            errors.append(f"{prefix}: referencia duplicada '{ref}'")
        refs_seen.add(ref)

    # ── Conexoes ──
    connections = circuit_desc.get("connections", [])
    if not connections:
        warnings.append("Nenhuma conexao (wire) definida — componentes podem ficar desconectados")

    for i, conn in enumerate(connections):
        prefix = f"connections[{i}]"
        has_from_to = "from" in conn and "to" in conn
        has_points = "points" in conn
        if not has_from_to and not has_points:
            errors.append(f"{prefix}: precisa de 'from'+'to' ou 'points'")
        if has_from_to:
            for key in ("from", "to"):
                pt = conn.get(key, [])
                if not isinstance(pt, list) or len(pt) != 2:
                    errors.append(f"{prefix}.{key}: deve ser lista [x, y] com 2 elementos")

    # ── Power rails ──
    power_rails = circuit_desc.get("power_rails", [])
    if not power_rails:
        warnings.append("Nenhum power rail (VCC/GND) definido")

    has_gnd = any(p.get("name", "").upper() == "GND" for p in power_rails)
    has_supply = any(p.get("name", "").upper() != "GND" for p in power_rails)
    if power_rails and not has_gnd:
        warnings.append("Nenhum GND definido nos power rails")
    if power_rails and not has_supply:
        warnings.append("Nenhuma fonte (VCC/+5V/+3V3/+12V) definida nos power rails")

    ok = len(errors) == 0
    return ok, errors, warnings


# ── Validacao ERC via kicad-cli ───────────────────────────────────────

def validate_schematic_erc(sch_path, output_dir):
    """Executa ERC (Electrical Rules Check) no esquematico via kicad-cli.

    Returns:
        (ok: bool, erc_errors: int, erc_warnings: int, report_path: Path)
    """
    erc_report = output_dir / "erc-report.json"

    result = subprocess.run(
        [KICAD_CLI, "sch", "erc",
         "--severity-all",
         "--units", "mm",
         "--format", "json",
         "--output", str(erc_report),
         str(sch_path)],
        capture_output=True, text=True,
    )

    erc_errors = 0
    erc_warnings = 0

    if erc_report.exists():
        with open(erc_report) as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                log("!", "ERC report JSON invalido")
                return False, 0, 0, erc_report

        # KiCad ERC JSON has "violations" and/or "sheets" with violations
        violations = data.get("violations", [])
        for v in violations:
            severity = v.get("severity", "")
            if severity == "error":
                erc_errors += 1
            elif severity == "warning":
                erc_warnings += 1

    ok = erc_errors == 0
    return ok, erc_errors, erc_warnings, erc_report


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Foto -> PCB: analisa imagem de circuito via IA e gera PCB completo"
    )
    parser.add_argument("input", help="Caminho da imagem (JPG/PNG) ou JSON (com --from-json)")
    parser.add_argument("--project", required=True,
                        help="Nome do projeto (obrigatorio)")
    parser.add_argument("--from-json", action="store_true",
                        help="Input eh JSON pre-existente (pula analise de imagem)")
    parser.add_argument("--model", default="claude-sonnet-4-20250514",
                        help="Modelo Claude para analise (default: sonnet)")
    parser.add_argument("--fill-ratio", type=float, default=0.30,
                        help="Target fill ratio (default 0.30)")
    parser.add_argument("--logo-width", type=float, default=12,
                        help="Largura da logo em mm (default 12)")
    parser.add_argument("--no-logo", action="store_true",
                        help="Pula injecao da logo")
    parser.add_argument("--skip-route", action="store_true",
                        help="Pula autoroute")
    parser.add_argument("--skip-validation", action="store_true",
                        help="Pula validacao (JSON + ERC) e segue direto pro pipeline")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        log("X", f"Arquivo nao encontrado: {input_path}")
        sys.exit(1)

    project_name = args.project
    output_dir = PROJECT_DIR / f"output-{project_name}"
    output_dir.mkdir(exist_ok=True)

    sch_path = output_dir / f"{project_name}.kicad_sch"
    netlist_path = output_dir / "circuit.net"
    circuit_json_path = output_dir / "circuit-description.json"

    total_steps = 5
    if args.skip_validation:
        total_steps = 4

    print("=" * 60)
    print(f"  FOTO -> PCB Pipeline")
    print(f"  Input:   {input_path.name}")
    print(f"  Project: {project_name}")
    print(f"  Output:  {output_dir}")
    print("=" * 60)

    # ── Step 1: Analyze image (or load JSON) ──
    step = 1
    print(f"\n[{step}/{total_steps}] Analise do circuito")
    print("=" * 60)

    if args.from_json:
        log(">>", f"Carregando descricao de {input_path.name}")
        with open(input_path) as f:
            circuit_desc = json.load(f)
        n_comp = len(circuit_desc.get("components", []))
        log("OK", f"{n_comp} componentes carregados do JSON")
    else:
        from pcb_autoplacer.ai.circuit_analyzer import analyze_circuit_image
        circuit_desc = analyze_circuit_image(str(input_path), model=args.model)

    # Save circuit description for reference/editing
    with open(circuit_json_path, "w") as f:
        json.dump(circuit_desc, f, indent=2)
    log("OK", f"Descricao salva em {circuit_json_path.name}")

    # ── Step 2: Validate JSON + Generate + Validate ERC ──
    if not args.skip_validation:
        step += 1
        print(f"\n[{step}/{total_steps}] Validacao do circuito")
        print("=" * 60)

        # 2a. Validacao estrutural do JSON
        print("  --- Validacao JSON ---")
        ok, errs, warns = validate_circuit_desc(circuit_desc)

        for w in warns:
            log("!", f"WARN: {w}")
        for e in errs:
            log("X", f"ERRO: {e}")

        if not ok:
            log("X", f"{len(errs)} erros encontrados na descricao do circuito")
            log("!", f"Corrija o JSON em: {circuit_json_path}")
            log("!", f"Re-execute com: python3 {sys.argv[0]} {circuit_json_path} --from-json --project {project_name}")
            sys.exit(1)

        n_comp = len(circuit_desc.get("components", []))
        n_conn = len(circuit_desc.get("connections", []))
        n_pwr = len(circuit_desc.get("power_rails", []))
        log("OK", f"JSON valido: {n_comp} componentes, {n_conn} conexoes, {n_pwr} power rails")
        if warns:
            log("!", f"{len(warns)} warnings (ver acima)")

        # 2b. Gerar esquematico
        print("\n  --- Geracao do esquematico ---")
        from pcb_autoplacer.generators.schematic_gen import build_from_dict

        builder = build_from_dict(circuit_desc)
        builder.save(str(sch_path), generator_name="photo_to_pcb")

        n_elements = len(builder.elements)
        size_kb = sch_path.stat().st_size / 1024
        log("OK", f"Esquematico gerado: {sch_path.name} ({size_kb:.1f}KB, {n_elements} elementos)")

        # 2c. ERC via kicad-cli
        print("\n  --- ERC (Electrical Rules Check) ---")
        erc_ok, erc_errors, erc_warnings, erc_report = validate_schematic_erc(sch_path, output_dir)

        log(">>", f"ERC: {erc_errors} errors, {erc_warnings} warnings")

        if not erc_ok:
            log("!", f"ERC encontrou {erc_errors} erros!")
            log("!", f"Relatorio: {erc_report}")
            log("!", f"Esquematico: {sch_path}")
            print()
            log("?", "Opcoes:")
            print("     1. Abrir o .kicad_sch no KiCad, corrigir, e usar sch_to_pcb.py")
            print(f"     2. Editar {circuit_json_path.name} e re-executar com --from-json")
            print(f"     3. Re-executar com --skip-validation para ignorar erros")
            print()

            resp = input("  Continuar mesmo com erros ERC? [s/N] ").strip().lower()
            if resp not in ("s", "sim", "y", "yes"):
                log(">>", "Abortado pelo usuario. Corrija e re-execute.")
                sys.exit(1)
            log(">>", "Continuando apesar dos erros ERC (usuario confirmou)")
        else:
            log("OK", "ERC passou sem erros")

        # 2d. Resumo de validacao
        print("\n  --- Resumo de validacao ---")
        print(f"  Componentes:  {n_comp}")
        print(f"  Conexoes:     {n_conn}")
        print(f"  Power rails:  {n_pwr}")
        print(f"  ERC errors:   {erc_errors}")
        print(f"  ERC warnings: {erc_warnings}")
        print(f"  Esquematico:  {sch_path}")

    else:
        # skip-validation: gerar esquematico sem validar
        step += 1
        print(f"\n[{step}/{total_steps}] Geracao do esquematico KiCad (sem validacao)")
        print("=" * 60)

        from pcb_autoplacer.generators.schematic_gen import build_from_dict

        builder = build_from_dict(circuit_desc)
        builder.save(str(sch_path), generator_name="photo_to_pcb")

        n_elements = len(builder.elements)
        log("OK", f"Esquematico gerado: {sch_path.name} ({n_elements} elementos)")
        log("!", "Validacao pulada (--skip-validation)")

    # ── Step 3: Export netlist ──
    step += 1
    print(f"\n[{step}/{total_steps}] Export netlist via kicad-cli")
    print("=" * 60)

    result = subprocess.run(
        [KICAD_CLI, "sch", "export", "netlist",
         "-o", str(netlist_path),
         str(sch_path)],
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        log("X", f"kicad-cli falhou ao exportar netlist: {result.stderr}")
        log("!", "Verifique o esquematico gerado no KiCad para erros")
        log("!", f"  {sch_path}")
        sys.exit(1)

    if not netlist_path.exists():
        log("X", f"Netlist nao foi gerado em {netlist_path}")
        sys.exit(1)

    size_kb = netlist_path.stat().st_size / 1024
    log("OK", f"Netlist gerado: {netlist_path.name} ({size_kb:.1f}KB)")

    # ── Step 4: Run pipeline ──
    step += 1
    print(f"\n[{step}/{total_steps}] Executando pipeline completo")
    print("=" * 60)

    from run_pipeline import run_pipeline

    result = run_pipeline(
        str(netlist_path),
        fill_ratio=args.fill_ratio,
        logo_width=args.logo_width,
        no_logo=args.no_logo,
        skip_route=args.skip_route,
    )

    return result


if __name__ == "__main__":
    main()
