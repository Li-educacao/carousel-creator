-- Knowledge Graph: Auto-feed triggers for LIOS
-- Date: 2026-03-20
-- Auto-populates KG when students, enrollments, telegram members change

-- -------------------------------------------------------
-- 1. Trigger: auto-feed KG on new student
-- -------------------------------------------------------
CREATE OR REPLACE FUNCTION kg_feed_student()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  PERFORM kg_upsert_node(
    'student', NEW.name, 'lios', NEW.id::TEXT,
    jsonb_build_object(
      'email', COALESCE(NEW.email, ''),
      'phone', COALESCE(NEW.phone, ''),
      'status', COALESCE(NEW.status, 'active')
    )
  );
  RETURN NEW;
END; $$;

DROP TRIGGER IF EXISTS kg_auto_feed_student ON ped_students;
CREATE TRIGGER kg_auto_feed_student
  AFTER INSERT OR UPDATE ON ped_students
  FOR EACH ROW EXECUTE FUNCTION kg_feed_student();

-- -------------------------------------------------------
-- 2. Trigger: auto-feed KG on enrollment (student → class edge)
-- -------------------------------------------------------
CREATE OR REPLACE FUNCTION kg_feed_enrollment()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE
  v_student_node UUID;
  v_class_node UUID;
BEGIN
  -- Find student node
  SELECT id INTO v_student_node FROM kg_nodes
  WHERE type = 'student' AND source = 'lios' AND source_id = NEW.student_id::TEXT
  LIMIT 1;

  -- Find class node
  SELECT id INTO v_class_node FROM kg_nodes
  WHERE type = 'class' AND source = 'lios' AND source_id = NEW.class_id::TEXT
  LIMIT 1;

  IF v_student_node IS NOT NULL AND v_class_node IS NOT NULL THEN
    PERFORM kg_upsert_edge(
      v_student_node, v_class_node, 'matriculado_em',
      1.0, NULL, 'auto_trigger'
    );
  END IF;

  RETURN NEW;
END; $$;

DROP TRIGGER IF EXISTS kg_auto_feed_enrollment ON ped_enrollments;
CREATE TRIGGER kg_auto_feed_enrollment
  AFTER INSERT ON ped_enrollments
  FOR EACH ROW EXECUTE FUNCTION kg_feed_enrollment();

-- -------------------------------------------------------
-- 3. Trigger: auto-feed KG on new class
-- -------------------------------------------------------
CREATE OR REPLACE FUNCTION kg_feed_class()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
  PERFORM kg_upsert_node(
    'class', NEW.name, 'lios', NEW.id::TEXT,
    jsonb_build_object(
      'status', COALESCE(NEW.status, 'active')
    )
  );
  RETURN NEW;
END; $$;

DROP TRIGGER IF EXISTS kg_auto_feed_class ON ped_classes;
CREATE TRIGGER kg_auto_feed_class
  AFTER INSERT OR UPDATE ON ped_classes
  FOR EACH ROW EXECUTE FUNCTION kg_feed_class();

-- -------------------------------------------------------
-- 4. RPC: top students by connections
-- -------------------------------------------------------
CREATE OR REPLACE FUNCTION kg_top_students(p_limit INT DEFAULT 10)
RETURNS TABLE(
  node_id UUID, name TEXT, total_connections BIGINT,
  turmas BIGINT, grupos_telegram BIGINT
) LANGUAGE sql SECURITY DEFINER STABLE AS $$
  SELECT
    n.id AS node_id,
    n.name,
    COUNT(DISTINCT e.id) AS total_connections,
    COUNT(DISTINCT e.id) FILTER (WHERE e.relation = 'matriculado_em') AS turmas,
    COUNT(DISTINCT e.id) FILTER (WHERE e.relation = 'participa_de') AS grupos_telegram
  FROM kg_nodes n
  JOIN kg_edges e ON e.source_id = n.id
  WHERE n.type = 'student'
  GROUP BY n.id, n.name
  ORDER BY total_connections DESC
  LIMIT p_limit;
$$;

-- -------------------------------------------------------
-- 5. RPC: top classes by enrollment count
-- -------------------------------------------------------
CREATE OR REPLACE FUNCTION kg_top_classes(p_limit INT DEFAULT 10)
RETURNS TABLE(
  node_id UUID, name TEXT, total_alunos BIGINT
) LANGUAGE sql SECURITY DEFINER STABLE AS $$
  SELECT
    n.id AS node_id,
    n.name,
    COUNT(DISTINCT e.id) AS total_alunos
  FROM kg_nodes n
  JOIN kg_edges e ON e.target_id = n.id AND e.relation = 'matriculado_em'
  WHERE n.type = 'class'
  GROUP BY n.id, n.name
  ORDER BY total_alunos DESC
  LIMIT p_limit;
$$;

-- -------------------------------------------------------
-- 6. RPC: telegram member activity (members with most relations)
-- -------------------------------------------------------
CREATE OR REPLACE FUNCTION kg_top_telegram_members(p_limit INT DEFAULT 10)
RETURNS TABLE(
  node_id UUID, name TEXT, total_relations BIGINT,
  topics BIGINT, groups BIGINT
) LANGUAGE sql SECURITY DEFINER STABLE AS $$
  SELECT
    n.id AS node_id,
    n.name,
    COUNT(DISTINCT e.id) AS total_relations,
    COUNT(DISTINCT e.id) FILTER (WHERE e.relation = 'especialista_em') AS topics,
    COUNT(DISTINCT e.id) FILTER (WHERE e.relation = 'participa_de') AS groups
  FROM kg_nodes n
  JOIN kg_edges e ON e.source_id = n.id
  WHERE n.type = 'telegram_member'
  GROUP BY n.id, n.name
  ORDER BY total_relations DESC
  LIMIT p_limit;
$$;
