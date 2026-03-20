import { useState, useEffect } from 'react';
import { Video } from 'lucide-react';
import { useYouTubeStats } from '../hooks/useYouTubeStats';
import { useDrafts } from '../hooks/useDrafts';
import { StatsBar } from '../components/StatsBar';
import { DraftCard } from '../components/DraftCard';
import { StatusFilter } from '../components/StatusFilter';
import type { DraftStatus } from '../types';

const PAGE_SIZE = 20;

function CardSkeleton() {
  return (
    <div className="rounded-xl border border-lios-border bg-lios-surface h-48 animate-pulse" />
  );
}

export default function YouTubeDashboard() {
  const [statusFilter, setStatusFilter] = useState<DraftStatus | null>(null);
  const [draftsOffset, setDraftsOffset] = useState(0);
  const [allDrafts, setAllDrafts] = useState<ReturnType<typeof useDrafts>['drafts']>([]);

  const { stats, loading: statsLoading, fetchStats } = useYouTubeStats();
  const { drafts, total: draftsTotal, loading: draftsLoading, fetchDrafts, updateDraft } = useDrafts();

  // Load stats on mount
  useEffect(() => {
    fetchStats();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Load drafts when filter changes (reset)
  useEffect(() => {
    setDraftsOffset(0);
    setAllDrafts([]);
    fetchDrafts({
      status: statusFilter ?? undefined,
      limit: PAGE_SIZE,
      offset: 0,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter]);

  // Load more
  useEffect(() => {
    if (draftsOffset === 0) return;
    fetchDrafts({
      status: statusFilter ?? undefined,
      limit: PAGE_SIZE,
      offset: draftsOffset,
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draftsOffset]);

  // Accumulate drafts
  useEffect(() => {
    if (draftsOffset === 0) {
      setAllDrafts(drafts);
    } else {
      setAllDrafts((prev) => [...prev, ...drafts]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [drafts]);

  async function handleUpdateDraft(id: string, payload: { status: string; edited_text?: string }) {
    const result = await updateDraft(id, payload as Parameters<typeof updateDraft>[1]);
    // Refresh stats after action
    if (result) fetchStats();
    return result;
  }

  const hasMore = allDrafts.length < draftsTotal;

  return (
    <div className="px-6 py-8">
      <div className="max-w-5xl mx-auto">

        {/* Page header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-lios-green/15 flex items-center justify-center">
            <Video size={20} className="text-lios-green" />
          </div>
          <div>
            <h2 className="text-2xl font-heading text-white">YouTube Responder</h2>
            <p className="text-sm font-body text-lios-gray-400 mt-0.5">
              Revise as respostas geradas pelo seu clone — aprove, edite ou rejeite
            </p>
          </div>
        </div>

        {/* Stats */}
        <StatsBar stats={stats} loading={statsLoading} />

        {/* Status filter */}
        <div className="mb-5 overflow-x-auto pb-1">
          <StatusFilter
            selected={statusFilter}
            onChange={setStatusFilter}
          />
        </div>

        {/* Drafts list */}
        {draftsLoading && allDrafts.length === 0 ? (
          <div className="space-y-4">
            {Array.from({ length: 3 }).map((_, i) => <CardSkeleton key={i} />)}
          </div>
        ) : allDrafts.length === 0 ? (
          <div className="py-16 text-center">
            <p className="text-sm font-body text-lios-gray-400">
              {statusFilter
                ? `Nenhuma resposta com status "${statusFilter}".`
                : 'Nenhuma resposta gerada ainda. Rode o gerador para criar drafts.'}
            </p>
          </div>
        ) : (
          <>
            <div className="space-y-4">
              {allDrafts.map((draft) => (
                <DraftCard
                  key={draft.id}
                  draft={draft}
                  onUpdate={handleUpdateDraft}
                />
              ))}
            </div>

            {draftsLoading && (
              <div className="mt-4 space-y-4">
                {Array.from({ length: 2 }).map((_, i) => <CardSkeleton key={i} />)}
              </div>
            )}

            {hasMore && !draftsLoading && (
              <div className="mt-6 text-center">
                <button
                  onClick={() => setDraftsOffset((prev) => prev + PAGE_SIZE)}
                  className="px-5 py-2 rounded-lg text-sm font-subtitle border border-lios-border bg-lios-surface text-lios-gray-300 hover:text-white hover:border-lios-border/60 transition-colors"
                >
                  Carregar mais
                </button>
              </div>
            )}
          </>
        )}

      </div>
    </div>
  );
}
