import { Router, Response } from 'express';
import { authMiddleware, AuthenticatedRequest } from '../../middleware/auth.js';
import { createSupabaseClient } from '../../lib/supabase.js';

const router = Router();

// All routes require authentication
router.use(authMiddleware);

// GET /api/v1/youtube/stats
router.get('/stats', async (req, res: Response): Promise<void> => {
  const authReq = req as AuthenticatedRequest;
  const sb = createSupabaseClient(authReq.token);

  const [videosRes, commentsRes, ownerCommentsRes, pendingRes, approvedRes] = await Promise.all([
    sb.from('yt_videos').select('id', { count: 'exact', head: true }),
    sb.from('yt_comments').select('id', { count: 'exact', head: true }),
    sb.from('yt_comments').select('id', { count: 'exact', head: true }).eq('is_from_owner', true),
    sb.from('yt_response_drafts').select('id', { count: 'exact', head: true }).eq('status', 'pending'),
    sb.from('yt_response_drafts').select('id', { count: 'exact', head: true }).in('status', ['approved', 'edited']),
  ]);

  const totalComments = commentsRes.count || 0;
  const ownerComments = ownerCommentsRes.count || 0;
  const respondableComments = totalComments - ownerComments;
  const approvedDrafts = approvedRes.count || 0;
  const responseRate = respondableComments > 0
    ? Math.round((approvedDrafts / respondableComments) * 100)
    : 0;

  res.json({
    total_videos: videosRes.count || 0,
    total_comments: totalComments,
    pending_drafts: pendingRes.count || 0,
    approved_drafts: approvedDrafts,
    response_rate: responseRate,
  });
});

// GET /api/v1/youtube/videos
router.get('/videos', async (req, res: Response): Promise<void> => {
  const authReq = req as AuthenticatedRequest;
  const sb = createSupabaseClient(authReq.token);

  const { limit, offset } = req.query;

  let query = sb
    .from('yt_videos')
    .select('*')
    .order('comment_count', { ascending: false });

  if (limit && typeof limit === 'string') {
    query = query.limit(parseInt(limit, 10));
  }

  if (offset && typeof offset === 'string') {
    const lim = parseInt((limit as string) || '20', 10);
    const off = parseInt(offset, 10);
    query = query.range(off, off + lim - 1);
  }

  const { data, error } = await query;

  if (error) {
    res.status(500).json({ error: { message: error.message, code: 'DB_ERROR' } });
    return;
  }

  res.json({ data: data || [], total: data?.length || 0 });
});

// GET /api/v1/youtube/comments
router.get('/comments', async (req, res: Response): Promise<void> => {
  const authReq = req as AuthenticatedRequest;
  const sb = createSupabaseClient(authReq.token);

  const { video_id, category, has_response, is_from_owner, limit, offset, search } = req.query;

  let query = sb
    .from('yt_comments')
    .select('*, yt_videos(title)')
    .order('comment_date', { ascending: false });

  // Default: exclude owner's own comments
  const fromOwnerFilter = is_from_owner !== undefined ? is_from_owner === 'true' : false;
  query = query.eq('is_from_owner', fromOwnerFilter);

  if (video_id && typeof video_id === 'string') {
    query = query.eq('video_id', video_id);
  }

  if (category && typeof category === 'string') {
    query = query.eq('category', category);
  }

  if (has_response !== undefined && typeof has_response === 'string') {
    if (has_response === 'true') {
      query = query.not('id', 'in', '(select comment_id from yt_response_drafts)');
    } else if (has_response === 'false') {
      query = query.not('id', 'in', '(select comment_id from yt_response_drafts)');
    }
  }

  if (search && typeof search === 'string') {
    query = query.ilike('text', `%${search}%`);
  }

  const lim = limit && typeof limit === 'string' ? parseInt(limit, 10) : 50;
  query = query.limit(lim);

  if (offset && typeof offset === 'string') {
    const off = parseInt(offset, 10);
    query = query.range(off, off + lim - 1);
  }

  const { data, error } = await query;

  if (error) {
    res.status(500).json({ error: { message: error.message, code: 'DB_ERROR' } });
    return;
  }

  res.json({ data: data || [], total: data?.length || 0 });
});

// GET /api/v1/youtube/comments/:id
router.get('/comments/:id', async (req, res: Response): Promise<void> => {
  const authReq = req as AuthenticatedRequest;
  const sb = createSupabaseClient(authReq.token);

  const { data: comment, error: commentError } = await sb
    .from('yt_comments')
    .select('*, yt_videos(*)')
    .eq('id', req.params.id)
    .single();

  if (commentError) {
    res.status(404).json({ error: { message: 'Comentário não encontrado', code: 'NOT_FOUND' } });
    return;
  }

  const { data: drafts, error: draftsError } = await sb
    .from('yt_response_drafts')
    .select('*')
    .eq('comment_id', req.params.id)
    .order('created_at', { ascending: false });

  if (draftsError) {
    res.status(500).json({ error: { message: draftsError.message, code: 'DB_ERROR' } });
    return;
  }

  res.json({ ...comment, drafts: drafts || [] });
});

// GET /api/v1/youtube/drafts
router.get('/drafts', async (req, res: Response): Promise<void> => {
  const authReq = req as AuthenticatedRequest;
  const sb = createSupabaseClient(authReq.token);

  const { status, limit, offset } = req.query;

  let query = sb
    .from('yt_response_drafts')
    .select('*, yt_comments(text, author, category, yt_videos(title))')
    .order('created_at', { ascending: false });

  if (status && typeof status === 'string') {
    query = query.eq('status', status);
  }

  const lim = limit && typeof limit === 'string' ? parseInt(limit, 10) : 50;
  query = query.limit(lim);

  if (offset && typeof offset === 'string') {
    const off = parseInt(offset, 10);
    query = query.range(off, off + lim - 1);
  }

  const { data, error } = await query;

  if (error) {
    res.status(500).json({ error: { message: error.message, code: 'DB_ERROR' } });
    return;
  }

  res.json({ data: data || [], total: data?.length || 0 });
});

// PATCH /api/v1/youtube/drafts/:id
router.patch('/drafts/:id', async (req, res: Response): Promise<void> => {
  const authReq = req as AuthenticatedRequest;
  const sb = createSupabaseClient(authReq.token);

  const { status, edited_text } = req.body as { status?: string; edited_text?: string };

  const updates: Record<string, unknown> = {};

  if (status !== undefined) {
    updates.status = status;
    if (status === 'approved' || status === 'edited') {
      updates.reviewed_at = new Date().toISOString();
    }
    if (status === 'posted') {
      updates.posted_at = new Date().toISOString();
    }
  }

  if (edited_text !== undefined) {
    updates.edited_text = edited_text;
  }

  const { data, error } = await sb
    .from('yt_response_drafts')
    .update(updates)
    .eq('id', req.params.id)
    .select()
    .single();

  if (error) {
    res.status(500).json({ error: { message: error.message, code: 'DB_ERROR' } });
    return;
  }

  res.json(data);
});

// POST /api/v1/youtube/drafts/:id/regenerate
router.post('/drafts/:id/regenerate', async (_req, res: Response): Promise<void> => {
  res.status(501).json({ error: { message: 'Geração de drafts não implementada ainda', code: 'NOT_IMPLEMENTED' } });
});

export default router;
