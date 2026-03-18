-- ============================================================================
-- Módulo Pedagógico — Schema & RBAC
-- Story: 1.1 — Database Schema & RBAC Setup
-- Module prefix: ped_ (Pedagógico — Gestão de Alunos)
-- Target: tqpkymereiyfxroiuaip.supabase.co (LI Educação)
-- Date: 2026-03-18
-- ============================================================================
-- Tables: ped_classes, ped_students, ped_enrollments, ped_contract_templates,
--         ped_contracts, ped_whatsapp_templates, ped_webhook_logs
-- RLS: admin + pedagogico roles (full CRUD, no anon)
-- Permissions: pedagogico:read, pedagogico:write, pedagogico:admin
-- ============================================================================

-- ─── HELPER: role check ────────────────────────────────────────────────────
-- Returns true if the calling user has any of the given role names.
-- Mirrors tg_has_role() pattern from telegram_intelligence migration.

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

-- ─── TABLE: ped_contract_templates ───────────────────────────────────────────
-- Must be created before ped_classes (FK reference).

CREATE TABLE IF NOT EXISTS ped_contract_templates (
  id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  name            TEXT        NOT NULL,
  content         TEXT        NOT NULL,                -- HTML template com {{variaveis}}
  variables       JSONB       NOT NULL DEFAULT '[]',   -- lista de variaveis disponíveis
  is_default      BOOLEAN     NOT NULL DEFAULT false,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── TABLE: ped_classes (Turmas) ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_classes (
  id                        UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  name                      TEXT        NOT NULL,              -- "Turma Técnico em Climatização 01"
  abbreviation              TEXT        NOT NULL UNIQUE,       -- "TEC01"
  product_hotmart_id        TEXT,                              -- ID do produto na Hotmart
  product_name              TEXT,                              -- Nome do produto/curso
  start_date                DATE,
  end_date                  DATE,
  status                    TEXT        NOT NULL DEFAULT 'active'
                              CHECK (status IN ('active', 'completed', 'cancelled')),
  drive_folder_id           TEXT,                              -- ID da pasta no Google Drive
  sheets_spreadsheet_id     TEXT,                              -- ID da planilha Google Sheets
  whatsapp_welcome_template TEXT,                              -- Template inline (legacy)
  contract_template_id      UUID        REFERENCES ped_contract_templates(id) ON DELETE SET NULL,
  metadata                  JSONB       NOT NULL DEFAULT '{}',
  created_at                TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at                TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── TABLE: ped_students (Alunos) ────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_students (
  id                    UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  full_name             TEXT        NOT NULL,
  email                 TEXT        NOT NULL UNIQUE,
  phone                 TEXT,                              -- formato internacional (+5511...)
  cpf                   TEXT,
  hotmart_buyer_email   TEXT,                              -- email do comprador (pode diferir)
  status                TEXT        NOT NULL DEFAULT 'active'
                          CHECK (status IN ('active', 'inactive', 'cancelled', 'refunded')),
  google_contact_id     TEXT,                              -- ID do contato no Google Contacts
  notes                 TEXT,
  metadata              JSONB       NOT NULL DEFAULT '{}', -- dados extras da Hotmart
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── TABLE: ped_enrollments (Matrículas) ─────────────────────────────────────
-- Relação N:N entre alunos e turmas. Cada compra gera um enrollment.

CREATE TABLE IF NOT EXISTS ped_enrollments (
  id                    UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id            UUID          NOT NULL REFERENCES ped_students(id) ON DELETE CASCADE,
  class_id              UUID          NOT NULL REFERENCES ped_classes(id) ON DELETE CASCADE,
  hotmart_transaction   TEXT          UNIQUE,              -- idempotency key
  hotmart_product_id    TEXT,
  purchase_date         TIMESTAMPTZ,
  amount_paid           NUMERIC(10,2),
  payment_method        TEXT,
  status                TEXT          NOT NULL DEFAULT 'active'
                          CHECK (status IN ('active', 'pending', 'accessed', 'cancelled', 'refunded', 'chargeback', 'expired')),
  accessed_at           TIMESTAMPTZ,                         -- quando acessou a plataforma Hotmart
  enrolled_at           TIMESTAMPTZ   NOT NULL DEFAULT now(),
  metadata              JSONB         NOT NULL DEFAULT '{}', -- payload completo do webhook
  UNIQUE(student_id, class_id, hotmart_transaction)
);

-- ─── TABLE: ped_contracts ────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_contracts (
  id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id        UUID        NOT NULL REFERENCES ped_students(id) ON DELETE CASCADE,
  enrollment_id     UUID        REFERENCES ped_enrollments(id) ON DELETE SET NULL,
  template_id       UUID        REFERENCES ped_contract_templates(id) ON DELETE SET NULL,
  status            TEXT        NOT NULL DEFAULT 'generated'
                      CHECK (status IN ('generated', 'sent', 'viewed', 'signed')),
  pdf_storage_path  TEXT,                              -- path no Supabase Storage
  drive_file_id     TEXT,                              -- ID do arquivo no Google Drive
  drive_url         TEXT,                              -- URL direta do Drive
  sent_at           TIMESTAMPTZ,
  viewed_at         TIMESTAMPTZ,
  signed_at         TIMESTAMPTZ,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── TABLE: ped_whatsapp_templates ───────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_whatsapp_templates (
  id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  name            TEXT        NOT NULL,
  class_id        UUID        REFERENCES ped_classes(id) ON DELETE SET NULL,
  message_text    TEXT        NOT NULL,                -- template com {{variaveis}}
  attachments     JSONB       NOT NULL DEFAULT '[]',   -- [{type:'pdf',url:'...'},{type:'link',url:'...'}]
  is_default      BOOLEAN     NOT NULL DEFAULT false,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── TABLE: ped_webhook_logs ─────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS ped_webhook_logs (
  id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  source            TEXT        NOT NULL DEFAULT 'hotmart'
                      CHECK (source IN ('hotmart', 'manual')),
  event_type        TEXT,                              -- PURCHASE_COMPLETE, PURCHASE_REFUNDED, etc.
  payload           JSONB       NOT NULL,
  status            TEXT        NOT NULL DEFAULT 'received'
                      CHECK (status IN ('received', 'processing', 'completed', 'failed', 'skipped')),
  error_message     TEXT,
  student_id        UUID        REFERENCES ped_students(id) ON DELETE SET NULL,
  enrollment_id     UUID        REFERENCES ped_enrollments(id) ON DELETE SET NULL,
  processing_steps  JSONB       NOT NULL DEFAULT '[]', -- [{step,status,timestamp,error}]
  processed_at      TIMESTAMPTZ,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── INDEXES ─────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_ped_students_email
  ON ped_students (email);

CREATE INDEX IF NOT EXISTS idx_ped_students_status
  ON ped_students (status);

CREATE INDEX IF NOT EXISTS idx_ped_enrollments_student_id
  ON ped_enrollments (student_id);

CREATE INDEX IF NOT EXISTS idx_ped_enrollments_class_id
  ON ped_enrollments (class_id);

CREATE INDEX IF NOT EXISTS idx_ped_enrollments_hotmart_transaction
  ON ped_enrollments (hotmart_transaction);

CREATE INDEX IF NOT EXISTS idx_ped_contracts_student_id
  ON ped_contracts (student_id);

CREATE INDEX IF NOT EXISTS idx_ped_contracts_enrollment_id
  ON ped_contracts (enrollment_id);

CREATE INDEX IF NOT EXISTS idx_ped_webhook_logs_created_at
  ON ped_webhook_logs (created_at DESC);

CREATE INDEX IF NOT EXISTS idx_ped_webhook_logs_status
  ON ped_webhook_logs (status);

CREATE INDEX IF NOT EXISTS idx_ped_classes_product_hotmart_id
  ON ped_classes (product_hotmart_id);

-- ─── UPDATED_AT TRIGGERS ─────────────────────────────────────────────────────
-- update_updated_at_column() is defined in 20260227180000_reset_schema.sql.

CREATE TRIGGER ped_contract_templates_updated_at
  BEFORE UPDATE ON ped_contract_templates
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER ped_classes_updated_at
  BEFORE UPDATE ON ped_classes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER ped_students_updated_at
  BEFORE UPDATE ON ped_students
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ─── RLS: 3-LAYER PATTERN ────────────────────────────────────────────────────

-- ped_contract_templates
ALTER TABLE ped_contract_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_contract_templates FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_contract_templates FROM anon;
GRANT ALL ON ped_contract_templates TO authenticated;

-- ped_classes
ALTER TABLE ped_classes ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_classes FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_classes FROM anon;
GRANT ALL ON ped_classes TO authenticated;

-- ped_students
ALTER TABLE ped_students ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_students FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_students FROM anon;
GRANT ALL ON ped_students TO authenticated;

-- ped_enrollments
ALTER TABLE ped_enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_enrollments FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_enrollments FROM anon;
GRANT ALL ON ped_enrollments TO authenticated;

-- ped_contracts
ALTER TABLE ped_contracts ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_contracts FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_contracts FROM anon;
GRANT ALL ON ped_contracts TO authenticated;

-- ped_whatsapp_templates
ALTER TABLE ped_whatsapp_templates ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_whatsapp_templates FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_whatsapp_templates FROM anon;
GRANT ALL ON ped_whatsapp_templates TO authenticated;

-- ped_webhook_logs
ALTER TABLE ped_webhook_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE ped_webhook_logs FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ped_webhook_logs FROM anon;
GRANT ALL ON ped_webhook_logs TO authenticated;

-- ─── POLICIES ────────────────────────────────────────────────────────────────
-- Access: admin and pedagogico roles — full CRUD.
-- Read-only policies use ped_has_role(['admin','pedagogico']).
-- Write policies use ped_has_role(['admin','pedagogico']) — pedagogico:write
--   checked at API layer via requirePermission middleware.

-- ped_contract_templates
CREATE POLICY "ped_contract_templates_select"
  ON ped_contract_templates FOR SELECT TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_contract_templates_insert"
  ON ped_contract_templates FOR INSERT TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_contract_templates_update"
  ON ped_contract_templates FOR UPDATE TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_contract_templates_delete"
  ON ped_contract_templates FOR DELETE TO authenticated
  USING (ped_has_role(ARRAY['admin']));

-- ped_classes
CREATE POLICY "ped_classes_select"
  ON ped_classes FOR SELECT TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_classes_insert"
  ON ped_classes FOR INSERT TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_classes_update"
  ON ped_classes FOR UPDATE TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_classes_delete"
  ON ped_classes FOR DELETE TO authenticated
  USING (ped_has_role(ARRAY['admin']));

-- ped_students
CREATE POLICY "ped_students_select"
  ON ped_students FOR SELECT TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_students_insert"
  ON ped_students FOR INSERT TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_students_update"
  ON ped_students FOR UPDATE TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_students_delete"
  ON ped_students FOR DELETE TO authenticated
  USING (ped_has_role(ARRAY['admin']));

-- ped_enrollments
CREATE POLICY "ped_enrollments_select"
  ON ped_enrollments FOR SELECT TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_enrollments_insert"
  ON ped_enrollments FOR INSERT TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_enrollments_update"
  ON ped_enrollments FOR UPDATE TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_enrollments_delete"
  ON ped_enrollments FOR DELETE TO authenticated
  USING (ped_has_role(ARRAY['admin']));

-- ped_contracts
CREATE POLICY "ped_contracts_select"
  ON ped_contracts FOR SELECT TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_contracts_insert"
  ON ped_contracts FOR INSERT TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_contracts_update"
  ON ped_contracts FOR UPDATE TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_contracts_delete"
  ON ped_contracts FOR DELETE TO authenticated
  USING (ped_has_role(ARRAY['admin']));

-- ped_whatsapp_templates
CREATE POLICY "ped_whatsapp_templates_select"
  ON ped_whatsapp_templates FOR SELECT TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_whatsapp_templates_insert"
  ON ped_whatsapp_templates FOR INSERT TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_whatsapp_templates_update"
  ON ped_whatsapp_templates FOR UPDATE TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_whatsapp_templates_delete"
  ON ped_whatsapp_templates FOR DELETE TO authenticated
  USING (ped_has_role(ARRAY['admin']));

-- ped_webhook_logs
CREATE POLICY "ped_webhook_logs_select"
  ON ped_webhook_logs FOR SELECT TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_webhook_logs_insert"
  ON ped_webhook_logs FOR INSERT TO authenticated
  WITH CHECK (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_webhook_logs_update"
  ON ped_webhook_logs FOR UPDATE TO authenticated
  USING (ped_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ped_webhook_logs_delete"
  ON ped_webhook_logs FOR DELETE TO authenticated
  USING (ped_has_role(ARRAY['admin']));

-- ─── PERMISSIONS: pedagogico module ──────────────────────────────────────────

INSERT INTO core_permissions (module, action, description) VALUES
  ('pedagogico', 'read', 'Visualizar alunos, turmas e matrículas'),
  ('pedagogico', 'write', 'Criar e editar alunos, turmas e dados pedagógicos'),
  ('pedagogico', 'admin', 'Gerenciar configurações, templates e dados sensíveis do módulo')
ON CONFLICT (module, action) DO NOTHING;

-- Assign ALL pedagogico permissions to admin role
INSERT INTO core_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM core_roles r
CROSS JOIN core_permissions p
WHERE r.name = 'admin'
  AND p.module = 'pedagogico'
ON CONFLICT DO NOTHING;

-- Assign pedagogico:read + pedagogico:write to pedagogico role
INSERT INTO core_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM core_roles r
CROSS JOIN core_permissions p
WHERE r.name = 'pedagogico'
  AND p.module = 'pedagogico'
  AND p.action IN ('read', 'write')
ON CONFLICT DO NOTHING;

-- ─── SEED: turma de exemplo ──────────────────────────────────────────────────

INSERT INTO ped_classes (name, abbreviation, product_name, status)
VALUES ('Turma Técnico em Climatização 01', 'TEC01', 'Curso Técnico em Climatização', 'active')
ON CONFLICT (abbreviation) DO NOTHING;

-- ============================================================================
-- Done.
-- 7 tables: ped_contract_templates, ped_classes, ped_students, ped_enrollments,
--           ped_contracts, ped_whatsapp_templates, ped_webhook_logs
-- RLS: 3-layer (ENABLE + FORCE + REVOKE anon), admin + pedagogico access
-- DELETE: admin only (safety)
-- Triggers: updated_at on ped_contract_templates, ped_classes, ped_students
-- Helper: ped_has_role() — SECURITY DEFINER, safe in policies
-- Permissions: pedagogico:read, pedagogico:write, pedagogico:admin
-- Seed: 1 turma de exemplo (TEC01)
-- ============================================================================
