import { useState } from 'react';
import { CheckCircle, Edit2, X, Save, Film, User, ArrowRight } from 'lucide-react';
import { cn } from '../../../lib/utils';
import { STATUS_LABELS, STATUS_COLORS, CATEGORY_LABELS, CATEGORY_COLORS } from '../types';
import type { YtDraft, CommentCategory } from '../types';

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

interface DraftCardProps {
  draft: YtDraft;
  onUpdate: (id: string, payload: { status: string; edited_text?: string }) => Promise<boolean>;
}

export function DraftCard({ draft, onUpdate }: DraftCardProps) {
  const [editMode, setEditMode] = useState(false);
  const [editText, setEditText] = useState(draft.draft_text);
  const [busy, setBusy] = useState(false);

  const statusColors = STATUS_COLORS[draft.status];
  const statusLabel  = STATUS_LABELS[draft.status];

  const commentCategory = draft.yt_comments?.category as CommentCategory | null | undefined;
  const categoryColors  = commentCategory ? CATEGORY_COLORS[commentCategory] : null;
  const categoryLabel   = commentCategory ? CATEGORY_LABELS[commentCategory] : null;

  const isResolved = draft.status === 'approved' || draft.status === 'edited' || draft.status === 'rejected' || draft.status === 'posted';

  async function handleApprove() {
    setBusy(true);
    await onUpdate(draft.id, { status: 'approved' });
    setBusy(false);
  }

  async function handleReject() {
    setBusy(true);
    await onUpdate(draft.id, { status: 'rejected' });
    setBusy(false);
  }

  async function handleSaveEdit() {
    if (!editText.trim()) return;
    setBusy(true);
    const ok = await onUpdate(draft.id, { status: 'edited', edited_text: editText.trim() });
    setBusy(false);
    if (ok) setEditMode(false);
  }

  function handleCancelEdit() {
    setEditText(draft.draft_text);
    setEditMode(false);
  }

  return (
    <div className="rounded-xl border border-lios-border bg-lios-surface p-5 transition-colors hover:border-lios-border/70">
      {/* Video title + status + date */}
      <div className="flex items-center gap-2 mb-4 flex-wrap">
        {draft.yt_comments?.yt_videos?.title && (
          <div className="flex items-center gap-1.5 mr-auto min-w-0">
            <Film size={12} className="text-lios-gray-400 shrink-0" />
            <span className="text-xs font-body text-lios-gray-400 truncate">
              {draft.yt_comments.yt_videos.title}
            </span>
          </div>
        )}

        <span
          className={cn(
            'inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-subtitle shrink-0',
            statusColors.bg,
            statusColors.text
          )}
        >
          {statusLabel}
        </span>

        <span className="text-[11px] font-body text-lios-gray-400 shrink-0">
          {formatDate(draft.created_at)}
        </span>
      </div>

      {/* Two-column layout: Comment (left) → Response (right) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">

        {/* ── COMENTÁRIO COMPLETO ─────────────────────────────────────── */}
        <div className="rounded-lg border border-lios-border bg-lios-surface-2 p-4">
          <div className="flex items-center gap-2 mb-2">
            <User size={14} className="text-lios-gray-400 shrink-0" />
            <span className="text-sm font-subtitle text-lios-gray-300">
              {draft.yt_comments?.author ?? 'Autor desconhecido'}
            </span>

            {categoryColors && categoryLabel && (
              <span
                className={cn(
                  'inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-subtitle border',
                  categoryColors.bg,
                  categoryColors.text,
                  categoryColors.border
                )}
              >
                {categoryLabel}
              </span>
            )}
          </div>

          {/* Full comment text — no truncation */}
          <p className="text-sm font-body text-white leading-relaxed whitespace-pre-wrap">
            {draft.yt_comments?.text ?? '—'}
          </p>
        </div>

        {/* ── RESPOSTA PROPOSTA ───────────────────────────────────────── */}
        <div className="rounded-lg border border-lios-green/20 bg-lios-green/5 p-4">
          <div className="flex items-center gap-2 mb-2">
            <ArrowRight size={14} className="text-lios-green shrink-0" />
            <span className="text-sm font-subtitle text-lios-green">
              Resposta proposta
            </span>

            {draft.confidence_score !== null && (
              <span className="ml-auto text-[11px] font-body text-lios-gray-400">
                {Math.round(draft.confidence_score * 100)}% confiança
              </span>
            )}
          </div>

          {editMode ? (
            <textarea
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              rows={5}
              className="w-full rounded-lg border border-lios-border bg-lios-surface-2 px-3 py-2.5 text-sm font-body text-white placeholder-lios-gray-400 focus:outline-none focus:border-lios-green/50 resize-none transition-colors"
              disabled={busy}
              autoFocus
            />
          ) : (
            <p className="text-sm font-body text-white leading-relaxed whitespace-pre-wrap">
              {draft.status === 'edited' && draft.edited_text ? draft.edited_text : draft.draft_text}
            </p>
          )}
        </div>
      </div>

      {/* Action buttons */}
      {!isResolved && (
        <div className="mt-4 flex items-center gap-2 flex-wrap">
          {editMode ? (
            <>
              <button
                onClick={handleSaveEdit}
                disabled={busy || !editText.trim()}
                className={cn(
                  'inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-subtitle transition-colors border',
                  'bg-blue-500/15 text-blue-400 border-blue-500/30 hover:bg-blue-500/25',
                  'disabled:opacity-50 disabled:pointer-events-none'
                )}
              >
                <Save size={13} />
                Salvar correção
              </button>
              <button
                onClick={handleCancelEdit}
                disabled={busy}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-subtitle transition-colors border bg-lios-surface-2 text-lios-gray-400 border-lios-border hover:text-white disabled:opacity-50 disabled:pointer-events-none"
              >
                Cancelar
              </button>
            </>
          ) : (
            <>
              <button
                onClick={handleApprove}
                disabled={busy}
                className={cn(
                  'inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-subtitle transition-colors border',
                  'bg-emerald-500/15 text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/25',
                  'disabled:opacity-50 disabled:pointer-events-none'
                )}
              >
                <CheckCircle size={13} />
                Aprovar
              </button>
              <button
                onClick={() => setEditMode(true)}
                disabled={busy}
                className={cn(
                  'inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-subtitle transition-colors border',
                  'bg-blue-500/15 text-blue-400 border-blue-500/30 hover:bg-blue-500/25',
                  'disabled:opacity-50 disabled:pointer-events-none'
                )}
              >
                <Edit2 size={13} />
                Editar
              </button>
              <button
                onClick={handleReject}
                disabled={busy}
                className={cn(
                  'inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-xs font-subtitle transition-colors border',
                  'bg-red-500/15 text-red-400 border-red-500/30 hover:bg-red-500/25',
                  'disabled:opacity-50 disabled:pointer-events-none'
                )}
              >
                <X size={13} />
                Rejeitar
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
}
