# Workflow: Pipeline Completo — Esquematico ate Gerbers

Pipeline automatizado para gerar PCB completo com componentes, trilhas, malha de terra, logo Lawteck e Gerbers prontos para fabricacao.

Testado com: KiCad 9.0.5, Freerouter, Python 3.12

---

## Modo Automatico (Recomendado para novos projetos)

Para novos projetos, basta fornecer o netlist — o sistema calcula o tamanho ideal da placa automaticamente, incluindo espaco para a logo Lawteck.

**Comando unico:**
```
Gera a placa completa do projeto [NOME] com o netlist [CAMINHO]. Logo Lawteck. Entrega os Gerbers.
```

**Script:**
```bash
cd pcb-autoplacer
PYTHONPATH=src python3 scripts/place_auto.py output-NOME/circuito.net
```

**O que faz automaticamente:**
1. Parseia o netlist → componentes + nets
2. Carrega footprints de todas as bibliotecas KiCad
3. Calcula tamanho ideal da placa (area-based + iterativo)
4. Reserva espaco para logo Lawteck (15x7mm default)
5. Posiciona componentes em grid com anti-overlap
6. Gera `.kicad_pcb` com ground zone em B.Cu
7. Imprime resumo: board size, fill ratio, component count

**Argumentos opcionais:**
| Argumento | Default | Descricao |
|-----------|---------|-----------|
| `--output-dir` | mesmo dir do netlist | Diretorio de saida |
| `--logo-width` | 15 | Largura da logo em mm |
| `--no-logo` | — | Desabilita reserva de espaco para logo |
| `--min-size` | 30 | Tamanho minimo do board em mm |
| `--fill-ratio` | 0.25 | Target fill ratio (0.25 = 25%) |

**Depois do auto-placement**, continue com o pipeline normal a partir do Passo 2 (Export DSN → Freerouter → Import trilhas → Logo → DRC → Gerbers).

---

## Pipeline Visual

```
Netlist (.net)
    |
    v
[1] place_XX_manual.py         --> board.kicad_pcb (componentes + labels + ground zone)
    |
    v
[2] KiCad: Export DSN           --> board.dsn (ou kicad_bridge.py export-dsn)
    |
    v
[3] Freerouter                  --> board.ses (rotas automaticas)
    |
    v
[4] import_ses_routes.py        --> injeta trilhas no board.kicad_pcb
    |
    v
[5] inject_logo.py              --> adiciona logo Lawteck na F.SilkS
    |
    v
[6] KiCad DRC                   --> drc-report.json (0 errors = OK)
    |
    v
[7] kicad-cli export gerbers    --> gerbers/ + drill files
    |
    v
[8] zip gerbers                 --> gerbers-jlcpcb.zip (pronto para upload)
```

**COMANDO UNICO:** Ao receber um netlist, executar todos os passos nesta ordem. Cada passo depende do anterior.

---

## Passo 1: Gerar PCB com Componentes + Ground Zone

```bash
cd pcb-autoplacer
PYTHONPATH=src python3 scripts/place_XX_manual.py
```

**O que faz:**
- Parseia o netlist (.net)
- Posiciona componentes conforme VISUAL_CENTERS
- Aplica labels customizados (LABEL_CONFIG)
- Gera net classes (AC_Mains 1.0mm, Power 0.5mm, Signal 0.25mm)
- **Adiciona ground zone em B.Cu** (malha de terra automatica)
- Gera board outline em Edge.Cuts

**Saida:** `output-XX/board.kicad_pcb` com componentes + zona GND, SEM trilhas.

### Configuracao do Ground Zone

Gerado automaticamente por `generate_ground_zone()` em `board_setup.py`:
- Camada: B.Cu
- Net: GND (detecta automaticamente)
- Clearance pad-zona: 0.5mm
- Thermal relief: 0.5mm gap + 0.5mm bridge
- Margem da borda: `board.edge_clearance_mm` (default 1.0mm)
- Espessura minima: 0.25mm

---

## Passo 2: Exportar DSN para Roteamento

### Opcao A: Via KiCad GUI
1. Abrir `board.kicad_pcb` no KiCad PCB Editor
2. **File > Export > Specctra DSN...**
3. Salvar como `output-XX/board.dsn`

### Opcao B: Via Script (requer Python do KiCad)
```bash
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 \
    scripts/kicad_bridge.py export-dsn output-XX/board.kicad_pcb output-XX/board.dsn
```

---

## Passo 3: Autorouter (Freerouter)

1. Abrir Freerouter (`java -jar freerouting.jar`)
2. **File > Open Design** → `board.dsn`
3. **Route > Autorouter** → aguardar conclusao
4. **File > Export Specctra Session** → `board.ses`

---

## Passo 4: Importar Trilhas

```bash
PYTHONPATH=src python3 scripts/import_ses_routes.py
```

**Saida:** Trilhas injetadas no `board.kicad_pcb` existente.

---

## Passo 5: Injetar Logo Lawteck

Script automatizado que converte o SVG da logo para poligonos na serigrafia.

```bash
PYTHONPATH=src python3 scripts/inject_logo.py \
    --board output-XX/board.kicad_pcb \
    --svg "/Users/lawhander/Downloads/lawteck vector.svg" \
    --width 15 \
    --position 120,148 \
    --layer F.SilkS
```

**O que faz:**
1. Renderiza SVG → PNG alta resolucao (2000px)
2. Extrai pixels escuros (brightness < 160) = elementos da logo
3. Recorta area da logo principal (sem background)
4. Limpa ruido com filtro morfologico
5. Converte para scanline rectangles → fp_poly em F.SilkS
6. Injeta footprint no .kicad_pcb com `(hide yes)` no Reference

**Parametros:**
- `--width`: largura em mm (default 15)
- `--position`: coordenada X,Y no board (default: canto inferior-esquerdo)
- `--layer`: camada (default F.SilkS)

---

## Passo 6: Rodar DRC

```bash
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc \
    --severity-all --units mm --format json \
    --output output-XX/drc-report.json \
    output-XX/board.kicad_pcb
```

**Criterio de aprovacao:**
- 0 errors (tipo error)
- 0 unconnected items
- Warnings sao aceitaveis (lib_footprint_mismatch, silk_over_copper)

---

## Passo 7: Exportar Gerbers + Drill

```bash
# Gerbers (7 camadas)
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export gerbers \
    --layers "F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" \
    --subtract-soldermask \
    --output output-XX/gerbers/ \
    output-XX/board.kicad_pcb

# Drill files (Excellon, PTH + NPTH separados)
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export drill \
    --format excellon \
    --excellon-separate-th \
    --excellon-units mm \
    --generate-map --map-format gerberx2 \
    --output output-XX/gerbers/ \
    output-XX/board.kicad_pcb
```

**Arquivos gerados:**

| Arquivo | Camada |
|---------|--------|
| `board-F_Cu.gtl` | Cobre frente |
| `board-B_Cu.gbl` | Cobre tras (com ground plane) |
| `board-F_Silkscreen.gto` | Serigrafia frente (com logo) |
| `board-B_Silkscreen.gbo` | Serigrafia tras |
| `board-F_Mask.gts` | Mascara de solda frente |
| `board-B_Mask.gbs` | Mascara de solda tras |
| `board-Edge_Cuts.gm1` | Contorno da placa |
| `board-PTH.drl` | Furos metalizados |
| `board-NPTH.drl` | Furos nao-metalizados |

---

## Passo 8: Zipar para Upload

```bash
cd output-XX/gerbers
zip -j ../gerbers-jlcpcb.zip *.gtl *.gbl *.gto *.gbo *.gts *.gbs *.gm1 *.drl
```

O ZIP esta pronto para upload direto na JLCPCB, PCBWay ou outro fabricante.

---

## Passo 9 (KiCad): Fill Zones + Verificacao Visual

1. Abrir `board.kicad_pcb` no KiCad
2. Pressionar **B** (Fill All Zones) — preenche a malha de terra
3. Verificar:
   - Trilhas conectadas (sem ratsnest)
   - Ground plane cobrindo B.Cu
   - Logo visivel na F.SilkS
   - Thermal relief nos pads GND

---

## Posicionamento de Componentes

### VISUAL_CENTERS

Dict com posicao visual (centro do componente) de cada referencia:

```python
VISUAL_CENTERS = {
    "R1": (x_mm, y_mm, rotacao_graus),
    "C1": (10.0, 20.0, 0),
}
```

### LABEL_CONFIG

Overrides de posicao dos labels por componente:

```python
LABEL_CONFIG = {
    "ref": {
        "ref_offset": (dx, dy),    # posicao do Reference
        "hide_value": True,         # esconde o Value label
    },
}
```

**Estrategias por zona:**

| Situacao | Estrategia | Exemplo |
|----------|-----------|---------|
| Componentes empilhados verticalmente | Labels a direita ou esquerda | `(3.5, 0.0)` |
| Componentes em coluna apertada | Alternar esquerda/direita | C6 left, C7 right |
| Componente grande (PS1, U3) | Label bem acima | `(0.0, -10.0)` |
| LEDs em fila horizontal | Labels acima | `(0.0, -2.5)` |
| Part numbers longos | `hide_value: True` | Sempre |

---

## Criando para um Novo Projeto

### Opcao A: Modo Automatico (recomendado)

1. Criar diretorio: `mkdir output-NOVO`
2. Colocar o netlist em `output-NOVO/nome.net`
3. `PYTHONPATH=src python3 scripts/place_auto.py output-NOVO/nome.net`
4. Seguir pipeline a partir do Passo 2 (Export DSN)

### Opcao B: Modo Manual (controle total)

1. Copiar `scripts/place_lg_manual.py` → `scripts/place_NOVO_manual.py`
2. Atualizar:
   - `BOARD_W`, `BOARD_H` para as dimensoes do novo board
   - `VISUAL_CENTERS` com as posicoes dos novos componentes
   - `LABEL_CONFIG` com offsets customizados
   - `netlist_path` e `output_path`
3. Criar diretorio de saida: `mkdir output-NOVO`
4. Colocar o netlist em `output-NOVO/nome.net`
5. Seguir o pipeline completo (Passos 1-8)

---

## Troubleshooting

### DRC com erros de clearance
- Verificar se net classes estao corretas (AC > Power > Signal)
- Se trilhas AC muito proximas, aumentar board ou reposicionar componentes

### Logo nao aparece
- Verificar camada F.SilkS ativa no painel de camadas
- Fechar e reabrir KiCad (nao so reload — `Cmd+Q` e abrir de novo)

### Ground zone nao preenche
- Pressionar **B** (Fill All Zones)
- Se nao preencher: verificar que a net GND existe no netlist

### Rotas sumiram apos regenerar
- `place_XX_manual.py` gera PCB do zero, sem trilhas
- Precisa rodar `import_ses_routes.py` depois de cada regeneracao
- O `board.ses` persiste — nao precisa re-rotear se posicoes nao mudaram

---

## Arquivos Chave

| Arquivo | Funcao |
|---------|--------|
| `scripts/place_XX_manual.py` | Posicionamento manual + labels + ground zone |
| `scripts/import_ses_routes.py` | Importa rotas SES para o PCB |
| `scripts/inject_logo.py` | Injeta logo Lawteck na serigrafia |
| `scripts/kicad_bridge.py` | Bridge para pcbnew (export DSN, import SES) |
| `src/pcb_autoplacer/generators/kicad_pcb.py` | Gera S-expression do PCB |
| `src/pcb_autoplacer/generators/board_setup.py` | Layers, setup, nets, ground zone |
| `src/pcb_autoplacer/generators/sexpr_writer.py` | Serializa S-expressions |
| `src/pcb_autoplacer/models.py` | Dataclasses (BoardConfig, Net, etc.) |
| `src/pcb_autoplacer/placer/engine.py` | Motor de placement |

---

## Comando Rapido (resumo)

```bash
cd pcb-autoplacer

# 1. Gerar PCB
PYTHONPATH=src python3 scripts/place_lg_manual.py

# 2. Importar trilhas
PYTHONPATH=src python3 scripts/import_ses_routes.py

# 3. Injetar logo
PYTHONPATH=src python3 scripts/inject_logo.py --board output-lg/board.kicad_pcb

# 4. DRC
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb drc \
    --severity-all --units mm --format json \
    --output output-lg/drc-report.json output-lg/board.kicad_pcb

# 5. Gerbers + Drill
/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export gerbers \
    --layers "F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" \
    --subtract-soldermask --output output-lg/gerbers/ output-lg/board.kicad_pcb

/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli pcb export drill \
    --format excellon --excellon-separate-th --excellon-units mm \
    --generate-map --map-format gerberx2 \
    --output output-lg/gerbers/ output-lg/board.kicad_pcb

# 6. Zip
cd output-lg/gerbers && zip -j ../gerbers-jlcpcb.zip *.gtl *.gbl *.gto *.gbo *.gts *.gbs *.gm1 *.drl

# 7. Abrir no KiCad → B (Fill Zones)
open output-lg/board.kicad_pcb
```
