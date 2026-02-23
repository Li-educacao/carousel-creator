# AGENTS.md - AIOS for Codex (Workspace Root)

Este arquivo define como usar agentes AIOS no Codex, nesta pasta raiz:
`/Users/lawhander/Projetos com IA`

Objetivo:
- Permitir ativacao de agentes AIOS no Codex para todos os projetos dentro desta pasta.
- Manter configuracao do Claude Code separada (sem sobrescrever `.claude`).

## Escopo e isolamento

- Esta configuracao e exclusiva do Codex (`AGENTS.md` + `.codex/`).
- Nao editar arquivos de Claude (`.claude/`) automaticamente.
- Nao sobrescrever instalacoes AIOS existentes sem pedido explicito.

## Como ativar agentes no Codex

Preferencia (confiavel):
1. Use `/skills` e selecione `aios-<agent-id>` (ex.: `aios-dev`, `aios-architect`).
2. Em seguida, use comandos do proprio agente com prefixo `*` (ex.: `*help`, `*develop`).

Observacao:
- Alguns clientes Codex nao expõem `/skills` na interface.
- Nesses casos, trate comandos de slash como texto e aplique o roteador abaixo.

## Roteador de comandos (fallback para app sem /skills)

Se a mensagem do usuario for exatamente um dos atalhos abaixo, ativar o agente correspondente de `.codex/agents` e responder com greeting + comandos principais:

- `/aios-master` ou `/master` -> `.codex/agents/aios-master.md`
- `/analyst` -> `.codex/agents/analyst.md`
- `/architect` -> `.codex/agents/architect.md`
- `/data-engineer` -> `.codex/agents/data-engineer.md`
- `/dev` -> `.codex/agents/dev.md`
- `/devops` -> `.codex/agents/devops.md`
- `/pm` -> `.codex/agents/pm.md`
- `/po` -> `.codex/agents/po.md`
- `/qa` -> `.codex/agents/qa.md`
- `/sm` -> `.codex/agents/sm.md`
- `/squad-creator` -> `.codex/agents/squad-creator.md`
- `/ux` ou `/ux-design-expert` -> `.codex/agents/ux-design-expert.md`

Depois de ativado, comandos com `*` devem ser encaminhados para o agente ativo (`*help`, `*develop`, `*draft`, `*run-workflow`, etc.).

Fonte dos agentes no Codex:
- Primaria: `.codex/agents/*.md`
- Fallback (se necessario): `.claude/commands/AIOS/agents/*.md` em modo somente leitura

## Agentes disponiveis

- `aios-master`
- `analyst`
- `architect`
- `data-engineer`
- `dev`
- `devops`
- `pm`
- `po`
- `qa`
- `sm`
- `squad-creator`
- `ux-design-expert`

## Fluxo de trabalho multi-projeto

- Sempre confirmar o projeto alvo antes de executar mudancas.
- Entrar no diretorio do projeto escolhido e seguir as regras locais dele.
- Se houver `AGENTS.md` no projeto filho, ele tem prioridade para aquele projeto.

## Separacao Claude x Codex

- No Claude Code: use os agentes via `.claude/commands/...` como voce ja faz hoje.
- No Codex: use os agentes via `.codex/skills` ou `.codex/agents`.
- As duas integracoes coexistem sem conflito.
