/* ─── YouTube Responder — Shared Types ───────────────────────────────────── */

export interface YtVideo {
  id: string;
  youtube_video_id: string;
  title: string;
  published_at: string | null;
  comment_count: number;
  responded_count: number;
  created_at: string;
}

export interface YtComment {
  id: string;
  video_id: string;
  author: string;
  text: string;
  likes: number;
  is_reply: boolean;
  category: CommentCategory | null;
  has_response: boolean;
  is_from_owner: boolean;
  comment_date: string | null;
  collected_at: string;
  yt_videos?: { title: string };
}

export interface YtDraft {
  id: string;
  comment_id: string;
  draft_text: string;
  status: DraftStatus;
  edited_text: string | null;
  confidence_score: number | null;
  category_used: string | null;
  reviewed_at: string | null;
  posted_at: string | null;
  created_at: string;
  yt_comments?: {
    text: string;
    author: string;
    category: string | null;
    yt_videos?: { title: string };
  };
}

export type CommentCategory =
  | 'technical_question'
  | 'praise'
  | 'complaint'
  | 'course_inquiry'
  | 'share_experience'
  | 'correction_needed'
  | 'general'
  | 'spam';

export type DraftStatus = 'pending' | 'approved' | 'edited' | 'rejected' | 'posted';

export const CATEGORY_LABELS: Record<CommentCategory, string> = {
  technical_question: 'Pergunta Técnica',
  praise: 'Elogio',
  complaint: 'Reclamação',
  course_inquiry: 'Interesse no Curso',
  share_experience: 'Compartilhando Experiência',
  correction_needed: 'Precisa Correção',
  general: 'Geral',
  spam: 'Spam',
};

export const CATEGORY_COLORS: Record<CommentCategory, { bg: string; text: string; border: string }> = {
  technical_question: { bg: 'bg-blue-500/15',    text: 'text-blue-400',          border: 'border-blue-500/30' },
  praise:             { bg: 'bg-emerald-500/15',  text: 'text-emerald-400',       border: 'border-emerald-500/30' },
  complaint:          { bg: 'bg-red-500/15',      text: 'text-red-400',           border: 'border-red-500/30' },
  course_inquiry:     { bg: 'bg-amber-500/15',    text: 'text-amber-400',         border: 'border-amber-500/30' },
  share_experience:   { bg: 'bg-violet-500/15',   text: 'text-violet-400',        border: 'border-violet-500/30' },
  correction_needed:  { bg: 'bg-orange-500/15',   text: 'text-orange-400',        border: 'border-orange-500/30' },
  general:            { bg: 'bg-white/10',         text: 'text-lios-gray-300',    border: 'border-white/15' },
  spam:               { bg: 'bg-lios-gray-400/10', text: 'text-lios-gray-400',    border: 'border-lios-gray-400/20' },
};

export const STATUS_LABELS: Record<DraftStatus, string> = {
  pending:  'Pendente',
  approved: 'Aprovado',
  edited:   'Editado',
  rejected: 'Rejeitado',
  posted:   'Postado',
};

export const STATUS_COLORS: Record<DraftStatus, { bg: string; text: string }> = {
  pending:  { bg: 'bg-yellow-500/15',   text: 'text-yellow-400' },
  approved: { bg: 'bg-emerald-500/15',  text: 'text-emerald-400' },
  edited:   { bg: 'bg-blue-500/15',     text: 'text-blue-400' },
  rejected: { bg: 'bg-red-500/15',      text: 'text-red-400' },
  posted:   { bg: 'bg-lios-green/15',   text: 'text-lios-green' },
};

export interface YtStats {
  total_videos: number;
  total_comments: number;
  pending_drafts: number;
  approved_drafts: number;
  response_rate: number;
}
