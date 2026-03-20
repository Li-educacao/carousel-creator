import { useEffect, useState, useCallback } from 'react';
import { Search, Video, MessageSquare, TrendingUp, Lightbulb, RefreshCw } from 'lucide-react';
import { cn } from '../../../lib/utils';
import { useContentStudio } from '../hooks/useContentStudio';
import VideoTable from '../components/VideoTable';
import TopVideosSection from '../components/TopVideosSection';
import IdeasSection from '../components/IdeasSection';

type Section = 'historico' | 'top10' | 'ideias';

export default function ContentPage() {
  const {
    videos,
    insights,
    totalVideos,
    totalComments,
    lastUpdated,
    loading,
    error,
    fetchVideos,
    fetchInsights,
  } = useContentStudio();

  const [search, setSearch] = useState('');
  const [activeSection, setActiveSection] = useState<Section>('top10');

  useEffect(() => {
    fetchVideos();
    fetchInsights();
  }, [fetchVideos, fetchInsights]);

  const handleSearch = useCallback((value: string) => {
    setSearch(value);
    fetchVideos({ search: value || undefined });
  }, [fetchVideos]);

  const sections: { key: Section; label: string; icon: typeof Video }[] = [
    { key: 'historico', label: 'Histórico de Aulas', icon: Video },
    { key: 'top10', label: 'Top 10 Aulas', icon: TrendingUp },
    { key: 'ideias', label: 'Ideias de Conteúdo', icon: Lightbulb },
  ];

  return (
    <div className="p-4 sm:p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl font-heading text-white">Conteúdo</h1>
          <p className="text-sm font-body text-lios-gray-400 mt-1">
            YouTube Content Studio — Análise e ideias de conteúdo
          </p>
        </div>
        {lastUpdated && (
          <div className="flex items-center gap-2 text-xs text-lios-gray-400 font-body">
            <RefreshCw size={12} />
            Atualizado em {new Date(lastUpdated).toLocaleDateString('pt-BR', {
              day: '2-digit',
              month: '2-digit',
              year: 'numeric',
            })}
          </div>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <StatCard
          label="Vídeos"
          value={totalVideos}
          icon={<Video size={16} />}
          color="text-lios-green"
        />
        <StatCard
          label="Comentários"
          value={totalComments}
          icon={<MessageSquare size={16} />}
          color="text-lios-blue"
        />
        <StatCard
          label="Total Views"
          value={videos.reduce((sum, v) => sum + v.views, 0)}
          icon={<TrendingUp size={16} />}
          color="text-amber-400"
          format
        />
        <StatCard
          label="Ideias Geradas"
          value={insights?.data?.length ?? 0}
          icon={<Lightbulb size={16} />}
          color="text-violet-400"
        />
      </div>

      {/* Section tabs */}
      <div className="flex items-center gap-1 bg-lios-surface rounded-lg p-1 border border-lios-border">
        {sections.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            onClick={() => setActiveSection(key)}
            className={cn(
              'flex-1 flex items-center justify-center gap-2 px-3 py-2.5 rounded-md text-sm font-subtitle transition-colors',
              activeSection === key
                ? 'bg-lios-green/15 text-lios-green'
                : 'text-lios-gray-400 hover:text-white hover:bg-white/5'
            )}
          >
            <Icon size={16} />
            <span className="hidden sm:inline">{label}</span>
          </button>
        ))}
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-lg px-4 py-3 text-sm text-red-400 font-body">
          {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="text-center py-12 text-lios-gray-400 font-body">
          Carregando...
        </div>
      )}

      {/* Content sections */}
      {!loading && (
        <>
          {activeSection === 'historico' && (
            <div className="space-y-4">
              {/* Search */}
              <div className="relative max-w-md">
                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-lios-gray-400" />
                <input
                  type="text"
                  placeholder="Buscar por título..."
                  value={search}
                  onChange={(e) => handleSearch(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-lios-surface border border-lios-border rounded-lg text-sm text-white font-body placeholder:text-lios-gray-400/60 focus:outline-none focus:border-lios-green/50 transition-colors"
                />
              </div>
              <VideoTable videos={videos} />
            </div>
          )}

          {activeSection === 'top10' && (
            <TopVideosSection videos={videos} />
          )}

          {activeSection === 'ideias' && (
            <IdeasSection
              ideas={insights?.data ?? []}
              generatedAt={insights?.generated_at ?? null}
            />
          )}
        </>
      )}
    </div>
  );
}

/* ─── StatCard ────────────────────────────────────────────────────────────── */

function StatCard({
  label,
  value,
  icon,
  color,
  format,
}: {
  label: string;
  value: number;
  icon: React.ReactNode;
  color: string;
  format?: boolean;
}) {
  const formatted = format
    ? value >= 1_000_000
      ? `${(value / 1_000_000).toFixed(1)}M`
      : value >= 1_000
        ? `${(value / 1_000).toFixed(1)}K`
        : String(value)
    : String(value);

  return (
    <div className="bg-lios-surface rounded-lg border border-lios-border p-4">
      <div className="flex items-center gap-2 mb-2">
        <span className={color}>{icon}</span>
        <span className="text-xs font-subtitle text-lios-gray-400">{label}</span>
      </div>
      <p className={cn('text-2xl font-heading', color)}>{formatted}</p>
    </div>
  );
}
