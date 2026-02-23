---
paths: "**/supabase/**,**/migrations/**,**/*.sql"
---

# Supabase & SQL Rules

## Migration Files

- Naming: `YYYYMMDDHHMMSS_descriptive-slug.sql` (timestamp prefix)
- Header comment: `-- Story: ID` + `-- Date: YYYY-MM-DD`
- Wrap DDL in idempotent checks: `IF NOT EXISTS`, `CREATE OR REPLACE`
- Reference rollback file if migration is destructive

## RLS Pattern (Non-Negotiable)

Every new table MUST follow the 3-layer security model:

```sql
-- 1. Enable RLS
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- 2. Force RLS (even table owner respects policies)
ALTER TABLE table_name FORCE ROW LEVEL SECURITY;

-- 3. Revoke anon
REVOKE ALL ON table_name FROM anon;
```

Never skip FORCE or REVOKE. Anon key is public — security = RLS only.

## Policy Naming

- Format: `{table}_{operation}` (e.g., `services_select`, `clients_insert`)
- Always target `TO authenticated` (never `TO anon` or `TO public`)
- Role check via: `get_user_role() IN ('admin', 'role1', ...)`

## Roles

Grupo Lawteck: `admin`, `gestor`, `estoquista`, `tecnico`, `vendedor`, `expedicao`
RepairHub: `admin`, `tecnico_senior`, `tecnico`
Roles stored in: `auth.jwt()->'app_metadata'->>'role'`

## Required Patterns

- All tables must have `created_at TIMESTAMPTZ DEFAULT now()` and `updated_at TIMESTAMPTZ DEFAULT now()`
- Add `update_updated_at_column()` trigger on every table with `updated_at`
- Use CHECK constraints for enum-like fields: `CHECK (status IN (...))`
- Use `SECURITY DEFINER` on helper functions that read JWT claims
- FK constraints should specify ON DELETE behavior explicitly

## Client Usage

- Frontend: anon key via `import.meta.env.VITE_SUPABASE_ANON_KEY` (public, safe)
- Scripts: service_role key for admin operations (bypass RLS) — never in frontend code
- Queries: always destructure `const { data, error } = await supabase.from(...)`; always check error

## Before Any Schema Change

- Read the COMPLETE current schema (all tables, constraints, policies)
- Check existing migration files for patterns
- Verify RLS policies won't break after changes
- Test with both admin and non-admin roles
