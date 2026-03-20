-- ============================================================================
-- YouTube Responder — Feedback Learning
-- Module: yt_ (Learning from approved/edited/rejected drafts)
-- Target: tqpkymereiyfxroiuaip.supabase.co (LI Educação)
-- Date: 2026-03-20
-- ============================================================================
-- View: yt_feedback_examples (materialized from drafts + comments for few-shot)
-- ============================================================================

-- ─── VIEW: yt_feedback_examples ──────────────────────────────────────────────
-- Joins approved/edited drafts with their comments to create training examples.
-- The generator script queries this view to build few-shot examples.

CREATE OR REPLACE VIEW yt_feedback_examples AS
SELECT
  d.id                    AS draft_id,
  d.status                AS feedback_type,
  c.category              AS comment_category,
  c.author                AS comment_author,
  c.text                  AS comment_text,
  v.title                 AS video_title,
  d.draft_text            AS original_draft,
  COALESCE(d.edited_text, d.draft_text) AS final_response,
  d.reviewed_at,
  d.created_at
FROM yt_response_drafts d
JOIN yt_comments c ON c.id = d.comment_id
JOIN yt_videos v   ON v.id = c.video_id
WHERE d.status IN ('approved', 'edited', 'rejected')
ORDER BY d.reviewed_at DESC NULLS LAST;

-- RLS: view inherits from underlying tables (already protected)
-- No additional RLS needed on views

-- ─── Add rejection_reason to yt_response_drafts ─────────────────────────────
-- When user rejects a draft, they can optionally say why (improves learning)

ALTER TABLE yt_response_drafts
ADD COLUMN IF NOT EXISTS rejection_reason TEXT;
