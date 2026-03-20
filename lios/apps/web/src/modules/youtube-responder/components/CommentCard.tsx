import { Film, ThumbsUp, Calendar } from 'lucide-react';
import { cn } from '../../../lib/utils';
import { CATEGORY_LABELS, CATEGORY_COLORS } from '../types';
import type { YtComment } from '../types';

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

interface CommentCardProps {
  comment: YtComment;
}

export function CommentCard({ comment }: CommentCardProps) {
  const colors = comment.category ? CATEGORY_COLORS[comment.category] : null;
  const label = comment.category ? CATEGORY_LABELS[comment.category] : null;

  return (
    <div className="rounded-xl border border-lios-border bg-lios-surface p-4 transition-colors hover:border-lios-border/70">
      {/* Header row: author + badges */}
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-sm font-subtitle text-lios-gray-300">
            {comment.author}
          </span>

          {colors && label && (
            <span
              className={cn(
                'inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-subtitle border',
                colors.bg,
                colors.text,
                colors.border
              )}
            >
              {label}
            </span>
          )}

          {comment.has_response && (
            <span className="inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-subtitle border bg-lios-green/15 text-lios-green border-lios-green/30">
              Respondido
            </span>
          )}
        </div>

        {/* Likes */}
        <span className="flex items-center gap-1 text-[11px] font-body text-lios-gray-400 shrink-0">
          <ThumbsUp size={11} />
          {comment.likes}
        </span>
      </div>

      {/* Video title */}
      {comment.yt_videos?.title && (
        <div className="flex items-center gap-1 mb-2">
          <Film size={11} className="text-lios-gray-400 shrink-0" />
          <span className="text-[11px] font-body text-lios-gray-400 line-clamp-1">
            {comment.yt_videos.title}
          </span>
        </div>
      )}

      {/* Comment text */}
      <p className="text-sm font-body text-white leading-relaxed">
        {comment.text}
      </p>

      {/* Date */}
      <div className="mt-3 flex items-center gap-1 text-[11px] font-body text-lios-gray-400">
        <Calendar size={11} />
        {formatDate(comment.comment_date)}
      </div>
    </div>
  );
}
