import { ShieldCheck } from 'lucide-react';
import type { TgMetricsSLA, TgMetricsResponseTime } from '../types';

/* ─── Helpers ─────────────────────────────────────────────────────────────── */

function formatMinutes(totalMin: number): string {
  if (totalMin < 60) return `${totalMin}min`;
  const h = Math.floor(totalMin / 60);
  const m = totalMin % 60;
  return m === 0 ? `${h}h` : `${h}h${String(m).padStart(2, '0')}`;
}

function improvementFactor(promised_min: number, actual_min: number): number {
  return Math.round(promised_min / actual_min);
}

/* ─── Period column ───────────────────────────────────────────────────────── */

interface PeriodColProps {
  label: string;
  supportMin: number;
  groupMin: number;
  isWorkday: boolean;
}

function PeriodCol({ label, supportMin, groupMin, isWorkday }: PeriodColProps) {
  // SLA promise = 24h úteis = 1440min weekday
  const promisedMin = 24 * 60;
  const supportFactor = improvementFactor(promisedMin, supportMin);
  const groupFactor = improvementFactor(promisedMin, groupMin);

  return (
    <div className="flex-1 rounded-lg border border-lios-border bg-lios-surface-2 p-4">
      <p className="text-xs font-subtitle text-lios-gray-400 uppercase tracking-wide mb-4">
        {label}
      </p>

      {/* Support row */}
      <div className="mb-3">
        <p className="text-[10px] font-body text-lios-gray-400 mb-1">Suporte</p>
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-lg font-heading text-white">{formatMinutes(supportMin)}</span>
          {isWorkday && (
            <span className="px-1.5 py-0.5 rounded text-[10px] font-subtitle bg-lios-green/15 text-lios-green border border-lios-green/30">
              {supportFactor}x melhor
            </span>
          )}
        </div>
        {!isWorkday && (
          <p className="text-[10px] font-body text-lios-gray-400 mt-0.5">(não prometido)</p>
        )}
      </div>

      {/* Group row */}
      <div>
        <p className="text-[10px] font-body text-lios-gray-400 mb-1">Comunidade</p>
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-lg font-heading text-white">{formatMinutes(groupMin)}</span>
          {isWorkday && (
            <span className="px-1.5 py-0.5 rounded text-[10px] font-subtitle bg-lios-green/15 text-lios-green border border-lios-green/30">
              {groupFactor}x melhor
            </span>
          )}
        </div>
        {!isWorkday && (
          <p className="text-[10px] font-body text-lios-gray-400 mt-0.5">(cobertura voluntária)</p>
        )}
      </div>
    </div>
  );
}

/* ─── SLACard ─────────────────────────────────────────────────────────────── */

interface SLACardProps {
  sla: TgMetricsSLA;
  responseTime: TgMetricsResponseTime;
}

export function SLACard({ sla, responseTime }: SLACardProps) {
  const supportPct = responseTime.support_first_pct;
  const groupPct = responseTime.group_first_pct;

  return (
    <div className="rounded-xl border border-lios-border bg-lios-surface p-6 mb-6">
      {/* Header */}
      <div className="flex items-center gap-2 mb-1">
        <ShieldCheck size={16} className="text-lios-green shrink-0" />
        <h3 className="text-base font-subtitle text-white">SLA do Suporte</h3>
      </div>
      <p className="text-xs font-body text-lios-gray-400 mb-5">
        Prometemos: <span className="text-white font-subtitle">{sla.promised}</span>
      </p>

      {/* Period columns */}
      <div className="flex gap-3 mb-5">
        <PeriodCol
          label="Seg — Sex"
          supportMin={sla.support_weekday_median_min}
          groupMin={sla.group_weekday_median_min}
          isWorkday
        />
        <PeriodCol
          label="Fim de semana"
          supportMin={sla.support_weekend_median_min}
          groupMin={sla.group_weekend_median_min}
          isWorkday={false}
        />
      </div>

      {/* Who responds first */}
      <div>
        <p className="text-xs font-body text-lios-gray-400 mb-2">Quem responde primeiro</p>
        <div className="h-2 rounded-full overflow-hidden bg-lios-surface-2 flex">
          <div
            className="h-full bg-lios-green transition-all"
            style={{ width: `${supportPct}%` }}
          />
          <div
            className="h-full bg-white/20 transition-all"
            style={{ width: `${groupPct}%` }}
          />
        </div>
        <div className="flex justify-between mt-1.5">
          <span className="text-[11px] font-body text-lios-green">
            Suporte {supportPct}%
          </span>
          <span className="text-[11px] font-body text-lios-gray-400">
            Comunidade {groupPct}%
          </span>
        </div>
        <p className="text-[10px] font-body text-lios-gray-400 mt-1">
          {responseTime.total_responses.toLocaleString('pt-BR')} respostas analisadas
        </p>
      </div>
    </div>
  );
}
