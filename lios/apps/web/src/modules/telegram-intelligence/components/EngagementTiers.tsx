import { AlertTriangle, Users } from 'lucide-react';
import type { TgMetricsEngagement } from '../types';

/* ─── Tier definitions ────────────────────────────────────────────────────── */

interface Tier {
  key: keyof Omit<TgMetricsEngagement, 'total_participants'>;
  label: string;
  sublabel: string;
  barClass: string;
  textClass: string;
}

const TIERS: Tier[] = [
  {
    key: 'high',
    label: 'Alto',
    sublabel: '20+ msgs',
    barClass: 'bg-lios-green',
    textClass: 'text-lios-green',
  },
  {
    key: 'medium',
    label: 'Médio',
    sublabel: '5–19 msgs',
    barClass: 'bg-yellow-400',
    textClass: 'text-yellow-400',
  },
  {
    key: 'low',
    label: 'Baixo',
    sublabel: '1–4 msgs',
    barClass: 'bg-orange-400',
    textClass: 'text-orange-400',
  },
  {
    key: 'zero',
    label: 'Zero',
    sublabel: '0 substanciais',
    barClass: 'bg-red-500',
    textClass: 'text-red-400',
  },
];

/* ─── EngagementTiers ─────────────────────────────────────────────────────── */

interface EngagementTiersProps {
  engagement: TgMetricsEngagement;
}

export function EngagementTiers({ engagement }: EngagementTiersProps) {
  const { total_participants } = engagement;

  const atRisk = engagement.low + engagement.zero;
  const atRiskPct = Math.round((atRisk / total_participants) * 100);

  return (
    <div className="rounded-xl border border-lios-border bg-lios-surface p-6 h-full">
      {/* Header */}
      <div className="flex items-start justify-between gap-2 mb-5">
        <div className="flex items-center gap-2">
          <Users size={16} className="text-lios-green shrink-0" />
          <h3 className="text-base font-subtitle text-white">Engajamento dos Alunos</h3>
        </div>
        <span className="text-sm font-heading text-lios-gray-400 whitespace-nowrap">
          {total_participants.toLocaleString('pt-BR')} participantes
        </span>
      </div>

      {/* Stacked bar */}
      <div className="h-4 rounded-full overflow-hidden flex mb-4">
        {TIERS.map((tier) => {
          const count = engagement[tier.key] as number;
          const pct = (count / total_participants) * 100;
          return (
            <div
              key={tier.key}
              className={`h-full ${tier.barClass} transition-all`}
              style={{ width: `${pct}%` }}
              title={`${tier.label}: ${count} (${Math.round(pct)}%)`}
            />
          );
        })}
      </div>

      {/* Legend */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
        {TIERS.map((tier) => {
          const count = engagement[tier.key] as number;
          const pct = Math.round((count / total_participants) * 100);
          return (
            <div key={tier.key}>
              <div className="flex items-center gap-1.5 mb-0.5">
                <span className={`w-2.5 h-2.5 rounded-sm ${tier.barClass} shrink-0`} />
                <span className={`text-xs font-subtitle ${tier.textClass}`}>{tier.label}</span>
              </div>
              <p className="text-base font-heading text-white leading-none">{count}</p>
              <p className="text-[10px] font-body text-lios-gray-400 mt-0.5">
                {pct}% · {tier.sublabel}
              </p>
            </div>
          );
        })}
      </div>

      {/* Alert */}
      {atRisk > 0 && (
        <div className="flex items-start gap-2 p-3 rounded-lg bg-orange-500/10 border border-orange-500/20">
          <AlertTriangle size={14} className="text-orange-400 shrink-0 mt-0.5" />
          <div>
            <p className="text-xs font-subtitle text-orange-400">
              {atRisk} alunos com engajamento baixo ou zero ({atRiskPct}%)
            </p>
            <p className="text-[10px] font-body text-lios-gray-400 mt-0.5">
              Candidatos para programa de reativação
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
