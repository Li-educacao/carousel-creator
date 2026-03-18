# Architecture: Epic 1 — Hotmart Integration & Student Database

**Module:** Pedagógico — Gestão de Alunos
**Epic:** 1 of 5 — Hotmart Integration & Student Database
**Stories:** 1.1 (Schema + RBAC), 1.2 (Webhook Receiver), 1.3 (Student CRUD API), 1.4 (Student UI), 1.5 (Google Sheets Export)
**Author:** @architect
**Date:** 2026-03-18
**Status:** Ready for implementation

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Database Design](#2-database-design)
3. [API Architecture](#3-api-architecture)
4. [Frontend Architecture](#4-frontend-architecture)
5. [Hotmart Webhook Integration](#5-hotmart-webhook-integration)
6. [Google Sheets Export](#6-google-sheets-export)
7. [Implementation Order](#7-implementation-order)
8. [Risks & Decisions](#8-risks--decisions)

---

## 1. Architecture Overview

### 1.1 Position in Existing LIOS Architecture

LIOS currently has two active modules:

- **Social Media** (`modules/social-media/`) — Carousel Creator, mounted at `/api/v1/` on API and `/app/social-media` on web
- **Telegram Intelligence** (`modules/telegram-intelligence/`) — mounted at `/api/v1/telegram/` and `/app/alunos/inteligencia`

Epic 1 adds the **Pedagógico** module as the third module, following identical structural conventions. The module occupies:

- API: `apps/api/src/modules/pedagogico/` → mounted at `/api/v1/pedagogico/`
- Webhook: a separate public router at `/api/v1/webhooks/hotmart` (not inside the module, because it is public and requires different middleware)
- Web: `apps/web/src/modules/pedagogico/` → mounted at `/app/pedagogico/`

The existing `AppShell.tsx` sidebar already has the Pedagógico sector defined with green color tokens (`lios-green`). The `alunos` entry is currently `comingSoon: true` — that flag gets removed and routed to the new module.

### 1.2 Module Boundaries

```
┌─────────────────────────────────────────────────────────────────┐
│  LIOS Platform                                                  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Infra Layer                                            │   │
│  │  authMiddleware  |  requirePermission  |  supabaseAdmin │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐    │
│  │ social-media  │  │   pedagógico  │  │    webhooks/    │    │
│  │ /api/v1/      │  │ /api/v1/      │  │    hotmart      │    │
│  │ carousels     │  │ pedagogico/   │  │    (public)     │    │
│  │ templates     │  │ students      │  └────────┬────────┘    │
│  │ personas      │  │ classes       │           │             │
│  └───────────────┘  │ enrollments   │           │             │
│                     │ export/sheets │           │             │
│                     └───────┬───────┘           │             │
│                             │                   │             │
│  ┌──────────────────────────▼───────────────────▼──────────┐   │
│  │  Supabase (tqpkymereiyfxroiuaip)                        │   │
│  │  core_* tables   |   ped_* tables   |   tg_* tables    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Data Flow: Webhook → Student Creation

```
Hotmart Platform
     │
     │  POST /api/v1/webhooks/hotmart
     │  Header: X-Hotmart-Hottok: <secret>
     │  Body: { event: "PURCHASE_COMPLETE", data: {...} }
     ▼
Railway Express API
     │
     ├─ 1. Validate X-Hotmart-Hottok header (reject if invalid → 401)
     ├─ 2. Insert ped_webhook_logs { status: 'received', payload }
     ├─ 3. Respond 200 OK immediately (NFR1: < 5 seconds)
     │
     └─ 4. Background async processing (setImmediate / Promise chain):
           │
           ├─ 4a. HotmartService.parsePayload(payload)
           │       → extract: buyer email, name, phone, product_id, transaction_id
           │
           ├─ 4b. Idempotency check: SELECT from ped_enrollments
           │       WHERE hotmart_transaction = transaction_id
           │       → if found: log 'skipped_duplicate', exit
           │
           ├─ 4c. StudentService.upsertStudent(email, data)
           │       → INSERT ... ON CONFLICT (email) DO UPDATE
           │       → returns student_id
           │
           ├─ 4d. ClassService.resolveClass(product_hotmart_id)
           │       → SELECT ped_classes WHERE product_hotmart_id = ?
           │       → returns class_id (or null if unmapped)
           │
           ├─ 4e. EnrollmentService.createEnrollment(student_id, class_id, tx_data)
           │       → INSERT ped_enrollments
           │
           ├─ 4f. Update ped_webhook_logs { status: 'completed', processing_steps }
           │
           └─ Errors at any step → update ped_webhook_logs { status: 'failed', error_message }
                                  (each step is try/catch independent)
```

---

## 2. Database Design

### 2.1 Migration File Structure

**Naming convention** (matches existing `20260304120000_rbac_system.sql` pattern):

```
lios/supabase/migrations/
  20260318120000_ped_schema.sql          ← Story 1.1: all ped_* tables + RLS
  20260318130000_ped_rbac_permissions.sql ← Story 1.1: pedagogico permissions seed
  20260320120000_ped_sheets_columns.sql  ← Story 1.5: last_synced_at column (if needed)
```

Keep migrations minimal and additive. Never modify existing migration files.

### 2.2 Complete Schema — `20260318120000_ped_schema.sql`

```sql
-- ============================================================================
-- Pedagógico Module — Student Database Schema
-- Story: 1.1 — Database Schema & RBAC Setup
-- Date: 2026-03-18
-- Target: tqpkymereiyfxroiuaip.supabase.co
-- ============================================================================
-- Tables: ped_classes, ped_students, ped_enrollments, ped_webhook_logs,
--         ped_contract_templates, ped_contracts, ped_whatsapp_templates
-- RLS: 3-layer pattern (ENABLE + FORCE + REVOKE anon)
-- ============================================================================

-- ─── HELPER: ped role check ─────────────────────────────────────────────────
-- Mirrors tg_has_role pattern from telegram intelligence migration.

CREATE OR REPLACE FUNCTION ped_has_role(p_roles TEXT[])
RETURNS BOOLEAN
LANGUAGE sql
STABLE
SECURITY DEFINER
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM core_user_roles ur
    JOIN core_roles r ON r.id = ur.role_id
    WHERE ur.user_id = auth.uid()
      AND r.name = ANY(p_roles)
  );
$$;

-- ─── HELPER: updated_at trigger (reuse existing function if available) ────────

-- update_updated_at() already exists from rbac migration.
-- No need to recreate. Just attach trigger to new tables.

-- ─── TABLE: ped_classes ──────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_classes (
  id                        UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  name                      TEXT        NOT NULL,
  abbreviation              TEXT        NOT NULL UNIQUE,
  product_hotmart_id        TEXT,
  product_name              TEXT,
  start_date                DATE,
  end_date                  DATE,
  status                    TEXT        NOT NULL DEFAULT 'active'
                              CHECK (status IN ('active', 'completed', 'cancelled')),
  drive_folder_id           TEXT,
  sheets_spreadsheet_id     TEXT,
  whatsapp_welcome_template TEXT,
  contract_template_id      UUID,       -- FK to ped_contract_templates added below
  metadata                  JSONB       NOT NULL DEFAULT '{}',
  created_at                TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at                TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER ped_classes_updated_at
  BEFORE UPDATE ON ped_classes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ─── TABLE: ped_students ─────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_students (
  id                     UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  full_name              TEXT        NOT NULL,
  email                  TEXT        NOT NULL UNIQUE,
  phone                  TEXT,
  cpf                    TEXT,
  hotmart_buyer_email    TEXT,
  status                 TEXT        NOT NULL DEFAULT 'active'
                           CHECK (status IN ('active', 'inactive', 'cancelled', 'refunded')),
  google_contact_id      TEXT,
  notes                  TEXT,
  metadata               JSONB       NOT NULL DEFAULT '{}',
  created_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at             TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER ped_students_updated_at
  BEFORE UPDATE ON ped_students
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ─── TABLE: ped_enrollments ──────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_enrollments (
  id                    UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id            UUID        NOT NULL REFERENCES ped_students(id) ON DELETE CASCADE,
  class_id              UUID        REFERENCES ped_classes(id) ON DELETE SET NULL,
  hotmart_transaction   TEXT        UNIQUE,   -- idempotency key
  hotmart_product_id    TEXT,
  purchase_date         TIMESTAMPTZ,
  amount_paid           NUMERIC(10,2),
  payment_method        TEXT,
  status                TEXT        NOT NULL DEFAULT 'active'
                          CHECK (status IN ('active', 'cancelled', 'refunded', 'expired')),
  enrolled_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
  metadata              JSONB       NOT NULL DEFAULT '{}'  -- full webhook payload stored here
);

-- ─── TABLE: ped_contract_templates ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_contract_templates (
  id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT        NOT NULL,
  content     TEXT        NOT NULL,  -- HTML with {{variable}} placeholders
  variables   JSONB       NOT NULL DEFAULT '[]',
  is_default  BOOLEAN     NOT NULL DEFAULT false,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TRIGGER ped_contract_templates_updated_at
  BEFORE UPDATE ON ped_contract_templates
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Add FK now that ped_contract_templates exists
ALTER TABLE ped_classes
  ADD CONSTRAINT fk_ped_classes_contract_template
  FOREIGN KEY (contract_template_id) REFERENCES ped_contract_templates(id) ON DELETE SET NULL;

-- ─── TABLE: ped_contracts ────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_contracts (
  id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id        UUID        NOT NULL REFERENCES ped_students(id) ON DELETE CASCADE,
  enrollment_id     UUID        REFERENCES ped_enrollments(id) ON DELETE SET NULL,
  template_id       UUID        REFERENCES ped_contract_templates(id) ON DELETE SET NULL,
  status            TEXT        NOT NULL DEFAULT 'generated'
                      CHECK (status IN ('generated', 'sent', 'viewed', 'signed')),
  pdf_storage_path  TEXT,
  drive_file_id     TEXT,
  drive_url         TEXT,
  sent_at           TIMESTAMPTZ,
  viewed_at         TIMESTAMPTZ,
  signed_at         TIMESTAMPTZ,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── TABLE: ped_whatsapp_templates ──────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_whatsapp_templates (
  id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  name          TEXT        NOT NULL,
  class_id      UUID        REFERENCES ped_classes(id) ON DELETE SET NULL,
  message_text  TEXT        NOT NULL,
  attachments   JSONB       NOT NULL DEFAULT '[]',
  is_default    BOOLEAN     NOT NULL DEFAULT false,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── TABLE: ped_webhook_logs ─────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_webhook_logs (
  id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  source            TEXT        NOT NULL DEFAULT 'hotmart'
                      CHECK (source IN ('hotmart', 'manual')),
  event_type        TEXT,
  payload           JSONB       NOT NULL,
  status            TEXT        NOT NULL DEFAULT 'received'
                      CHECK (status IN ('received', 'processing', 'completed', 'failed', 'skipped')),
  error_message     TEXT,
  student_id        UUID        REFERENCES ped_students(id) ON DELETE SET NULL,
  enrollment_id     UUID        REFERENCES ped_enrollments(id) ON DELETE SET NULL,
  processing_steps  JSONB       NOT NULL DEFAULT '[]',
  processed_at      TIMESTAMPTZ,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 2.3 Indices Strategy

```sql
-- ─── INDICES ─────────────────────────────────────────────────────────────────

-- ped_students: primary lookup by email (webhook upsert) + status filters
CREATE INDEX IF NOT EXISTS idx_ped_students_email       ON ped_students (email);
CREATE INDEX IF NOT EXISTS idx_ped_students_status      ON ped_students (status);
CREATE INDEX IF NOT EXISTS idx_ped_students_created_at  ON ped_students (created_at DESC);

-- ped_enrollments: join paths + idempotency check
CREATE INDEX IF NOT EXISTS idx_ped_enrollments_student  ON ped_enrollments (student_id);
CREATE INDEX IF NOT EXISTS idx_ped_enrollments_class    ON ped_enrollments (class_id);
CREATE INDEX IF NOT EXISTS idx_ped_enrollments_tx       ON ped_enrollments (hotmart_transaction);
CREATE INDEX IF NOT EXISTS idx_ped_enrollments_status   ON ped_enrollments (status);

-- ped_webhook_logs: admin monitoring + chronological display
CREATE INDEX IF NOT EXISTS idx_ped_webhook_logs_created ON ped_webhook_logs (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ped_webhook_logs_status  ON ped_webhook_logs (status);

-- ped_classes: product mapping (webhook resolution)
CREATE INDEX IF NOT EXISTS idx_ped_classes_product_id   ON ped_classes (product_hotmart_id);
```

### 2.4 RLS Policies

**Pattern:** identical to `tg_*` tables in `20260315180000_telegram_intelligence.sql` — use `ped_has_role()` helper.

```sql
-- ─── RLS: ped_classes ────────────────────────────────────────────────────────

ALTER TABLE ped_classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_classes FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_classes FROM anon;

CREATE POLICY "ped_classes_select"
  ON ped_classes FOR SELECT
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_classes_insert"
  ON ped_classes FOR INSERT
  TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_classes_update"
  ON ped_classes FOR UPDATE
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']))
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_classes_delete"
  ON ped_classes FOR DELETE
  TO authenticated
  USING (ped_has_role(ARRAY['admin']));

-- ─── RLS: ped_students ───────────────────────────────────────────────────────

ALTER TABLE ped_students ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_students FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_students FROM anon;

CREATE POLICY "ped_students_select"
  ON ped_students FOR SELECT
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_students_insert"
  ON ped_students FOR INSERT
  TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_students_update"
  ON ped_students FOR UPDATE
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']))
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_students_delete"
  ON ped_students FOR DELETE
  TO authenticated
  USING (ped_has_role(ARRAY['admin']));

-- ─── RLS: ped_enrollments ────────────────────────────────────────────────────

ALTER TABLE ped_enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_enrollments FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_enrollments FROM anon;

CREATE POLICY "ped_enrollments_select"
  ON ped_enrollments FOR SELECT
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_enrollments_insert"
  ON ped_enrollments FOR INSERT
  TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_enrollments_update"
  ON ped_enrollments FOR UPDATE
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']))
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

-- ─── RLS: ped_webhook_logs ───────────────────────────────────────────────────
-- Admin-only write; pedagogico can read for monitoring

ALTER TABLE ped_webhook_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_webhook_logs FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_webhook_logs FROM anon;

CREATE POLICY "ped_webhook_logs_select"
  ON ped_webhook_logs FOR SELECT
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_webhook_logs_insert"
  ON ped_webhook_logs FOR INSERT
  TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin']));

-- ─── RLS: ped_contract_templates ─────────────────────────────────────────────

ALTER TABLE ped_contract_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_contract_templates FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_contract_templates FROM anon;

CREATE POLICY "ped_contract_templates_select"
  ON ped_contract_templates FOR SELECT
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_contract_templates_write"
  ON ped_contract_templates FOR ALL
  TO authenticated
  USING (ped_has_role(ARRAY['admin']))
  WITH CHECK (ped_has_role(ARRAY['admin']));

-- ─── RLS: ped_contracts ──────────────────────────────────────────────────────

ALTER TABLE ped_contracts ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_contracts FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_contracts FROM anon;

CREATE POLICY "ped_contracts_select"
  ON ped_contracts FOR SELECT
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_contracts_write"
  ON ped_contracts FOR ALL
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']))
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

-- ─── RLS: ped_whatsapp_templates ─────────────────────────────────────────────

ALTER TABLE ped_whatsapp_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_whatsapp_templates FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_whatsapp_templates FROM anon;

CREATE POLICY "ped_whatsapp_templates_select"
  ON ped_whatsapp_templates FOR SELECT
  TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_whatsapp_templates_write"
  ON ped_whatsapp_templates FOR ALL
  TO authenticated
  USING (ped_has_role(ARRAY['admin']))
  WITH CHECK (ped_has_role(ARRAY['admin']));
```

### 2.5 RBAC Seed — `20260318130000_ped_rbac_permissions.sql`

```sql
-- ============================================================================
-- Pedagógico Module — RBAC Permissions Seed
-- Story: 1.1 — Database Schema & RBAC Setup
-- Date: 2026-03-18
-- ============================================================================
-- Extends existing core_permissions without altering social-media:* entries.
-- ============================================================================

INSERT INTO core_permissions (module, action, description) VALUES
  ('pedagogico', 'read',  'Visualizar alunos, turmas, matrículas e contratos'),
  ('pedagogico', 'write', 'Criar e editar alunos, turmas e matrículas'),
  ('pedagogico', 'admin', 'Configurações pedagógicas, templates, export, logs de webhook')
ON CONFLICT (module, action) DO NOTHING;

-- admin role receives all pedagogico permissions
INSERT INTO core_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM core_roles r
CROSS JOIN core_permissions p
WHERE r.name = 'admin'
  AND p.module = 'pedagogico'
ON CONFLICT DO NOTHING;

-- pedagogico role receives read + write (not admin)
INSERT INTO core_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM core_roles r
CROSS JOIN core_permissions p
WHERE r.name = 'pedagogico'
  AND p.module = 'pedagogico'
  AND p.action IN ('read', 'write')
ON CONFLICT DO NOTHING;
```

### 2.6 Seed Data (Development)

Append to `20260318130000_ped_rbac_permissions.sql`:

```sql
-- ─── DEV SEED: sample class ──────────────────────────────────────────────────
-- For local development only. Skip in production via conditional check.

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM ped_classes WHERE abbreviation = 'TEC01') THEN
    INSERT INTO ped_classes (name, abbreviation, product_name, status)
    VALUES (
      'Turma Técnico em Climatização 01',
      'TEC01',
      'Técnico em Climatização — Turma 01',
      'active'
    );
  END IF;
END;
$$;
```

### 2.7 Important Schema Notes

**Why `hotmart_transaction` is UNIQUE on `ped_enrollments`:** This is the primary idempotency mechanism. When the same webhook arrives twice, the `INSERT` into `ped_enrollments` will fail with a unique constraint violation, which the service catches and converts to a `skipped_duplicate` log entry.

**Why `class_id` is nullable on `ped_enrollments`:** A product in Hotmart may not yet be mapped to a class in the system. Students can be created without a class, and the enrollment stores `hotmart_product_id` for later mapping when an admin creates the class.

**Why `ped_webhook_logs` uses `supabaseAdmin` (bypasses RLS) for inserts:** The webhook endpoint is public and runs without a JWT. The service layer uses `supabaseAdmin` with the service role key for webhook log creation. This is safe because webhook logs are not user-accessible via the anon key.

---

## 3. API Architecture

### 3.1 Module File Structure

```
apps/api/src/
  modules/
    pedagogico/
      index.ts                    ← module router (matches social-media/index.ts pattern)
      routes/
        student.routes.ts
        class.routes.ts
        enrollment.routes.ts
        export.routes.ts
      services/
        hotmart.service.ts
        student.service.ts
        class.service.ts
        google-sheets.service.ts
      queue/
        webhook-processor.ts      ← async pipeline runner
  routes/
    index.ts                      ← ADD: import pedagogicoRouter, webhookRouter
    webhooks.ts                   ← NEW: public webhook endpoints (no auth middleware)
```

### 3.2 Module Router — `modules/pedagogico/index.ts`

```typescript
import { Router } from 'express';
import { authMiddleware } from '../../middleware/auth.js';
import { requirePermission } from '../../middleware/rbac.js';
import studentRoutes from './routes/student.routes.js';
import classRoutes from './routes/class.routes.js';
import enrollmentRoutes from './routes/enrollment.routes.js';
import exportRoutes from './routes/export.routes.js';

const pedagogicoRouter = Router();

// All pedagogico routes require authentication
pedagogicoRouter.use(authMiddleware);

pedagogicoRouter.use('/students',    studentRoutes);
pedagogicoRouter.use('/classes',     classRoutes);
pedagogicoRouter.use('/enrollments', enrollmentRoutes);
pedagogicoRouter.use('/export',      exportRoutes);

export default pedagogicoRouter;
```

### 3.3 RBAC Middleware — `middleware/rbac.ts`

This middleware does not exist yet. It needs to be created once and reused across modules.

```typescript
// apps/api/src/middleware/rbac.ts
import { Request, Response, NextFunction } from 'express';
import type { AuthenticatedRequest } from './auth.js';
import { supabaseAdmin } from '../lib/supabase.js';

export function requirePermission(permission: string) {
  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const { user } = req as AuthenticatedRequest;
    const [module, action] = permission.split(':');

    const { data, error } = await supabaseAdmin
      .rpc('has_permission', { p_user_id: user.id, p_module: module, p_action: action });

    if (error || !data) {
      res.status(403).json({
        error: { message: 'Permissão insuficiente', code: 'FORBIDDEN' },
      });
      return;
    }

    next();
  };
}
```

**Note:** `has_permission()` is an existing SQL function from `20260304120000_rbac_system.sql`. Admin users automatically pass because `has_permission()` checks the role-permission chain, and admin has all permissions assigned in the seed.

### 3.4 Route Definitions

#### Student Routes — `routes/student.routes.ts`

```typescript
import { Router, Request, Response } from 'express';
import { requirePermission } from '../../../middleware/rbac.js';
import { StudentService } from '../services/student.service.js';

const router = Router();
const studentService = new StudentService();

// GET /api/v1/pedagogico/students
// Permissions: pedagogico:read
// Query: ?page=1&limit=20&class_id=uuid&status=active&search=nome
router.get('/', requirePermission('pedagogico:read'), async (req: Request, res: Response): Promise<void> => { ... });

// GET /api/v1/pedagogico/students/:id
// Permissions: pedagogico:read
// Returns: student + enrollments (with class data) + contracts
router.get('/:id', requirePermission('pedagogico:read'), async (req: Request, res: Response): Promise<void> => { ... });

// PATCH /api/v1/pedagogico/students/:id
// Permissions: pedagogico:write
// Body: Partial<{ full_name, phone, cpf, notes, status }>
router.patch('/:id', requirePermission('pedagogico:write'), async (req: Request, res: Response): Promise<void> => { ... });

// DELETE /api/v1/pedagogico/students/:id   (soft delete: status = 'inactive')
// Permissions: pedagogico:admin
router.delete('/:id', requirePermission('pedagogico:admin'), async (req: Request, res: Response): Promise<void> => { ... });

export default router;
```

#### Class Routes — `routes/class.routes.ts`

```typescript
// GET  /api/v1/pedagogico/classes          → requirePermission('pedagogico:read')
// POST /api/v1/pedagogico/classes          → requirePermission('pedagogico:write')
// GET  /api/v1/pedagogico/classes/:id      → requirePermission('pedagogico:read')  (includes students)
// PATCH /api/v1/pedagogico/classes/:id     → requirePermission('pedagogico:write')
```

#### Enrollment Routes — `routes/enrollment.routes.ts`

```typescript
// GET /api/v1/pedagogico/enrollments?student_id=&class_id=&status=
// → requirePermission('pedagogico:read')
```

#### Export Routes — `routes/export.routes.ts`

```typescript
// POST /api/v1/pedagogico/export/sheets    → requirePermission('pedagogico:admin')
// Body: { class_id?: string }  (null = full consolidated export)
```

### 3.5 Webhook Route — `routes/webhooks.ts`

This lives **outside** the pedagogico module because it is public (no JWT auth) and uses a different middleware chain.

```typescript
// apps/api/src/routes/webhooks.ts
import { Router, Request, Response } from 'express';
import { supabaseAdmin } from '../lib/supabase.js';
import { validateHotmartSignature } from '../modules/pedagogico/services/hotmart.service.js';
import { processWebhookAsync } from '../modules/pedagogico/queue/webhook-processor.js';

const webhookRouter = Router();

// POST /api/v1/webhooks/hotmart
// Public — no authMiddleware.
// Security: X-Hotmart-Hottok header validation.
webhookRouter.post('/hotmart', async (req: Request, res: Response): Promise<void> => {
  // 1. Validate signature
  const hottok = req.headers['x-hotmart-hottok'] as string | undefined;
  if (!validateHotmartSignature(hottok)) {
    res.status(401).json({ error: { message: 'Invalid signature', code: 'INVALID_SIGNATURE' } });
    return;
  }

  const payload = req.body as Record<string, unknown>;
  const eventType = (payload['event'] as string) ?? 'UNKNOWN';

  // 2. Log immediately (supabaseAdmin bypasses RLS — webhook has no JWT)
  const { data: logEntry, error: logError } = await supabaseAdmin
    .from('ped_webhook_logs')
    .insert({
      source: 'hotmart',
      event_type: eventType,
      payload,
      status: 'received',
    })
    .select('id')
    .single();

  if (logError || !logEntry) {
    console.error('[webhook/hotmart] Failed to create log entry:', logError);
    // Still respond 200 to Hotmart to avoid retries
    res.status(200).json({ received: true });
    return;
  }

  // 3. Respond immediately (NFR1)
  res.status(200).json({ received: true, log_id: logEntry.id });

  // 4. Process async (does NOT await — fire and forget)
  setImmediate(() => {
    processWebhookAsync(logEntry.id as string, payload, eventType).catch((err) => {
      console.error('[webhook/hotmart] Async processing error:', err);
    });
  });
});

export default webhookRouter;
```

### 3.6 Async Webhook Processor — `queue/webhook-processor.ts`

```typescript
// apps/api/src/modules/pedagogico/queue/webhook-processor.ts

import { supabaseAdmin } from '../../../lib/supabase.js';
import { HotmartService } from '../services/hotmart.service.js';
import { StudentService } from '../services/student.service.js';
import { ClassService } from '../services/class.service.js';

type ProcessingStep = {
  step: string;
  status: 'success' | 'failed' | 'skipped';
  data?: unknown;
  error?: string;
  timestamp: string;
};

export async function processWebhookAsync(
  logId: string,
  payload: Record<string, unknown>,
  eventType: string
): Promise<void> {
  const steps: ProcessingStep[] = [];
  const now = () => new Date().toISOString();

  // Mark as processing
  await supabaseAdmin
    .from('ped_webhook_logs')
    .update({ status: 'processing' })
    .eq('id', logId);

  try {
    // Only process purchase events in Epic 1
    const purchaseEvents = ['PURCHASE_APPROVED', 'PURCHASE_COMPLETE'];
    const cancelEvents   = ['PURCHASE_REFUNDED', 'PURCHASE_CANCELED'];

    if (!purchaseEvents.includes(eventType) && !cancelEvents.includes(eventType)) {
      steps.push({ step: 'event_filter', status: 'skipped', data: { reason: 'unhandled_event_type', eventType }, timestamp: now() });
      await finalizeLog(logId, 'completed', null, null, steps);
      return;
    }

    // Step 1: Parse payload
    const hotmartService = new HotmartService();
    const parsed = hotmartService.parsePayload(payload);
    steps.push({ step: 'parse_payload', status: 'success', data: { transaction: parsed.transactionId, email: parsed.email }, timestamp: now() });

    if (cancelEvents.includes(eventType)) {
      // Handle cancellation: update enrollment status
      await handleCancellation(logId, parsed, eventType, steps, now);
      return;
    }

    // Step 2: Idempotency check
    const { data: existing } = await supabaseAdmin
      .from('ped_enrollments')
      .select('id')
      .eq('hotmart_transaction', parsed.transactionId)
      .maybeSingle();

    if (existing) {
      steps.push({ step: 'idempotency_check', status: 'skipped', data: { reason: 'duplicate_transaction' }, timestamp: now() });
      await finalizeLog(logId, 'completed', null, null, steps);
      return;
    }
    steps.push({ step: 'idempotency_check', status: 'success', timestamp: now() });

    // Step 3: Upsert student
    const studentService = new StudentService();
    const student = await studentService.upsertStudent({
      email:      parsed.email,
      full_name:  parsed.buyerName,
      phone:      parsed.phone,
      hotmart_buyer_email: parsed.buyerEmail,
      metadata:   { hotmart_name: parsed.buyerName },
    });
    steps.push({ step: 'upsert_student', status: 'success', data: { student_id: student.id }, timestamp: now() });

    // Step 4: Resolve class from product ID
    const classService = new ClassService();
    const resolvedClass = await classService.resolveByProductId(parsed.productId);
    steps.push({
      step: 'resolve_class',
      status: resolvedClass ? 'success' : 'skipped',
      data: { class_id: resolvedClass?.id ?? null, reason: resolvedClass ? undefined : 'no_class_mapped' },
      timestamp: now(),
    });

    // Step 5: Create enrollment
    const { data: enrollment, error: enrollError } = await supabaseAdmin
      .from('ped_enrollments')
      .insert({
        student_id:          student.id,
        class_id:            resolvedClass?.id ?? null,
        hotmart_transaction: parsed.transactionId,
        hotmart_product_id:  parsed.productId,
        purchase_date:       parsed.purchaseDate,
        amount_paid:         parsed.amount,
        payment_method:      parsed.paymentMethod,
        status:              'active',
        metadata:            payload,
      })
      .select('id')
      .single();

    if (enrollError || !enrollment) {
      throw new Error(`Failed to create enrollment: ${enrollError?.message}`);
    }
    steps.push({ step: 'create_enrollment', status: 'success', data: { enrollment_id: enrollment.id }, timestamp: now() });

    await finalizeLog(logId, 'completed', student.id, enrollment.id, steps);

  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    console.error(`[webhook-processor] Log ${logId} failed:`, message);
    steps.push({ step: 'fatal_error', status: 'failed', error: message, timestamp: now() });
    await finalizeLog(logId, 'failed', null, null, steps, message);
  }
}

async function handleCancellation(
  logId: string,
  parsed: ReturnType<HotmartService['parsePayload']>,
  eventType: string,
  steps: ProcessingStep[],
  now: () => string
): Promise<void> {
  const newStatus = eventType === 'PURCHASE_REFUNDED' ? 'refunded' : 'cancelled';
  const { error } = await supabaseAdmin
    .from('ped_enrollments')
    .update({ status: newStatus })
    .eq('hotmart_transaction', parsed.transactionId);

  steps.push({
    step: 'update_enrollment_status',
    status: error ? 'failed' : 'success',
    data: { new_status: newStatus, transaction: parsed.transactionId },
    error: error?.message,
    timestamp: now(),
  });

  await finalizeLog(logId, error ? 'failed' : 'completed', null, null, steps, error?.message);
}

async function finalizeLog(
  logId: string,
  status: 'completed' | 'failed',
  studentId: string | null,
  enrollmentId: string | null,
  steps: ProcessingStep[],
  errorMessage?: string
): Promise<void> {
  await supabaseAdmin
    .from('ped_webhook_logs')
    .update({
      status,
      student_id:       studentId,
      enrollment_id:    enrollmentId,
      processing_steps: steps,
      processed_at:     new Date().toISOString(),
      error_message:    errorMessage ?? null,
    })
    .eq('id', logId);
}
```

### 3.7 Service Layer Design

#### `services/hotmart.service.ts`

```typescript
import { config } from '../../../config.js';

export interface HotmartParsedPayload {
  transactionId: string;
  productId:     string;
  email:         string;         // student email (product_sub_id → first_user_email)
  buyerEmail:    string;         // buyer email (may differ from student)
  buyerName:     string;
  phone:         string | null;
  amount:        number | null;
  paymentMethod: string | null;
  purchaseDate:  string | null;
  eventType:     string;
}

export class HotmartService {
  /**
   * Validates the X-Hotmart-Hottok header.
   * Hotmart sends a static secret string (not HMAC) in this header.
   * Docs: https://developers.hotmart.com/docs/pt-BR/webhook
   */
  parsePayload(raw: Record<string, unknown>): HotmartParsedPayload {
    // Hotmart payload structure (PURCHASE_COMPLETE):
    // {
    //   event: "PURCHASE_COMPLETE",
    //   id: "...",
    //   creation_date: 1234567890000,
    //   data: {
    //     product: { id: 123, name: "..." },
    //     purchase: {
    //       transaction: "HP123456789",
    //       approved_date: 1234567890000,
    //       payment: { value: { cents: 59700, currency_value: "BRL" }, type: "CREDIT_CARD" }
    //     },
    //     buyer: { name: "João Silva", email: "joao@email.com", checkout_phone: "+5511999..." }
    //     producer: { ... }
    //     subscription: { ... }  // only if subscription product
    //   }
    // }

    const data = (raw['data'] as Record<string, unknown>) ?? {};
    const buyer = (data['buyer'] as Record<string, unknown>) ?? {};
    const purchase = (data['purchase'] as Record<string, unknown>) ?? {};
    const product = (data['product'] as Record<string, unknown>) ?? {};
    const payment = (purchase['payment'] as Record<string, unknown>) ?? {};
    const paymentValue = (payment['value'] as Record<string, unknown>) ?? {};

    const transactionId = (purchase['transaction'] as string) ?? '';
    if (!transactionId) throw new Error('Missing purchase.transaction in webhook payload');

    const buyerEmail = (buyer['email'] as string) ?? '';
    if (!buyerEmail) throw new Error('Missing buyer.email in webhook payload');

    const amountCents = paymentValue['cents'] as number | undefined;

    return {
      transactionId,
      productId:     String((product['id'] as number) ?? ''),
      email:         buyerEmail,
      buyerEmail,
      buyerName:     (buyer['name'] as string) ?? '',
      phone:         (buyer['checkout_phone'] as string) ?? null,
      amount:        amountCents != null ? amountCents / 100 : null,
      paymentMethod: (payment['type'] as string) ?? null,
      purchaseDate:  purchase['approved_date']
                       ? new Date(purchase['approved_date'] as number).toISOString()
                       : null,
      eventType:     (raw['event'] as string) ?? '',
    };
  }
}

export function validateHotmartSignature(hottok: string | undefined): boolean {
  if (!config.hotmartWebhookSecret) {
    console.warn('[hotmart] HOTMART_WEBHOOK_SECRET not set — allowing all webhooks (dev mode)');
    return true;
  }
  return hottok === config.hotmartWebhookSecret;
}
```

**Note on Hotmart authentication:** Hotmart uses a simple static token comparison (not HMAC-SHA256). The `X-Hotmart-Hottok` header contains the `hottok` value configured in the Hotmart webhook settings, and the API compares it against `HOTMART_WEBHOOK_SECRET`. This is simpler than HMAC but requires keeping the secret secure.

#### `services/student.service.ts`

```typescript
import { supabaseAdmin } from '../../../lib/supabase.js';

interface UpsertStudentData {
  email:              string;
  full_name:          string;
  phone?:             string | null;
  hotmart_buyer_email?: string;
  metadata?:          Record<string, unknown>;
}

export class StudentService {
  async upsertStudent(data: UpsertStudentData) {
    const { data: student, error } = await supabaseAdmin
      .from('ped_students')
      .upsert(
        {
          email:               data.email,
          full_name:           data.full_name,
          phone:               data.phone ?? null,
          hotmart_buyer_email: data.hotmart_buyer_email ?? null,
          metadata:            data.metadata ?? {},
        },
        {
          onConflict: 'email',
          // Update name/phone if the student already exists — latest data wins
          ignoreDuplicates: false,
        }
      )
      .select('id, email, full_name, status')
      .single();

    if (error || !student) {
      throw new Error(`StudentService.upsertStudent failed: ${error?.message}`);
    }

    return student;
  }

  async getStudentList(params: {
    page: number;
    limit: number;
    classId?: string;
    status?: string;
    search?: string;
  }) {
    const offset = (params.page - 1) * params.limit;

    // Base query: students with their class memberships via enrollments
    let query = supabaseAdmin
      .from('ped_students')
      .select(`
        *,
        ped_enrollments (
          id, status, purchase_date, hotmart_product_id,
          ped_classes ( id, name, abbreviation )
        )
      `, { count: 'exact' })
      .eq('ped_enrollments.status', 'active')  // only show active enrollments in list
      .order('created_at', { ascending: false })
      .range(offset, offset + params.limit - 1);

    if (params.status) query = query.eq('status', params.status);

    if (params.classId) {
      // Filter students who have an enrollment in the given class
      query = query.eq('ped_enrollments.class_id', params.classId);
    }

    if (params.search && params.search.trim().length > 0) {
      const q = params.search.trim();
      query = query.or(`full_name.ilike.%${q}%,email.ilike.%${q}%`);
    }

    return query;
  }
}
```

#### `services/class.service.ts`

```typescript
import { supabaseAdmin } from '../../../lib/supabase.js';

export class ClassService {
  async resolveByProductId(productId: string) {
    const { data } = await supabaseAdmin
      .from('ped_classes')
      .select('id, name, abbreviation')
      .eq('product_hotmart_id', productId)
      .eq('status', 'active')
      .maybeSingle();

    return data;
  }

  async getClassWithStudents(classId: string) {
    const { data, error } = await supabaseAdmin
      .from('ped_classes')
      .select(`
        *,
        ped_enrollments (
          id, status, purchase_date,
          ped_students ( id, full_name, email, phone, status )
        )
      `)
      .eq('id', classId)
      .single();

    if (error) throw new Error(`ClassService.getClassWithStudents: ${error.message}`);
    return data;
  }
}
```

### 3.8 Config Extension — `config.ts`

Add new environment variables:

```typescript
export const config = {
  // ... existing keys ...
  hotmartWebhookSecret:    process.env.HOTMART_WEBHOOK_SECRET || '',
  hotmartToken:            process.env.HOTMART_TOKEN || '',
  googleServiceAccountJson: process.env.GOOGLE_SERVICE_ACCOUNT_JSON || '',
  googleSheetConsolidatedId: process.env.GOOGLE_SHEETS_CONSOLIDATED_ID || '',
} as const;
```

### 3.9 Routes Index Update — `routes/index.ts`

```typescript
import { Router, Request, Response } from 'express';
import socialMediaRouter from '../modules/social-media/index.js';
import telegramRouter from '../modules/telegram-intelligence/routes.js';
import pedagogicoRouter from '../modules/pedagogico/index.js';
import webhookRouter from './webhooks.js';

const router = Router();

router.get('/', (_req: Request, res: Response): void => {
  res.json({ message: 'LIOS API', version: '1.0.0' });
});

router.use('/v1', socialMediaRouter);
router.use('/v1/telegram', telegramRouter);
router.use('/v1/pedagogico', pedagogicoRouter);
router.use('/v1/webhooks', webhookRouter);

export default router;
```

### 3.10 Error Response Conventions

All error responses follow the existing pattern established in `carousel.routes.ts`:

```json
{ "error": { "message": "Mensagem em pt-BR para o usuário", "code": "SNAKE_CASE_CODE" } }
```

Common codes for this module:
- `INVALID_SIGNATURE` — webhook signature validation failed
- `DUPLICATE_TRANSACTION` — idempotent webhook re-delivery
- `STUDENT_NOT_FOUND` — 404 on student lookup
- `CLASS_NOT_FOUND` — 404 on class lookup
- `VALIDATION_ERROR` — bad request body
- `DB_ERROR` — Supabase query failure
- `FORBIDDEN` — requirePermission gate

---

## 4. Frontend Architecture

### 4.1 Module File Structure

```
apps/web/src/
  modules/
    pedagogico/
      routes.tsx                     ← lazy route definitions (matches social-media/routes.tsx)
      pages/
        DashboardPage.tsx
        StudentsPage.tsx
        StudentDetailPage.tsx
        ClassesPage.tsx
        ClassDetailPage.tsx
        WebhookLogPage.tsx
        ComingSoonSettingsPage.tsx    ← placeholder for Epic settings
      components/
        StudentTable.tsx
        ClassCard.tsx
        MetricsCards.tsx
        WebhookLogTable.tsx
        EnrollmentHistory.tsx
      hooks/
        useStudents.ts
        useClasses.ts
        usePedagogicoMetrics.ts
        useWebhookLogs.ts
```

### 4.2 Module Routes — `modules/pedagogico/routes.tsx`

```typescript
import { lazy } from 'react';
import { Route, Navigate } from 'react-router-dom';

const DashboardPage     = lazy(() => import('./pages/DashboardPage'));
const StudentsPage      = lazy(() => import('./pages/StudentsPage'));
const StudentDetailPage = lazy(() => import('./pages/StudentDetailPage'));
const ClassesPage       = lazy(() => import('./pages/ClassesPage'));
const ClassDetailPage   = lazy(() => import('./pages/ClassDetailPage'));
const WebhookLogPage    = lazy(() => import('./pages/WebhookLogPage'));

export const pedagogicoRoutes = (
  <>
    <Route index element={<Navigate to="alunos" replace />} />
    <Route path="dashboard"        element={<DashboardPage />} />
    <Route path="alunos"           element={<StudentsPage />} />
    <Route path="alunos/:id"       element={<StudentDetailPage />} />
    <Route path="turmas"           element={<ClassesPage />} />
    <Route path="turmas/:id"       element={<ClassDetailPage />} />
    <Route path="webhook-logs"     element={<WebhookLogPage />} />
  </>
);
```

### 4.3 App.tsx Integration

Replace the existing `<Route path="alunos" element={<ComingSoonPage moduleName="Alunos" />} />` with:

```typescript
import { pedagogicoRoutes } from './modules/pedagogico/routes';

// Inside <Route path="/app" element={<ProtectedRoute />}>:
<Route path="pedagogico">
  {pedagogicoRoutes}
</Route>
```

The route path is `/app/pedagogico/*`. The sidebar entry for "Alunos" must update its `path` from `/app/alunos` to `/app/pedagogico/alunos` and remove `comingSoon: true`.

### 4.4 AppShell Sidebar Update

In `AppShell.tsx`, update the Pedagógico group's "Alunos" entry:

```typescript
// In NAV_GROUPS, Pedagógico sector:
{ label: 'Alunos', path: '/app/pedagogico', icon: <Users size={18} />, permission: 'pedagogico:read' },
```

Also add breadcrumb labels for new segments:

```typescript
// In Breadcrumb labels map:
'pedagogico':     { label: 'Pedagógico', color: 'text-lios-green' },
'turmas':         { label: 'Turmas', color: 'text-lios-green' },
'webhook-logs':   { label: 'Logs de Webhook', color: 'text-lios-green' },
'dashboard':      { label: 'Dashboard Pedagógico', color: 'text-lios-green' },
```

### 4.5 Hook Design

All hooks follow the `useCarousel.ts` pattern exactly: `useState` + `useCallback`, return plain object, call `api.*` from `lib/api.ts`.

#### `hooks/useStudents.ts`

```typescript
import { useState, useCallback } from 'react';
import { api } from '../../../lib/api';

interface Student {
  id: string;
  full_name: string;
  email: string;
  phone: string | null;
  status: 'active' | 'inactive' | 'cancelled' | 'refunded';
  created_at: string;
  updated_at: string;
  ped_enrollments: Array<{
    id: string;
    status: string;
    purchase_date: string | null;
    ped_classes: { id: string; name: string; abbreviation: string } | null;
  }>;
}

interface StudentListResponse {
  data: Student[];
  pagination: { page: number; limit: number; total: number; pages: number };
}

interface StudentDetailResponse {
  data: Student;
}

interface UseStudentsReturn {
  loading: boolean;
  error: string | null;
  clearError: () => void;
  getStudents: (params: {
    page?: number;
    limit?: number;
    classId?: string;
    status?: string;
    search?: string;
  }) => Promise<StudentListResponse | null>;
  getStudent: (id: string) => Promise<StudentDetailResponse | null>;
  updateStudent: (id: string, data: Partial<Pick<Student, 'full_name' | 'phone' | 'notes' | 'status'>>) => Promise<Student | null>;
}

export function useStudents(): UseStudentsReturn {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const clearError = useCallback(() => setError(null), []);

  const getStudents = useCallback(async (params: {
    page?: number; limit?: number; classId?: string; status?: string; search?: string;
  }) => {
    setLoading(true);
    setError(null);

    const qs = new URLSearchParams();
    if (params.page)    qs.set('page',     String(params.page));
    if (params.limit)   qs.set('limit',    String(params.limit));
    if (params.classId) qs.set('class_id', params.classId);
    if (params.status)  qs.set('status',   params.status);
    if (params.search?.trim()) qs.set('search', params.search.trim());

    const { data, error: apiError } = await api.get<StudentListResponse>(
      `/api/v1/pedagogico/students?${qs.toString()}`
    );

    setLoading(false);
    if (apiError) { setError(apiError.message); return null; }
    return data;
  }, []);

  const getStudent = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    const { data, error: apiError } = await api.get<StudentDetailResponse>(`/api/v1/pedagogico/students/${id}`);
    setLoading(false);
    if (apiError) { setError(apiError.message); return null; }
    return data;
  }, []);

  const updateStudent = useCallback(async (id: string, payload: Record<string, unknown>) => {
    setLoading(true);
    setError(null);
    const { data, error: apiError } = await api.patch<{ data: Student }>(`/api/v1/pedagogico/students/${id}`, payload);
    setLoading(false);
    if (apiError) { setError(apiError.message); return null; }
    return data?.data ?? null;
  }, []);

  return { loading, error, clearError, getStudents, getStudent, updateStudent };
}
```

#### `hooks/useClasses.ts`

Same pattern as `useStudents.ts`, calling:
- `GET /api/v1/pedagogico/classes`
- `GET /api/v1/pedagogico/classes/:id`
- `POST /api/v1/pedagogico/classes`
- `PATCH /api/v1/pedagogico/classes/:id`

#### `hooks/useWebhookLogs.ts`

Same pattern, calling `GET /api/v1/pedagogico/webhook-logs?status=&page=&limit=`.

### 4.6 Component Patterns

All components follow the patterns seen in `DashboardPage.tsx`:

- Use `Card`, `Badge`, `Button`, `Modal` from `../../../components/ui`
- Use `cn()` from `../../../lib/utils` for conditional classes
- Use green accent: `bg-[rgba(0,179,126,0.12)]`, `text-lios-green`, `bg-lios-green`
- Loading state: skeleton divs with `animate-pulse` (as in `SkeletonCard`)
- Empty state: centered div with icon placeholder and descriptive text
- Permission guard: call `usePermissions()` and check `hasPermission('pedagogico', 'read')`

#### Permission Guard Pattern in Pages

```typescript
// At the top of each protected page:
import { usePermissions } from '../../../hooks/usePermissions';
import ComingSoonPage from '../../../pages/ComingSoonPage';

export default function StudentsPage() {
  const { hasPermission, loading: permLoading } = usePermissions();

  if (permLoading) return <LoadingScreen />;
  if (!hasPermission('pedagogico', 'read')) {
    return <ComingSoonPage moduleName="Alunos" />;
  }

  // ... page content
}
```

### 4.7 Shared Types

Add to `packages/shared/src/types.ts` (or a new `pedagogico.types.ts` inside the module):

```typescript
// apps/web/src/modules/pedagogico/types.ts

export type StudentStatus = 'active' | 'inactive' | 'cancelled' | 'refunded';
export type EnrollmentStatus = 'active' | 'cancelled' | 'refunded' | 'expired';
export type ClassStatus = 'active' | 'completed' | 'cancelled';
export type WebhookStatus = 'received' | 'processing' | 'completed' | 'failed' | 'skipped';

export interface PedClass {
  id: string;
  name: string;
  abbreviation: string;
  product_hotmart_id: string | null;
  product_name: string | null;
  start_date: string | null;
  end_date: string | null;
  status: ClassStatus;
  created_at: string;
}

export interface PedEnrollment {
  id: string;
  student_id: string;
  class_id: string | null;
  hotmart_transaction: string | null;
  hotmart_product_id: string | null;
  purchase_date: string | null;
  amount_paid: number | null;
  payment_method: string | null;
  status: EnrollmentStatus;
  enrolled_at: string;
  ped_classes?: PedClass | null;
}

export interface PedStudent {
  id: string;
  full_name: string;
  email: string;
  phone: string | null;
  cpf: string | null;
  status: StudentStatus;
  created_at: string;
  updated_at: string;
  ped_enrollments?: PedEnrollment[];
}
```

---

## 5. Hotmart Webhook Integration

### 5.1 Expected Payload Structure

Hotmart's payload for `PURCHASE_COMPLETE` (most reliable event — payment confirmed and product delivered):

```json
{
  "id": "evt_01J...",
  "creation_date": 1740000000000,
  "event": "PURCHASE_COMPLETE",
  "version": "2.0.0",
  "data": {
    "product": {
      "id": 1234567,
      "name": "Técnico em Climatização — Turma 01",
      "has_co_production": false
    },
    "purchase": {
      "transaction": "HP12345678901",
      "approved_date": 1740000000000,
      "full_price": { "value": 597.00, "currency_value": "BRL" },
      "payment": {
        "type": "CREDIT_CARD",
        "installments_number": 12,
        "value": { "cents": 59700, "currency_value": "BRL" }
      },
      "offer": { "code": "oferta_01" }
    },
    "buyer": {
      "name": "João Silva",
      "email": "joao@email.com",
      "checkout_phone": "+5511999990000",
      "document": null
    },
    "producer": {
      "name": "LI Educação Online",
      "document": "..."
    }
  }
}
```

**Key fields mapped by `HotmartService.parsePayload()`:**

| Hotmart field | DB column |
|---|---|
| `data.purchase.transaction` | `ped_enrollments.hotmart_transaction` (idempotency key) |
| `data.product.id` | `ped_enrollments.hotmart_product_id` → resolves to `class_id` |
| `data.buyer.email` | `ped_students.email` (unique key for upsert) |
| `data.buyer.name` | `ped_students.full_name` |
| `data.buyer.checkout_phone` | `ped_students.phone` |
| `data.purchase.payment.value.cents / 100` | `ped_enrollments.amount_paid` |
| `data.purchase.payment.type` | `ped_enrollments.payment_method` |
| `data.purchase.approved_date` | `ped_enrollments.purchase_date` |
| Full `raw` payload | `ped_enrollments.metadata` |

### 5.2 Event Types and Handling

| Event | Action |
|---|---|
| `PURCHASE_APPROVED` | Create student + enrollment (payment approved, may still be processing) |
| `PURCHASE_COMPLETE` | Create student + enrollment (preferred — full delivery confirmed) |
| `PURCHASE_REFUNDED` | Update enrollment status → `refunded`; update student status → `refunded` if all enrollments refunded |
| `PURCHASE_CANCELED` | Update enrollment status → `cancelled` |
| `PURCHASE_PROTEST` | Log only (no state change in Epic 1) |
| `PURCHASE_CHARGEBACK` | Log only (no state change in Epic 1) |
| `CLUB_FIRST_ACCESS` | Log only — no action in Epic 1 |
| Any other | Log as `skipped`, `status: 'completed'` |

**Recommendation:** Configure Hotmart to send only `PURCHASE_COMPLETE` events initially. Add `PURCHASE_REFUNDED` and `PURCHASE_CANCELED` in the same webhook subscription. Avoid `PURCHASE_APPROVED` to prevent double-processing (transaction IDs are shared between APPROVED and COMPLETE).

### 5.3 Signature Validation

Hotmart uses a **static token** model (not HMAC). When configuring the webhook in Hotmart's developer dashboard:

1. Set a "Hottok" password in the webhook configuration
2. Hotmart sends this value verbatim in the `X-Hotmart-Hottok` header on every request
3. The API compares `req.headers['x-hotmart-hottok'] === process.env.HOTMART_WEBHOOK_SECRET`

```typescript
// From hotmart.service.ts:
export function validateHotmartSignature(hottok: string | undefined): boolean {
  if (!config.hotmartWebhookSecret) {
    // Dev mode: allow all (log warning)
    console.warn('[hotmart] HOTMART_WEBHOOK_SECRET not configured');
    return true;
  }
  return typeof hottok === 'string' && hottok === config.hotmartWebhookSecret;
}
```

**Security note:** The comparison should use `timingSafeEqual` from Node.js crypto to prevent timing attacks:

```typescript
import { timingSafeEqual } from 'crypto';

export function validateHotmartSignature(hottok: string | undefined): boolean {
  if (!config.hotmartWebhookSecret || !hottok) return false;
  try {
    return timingSafeEqual(
      Buffer.from(hottok, 'utf8'),
      Buffer.from(config.hotmartWebhookSecret, 'utf8')
    );
  } catch {
    return false;
  }
}
```

### 5.4 Idempotency Strategy

The primary idempotency mechanism is the `UNIQUE` constraint on `ped_enrollments.hotmart_transaction`.

Processing flow:

1. Webhook arrives → log to `ped_webhook_logs` (always, even duplicates)
2. `processWebhookAsync` checks: `SELECT id FROM ped_enrollments WHERE hotmart_transaction = $1`
3. If found → set `processing_steps` with `{ step: 'idempotency_check', status: 'skipped', reason: 'duplicate_transaction' }` → set log status `completed` → exit
4. If not found → proceed with student upsert + enrollment insert

The `ped_students` table uses `ON CONFLICT (email) DO UPDATE` — a student who buys multiple products gets their record updated (not duplicated). Each product gets its own `ped_enrollments` row.

### 5.5 Rate Limiting

Add rate limiting to the webhook endpoint using `express-rate-limit`:

```typescript
// In routes/webhooks.ts:
import rateLimit from 'express-rate-limit';

const webhookLimiter = rateLimit({
  windowMs: 60 * 1000,   // 1 minute window
  max: 100,              // Hotmart sends at most a few per minute in production
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: { message: 'Too many requests', code: 'RATE_LIMITED' } },
});

webhookRouter.post('/hotmart', webhookLimiter, async (req, res) => { ... });
```

Add `express-rate-limit` to `apps/api/package.json`.

### 5.6 Async Processing Approach

The current Express setup on Railway does not have a message queue (no Redis, no Bull). The async processing uses `setImmediate()` which schedules the callback after the current event loop tick — ensuring the `res.status(200).json(...)` is sent first.

**Limitation:** If the Railway instance restarts mid-processing, in-flight webhooks (status `processing`) will be stuck. Mitigation:
- On API startup, query for `ped_webhook_logs WHERE status = 'processing' AND created_at < now() - interval '5 minutes'` and requeue them
- For Epic 1 this is acceptable. Epic 5 addresses full pipeline orchestration with retry UI.

```typescript
// In apps/api/src/index.ts — add after app.listen():
import { requeueStuckWebhooks } from './modules/pedagogico/queue/webhook-processor.js';

// Recovery on startup
setTimeout(() => {
  requeueStuckWebhooks().catch(console.error);
}, 5000);
```

---

## 6. Google Sheets Export (Story 1.5)

### 6.1 Service Account Authentication

The Google Sheets integration uses a service account (not OAuth2 user flow). The service account JSON credentials are stored as a base64-encoded environment variable `GOOGLE_SERVICE_ACCOUNT_JSON`.

```typescript
// apps/api/src/modules/pedagogico/services/google-sheets.service.ts

import { google, sheets_v4 } from 'googleapis';

export class GoogleSheetsService {
  private getAuth() {
    const credentialsJson = Buffer.from(
      config.googleServiceAccountJson,
      'base64'
    ).toString('utf-8');
    const credentials = JSON.parse(credentialsJson);

    return new google.auth.GoogleAuth({
      credentials,
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });
  }

  async getSheetsClient(): Promise<sheets_v4.Sheets> {
    const auth = this.getAuth();
    return google.sheets({ version: 'v4', auth });
  }

  async exportStudentsToSheet(spreadsheetId: string, students: PedStudent[]): Promise<void> {
    const sheets = await this.getSheetsClient();

    const headers = ['Nome', 'Email', 'Telefone', 'CPF', 'Turma', 'Sigla', 'Produto', 'Data Compra', 'Valor (R$)', 'Status', 'Data Cadastro'];

    const rows = students.flatMap((student) => {
      if (!student.ped_enrollments || student.ped_enrollments.length === 0) {
        return [[student.full_name, student.email, student.phone ?? '', '', '', '', '', '', '', student.status, student.created_at]];
      }
      return student.ped_enrollments.map((enr) => [
        student.full_name,
        student.email,
        student.phone ?? '',
        student.cpf ?? '',
        enr.ped_classes?.name ?? '',
        enr.ped_classes?.abbreviation ?? '',
        enr.hotmart_product_id ?? '',
        enr.purchase_date ? new Date(enr.purchase_date).toLocaleDateString('pt-BR') : '',
        enr.amount_paid != null ? enr.amount_paid.toFixed(2) : '',
        enr.status,
        new Date(student.created_at).toLocaleDateString('pt-BR'),
      ]);
    });

    const values = [headers, ...rows];

    // Clear then write (avoid duplicates on re-export)
    await sheets.spreadsheets.values.clear({
      spreadsheetId,
      range: 'Consolidado!A:K',
    });

    await sheets.spreadsheets.values.update({
      spreadsheetId,
      range: 'Consolidado!A1',
      valueInputOption: 'USER_ENTERED',
      requestBody: { values },
    });
  }

  async exportClassTab(spreadsheetId: string, classData: PedClass & { students: PedStudent[] }): Promise<void> {
    const sheets = await this.getSheetsClient();
    const tabName = classData.abbreviation; // e.g. "TEC01"

    // Create tab if it doesn't exist
    const sheetMeta = await sheets.spreadsheets.get({ spreadsheetId });
    const existingSheets = sheetMeta.data.sheets?.map(s => s.properties?.title) ?? [];

    if (!existingSheets.includes(tabName)) {
      await sheets.spreadsheets.batchUpdate({
        spreadsheetId,
        requestBody: {
          requests: [{ addSheet: { properties: { title: tabName } } }],
        },
      });
    }

    // Write student rows for this class
    const headers = ['Nome', 'Email', 'Telefone', 'CPF', 'Data Compra', 'Valor (R$)', 'Status'];
    const rows = classData.students.map((s) => {
      const enr = s.ped_enrollments?.find(e => e.class_id === classData.id);
      return [
        s.full_name, s.email, s.phone ?? '', s.cpf ?? '',
        enr?.purchase_date ? new Date(enr.purchase_date).toLocaleDateString('pt-BR') : '',
        enr?.amount_paid != null ? enr.amount_paid.toFixed(2) : '',
        enr?.status ?? s.status,
      ];
    });

    await sheets.spreadsheets.values.clear({ spreadsheetId, range: `${tabName}!A:G` });
    await sheets.spreadsheets.values.update({
      spreadsheetId,
      range: `${tabName}!A1`,
      valueInputOption: 'USER_ENTERED',
      requestBody: { values: [headers, ...rows] },
    });
  }
}
```

**Required npm package:** `googleapis` — add to `apps/api/package.json`.

**Service account setup (DevOps task):**
1. Create Google Cloud service account
2. Enable Google Sheets API
3. Share the target spreadsheet with the service account email (Editor role)
4. Download JSON key → base64-encode → store as `GOOGLE_SERVICE_ACCOUNT_JSON` on Railway

### 6.2 Export Endpoint

```typescript
// In export.routes.ts:
router.post('/sheets', requirePermission('pedagogico:admin'), async (req, res) => {
  const { class_id } = req.body as { class_id?: string };
  const sheetsService = new GoogleSheetsService();
  const studentService = new StudentService();

  const consolidatedId = config.googleSheetConsolidatedId;
  if (!consolidatedId) {
    res.status(503).json({ error: { message: 'Google Sheets não configurado', code: 'NOT_CONFIGURED' } });
    return;
  }

  try {
    if (class_id) {
      // Export single class tab
      const classService = new ClassService();
      const classData = await classService.getClassWithStudents(class_id);
      await sheetsService.exportClassTab(consolidatedId, classData);
      res.json({ success: true, type: 'class', class_id, exported_at: new Date().toISOString() });
    } else {
      // Full consolidated export
      const { data: students } = await studentService.getStudentList({ page: 1, limit: 10000 });
      await sheetsService.exportStudentsToSheet(consolidatedId, students?.data ?? []);
      res.json({ success: true, type: 'consolidated', exported_at: new Date().toISOString() });
    }
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Erro ao exportar';
    console.error('[export/sheets]', err);
    res.status(502).json({ error: { message: `Falha ao exportar para Google Sheets: ${message}`, code: 'SHEETS_ERROR' } });
  }
});
```

### 6.3 Scheduled Export (Optional)

For Story 1.5 AC8 (scheduled export), add a cron job that triggers the consolidated export once per day:

```typescript
// In apps/api/src/index.ts — add after startup:
import cron from 'node-cron';

// Daily export at 6am BRT (9am UTC)
cron.schedule('0 9 * * *', async () => {
  console.log('[cron] Starting daily Sheets export');
  // Call the export service directly (no HTTP)
  // ...
});
```

Add `node-cron` to `apps/api/package.json` if using this approach. For Epic 1 this is optional — manual export via UI button is sufficient.

---

## 7. Implementation Order

### 7.1 Story Sequence and Dependencies

```
Story 1.1 (Schema + RBAC)
  │
  ├── No dependencies — can start immediately
  │
  ▼
Story 1.2 (Webhook Receiver)
  │
  ├── Requires: Story 1.1 tables (ped_webhook_logs, ped_students, ped_enrollments, ped_classes)
  ├── Requires: HOTMART_WEBHOOK_SECRET env var on Railway
  │
  ▼
Story 1.3 (Student CRUD API)
  │
  ├── Requires: Story 1.1 tables + RLS policies
  ├── Requires: middleware/rbac.ts (new file, created in this story)
  ├── Can be developed in parallel with Story 1.2 after 1.1 is complete
  │
  ▼
Story 1.4 (Student UI)
  │
  ├── Requires: Story 1.3 API endpoints (all GET routes at minimum)
  ├── Can be partially developed with mock data while 1.3 is in progress
  │
  ▼
Story 1.5 (Google Sheets Export)
  │
  ├── Requires: Story 1.3 (student list data)
  ├── Requires: Google service account credentials on Railway
  │
  └── Can be the last story in the epic (least critical for core functionality)
```

### 7.2 Parallelization Opportunities

After Story 1.1 is merged:

- **Team member A:** Story 1.2 (Webhook receiver + async processor)
- **Team member B:** Story 1.3 (CRUD API routes and services)

After Stories 1.2 and 1.3 are merged:

- **Team member A:** Story 1.4 (Frontend) — unblocked by 1.3
- **Team member B:** Story 1.5 (Sheets) — unblocked by 1.3

### 7.3 Commit Checkpoints per Story

**Story 1.1:**
1. `feat: add ped_* schema migration [Story 1.1]`
2. `feat: add pedagogico RBAC permissions seed [Story 1.1]`
3. `test: verify RLS policies with admin and pedagogico roles [Story 1.1]`

**Story 1.2:**
1. `feat: add webhook router with hotmart signature validation [Story 1.2]`
2. `feat: add webhook-processor async pipeline [Story 1.2]`
3. `feat: add HotmartService payload parser [Story 1.2]`
4. `feat: add StudentService.upsertStudent [Story 1.2]`
5. `feat: add ClassService.resolveByProductId [Story 1.2]`

**Story 1.3:**
1. `feat: add requirePermission middleware [Story 1.3]`
2. `feat: add pedagogico module router [Story 1.3]`
3. `feat: add student CRUD routes [Story 1.3]`
4. `feat: add class CRUD routes [Story 1.3]`
5. `feat: add enrollment list route [Story 1.3]`

**Story 1.4:**
1. `feat: add pedagogico module routes and lazy pages [Story 1.4]`
2. `feat: update AppShell sidebar for pedagogico sector [Story 1.4]`
3. `feat: add StudentsPage with table and filters [Story 1.4]`
4. `feat: add StudentDetailPage [Story 1.4]`
5. `feat: add ClassesPage and ClassDetailPage [Story 1.4]`
6. `feat: add pedagogico DashboardPage with metrics [Story 1.4]`

**Story 1.5:**
1. `feat: add GoogleSheetsService [Story 1.5]`
2. `feat: add export/sheets API endpoint [Story 1.5]`
3. `feat: add export button to ClassDetailPage and StudentsPage [Story 1.5]`

---

## 8. Risks & Decisions

### 8.1 Technical Decisions

**Decision 1: `setImmediate` for async processing (not a message queue)**

- **Chosen:** `setImmediate` + in-process async function
- **Alternative considered:** Bull/BullMQ with Redis queue
- **Rationale:** Epic 1 does not have UazAPI or Google Drive (those come in Epics 2-4). The webhook pipeline in Epic 1 only creates a student and enrollment in Supabase — if it fails, it fails cleanly with a log entry. Adding Redis would require a new Railway service and additional complexity. Epic 5 is specifically designed to address pipeline orchestration — the architecture can evolve then.
- **Mitigation:** Startup recovery scans for stuck `processing` webhooks and requeues them.

**Decision 2: Static token (hottok) vs HMAC signature for Hotmart**

- **Chosen:** Static token comparison with `timingSafeEqual`
- **Rationale:** Hotmart's documentation (as of 2025) uses a static `hottok` header, not HMAC. If Hotmart adds HMAC in future versions (`version: "2.0.0"` payload field suggests versioning), the `validateHotmartSignature` function can be updated without changing the endpoint.

**Decision 3: Webhook endpoint path outside module router**

- **Chosen:** `/api/v1/webhooks/hotmart` in a separate `routes/webhooks.ts`
- **Rationale:** The webhook endpoint is public (no `authMiddleware`). The pedagogico module router applies `authMiddleware` at the top — mixing public and authenticated routes in the same router would require per-route middleware overrides, which is error-prone. Separating into `routes/webhooks.ts` keeps the security boundary explicit and mirrors the PRD's specification.

**Decision 4: `supabaseAdmin` for webhook log inserts (bypasses RLS)**

- **Chosen:** Use `supabaseAdmin` (service role) for all webhook-processor writes
- **Rationale:** The webhook processor runs without a user JWT. Using `createSupabaseClient(token)` is not possible. The `supabaseAdmin` client with service role bypasses RLS — this is acceptable because the webhook processor is server-side code, not accessible from the browser. All user-facing reads of `ped_webhook_logs` go through the RLS-enforced anon client from the frontend.

**Decision 5: Supabase Relational SELECT for student list (not separate queries)**

- **Chosen:** Nested `select('*, ped_enrollments(*, ped_classes(*))')` in one query
- **Rationale:** Supabase's PostgREST supports nested resource embedding, which avoids N+1 queries. The filter `eq('ped_enrollments.status', 'active')` in the Supabase client filters the embedded join, not the parent. Students without active enrollments still appear in the list (enrollment column will be empty array).
- **Caveat:** If the student list grows beyond 5,000 records, the nested join may become slow. At that scale, a materialized view or separate aggregation should be considered. For Epic 1 this is premature optimization.

**Decision 6: UNIQUE on `ped_enrollments.hotmart_transaction` (not composite key)**

- **Chosen:** Single `UNIQUE` constraint on `hotmart_transaction`
- **Alternative:** `UNIQUE(student_id, class_id)` as in the PRD's schema
- **Rationale:** `UNIQUE(student_id, class_id)` would prevent the same student from enrolling in the same class twice (via different transactions). However, if a student pays, gets refunded, and re-enrolls, you would need to delete the old enrollment to insert the new one — losing history. Using `hotmart_transaction` as the idempotency key preserves full enrollment history and allows the same student/class pair to have multiple rows (with different statuses).

### 8.2 Risks Identified

**Risk 1: Hotmart payload structure variations**
- **Probability:** Medium
- **Impact:** High — webhook parsing fails silently, students not created
- **Mitigation:** Log the full raw payload in `ped_webhook_logs.payload`. The `HotmartService.parsePayload()` wraps each field access with `?? defaultValue` — it never throws on missing optional fields, only on `transaction` and `buyer.email` (required). Admin can inspect the raw payload in the webhook log UI to debug parsing issues.

**Risk 2: Railway instance restart mid-webhook-processing**
- **Probability:** Low (Railway has low restart frequency)
- **Impact:** Low — webhook stuck in `processing` status, not re-processed until next startup
- **Mitigation:** Startup recovery queries and the webhook log UI (Story 5.2) allows manual reprocessing. For Epic 1, this is acceptable.

**Risk 3: `product_hotmart_id` not mapped to a class**
- **Probability:** High initially — classes must be manually configured
- **Impact:** Medium — student created but without class assignment
- **Mitigation:** Students are created without a class (enrollment has `class_id = null`). The admin must create the class and set `product_hotmart_id` before enrollments will have class assignments. Existing null-class enrollments can be batch-updated later. This is by design.

**Risk 4: Google Sheets service account permissions**
- **Probability:** Low (one-time setup issue)
- **Impact:** Medium — export endpoint returns 502
- **Mitigation:** The export endpoint returns a clear error message when Sheets fails. The feature is non-critical (manual export, not core flow).

**Risk 5: Supabase `upsert` with `ON CONFLICT` updating wrong fields**
- **Probability:** Low
- **Impact:** Medium — student data overwritten with older/incomplete data from a re-delivered webhook
- **Mitigation:** The `upsert` in `StudentService.upsertStudent()` should only update `phone` and `hotmart_buyer_email` on conflict — not `full_name` (to preserve manual corrections). This should be implemented with Supabase's `update: { phone: ..., hotmart_buyer_email: ... }` syntax on the upsert, or by fetching first and only updating if new data is more complete.

### 8.3 Open Questions for the User

1. **Hotmart `PURCHASE_APPROVED` vs `PURCHASE_COMPLETE`:** Should both events create enrollments, or only `PURCHASE_COMPLETE`? If both, the same transaction would be processed twice (Epic 1 handles this via idempotency, but it creates noise in logs). Recommendation: configure Hotmart webhook to send only `PURCHASE_COMPLETE`.

2. **Class mapping before going live:** The system requires `ped_classes.product_hotmart_id` to be set for automatic class assignment. Before the webhook goes live, the admin must create the classes and map them to Hotmart product IDs. Who will do this, and when?

3. **Student email vs buyer email:** In Hotmart, the buyer might purchase for someone else (different email). Is the buyer's email always the student's email for LI Educação? If not, the system needs to handle the `subscriptions` or `students` object in the webhook payload (which contains the actual student's data in subscription products).

4. **Multiple purchases by same student:** If a student buys `TEC01` and later buys `CLI01` (different product), they get one `ped_students` record and two `ped_enrollments`. Is this the intended behavior? (Answer from PRD: yes — FR3 and FR14 confirm this.)

5. **Google Sheets spreadsheet ID:** The PRD mentions `GOOGLE_SHEETS_CONSOLIDATED_ID`. Does this spreadsheet already exist, or should the system create it? The current architecture assumes it exists and the service account has Editor access.

6. **Hotmart `hottok` value:** This needs to be defined by the user and configured in both Hotmart's webhook settings and Railway's `HOTMART_WEBHOOK_SECRET` env var before testing.

---

## Appendix: Environment Variables Checklist

Variables to add to Railway (API) before each story's features go live:

| Variable | Story | Description |
|---|---|---|
| `HOTMART_WEBHOOK_SECRET` | 1.2 | Static token from Hotmart webhook config |
| `HOTMART_TOKEN` | Future | Hotmart API Bearer token (not needed in Epic 1) |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | 1.5 | Base64-encoded service account JSON |
| `GOOGLE_SHEETS_CONSOLIDATED_ID` | 1.5 | Google Sheets spreadsheet ID for exports |

Variables added to `apps/api/src/config.ts` to reflect the above.

No new Vercel env vars needed — the frontend does not call Google APIs or Hotmart directly.

---

## Appendix: File Checklist per Story

### Story 1.1 — Files to create
- `lios/supabase/migrations/20260318120000_ped_schema.sql`
- `lios/supabase/migrations/20260318130000_ped_rbac_permissions.sql`

### Story 1.2 — Files to create
- `lios/apps/api/src/routes/webhooks.ts`
- `lios/apps/api/src/modules/pedagogico/services/hotmart.service.ts`
- `lios/apps/api/src/modules/pedagogico/services/student.service.ts`
- `lios/apps/api/src/modules/pedagogico/services/class.service.ts`
- `lios/apps/api/src/modules/pedagogico/queue/webhook-processor.ts`

### Story 1.2 — Files to modify
- `lios/apps/api/src/config.ts` — add `hotmartWebhookSecret`
- `lios/apps/api/src/routes/index.ts` — mount `webhookRouter` at `/v1/webhooks`

### Story 1.3 — Files to create
- `lios/apps/api/src/middleware/rbac.ts`
- `lios/apps/api/src/modules/pedagogico/index.ts`
- `lios/apps/api/src/modules/pedagogico/routes/student.routes.ts`
- `lios/apps/api/src/modules/pedagogico/routes/class.routes.ts`
- `lios/apps/api/src/modules/pedagogico/routes/enrollment.routes.ts`

### Story 1.3 — Files to modify
- `lios/apps/api/src/routes/index.ts` — mount `pedagogicoRouter` at `/v1/pedagogico`

### Story 1.4 — Files to create
- `lios/apps/web/src/modules/pedagogico/routes.tsx`
- `lios/apps/web/src/modules/pedagogico/types.ts`
- `lios/apps/web/src/modules/pedagogico/hooks/useStudents.ts`
- `lios/apps/web/src/modules/pedagogico/hooks/useClasses.ts`
- `lios/apps/web/src/modules/pedagogico/hooks/useWebhookLogs.ts`
- `lios/apps/web/src/modules/pedagogico/hooks/usePedagogicoMetrics.ts`
- `lios/apps/web/src/modules/pedagogico/pages/DashboardPage.tsx`
- `lios/apps/web/src/modules/pedagogico/pages/StudentsPage.tsx`
- `lios/apps/web/src/modules/pedagogico/pages/StudentDetailPage.tsx`
- `lios/apps/web/src/modules/pedagogico/pages/ClassesPage.tsx`
- `lios/apps/web/src/modules/pedagogico/pages/ClassDetailPage.tsx`
- `lios/apps/web/src/modules/pedagogico/pages/WebhookLogPage.tsx`
- `lios/apps/web/src/modules/pedagogico/components/StudentTable.tsx`
- `lios/apps/web/src/modules/pedagogico/components/ClassCard.tsx`
- `lios/apps/web/src/modules/pedagogico/components/MetricsCards.tsx`
- `lios/apps/web/src/modules/pedagogico/components/WebhookLogTable.tsx`
- `lios/apps/web/src/modules/pedagogico/components/EnrollmentHistory.tsx`

### Story 1.4 — Files to modify
- `lios/apps/web/src/App.tsx` — add pedagogico routes, remove alunos ComingSoon
- `lios/apps/web/src/components/AppShell.tsx` — update sidebar entry + breadcrumbs

### Story 1.5 — Files to create
- `lios/apps/api/src/modules/pedagogico/services/google-sheets.service.ts`
- `lios/apps/api/src/modules/pedagogico/routes/export.routes.ts`

### Story 1.5 — Files to modify
- `lios/apps/api/src/modules/pedagogico/index.ts` — add export routes
- `lios/apps/api/src/config.ts` — add Google Sheets env vars
- `lios/apps/web/src/modules/pedagogico/pages/ClassDetailPage.tsx` — add export button
- `lios/apps/web/src/modules/pedagogico/pages/StudentsPage.tsx` — add export button
