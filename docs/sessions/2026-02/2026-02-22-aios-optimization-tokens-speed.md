# Handoff: AIOS Optimization — Menos Tokens, Mais Velocidade

**Data:** 2026-02-22
**Motivacao:** Video do Erico Renato ("AIOS e Revolucao ou So Hype?") — 3 problemas identificados

---

## O que foi feito

### 1. CLAUDE.md slimmed (516 → 273 linhas, -47%)

**Problema:** Root CLAUDE.md carregava 516 linhas em TODA interacao, mesmo pra tarefas simples.

**Solucao:** Mover detalhes de projeto pra CLAUDE.md locais, condensar secoes pouco usadas.

| Secao | Antes | Depois | Acao |
|-------|-------|--------|------|
| Projects | 98 linhas | 14 linhas | Movido pra CLAUDE.md local de cada projeto |
| AIOS Squads | 94 linhas | ~20 linhas | Condensado, ref pra README.md do squad |
| MCP Infrastructure | 44 linhas | ~3 linhas | Condensado, ref pra `.claude/rules/mcp-usage.md` |
| Synapse | 23 linhas | ~3 linhas | Condensado, ref pra diretorio |
| Key Config Paths | 26 linhas | 10 linhas | Removidos paths raramente usados |
| Secoes criticas | intocadas | intocadas | Operational Rules, Constitution, Agent System, Model Routing |

**Arquivos criados:**
- `grupo-lawteck/.claude/CLAUDE.md` (30 linhas)
- `climatronico-blog/.claude/CLAUDE.md` (25 linhas)
- `relatorios_lawteck/.claude/CLAUDE.md` (25 linhas)
- `RepairHub/.claude/CLAUDE.md` (30 linhas) + diretorio `.claude/` criado

**Arquivo editado:**
- `.claude/CLAUDE.md` — versao v3.3

### 2. Agent Teams habilitado

**Problema:** Subagents nao se comunicavam entre si.

**Solucao:** Adicionado `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` em `.claude/settings.json` > `settings.env`.

**Limitacoes conhecidas:**
- Sem `/resume` para teammates
- Teammates as vezes nao marcam tasks como completas
- Shutdown lento (teammate termina request atual)

### 3. Ralph Loop workflow criado

**Problema:** QA Loop roda na mesma sessao (contexto acumula). Sem pattern de "fresh context per story".

**Solucao:** Workflow `ralph-loop` que spawna subagent limpo via Task tool pra cada story.

**Arquivos criados:**
- `.aios-core/development/workflows/ralph-loop.yaml` (375 linhas)
- `.aios-core/development/tasks/ralph-implement-story.md` (190 linhas)
- `.aios-core/development/tasks/ralph-verify-story.md` (227 linhas)

**Comandos:**
- `*ralph-loop` — inicia o loop
- `*stop-ralph-loop` — pausa, salva estado
- `*resume-ralph-loop` — retoma de onde parou
- `*ralph-status` — mostra progresso

**Model routing:** haiku (scan) → sonnet (implement) → opus (verify) → haiku (progress)

**Diferenca do QA Loop:**

| Aspecto | QA Loop | Ralph Loop |
|---------|---------|------------|
| Proposito | Review → fix → re-review | Implementar story por story |
| Contexto | Mesma sessao | Fresh context por story |
| Agent | QA fixo | Dinamico (dev + qa) |
| Tracking | `qa/loop-status.json` | `ralph/loop-status.json` + `ralph/progress.md` |

### 4. Hooks de Claude Code adicionados

**PreCompact hook** (`.claude/hooks/pre-compact.sh`):
- Roda ANTES da compactacao, quando o contexto ainda esta completo
- Salva snapshot em `.claude/snapshots/pre-compact-latest.md` com:
  - Git status de projetos com mudancas uncommitted
  - Ralph Loop status + progress (ultimas 10 linhas)
  - Ultimos 5 subagents executados (do agent-log.jsonl)
  - Stories ativas (In Progress, Review, Draft)
- Mantem historico das ultimas 5 compactacoes (timestamped)

**SessionStart(compact) hook** — re-injeta o snapshot salvo pelo PreCompact:
- Le `.claude/snapshots/pre-compact-latest.md` e coloca no contexto novo
- Fallback gracioso se nao houver snapshot

**Fluxo completo:**
```
Contexto enchendo → PreCompact salva snapshot → Compactacao → SessionStart re-injeta snapshot
```

**SubagentStop logger**:
- Loga em `ralph/agent-log.jsonl` toda execucao de subagent
- Captura: timestamp, tipo, descricao, turnos, duracao
- Util pra ajustar timeouts e identificar stories lentas

---

## Arquivos modificados/criados nesta sessao

| Acao | Arquivo |
|------|---------|
| Editado | `.claude/CLAUDE.md` (v3.2 → v3.3) |
| Editado | `.claude/settings.json` (env + hooks) |
| Criado | `grupo-lawteck/.claude/CLAUDE.md` |
| Criado | `climatronico-blog/.claude/CLAUDE.md` |
| Criado | `relatorios_lawteck/.claude/CLAUDE.md` |
| Criado | `RepairHub/.claude/CLAUDE.md` |
| Criado | `.aios-core/development/workflows/ralph-loop.yaml` |
| Criado | `.aios-core/development/tasks/ralph-implement-story.md` |
| Criado | `.aios-core/development/tasks/ralph-verify-story.md` |
| Criado | `.claude/hooks/pre-compact.sh` |
| Criado | `docs/sessions/2026-02/2026-02-22-aios-optimization-tokens-speed.md` |

---

## Proximo passo sugerido

1. **Testar Ralph Loop** — criar 2-3 stories simples e rodar `*ralph-loop` pra validar o workflow end-to-end
2. **Testar compaction hooks** — sessao longa ate compactar e verificar que PreCompact salva snapshot e SessionStart re-injeta
3. **Revisar agent-log.jsonl** — apos algumas sessoes, analisar dados de duracao/turnos
4. **Considerar Stop hook com agent verification** — pra quality gate automatico antes do Claude parar

---

## Decisoes tomadas

- **273 vs 250 linhas:** ficou 23 linhas acima do target, mas todas as secoes criticas ficaram intocadas. Cortar mais exigiria remover info util (AIOS Master Commands, Brownfield Workflow, etc.)
- **Hooks no project settings (nao user):** hooks ficam em `.claude/settings.json` do projeto, nao em `~/.claude/settings.json`, pra serem compartilhaveis e especificos do workspace
- **SubagentStop sem matcher:** loga TODOS os subagents, nao so os do Ralph Loop — dados extras sao uteis pra entender uso geral
