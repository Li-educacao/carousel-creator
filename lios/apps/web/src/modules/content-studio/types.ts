/* ─── Content Studio — Shared Types ──────────────────────────────────────── */

export interface CtVideo {
  id: string;
  video_id: string;
  lesson_number: number | null;
  title: string;
  published_at: string | null;
  views: number;
  likes: number;
  comment_count: number;
  duration: number;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface CtComment {
  id: string;
  video_id: string;
  author: string;
  text: string;
  likes: number;
  comment_timestamp: number | null;
  created_at: string;
}

export interface ContentIdea {
  title: string;
  justification: string;
  priority: 'alta' | 'media' | 'baixa';
  source_comments: string[];
}

export interface CtInsights {
  id: string;
  type: string;
  data: ContentIdea[];
  generated_at: string;
  updated_at: string;
}

export type SortField = 'lesson_number' | 'title' | 'published_at' | 'views' | 'likes' | 'comment_count';
export type SortDirection = 'asc' | 'desc';

export const PRIORITY_LABELS: Record<ContentIdea['priority'], string> = {
  alta: 'Alta',
  media: 'Média',
  baixa: 'Baixa',
};

export const PRIORITY_COLORS: Record<ContentIdea['priority'], { bg: string; text: string }> = {
  alta:   { bg: 'bg-red-500/15',    text: 'text-red-400' },
  media:  { bg: 'bg-yellow-500/15', text: 'text-yellow-400' },
  baixa:  { bg: 'bg-blue-500/15',   text: 'text-blue-400' },
};
