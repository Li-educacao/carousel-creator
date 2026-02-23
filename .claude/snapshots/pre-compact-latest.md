# Pre-Compaction Snapshot v2
Saved at: 2026-02-23T02:28:45Z

## Active Projects
- **ads-integration-service** (branch: main): 33 uncommitted files | last commit: 3 hours ago
- **aios-squads** (branch: main): 13 uncommitted files | last commit: 12 days ago
- **climatronico-blog** (branch: main): 1 uncommitted files | last commit: 2 weeks ago
- **grupo-lawteck** (branch: main): 20 uncommitted files | last commit: 22 hours ago
- **oraculo-lawteck** (branch: main): 11 uncommitted files | last commit: 3 days ago

## Active Workflows
No active workflows

## Active PRD (summary)
No active PRD found

## Squads Used (recent)
(If empty, no squad-specific work detected)

## Ralph Loop
No active loop

## Recent Progress
No progress file

## Last 5 Subagents
- 2026-02-23T02:14:26Z |  | ? (0 turns, 0s)
- 2026-02-23T02:23:29Z |  | ? (0 turns, 0s)
- 2026-02-23T02:23:31Z |  | ? (0 turns, 0s)
- 2026-02-23T02:25:13Z |  | ? (0 turns, 0s)
- 2026-02-23T02:26:53Z |  | ? (0 turns, 0s)

## Active Stories
- [oraculo-lawteck] story-1.2-autenticacao.md: Story 1.2 — Autenticação e Controle de Acesso
  - [x] 1. Supabase Auth integrado com login por email/senha
  - [x] 2. Três papéis implementados via `app_metadata`: `admin`, `tecnico_senior`, `tecnico`
  - [x] 3. RLS policies configuradas: técnicos leem tudo, seniores podem aprovar, admin gerencia tudo
- [oraculo-lawteck] 3.1.0-feedback-analytics-vectorsearch.md: Story 3.1.0: Feedback Loop + Analytics + Vector Search
  - [ ] Feedback Loop: Técnicos podem avaliar cada defeito com rating 1-5 + notas
  - [ ] Analytics: Dashboard mostrando avg rating, efetividade, trends por defeito
  - [ ] Vector Search: Busca semântica ativa com pgvector, ranking por feedback
- [oraculo-lawteck] story-1.1-setup-projeto.md: Story 1.1 — Setup do Projeto e Infraestrutura
  - [x] 1. Projeto React + Vite + TailwindCSS criado e funcional no repositório `RepairHub/`
  - [x] 2. Radix UI e Lucide icons configurados
  - [x] 3. react-router-dom configurado com layout base (header, nav bottom, content area)
- [oraculo-lawteck] story-1.3-schema-banco.md: Story 1.3 — Schema do Banco de Dados
  - [x] 1. Tabela `fabricantes` (id, nome, logo_url)
  - [x] 2. Tabela `modelos_maquina` (id, fabricante_id, nome, tipo — split/inverter/etc)
  - [x] 3. Tabela `modelos_placa` (id, modelo_maquina_id, codigo_placa, potencia_btu, tipo_placa — evaporadora/condensadora/principal)
- [docs] 1.1.facebook-ads-mvp.md: Story 1.1: Facebook Ads Integration MVP - OAuth & Campaign Management
  - [ ] Pre-Commit (@dev): Run before marking story complete
  - [ ] Pre-PR (@github-devops): Run before creating pull request
  - [ ] Pre-Deployment (@github-devops): Run before deploying to Railway
- [climatronico-blog] story-4.2-pagination-toc.md: Story 4.2: Paginacao + Table of Contents
  - [x] Blog listing paginado (12 posts por pagina) — 58 posts / 5 paginas
  - [x] Componente Pagination com prev/next + numeros de pagina
  - [x] URLs SEO-friendly: `/blog/`, `/blog/2/`, `/blog/3/`
- [climatronico-blog] story-4.3-error-handling-ux.md: Story 4.3: Error Handling + UX Polish
  - [x] Pagina 500 criada com design consistente ao 404
  - [x] Skeleton screen componente reutilizavel (variantes: card, text, image)
  - [ ] Skeleton screen para search results — SKIPPED (busca e client-side instantanea, nao precisa)
- [climatronico-blog] epic-technical-debt.md: Epic: Resolucao de Debitos Tecnicos - Climatronico Blog
  - [Assessment Tecnico](../prd/technical-debt-assessment.md)
  - [Relatorio Executivo](../reports/TECHNICAL-DEBT-REPORT.md)
  - [Arquitetura do Sistema](../architecture/system-architecture.md)
- [climatronico-blog] story-4.1-image-performance.md: Story 4.1: Otimizacao de Imagens e Performance
  - [x] Imagens hero servidas com `<img>` real com width/height (antes era CSS background-image)
  - [x] PostCard e PostLayout usam `<img>` com width/height explicitos
  - [ ] `srcset` responsivo nos post cards — SKIPPED (imagens em public/, requer pre-geracao de multiplos tamanhos)

## Recent Architecture Decisions

