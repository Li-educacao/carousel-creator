# Session Handoff — 2026-02-25

## Objetivo

Reorganizar workspace e home directory. Consolidar todos os projetos Lawteck numa estrutura unificada e limpar arquivos espalhados.

## O que foi feito

### 1. Reorganização Grupo Lawteck

Consolidou 5 projetos dispersos em `Projetos com IA/` dentro de `grupo-lawteck/`:

```
grupo-lawteck/
├── apps/
│   ├── erp/                  ← antigo grupo-lawteck/
│   ├── oraculo/              ← antigo oraculo-lawteck/
│   └── trafego/              ← antigo ads-integration-service/
├── tools/
│   ├── relatorios/           ← antigo relatorios_lawteck/
│   └── aliexpress-exporter/  ← antigo aliexpress-csv-exporter/ (da home)
├── assets/
│   └── landing-pecas/        ← antigo Landing page Lawteck peças/
└── README.md
```

- Cada app manteve seu `.git` — nenhuma história perdida
- `RepairHub/` deletado (estava vazio, era nome antigo do Oráculo)
- 7 PNGs do Oráculo movidos para `apps/oraculo/assets/design/`

### 2. Limpeza da Home (`~/lawhander/`)

| Ação | Itens |
|------|-------|
| **Deletados** | 12 scripts Meta Ads (tokens expirados), test.zip, teste_claude.txt, batch_mod00.sh, ProjetosLocal/ |
| **Criado ~/engenharia/** | comunicacao_midea → midea/, esp → esp-idf/, teste de compressor → compressor/, ghidra_scripts + uart_decode → tools/ |
| **Consolidado ~/mcp/** | mcp-youtube + server.js → mcp/youtube-mcp/ |
| **Movido** | Videos_Backup/ (19 vídeos, ~750MB) → ~/Movies/Backup/ |
| **Removidos** | package.json, package-lock.json, node_modules órfãos da home |

### 3. Configs atualizados

- `.claude/CLAUDE.md` — tabela de projetos atualizada (9 projetos, novos paths)
- `.gitignore` — removidas entradas obsoletas (RepairHub, oraculo-lawteck, etc.), adicionado pcb-autoplacer
- `MEMORY.md` — nova seção "Grupo Lawteck Reorganization", paths corrigidos, repos atualizados
- `grupo-lawteck/README.md` — criado com índice completo

### 4. Testes

Todos os 3 apps testados com `npm run dev`:

| App | Porta | Status |
|-----|-------|--------|
| ERP | 5173 | HTTP 200 |
| Oráculo | 5173 | HTTP 200 |
| Tráfego API | 3000 (`/health`) | HTTP 200 |
| Tráfego Web | 5173 | HTTP 200 |

### 5. Git

- Commit: `3e26a9e` — `chore: reorganize Grupo Lawteck projects into unified folder structure`
- Pushed para `Li-educacao/synkra-aios-custom` (main)

## Paths importantes (pós-reorganização)

| Antes | Depois |
|-------|--------|
| `grupo-lawteck/` | `grupo-lawteck/apps/erp/` |
| `oraculo-lawteck/` | `grupo-lawteck/apps/oraculo/` |
| `ads-integration-service/` | `grupo-lawteck/apps/trafego/` |
| `relatorios_lawteck/` | `grupo-lawteck/tools/relatorios/` |
| `Landing page Lawteck peças/` | `grupo-lawteck/assets/landing-pecas/` |
| `aliexpress-csv-exporter/` (home) | `grupo-lawteck/tools/aliexpress-exporter/` |

## Próximos passos (Fase 2 — futuro)

- Adicionar `turbo.json` e `package.json` root no `grupo-lawteck/`
- Criar `packages/ui/`, `packages/auth/`, `packages/supabase/` compartilhados
- Migrar Oráculo pro mesmo Supabase do ERP
- Unificar login e sidebar entre apps
- Configurar Vercel rewrites por path

## Notas

- Portas dos apps não estão hardcoded — Oráculo e Tráfego Web usam 5173 por padrão (mesmo do ERP). Quando rodam juntos, Vite faz auto-increment. Para o futuro com Turborepo, configurar portas fixas no vite.config de cada app.
- Home `~/lawhander/` agora está limpa: só pastas de sistema macOS + `Projetos com IA/`, `engenharia/`, `mcp/`, `bin/`, `go/`, `Postman/`.
