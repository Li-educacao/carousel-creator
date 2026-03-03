# Setor Financeiro — Grupo Lawteck (Phases 1-3)

**Status:** DONE
**Date:** 2026-03-03
**Epic:** Setor Financeiro completo no ERP

## Phase 1: Foundation

### Story 1.1 — Migration Schema v2
- [x] financial_transactions: source, external_id, raw_description, match_status
- [x] bank_accounts: bank_code, api_enabled, last_sync_at
- [x] bank_sync_logs table with RLS (admin only)
- [x] conciliation_proposals table with RLS (admin + vendedor)
- [x] FORCE RLS + REVOKE anon on all financial tables
- [x] Unique index (source, external_id) for dedup

### Story 1.2 — Routes + Menu
- [x] ProtectedRoute fixed — actually enforces allowedRoles
- [x] /financeiro, /financeiro/dre, /financeiro/conciliacoes, /financeiro/sync
- [x] financeiroMenu in useModuleMenu with "Setor Financeiro" sidebar
- [x] Conciliacoes visible for admin + vendedor

### Story 1.3 — SmartConciliation
- [x] Proposed tab: confirm/reject cards for auto-matched transactions
- [x] Unmatched tab: manual categorization with dropdown
- [x] Source badges (Inter/Cora), confidence scores

### Story 1.4 — Lawdame Jr admin
- [x] Already admin (lawdamejr@hotmail.com, role=admin)

## Phase 2: Python Bank Collector

### Story 2.1 — Scaffold
- [x] grupo-lawteck/tools/bank-collector/ (14 files)
- [x] FastAPI + APScheduler + httpx + supabase

### Story 2.2 — Banco Inter integration
- [x] OAuth2 + mTLS, GET /banking/v2/extrato
- [x] Transform + upsert with dedup

### Story 2.3 — Banco Cora integration
- [x] OAuth2 + mTLS, GET /bank-statement/statement
- [x] Same dedup pattern

### Story 2.4 — Matcher
- [x] Credits only, amount tolerance +/-R$0.50, date +/-3 days
- [x] Inter->board_sales, Cora->services
- [x] Never auto-confirms

### Story 2.5 — Scheduler + Telegram
- [x] Inter 7h, Cora 7:15, Matcher 7:30, Telegram 8h (BRT)
- [x] Manual endpoints: POST /collect/inter, /collect/cora, /match
- [x] API key protection

## Phase 3: Dashboard + DRE Real

### Story 3.1 — useFinancialDashboard hook
- [x] Period selector (today/week/month/quarter)
- [x] Consolidated queries: accounts, summary, daily breakdown, pendents, uncategorized

### Story 3.2 — Dashboard with real data
- [x] Chart.js Line: entradas vs saidas diarias
- [x] Period selector functional
- [x] Uncategorized count badge
- [x] Cards react to period

### Story 3.3 — DRE consolidado
- [x] 3 columns: current month | previous month | YTD
- [x] Uncategorized transactions banner
- [x] consolidated prop for no company_context filter

### Story 3.4 — Sync Management
- [x] "Sincronizar Agora" button per bank (POST to bank-collector)
- [x] Last sync + API status per account
- [x] Requires VITE_BANK_COLLECTOR_URL in .env

## Files Created/Modified

### New Files
- `grupo-lawteck/apps/erp/migration_financial_sector.sql`
- `grupo-lawteck/apps/erp/src/hooks/useFinancialDashboard.js`
- `grupo-lawteck/apps/erp/src/components/Financial/FinancialDashboard.jsx`
- `grupo-lawteck/apps/erp/src/components/Financial/SmartConciliation.jsx`
- `grupo-lawteck/tools/bank-collector/` (14 files)

### Modified Files
- `grupo-lawteck/apps/erp/src/components/Routing/AppRoutes.jsx`
- `grupo-lawteck/apps/erp/src/hooks/useModuleMenu.js`
- `grupo-lawteck/apps/erp/src/components/Financial/DREView.jsx`
- `grupo-lawteck/apps/erp/.env.example`

## Next Steps (Phase 4-5, future)
- Auto-categorization regex rules for debits
- Contas a Pagar/Receber with alerts
- Cash flow projection
- Monthly close, YTD comparisons, PDF/CSV export
- Deprecate Make.com + N8N
