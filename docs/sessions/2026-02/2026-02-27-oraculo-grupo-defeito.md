# Session: Oráculo — Defect Group Classification + Error Code Sub-Groups
**Date:** 2026-02-27
**Project:** grupo-lawteck/apps/oraculo

## What was done

### Phase 1: grupo_defeito feature (session anterior)

1. **SQL Migration** (`sql/009_grupo_defeito.sql`)
   - Added `grupo_defeito` column, auto-classification trigger (22 categories)
   - Replaced `get_defeitos_grouped_by_tipo` RPC → GROUP BY `grupo_defeito`
   - New RPC `get_defeitos_by_grupo_for_tipo`

2. **ETL Batch Script** (`etl/audit/batch/07_classify_defects.py`)
   - Classified 5,836 of 7,075 defeitos

3. **Frontend** — DefectGroupCard, defectCategories, useDefeitosByGrupo

### Phase 2: Deploy fix + UX improvements (esta sessao)

4. **Vercel deploy fix**
   - Diagnosticado: deploy automatico falhava porque user `lawhander` no GitHub nao tinha acesso ao time Vercel `lawteckeletronica`
   - Solucao: `vercel login` como `lawteckeletronica`, deploy manual com `git author lawteckeletronica@gmail.com`
   - **Dois projetos Vercel existem:** `oraculo` (novo, sem dominio) e `oraculo-lawteck` (com dominio `oraculo.lawteck.com.br`)
   - Linkado ao projeto correto: `vercel link --project oraculo-lawteck --scope lawteckeletronicas-projects`

5. **DefectVideoCard — sintomas em vez de modelo** (`e1f9355`)
   - Cards de defeito agora mostram `sintomas` (2 linhas) em vez de `modelo_maquina`
   - Linha secundaria: `codigo_placa · Nx relatado`

6. **Error Code Sub-Groups** (`5236c90`)
   - **SQL Migration** (`sql/010_error_code_groups.sql` + `supabase/migrations/20260227130000_error_code_groups.sql`)
     - `get_error_code_groups_by_tipo` — extrai codigos de erro (E1, P0, F5...) via regex, agrupa individualmente
     - `get_defeitos_by_error_code_for_tipo` — retorna defeitos de um codigo especifico
     - Applied via `supabase db push`
   - **Frontend**
     - `useErrorCodeGroups` + `useDefeitosByErrorCode` hooks
     - `ErrorCodeGroupCard` component (icone # vermelho, badge vermelho)
     - `DefeitosGroupPage` — error codes no topo, grupo `erro_codigo` removido dos grupos normais
   - **Resultado:** Carrier split-inverter tem 25 codigos de erro individuais (P0=7, E1=4, E2=3, etc.)

## Commits

| Hash | Message |
|------|---------|
| `fc6cec6` | feat: group defects by behavior/symptom instead of exact title |
| `e76cbd3` | chore: trigger Vercel redeploy for grupo_defeito feature |
| `6dd600b` | chore: redeploy grupo_defeito feature |
| `e1f9355` | fix: show sintomas instead of model number in defect cards |
| `5236c90` | feat: split error codes into individual groups on catalog page |

## Vercel Deploy — IMPORTANTE

- Vercel CLI logada como `lawteckeletronica` (nao `li-educacao`)
- Para deploy: `git config user.email "lawteckeletronica@gmail.com"` antes do commit, depois restaurar `lawhander@gmail.com`
- Projeto Vercel: `oraculo-lawteck` (scope: `lawteckeletronicas-projects`)
- Deploy manual: `vercel --prod --yes --scope lawteckeletronicas-projects`
- Deploy automatico via GitHub webhook esta falhando (user access issue)

## Distribution (post-classification)

| Category | Count | % |
|----------|-------|---|
| dicas_perguntas | 1,542 | 21.8% |
| reparo_geral | 1,239 | 17.5% |
| nao_liga | 1,127 | 15.9% |
| erro_codigo | 1,036 | 14.6% |
| comunicacao | 322 | 4.6% |
| + 17 more | 1,809 | 25.6% |

## Next steps

- Fix Vercel auto-deploy: aceitar convite ou adicionar `lawhander` ao time Vercel
- Refine `reparo_geral` bucket (17.5% remaining) iteratively
- Consider adding category filters to search
- Story 1.7 (Nova agent integration) — pendente
