-- ============================================================================
-- YouTube Responder — Schema
-- Module: yt_ (YouTube Comments & Response Drafts)
-- Target: tqpkymereiyfxroiuaip.supabase.co (LI Educação)
-- Date: 2026-03-20
-- ============================================================================
-- Tables: yt_videos, yt_comments, yt_response_drafts
-- RLS: admin + pedagogico roles (full access, no anon)
-- ============================================================================

-- ─── HELPER: role check ────────────────────────────────────────────────────
-- Reusable inline to avoid repeating the subquery in every policy.
-- Returns true if the calling user has any of the given role names.

CREATE OR REPLACE FUNCTION yt_has_role(p_roles TEXT[])
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

-- ─── TABLE: yt_videos ──────────────────────────────────────────────────────
-- Video metadata for monitored YouTube videos.

CREATE TABLE IF NOT EXISTS yt_videos (
  id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  youtube_video_id  TEXT        NOT NULL UNIQUE,
  title             TEXT        NOT NULL,
  published_at      TIMESTAMPTZ,
  comment_count     INTEGER     DEFAULT 0,
  responded_count   INTEGER     DEFAULT 0,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── TABLE: yt_comments ────────────────────────────────────────────────────
-- Raw comments captured from monitored YouTube videos.

CREATE TABLE IF NOT EXISTS yt_comments (
  id                 UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id           UUID        NOT NULL REFERENCES yt_videos(id) ON DELETE CASCADE,
  youtube_comment_id TEXT,
  author             TEXT        NOT NULL,
  text               TEXT        NOT NULL,
  likes              INTEGER     DEFAULT 0,
  is_reply           BOOLEAN     DEFAULT false,
  parent_comment_id  UUID        REFERENCES yt_comments(id) ON DELETE SET NULL,
  category           TEXT        CHECK (category IN (
                       'technical_question', 'praise', 'complaint', 'course_inquiry',
                       'share_experience', 'correction_needed', 'general', 'spam'
                     )),
  has_response       BOOLEAN     DEFAULT false,
  is_from_owner      BOOLEAN     DEFAULT false,
  comment_date       TIMESTAMPTZ,
  collected_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (video_id, author, text)
);

-- ─── TABLE: yt_response_drafts ─────────────────────────────────────────────
-- AI-generated response drafts awaiting review before posting.

CREATE TABLE IF NOT EXISTS yt_response_drafts (
  id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  comment_id       UUID        NOT NULL REFERENCES yt_comments(id) ON DELETE CASCADE,
  draft_text       TEXT        NOT NULL,
  status           TEXT        NOT NULL DEFAULT 'pending'
                     CHECK (status IN ('pending', 'approved', 'edited', 'rejected', 'posted')),
  edited_text      TEXT,
  clone_version    TEXT        DEFAULT '1.0',
  confidence_score REAL,
  category_used    TEXT,
  reviewed_at      TIMESTAMPTZ,
  posted_at        TIMESTAMPTZ,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── INDEXES ───────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_yt_comments_video_id
  ON yt_comments (video_id);

CREATE INDEX IF NOT EXISTS idx_yt_comments_category
  ON yt_comments (category);

CREATE INDEX IF NOT EXISTS idx_yt_comments_has_response
  ON yt_comments (has_response);

CREATE INDEX IF NOT EXISTS idx_yt_response_drafts_comment_id
  ON yt_response_drafts (comment_id);

CREATE INDEX IF NOT EXISTS idx_yt_response_drafts_status
  ON yt_response_drafts (status);

-- ─── UPDATED_AT TRIGGERS ───────────────────────────────────────────────────
-- update_updated_at_column() is defined in 20260227180000_reset_schema.sql.

CREATE TRIGGER yt_videos_updated_at
  BEFORE UPDATE ON yt_videos
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ─── RLS: 3-LAYER PATTERN ──────────────────────────────────────────────────

-- yt_videos
ALTER TABLE yt_videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE yt_videos FORCE ROW LEVEL SECURITY;
REVOKE ALL ON yt_videos FROM anon;
GRANT ALL ON yt_videos TO authenticated;

-- yt_comments
ALTER TABLE yt_comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE yt_comments FORCE ROW LEVEL SECURITY;
REVOKE ALL ON yt_comments FROM anon;
GRANT ALL ON yt_comments TO authenticated;

-- yt_response_drafts
ALTER TABLE yt_response_drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE yt_response_drafts FORCE ROW LEVEL SECURITY;
REVOKE ALL ON yt_response_drafts FROM anon;
GRANT ALL ON yt_response_drafts TO authenticated;

-- ─── POLICIES ──────────────────────────────────────────────────────────────
-- Access: admin and pedagogico roles only (SELECT, INSERT, UPDATE).
-- The yt_has_role() helper is SECURITY DEFINER — safe to call from policies.

-- yt_videos
CREATE POLICY "yt_videos_select"
  ON yt_videos FOR SELECT TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "yt_videos_insert"
  ON yt_videos FOR INSERT TO authenticated
  WITH CHECK (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "yt_videos_update"
  ON yt_videos FOR UPDATE TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

-- yt_comments
CREATE POLICY "yt_comments_select"
  ON yt_comments FOR SELECT TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "yt_comments_insert"
  ON yt_comments FOR INSERT TO authenticated
  WITH CHECK (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "yt_comments_update"
  ON yt_comments FOR UPDATE TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

-- yt_response_drafts
CREATE POLICY "yt_response_drafts_select"
  ON yt_response_drafts FOR SELECT TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "yt_response_drafts_insert"
  ON yt_response_drafts FOR INSERT TO authenticated
  WITH CHECK (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "yt_response_drafts_update"
  ON yt_response_drafts FOR UPDATE TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

-- ============================================================================
-- Done.
-- 3 tables: yt_videos, yt_comments, yt_response_drafts
-- RLS: 3-layer (ENABLE + FORCE + REVOKE anon), admin + pedagogico access
-- Triggers: updated_at on yt_videos
-- Helper: yt_has_role() — SECURITY DEFINER, safe in policies
-- ============================================================================
