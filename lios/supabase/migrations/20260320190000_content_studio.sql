-- ============================================================================
-- Content Studio — Schema
-- Module prefix: ct_ (Content Studio — YouTube analytics & ideas)
-- Target: tqpkymereiyfxroiuaip.supabase.co (LI Educação)
-- Date: 2026-03-20
-- ============================================================================
-- Tables: ct_videos, ct_comments, ct_insights
-- RLS: admin + pedagogico roles (full access, no anon)
-- ============================================================================

-- ─── TABLE: ct_videos ────────────────────────────────────────────────────────
-- YouTube video metadata with engagement metrics.

CREATE TABLE IF NOT EXISTS ct_videos (
  id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id        TEXT            NOT NULL UNIQUE,
  lesson_number   INTEGER,
  title           TEXT            NOT NULL,
  published_at    TIMESTAMPTZ,
  views           INTEGER         DEFAULT 0,
  likes           INTEGER         DEFAULT 0,
  comment_count   INTEGER         DEFAULT 0,
  duration        INTEGER         DEFAULT 0,
  metadata        JSONB           NOT NULL DEFAULT '{}',
  created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- ─── TABLE: ct_comments ──────────────────────────────────────────────────────
-- Comments from YouTube videos (for content idea generation).

CREATE TABLE IF NOT EXISTS ct_comments (
  id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id            TEXT            NOT NULL,
  author              TEXT            NOT NULL,
  text                TEXT            NOT NULL,
  likes               INTEGER         DEFAULT 0,
  comment_timestamp   BIGINT,
  created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
  updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
  UNIQUE (video_id, author, text)
);

-- ─── TABLE: ct_insights ──────────────────────────────────────────────────────
-- Stores generated content ideas and metadata (single row per type).

CREATE TABLE IF NOT EXISTS ct_insights (
  id              UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
  type            TEXT            NOT NULL UNIQUE DEFAULT 'content_ideas',
  data            JSONB           NOT NULL DEFAULT '[]',
  generated_at    TIMESTAMPTZ     NOT NULL DEFAULT now(),
  created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now()
);

-- ─── INDEXES ─────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_ct_videos_video_id
  ON ct_videos (video_id);

CREATE INDEX IF NOT EXISTS idx_ct_videos_lesson_number
  ON ct_videos (lesson_number DESC);

CREATE INDEX IF NOT EXISTS idx_ct_videos_views
  ON ct_videos (views DESC);

CREATE INDEX IF NOT EXISTS idx_ct_comments_video_id
  ON ct_comments (video_id);

-- ─── UPDATED_AT TRIGGERS ─────────────────────────────────────────────────────

CREATE TRIGGER ct_videos_updated_at
  BEFORE UPDATE ON ct_videos
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER ct_comments_updated_at
  BEFORE UPDATE ON ct_comments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER ct_insights_updated_at
  BEFORE UPDATE ON ct_insights
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ─── RLS: 3-LAYER PATTERN ────────────────────────────────────────────────────

-- ct_videos
ALTER TABLE ct_videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE ct_videos FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ct_videos FROM anon;
GRANT ALL ON ct_videos TO authenticated;

-- ct_comments
ALTER TABLE ct_comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE ct_comments FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ct_comments FROM anon;
GRANT ALL ON ct_comments TO authenticated;

-- ct_insights
ALTER TABLE ct_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE ct_insights FORCE ROW LEVEL SECURITY;
REVOKE ALL ON ct_insights FROM anon;
GRANT ALL ON ct_insights TO authenticated;

-- ─── POLICIES ────────────────────────────────────────────────────────────────
-- Reuse yt_has_role() helper from youtube_responder migration.

-- ct_videos
CREATE POLICY "ct_videos_select"
  ON ct_videos FOR SELECT TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ct_videos_insert"
  ON ct_videos FOR INSERT TO authenticated
  WITH CHECK (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ct_videos_update"
  ON ct_videos FOR UPDATE TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

-- ct_comments
CREATE POLICY "ct_comments_select"
  ON ct_comments FOR SELECT TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ct_comments_insert"
  ON ct_comments FOR INSERT TO authenticated
  WITH CHECK (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ct_comments_update"
  ON ct_comments FOR UPDATE TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

-- ct_insights
CREATE POLICY "ct_insights_select"
  ON ct_insights FOR SELECT TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ct_insights_insert"
  ON ct_insights FOR INSERT TO authenticated
  WITH CHECK (yt_has_role(ARRAY['admin', 'pedagogico']));

CREATE POLICY "ct_insights_update"
  ON ct_insights FOR UPDATE TO authenticated
  USING (yt_has_role(ARRAY['admin', 'pedagogico']));

-- ─── SEED: initial insights row ──────────────────────────────────────────────
INSERT INTO ct_insights (type, data) VALUES ('content_ideas', '[]')
ON CONFLICT (type) DO NOTHING;

-- ============================================================================
-- Done.
-- 3 tables: ct_videos, ct_comments, ct_insights
-- RLS: 3-layer (ENABLE + FORCE + REVOKE anon), admin + pedagogico access
-- Triggers: updated_at on all tables
-- Reuses: yt_has_role() from youtube_responder migration
-- ============================================================================
