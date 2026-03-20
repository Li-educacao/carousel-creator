-- ============================================================
-- Knowledge Graph — Grafo de Conhecimento Leve
-- Módulo: kg_
-- Dependência: core_roles, core_user_roles, core_permissions
-- ============================================================

-- Extensão para busca fuzzy por nome
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- -------------------------------------------------------
-- Helper: kg_has_role
-- -------------------------------------------------------
CREATE OR REPLACE FUNCTION kg_has_role(p_roles TEXT[])
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

-- -------------------------------------------------------
-- Table: kg_nodes (Entidades)
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS kg_nodes (
  id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  type        TEXT        NOT NULL,  -- 'student', 'course', 'module', 'class', 'telegram_group', 'telegram_member', 'topic', 'campaign', 'product'
  name        TEXT        NOT NULL,
  source      TEXT,                  -- 'lios', 'telegram', 'hotmart', 'erp', 'manual'
  source_id   TEXT,                  -- ID original no sistema de origem (ex: student.id, tg_group.telegram_id)
  metadata    JSONB       NOT NULL DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Evitar duplicatas: mesmo tipo + source + source_id = mesmo nó
CREATE UNIQUE INDEX idx_kg_nodes_source_unique
  ON kg_nodes (type, source, source_id)
  WHERE source_id IS NOT NULL;

CREATE INDEX idx_kg_nodes_type ON kg_nodes (type);
CREATE INDEX idx_kg_nodes_name ON kg_nodes USING gin (name gin_trgm_ops);
CREATE INDEX idx_kg_nodes_source ON kg_nodes (source);
CREATE INDEX idx_kg_nodes_metadata ON kg_nodes USING gin (metadata);

-- -------------------------------------------------------
-- Table: kg_edges (Relações)
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS kg_edges (
  id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id   UUID        NOT NULL REFERENCES kg_nodes(id) ON DELETE CASCADE,
  target_id   UUID        NOT NULL REFERENCES kg_nodes(id) ON DELETE CASCADE,
  relation    TEXT        NOT NULL,  -- 'comprou', 'está_na_turma', 'reclamou_de', 'elogiou', 'mencionou', 'perguntou_sobre', 'ensina', 'monitora'
  weight      FLOAT       NOT NULL DEFAULT 1.0,
  evidence    TEXT,                  -- texto/msg que originou a relação
  evidence_source TEXT,              -- 'telegram_analyze', 'hotmart_webhook', 'manual', 'knowledge_ingest'
  metadata    JSONB       NOT NULL DEFAULT '{}',
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT kg_edges_no_self_loop CHECK (source_id != target_id)
);

-- Evitar arestas duplicadas exatas
CREATE UNIQUE INDEX idx_kg_edges_unique
  ON kg_edges (source_id, target_id, relation);

CREATE INDEX idx_kg_edges_source ON kg_edges (source_id);
CREATE INDEX idx_kg_edges_target ON kg_edges (target_id);
CREATE INDEX idx_kg_edges_relation ON kg_edges (relation);
CREATE INDEX idx_kg_edges_weight ON kg_edges (weight DESC);

-- -------------------------------------------------------
-- Table: kg_ingestion_log (Histórico de ingestão)
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS kg_ingestion_log (
  id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  source          TEXT        NOT NULL,  -- 'telegram_analyze', 'hotmart_webhook', 'manual', 'knowledge_ingest'
  source_ref      TEXT,                  -- referência específica (ex: summary_id, webhook_log_id)
  nodes_created   INT         NOT NULL DEFAULT 0,
  nodes_updated   INT         NOT NULL DEFAULT 0,
  edges_created   INT         NOT NULL DEFAULT 0,
  edges_updated   INT         NOT NULL DEFAULT 0,
  details         JSONB       NOT NULL DEFAULT '{}',
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_kg_ingestion_log_source ON kg_ingestion_log (source);
CREATE INDEX idx_kg_ingestion_log_created ON kg_ingestion_log (created_at DESC);

-- -------------------------------------------------------
-- Triggers: updated_at
-- -------------------------------------------------------
CREATE TRIGGER kg_nodes_updated_at
  BEFORE UPDATE ON kg_nodes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER kg_edges_updated_at
  BEFORE UPDATE ON kg_edges
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- -------------------------------------------------------
-- RLS: 3-Layer (NON-NEGOTIABLE)
-- -------------------------------------------------------

-- kg_nodes
ALTER TABLE kg_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE kg_nodes FORCE ROW LEVEL SECURITY;
REVOKE ALL ON kg_nodes FROM anon;
GRANT ALL ON kg_nodes TO authenticated;

CREATE POLICY kg_nodes_select ON kg_nodes
  FOR SELECT TO authenticated
  USING (kg_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY kg_nodes_insert ON kg_nodes
  FOR INSERT TO authenticated
  WITH CHECK (kg_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY kg_nodes_update ON kg_nodes
  FOR UPDATE TO authenticated
  USING (kg_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY kg_nodes_delete ON kg_nodes
  FOR DELETE TO authenticated
  USING (kg_has_role(ARRAY['admin']));

-- kg_edges
ALTER TABLE kg_edges ENABLE ROW LEVEL SECURITY;
ALTER TABLE kg_edges FORCE ROW LEVEL SECURITY;
REVOKE ALL ON kg_edges FROM anon;
GRANT ALL ON kg_edges TO authenticated;

CREATE POLICY kg_edges_select ON kg_edges
  FOR SELECT TO authenticated
  USING (kg_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY kg_edges_insert ON kg_edges
  FOR INSERT TO authenticated
  WITH CHECK (kg_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY kg_edges_update ON kg_edges
  FOR UPDATE TO authenticated
  USING (kg_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY kg_edges_delete ON kg_edges
  FOR DELETE TO authenticated
  USING (kg_has_role(ARRAY['admin']));

-- kg_ingestion_log
ALTER TABLE kg_ingestion_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE kg_ingestion_log FORCE ROW LEVEL SECURITY;
REVOKE ALL ON kg_ingestion_log FROM anon;
GRANT ALL ON kg_ingestion_log TO authenticated;

CREATE POLICY kg_ingestion_log_select ON kg_ingestion_log
  FOR SELECT TO authenticated
  USING (kg_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY kg_ingestion_log_insert ON kg_ingestion_log
  FOR INSERT TO authenticated
  WITH CHECK (kg_has_role(ARRAY['admin', 'pedagogico']));

-- -------------------------------------------------------
-- Permissions
-- -------------------------------------------------------
INSERT INTO core_permissions (module, action, description) VALUES
  ('knowledge-graph', 'read', 'Visualizar grafo de conhecimento'),
  ('knowledge-graph', 'write', 'Criar e editar entidades e relações'),
  ('knowledge-graph', 'admin', 'Gerenciar configuração do grafo')
ON CONFLICT (module, action) DO NOTHING;

-- Grant knowledge-graph permissions to admin and pedagogico roles
INSERT INTO core_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM core_roles r
CROSS JOIN core_permissions p
WHERE r.name = 'admin'
  AND p.module = 'knowledge-graph'
ON CONFLICT DO NOTHING;

INSERT INTO core_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM core_roles r
CROSS JOIN core_permissions p
WHERE r.name = 'pedagogico'
  AND p.module = 'knowledge-graph'
  AND p.action IN ('read', 'write')
ON CONFLICT DO NOTHING;

-- -------------------------------------------------------
-- Views: consultas úteis prontas
-- -------------------------------------------------------

-- Visão: entidades mais conectadas (hub nodes)
CREATE OR REPLACE VIEW kg_hub_nodes AS
SELECT
  n.id,
  n.type,
  n.name,
  n.source,
  COUNT(DISTINCT e_out.id) AS outgoing,
  COUNT(DISTINCT e_in.id) AS incoming,
  COUNT(DISTINCT e_out.id) + COUNT(DISTINCT e_in.id) AS total_connections
FROM kg_nodes n
LEFT JOIN kg_edges e_out ON e_out.source_id = n.id
LEFT JOIN kg_edges e_in ON e_in.target_id = n.id
GROUP BY n.id, n.type, n.name, n.source
ORDER BY total_connections DESC;

-- Visão: relações por tipo (para dashboard)
CREATE OR REPLACE VIEW kg_relation_stats AS
SELECT
  relation,
  COUNT(*) AS total,
  ROUND(AVG(weight)::numeric, 2) AS avg_weight,
  MIN(created_at) AS first_seen,
  MAX(created_at) AS last_seen
FROM kg_edges
GROUP BY relation
ORDER BY total DESC;

-- Visão: grafo completo (source_name → relation → target_name)
CREATE OR REPLACE VIEW kg_graph AS
SELECT
  e.id AS edge_id,
  ns.id AS source_node_id,
  ns.type AS source_type,
  ns.name AS source_name,
  e.relation,
  e.weight,
  nt.id AS target_node_id,
  nt.type AS target_type,
  nt.name AS target_name,
  e.evidence,
  e.created_at
FROM kg_edges e
JOIN kg_nodes ns ON e.source_id = ns.id
JOIN kg_nodes nt ON e.target_id = nt.id
ORDER BY e.created_at DESC;

-- -------------------------------------------------------
-- Functions: upsert helpers para ingestão
-- -------------------------------------------------------

-- Upsert nó (retorna ID, cria se não existe, atualiza metadata se existe)
CREATE OR REPLACE FUNCTION kg_upsert_node(
  p_type TEXT,
  p_name TEXT,
  p_source TEXT DEFAULT NULL,
  p_source_id TEXT DEFAULT NULL,
  p_metadata JSONB DEFAULT '{}'
)
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_id UUID;
BEGIN
  -- Tentar achar por source_id primeiro (match exato)
  IF p_source_id IS NOT NULL THEN
    SELECT id INTO v_id
    FROM kg_nodes
    WHERE type = p_type AND source = p_source AND source_id = p_source_id;

    IF FOUND THEN
      UPDATE kg_nodes
      SET metadata = kg_nodes.metadata || p_metadata,
          name = COALESCE(NULLIF(p_name, ''), kg_nodes.name),
          updated_at = now()
      WHERE id = v_id;
      RETURN v_id;
    END IF;
  END IF;

  -- Tentar achar por nome + tipo (match fuzzy)
  SELECT id INTO v_id
  FROM kg_nodes
  WHERE type = p_type AND lower(name) = lower(p_name)
  LIMIT 1;

  IF FOUND THEN
    UPDATE kg_nodes
    SET metadata = kg_nodes.metadata || p_metadata,
        source = COALESCE(kg_nodes.source, p_source),
        source_id = COALESCE(kg_nodes.source_id, p_source_id),
        updated_at = now()
    WHERE id = v_id;
    RETURN v_id;
  END IF;

  -- Criar novo
  INSERT INTO kg_nodes (type, name, source, source_id, metadata)
  VALUES (p_type, p_name, p_source, p_source_id, p_metadata)
  RETURNING id INTO v_id;

  RETURN v_id;
END;
$$;

-- Upsert aresta (incrementa weight se já existe)
CREATE OR REPLACE FUNCTION kg_upsert_edge(
  p_source_id UUID,
  p_target_id UUID,
  p_relation TEXT,
  p_weight FLOAT DEFAULT 1.0,
  p_evidence TEXT DEFAULT NULL,
  p_evidence_source TEXT DEFAULT NULL,
  p_metadata JSONB DEFAULT '{}'
)
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_id UUID;
BEGIN
  -- Tentar atualizar existente (incrementa weight)
  UPDATE kg_edges
  SET weight = kg_edges.weight + p_weight,
      evidence = COALESCE(p_evidence, kg_edges.evidence),
      metadata = kg_edges.metadata || p_metadata,
      updated_at = now()
  WHERE source_id = p_source_id
    AND target_id = p_target_id
    AND relation = p_relation
  RETURNING id INTO v_id;

  IF FOUND THEN
    RETURN v_id;
  END IF;

  -- Criar nova
  INSERT INTO kg_edges (source_id, target_id, relation, weight, evidence, evidence_source, metadata)
  VALUES (p_source_id, p_target_id, p_relation, p_weight, p_evidence, p_evidence_source, p_metadata)
  RETURNING id INTO v_id;

  RETURN v_id;
END;
$$;

-- FIM
