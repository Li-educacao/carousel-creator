# Session: Ground Plane + Logo + Gerbers — 2026-02-23

## Objetivo
Adicionar ground plane (malha de terra) na camada B.Cu do PCB gerado pelo autoplacer.

## Decisoes
- **Camada:** B.Cu (traseira)
- **Clearance:** 0.5mm (pad-to-zone)
- **Net:** GND (net code 2)
- **Margem da borda:** 1.0mm (usa `board.edge_clearance_mm`)
- **Thermal relief:** 0.5mm gap + 0.5mm bridge
- **Min thickness:** 0.25mm
- **Sem `filled_polygon`** — KiCad preenche automaticamente com Fill All Zones (tecla B)

## Arquivos Modificados

### 1. `src/pcb_autoplacer/generators/sexpr_writer.py`
- Adicionadas 12 keywords ao `_KICAD_KEYWORDS`: `zone`, `polygon`, `pts`, `xy`, `connect_pads`, `min_thickness`, `thermal_gap`, `thermal_bridge_width`, `hatch`, `edge`, `net_name`, `name`
- Sem isso o serializer colocaria aspas nesses tokens e KiCad rejeitaria

### 2. `src/pcb_autoplacer/generators/board_setup.py`
- Nova funcao `generate_ground_zone(board, net_code, net_name, layer)` (linhas 211-242)
- Retorna um node S-expression `(zone ...)` com poligono retangular inset pela margem
- Reutiliza `_uuid()` existente

### 3. `src/pcb_autoplacer/generators/kicad_pcb.py`
- Importada `generate_ground_zone` de `board_setup`
- Adicionado bloco apos footprints (linhas 51-55): busca net GND, gera zona, appenda na tree

## Pipeline de Geracao

```bash
# 1. Gerar PCB com componentes + zona
PYTHONPATH=src python3 scripts/place_lg_manual.py

# 2. Injetar trilhas roteadas
PYTHONPATH=src python3 scripts/import_ses_routes.py

# 3. Abrir no KiCad
open output-lg/board.kicad_pcb

# 4. Preencher zona: tecla B (Fill All Zones)

# 5. Rodar DRC
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc \
  --severity-all --units mm --format json \
  --output output-lg/drc-report.json \
  output-lg/board.kicad_pcb
```

## Resultado DRC

**47 violacoes — todas WARNING, 0 errors, 0 unconnected**

| Tipo | Qtd | Severidade | Descricao |
|------|-----|------------|-----------|
| `lib_footprint_mismatch` | 33 | warning | Footprints gerados nao batem 1:1 com biblioteca KiCad (esperado — geramos geometria simplificada) |
| `silk_over_copper` | 13 | warning | Serigrafia sobrepoe mascara de solda em SMD (ajuste fino de courtyard/silk margin) |
| `silk_overlap` | 1 | warning | Texto PS1 sobrepoe ref C6 (proximidade de componentes) |

**Nenhum erro de clearance, curto-circuito, ou net desconectada.** A zona GND funciona corretamente.

### Sobre os warnings
- **lib_footprint_mismatch (33):** Nosso gerador cria footprints com geometria simplificada (courtyard + fab + silk retangulares). O KiCad compara com a biblioteca oficial e detecta diferenca. Nao afeta fabricacao.
- **silk_over_copper (13):** Componentes SMD pequenos (0805, SOD-123, SOT-23) tem silk muito proximo dos pads. Corrigivel aumentando `silk_margin` no gerador ou removendo silk de SMD.
- **silk_overlap (1):** PS1 e C6 ficaram proximos. Corrigivel ajustando posicao do label.

## Verificacao Visual
- PCB abre sem erro no KiCad 9.0.5
- Zona aparece em B.Cu (retangulo pontilhado antes do fill)
- Apos Fill (B): cobre preenche toda a traseira com clearance ao redor das trilhas/pads
- Pads GND conectam via thermal relief
- Preview salvo em `output-lg/pcb_ground_plane_preview.png`

## Logo Lawteck (adicionado nesta sessao)

### Script: `scripts/inject_logo.py`
- Converte SVG → PNG (cairosvg) → threshold → crop → morphological clean → scanline rects → fp_poly
- SVG: `/Users/lawhander/Downloads/lawteck vector.svg`
- Crop: y=640-1420, x=100-1980 (area principal, sem circuito do fundo)
- Resultado: 1038 poligonos, 15.0 x 6.2 mm, F.SilkS
- Position: (120, 148) — canto inferior-esquerdo
- Reference "LOGO" com `(hide yes)` para nao poluir visual

### Uso:
```bash
PYTHONPATH=src python3 scripts/inject_logo.py \
    --board output-lg/board.kicad_pcb \
    --svg "/Users/lawhander/Downloads/lawteck vector.svg" \
    --width 15 --position 120,148
```

## Gerbers Exportados

### Camadas:
| Arquivo | Camada |
|---------|--------|
| `board-F_Cu.gtl` | Cobre frente |
| `board-B_Cu.gbl` | Cobre tras + ground plane |
| `board-F_Silkscreen.gto` | Serigrafia frente + logo |
| `board-B_Silkscreen.gbo` | Serigrafia tras |
| `board-F_Mask.gts` | Mascara solda frente |
| `board-B_Mask.gbs` | Mascara solda tras |
| `board-Edge_Cuts.gm1` | Contorno |
| `board-PTH.drl` | Furos metalizados |
| `board-NPTH.drl` | Furos nao-metalizados |

### ZIP: `output-lg/gerbers-jlcpcb.zip` (55KB, pronto para upload)

## Workflow Documentado
- **Pipeline completo** documentado em `docs/workflow-pcb-labels-routes.md`
- 8 passos: place → DSN → route → SES → logo → DRC → gerbers → zip
- Proximo projeto: dar netlist + posicoes → executa pipeline inteiro automaticamente
