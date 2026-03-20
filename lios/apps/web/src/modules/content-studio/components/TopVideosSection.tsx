import { useMemo } from 'react';
import { Eye, ThumbsUp, MessageSquare, TrendingUp, ExternalLink } from 'lucide-react';
import type { CtVideo } from '../types';

interface TopVideosSectionProps {
  videos: CtVideo[];
}

function engagementScore(v: CtVideo): number {
  return v.views + v.likes * 10 + v.comment_count * 20;
}

function formatNumber(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
}

function whyItPerformed(v: CtVideo, _rank: number): string {
  const reasons: string[] = [];
  if (v.views > 10_000) reasons.push('alto volume de views');
  if (v.likes > 200) reasons.push('muitos likes');
  if (v.comment_count > 30) reasons.push('gera muita discussão');
  if (v.title.toLowerCase().includes('erro')) reasons.push('resolve problema específico');
  if (v.title.toLowerCase().includes('como')) reasons.push('conteúdo prático');
  if (v.title.toLowerCase().includes('testar') || v.title.toLowerCase().includes('teste')) reasons.push('ensina diagnóstico');
  if (reasons.length === 0) reasons.push('boa combinação de métricas');
  return reasons.slice(0, 2).join(' + ');
}

export default function TopVideosSection({ videos }: TopVideosSectionProps) {
  const top10 = useMemo(() => {
    return [...videos]
      .sort((a, b) => engagementScore(b) - engagementScore(a))
      .slice(0, 10);
  }, [videos]);

  if (top10.length === 0) {
    return (
      <div className="text-center py-12 text-lios-gray-400 font-body">
        Nenhum vídeo disponível.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {top10.map((video, i) => (
        <div
          key={video.id}
          className="bg-lios-surface rounded-lg border border-lios-border p-4 hover:border-lios-green/30 transition-colors"
        >
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-lios-green/15 flex items-center justify-center shrink-0">
              <span className="text-sm font-subtitle text-lios-green">{i + 1}</span>
            </div>
            <div className="min-w-0 flex-1">
              <div className="flex items-start justify-between gap-2">
                <h3 className="text-sm font-subtitle text-white line-clamp-2 leading-snug">
                  {video.lesson_number && (
                    <span className="text-lios-green mr-1">#{video.lesson_number}</span>
                  )}
                  {video.title}
                </h3>
                <a
                  href={`https://youtube.com/watch?v=${video.video_id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-lios-gray-400 hover:text-lios-green transition-colors shrink-0 mt-0.5"
                >
                  <ExternalLink size={14} />
                </a>
              </div>

              <div className="flex items-center gap-4 mt-2.5 text-xs text-lios-gray-400">
                <span className="inline-flex items-center gap-1">
                  <Eye size={12} /> {formatNumber(video.views)}
                </span>
                <span className="inline-flex items-center gap-1">
                  <ThumbsUp size={12} /> {formatNumber(video.likes)}
                </span>
                <span className="inline-flex items-center gap-1">
                  <MessageSquare size={12} /> {formatNumber(video.comment_count)}
                </span>
              </div>

              <div className="mt-2 flex items-center gap-1.5 text-xs text-lios-green/80">
                <TrendingUp size={12} />
                <span className="font-body">{whyItPerformed(video, i)}</span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
