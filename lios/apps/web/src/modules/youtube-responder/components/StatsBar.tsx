import { MessageSquare, Clock, CheckCircle } from 'lucide-react';
import { Card } from '../../../components/ui';
import type { YtStats } from '../types';

function formatNumber(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}k`;
  return String(n);
}

interface StatItemProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  accent?: boolean;
}

function StatItem({ icon, label, value, accent }: StatItemProps) {
  return (
    <Card className="p-4 flex items-center gap-4">
      <div
        className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
          accent ? 'bg-lios-green/15' : 'bg-white/5'
        }`}
      >
        <span className={accent ? 'text-lios-green' : 'text-lios-gray-400'}>
          {icon}
        </span>
      </div>
      <div>
        <p className="text-xl font-heading text-white leading-none">{value}</p>
        <p className="text-xs font-body text-lios-gray-400 mt-1">{label}</p>
      </div>
    </Card>
  );
}

interface StatsBarProps {
  stats: YtStats | null;
  loading: boolean;
}

export function StatsBar({ stats, loading }: StatsBarProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-3 gap-3 mb-6">
        {Array.from({ length: 3 }).map((_, i) => (
          <div
            key={i}
            className="rounded-xl border border-lios-border bg-lios-surface p-4 h-20 animate-pulse"
          />
        ))}
      </div>
    );
  }

  const items = [
    {
      icon: <MessageSquare size={20} />,
      label: 'Comentários',
      value: stats ? formatNumber(stats.total_comments) : '—',
      accent: true,
    },
    {
      icon: <Clock size={20} />,
      label: 'Pendentes',
      value: stats ? formatNumber(stats.pending_drafts) : '—',
    },
    {
      icon: <CheckCircle size={20} />,
      label: 'Respondidos',
      value: stats ? formatNumber(stats.approved_drafts) : '—',
    },
  ];

  return (
    <div className="grid grid-cols-3 gap-3 mb-6">
      {items.map((item) => (
        <StatItem key={item.label} {...item} />
      ))}
    </div>
  );
}
