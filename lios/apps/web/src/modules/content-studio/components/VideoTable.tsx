import { useState, useMemo } from 'react';
import { cn } from '../../../lib/utils';
import { ArrowUpDown, ArrowUp, ArrowDown, ExternalLink } from 'lucide-react';
import type { CtVideo, SortField, SortDirection } from '../types';

interface VideoTableProps {
  videos: CtVideo[];
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}

function formatNumber(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
}

const COLUMNS: { key: SortField; label: string; align?: string }[] = [
  { key: 'lesson_number', label: '#' },
  { key: 'title', label: 'Título' },
  { key: 'published_at', label: 'Data' },
  { key: 'views', label: 'Views', align: 'text-right' },
  { key: 'likes', label: 'Likes', align: 'text-right' },
  { key: 'comment_count', label: 'Comentários', align: 'text-right' },
];

export default function VideoTable({ videos }: VideoTableProps) {
  const [sortField, setSortField] = useState<SortField>('lesson_number');
  const [sortDir, setSortDir] = useState<SortDirection>('desc');

  const sorted = useMemo(() => {
    return [...videos].sort((a, b) => {
      const aVal = a[sortField];
      const bVal = b[sortField];

      if (aVal == null && bVal == null) return 0;
      if (aVal == null) return 1;
      if (bVal == null) return -1;

      let cmp = 0;
      if (typeof aVal === 'string' && typeof bVal === 'string') {
        cmp = aVal.localeCompare(bVal, 'pt-BR', { sensitivity: 'base' });
      } else {
        cmp = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
      }

      return sortDir === 'asc' ? cmp : -cmp;
    });
  }, [videos, sortField, sortDir]);

  function handleSort(field: SortField) {
    if (field === sortField) {
      setSortDir((d) => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortField(field);
      setSortDir('desc');
    }
  }

  function SortIcon({ field }: { field: SortField }) {
    if (field !== sortField) return <ArrowUpDown size={14} className="text-lios-gray-400/40" />;
    return sortDir === 'asc'
      ? <ArrowUp size={14} className="text-lios-green" />
      : <ArrowDown size={14} className="text-lios-green" />;
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-lios-border">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-lios-border bg-lios-surface">
            {COLUMNS.map((col) => (
              <th
                key={col.key}
                className={cn(
                  'px-4 py-3 font-subtitle text-lios-gray-400 cursor-pointer select-none hover:text-white transition-colors',
                  col.align ?? 'text-left'
                )}
                onClick={() => handleSort(col.key)}
              >
                <span className="inline-flex items-center gap-1.5">
                  {col.label}
                  <SortIcon field={col.key} />
                </span>
              </th>
            ))}
            <th className="px-4 py-3 w-10" />
          </tr>
        </thead>
        <tbody>
          {sorted.map((video) => (
            <tr
              key={video.id}
              className="border-b border-lios-border/50 hover:bg-white/[0.02] transition-colors"
            >
              <td className="px-4 py-3 font-subtitle text-lios-gray-300 w-16">
                {video.lesson_number ? `#${video.lesson_number}` : '—'}
              </td>
              <td className="px-4 py-3 text-white font-body max-w-md">
                <span className="line-clamp-1">{video.title}</span>
              </td>
              <td className="px-4 py-3 text-lios-gray-400 font-body whitespace-nowrap">
                {formatDate(video.published_at)}
              </td>
              <td className="px-4 py-3 text-right text-lios-gray-300 font-subtitle tabular-nums">
                {formatNumber(video.views)}
              </td>
              <td className="px-4 py-3 text-right text-lios-gray-300 font-subtitle tabular-nums">
                {formatNumber(video.likes)}
              </td>
              <td className="px-4 py-3 text-right text-lios-gray-300 font-subtitle tabular-nums">
                {formatNumber(video.comment_count)}
              </td>
              <td className="px-4 py-3 text-right">
                <a
                  href={`https://youtube.com/watch?v=${video.video_id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-lios-gray-400 hover:text-lios-green transition-colors"
                  title="Abrir no YouTube"
                >
                  <ExternalLink size={14} />
                </a>
              </td>
            </tr>
          ))}
          {sorted.length === 0 && (
            <tr>
              <td colSpan={7} className="px-4 py-12 text-center text-lios-gray-400 font-body">
                Nenhum vídeo encontrado.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
