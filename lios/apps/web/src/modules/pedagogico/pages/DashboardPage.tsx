import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, GraduationCap, BookOpen, TrendingUp, DollarSign, AlertTriangle } from 'lucide-react';
import { api } from '../../../lib/api';
import { cn } from '../../../lib/utils';

interface Metrics {
  students: {
    total: number;
    byStatus: Record<string, number>;
    climatronicoLevels: Record<string, number>;
    planDistribution: Record<string, number>;
    renewalsDue: number;
  };
  classes: {
    total: number;
    active: number;
    topClasses: Array<{ abbreviation: string; name: string; product_name: string; student_count: number; status: string; start_date: string | null }>;
  };
  enrollments: {
    total: number;
    byProduct: Record<string, number>;
    monthlyTrend: Record<string, number>;
    paymentMethods: Record<string, number>;
  };
  revenue: {
    total: number;
    byProduct: Record<string, number>;
  };
}

function StatCard({ icon: Icon, label, value, sub, color }: { icon: typeof Users; label: string; value: string | number; sub?: string; color: string }) {
  return (
    <div className="rounded-xl border border-lios-border bg-lios-surface p-4">
      <div className="flex items-center gap-3 mb-2">
        <div className={cn('w-9 h-9 rounded-lg flex items-center justify-center', color)}>
          <Icon size={18} className="text-white" />
        </div>
        <span className="text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider">{label}</span>
      </div>
      <p className="text-2xl font-heading text-white">{value}</p>
      {sub && <p className="text-xs font-body text-lios-gray-400 mt-0.5">{sub}</p>}
    </div>
  );
}

function BarChart({ data, color = 'bg-lios-green' }: { data: Record<string, number>; color?: string }) {
  const entries = Object.entries(data).filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1]);
  const max = Math.max(...entries.map(([, v]) => v), 1);
  return (
    <div className="space-y-2">
      {entries.map(([label, value]) => (
        <div key={label} className="flex items-center gap-3">
          <span className="text-xs font-body text-lios-gray-400 w-32 truncate text-right">{label}</span>
          <div className="flex-1 h-5 bg-lios-surface-2 rounded-full overflow-hidden">
            <div className={cn('h-full rounded-full transition-all', color)} style={{ width: `${(value / max) * 100}%` }} />
          </div>
          <span className="text-xs font-subtitle text-white w-8 text-right">{value}</span>
        </div>
      ))}
    </div>
  );
}

function MiniBarChart({ data }: { data: Record<string, number> }) {
  const entries = Object.entries(data);
  const max = Math.max(...entries.map(([, v]) => v), 1);
  return (
    <div className="flex items-end gap-1 h-24">
      {entries.map(([label, value]) => (
        <div key={label} className="flex-1 flex flex-col items-center gap-1">
          <span className="text-[9px] font-caption text-lios-gray-400">{value || ''}</span>
          <div className="w-full bg-lios-surface-2 rounded-t" style={{ height: `${Math.max((value / max) * 100, 4)}%` }}>
            <div className={cn('w-full h-full rounded-t', value > 0 ? 'bg-lios-green' : 'bg-lios-surface-2')} />
          </div>
          <span className="text-[8px] font-caption text-lios-gray-400">{label.slice(5)}</span>
        </div>
      ))}
    </div>
  );
}

function formatCurrency(value: number) {
  return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', minimumFractionDigits: 0 });
}

export default function DashboardPage() {
  const navigate = useNavigate();
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchMetrics = useCallback(async () => {
    setLoading(true);
    const { data } = await api.get<Metrics>('/api/v1/pedagogico/metrics');
    if (data) setMetrics(data);
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchMetrics();
  }, [fetchMetrics]);

  if (loading || !metrics) {
    return (
      <div className="px-6 py-8">
        <div className="max-w-7xl mx-auto">
          <div className="mb-6">
            <h2 className="text-2xl font-heading text-white">Dashboard Pedagógico</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
            {[1, 2, 3, 4, 5, 6].map(i => (
              <div key={i} className="rounded-xl border border-lios-border bg-lios-surface h-24 animate-pulse" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  const { students, classes, enrollments, revenue } = metrics;

  return (
    <div className="px-6 py-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-heading text-white">Dashboard Pedagógico</h2>
          <p className="text-sm font-body text-lios-gray-400 mt-1">Visão geral da LI Educação Online</p>
        </div>

        {/* Top stats */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
          <StatCard icon={Users} label="Total Alunos" value={students.total} color="bg-lios-green/20" />
          <StatCard icon={TrendingUp} label="Ativos" value={students.byStatus.active || 0}
            sub={`${Math.round(((students.byStatus.active || 0) / students.total) * 100)}% do total`}
            color="bg-emerald-500/20" />
          <StatCard icon={AlertTriangle} label="Inativos" value={students.byStatus.inactive || 0} color="bg-yellow-500/20" />
          <StatCard icon={GraduationCap} label="Turmas" value={classes.total}
            sub={`${classes.active} ativas`}
            color="bg-blue-500/20" />
          <StatCard icon={BookOpen} label="Matrículas" value={enrollments.total} color="bg-purple-500/20" />
          <StatCard icon={DollarSign} label="Receita Total" value={formatCurrency(revenue.total)} color="bg-amber-500/20" />
        </div>

        {/* Row 2: Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Monthly trend */}
          <div className="rounded-xl border border-lios-border bg-lios-surface p-5">
            <h3 className="text-sm font-subtitle text-white mb-4">Matrículas por Mês</h3>
            <MiniBarChart data={enrollments.monthlyTrend} />
          </div>

          {/* By product */}
          <div className="rounded-xl border border-lios-border bg-lios-surface p-5">
            <h3 className="text-sm font-subtitle text-white mb-4">Alunos por Curso</h3>
            <BarChart data={enrollments.byProduct} />
          </div>

          {/* Revenue by product */}
          <div className="rounded-xl border border-lios-border bg-lios-surface p-5">
            <h3 className="text-sm font-subtitle text-white mb-4">Receita por Curso</h3>
            <div className="space-y-2">
              {Object.entries(revenue.byProduct)
                .filter(([, v]) => v > 0)
                .sort((a, b) => b[1] - a[1])
                .map(([label, value]) => (
                  <div key={label} className="flex items-center justify-between">
                    <span className="text-xs font-body text-lios-gray-400 truncate flex-1">{label}</span>
                    <span className="text-xs font-subtitle text-lios-green ml-2">{formatCurrency(value)}</span>
                  </div>
                ))}
            </div>
          </div>
        </div>

        {/* Row 3: Details */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Status breakdown */}
          <div className="rounded-xl border border-lios-border bg-lios-surface p-5">
            <h3 className="text-sm font-subtitle text-white mb-4">Status dos Alunos</h3>
            <div className="space-y-3">
              {[
                { key: 'active', label: 'Ativos', color: 'bg-emerald-500' },
                { key: 'inactive', label: 'Inativos', color: 'bg-yellow-500' },
                { key: 'cancelled', label: 'Cancelados', color: 'bg-red-500' },
                { key: 'refunded', label: 'Reembolsados', color: 'bg-orange-500' },
              ].map(({ key, label, color }) => {
                const count = students.byStatus[key] || 0;
                const pct = students.total > 0 ? (count / students.total) * 100 : 0;
                return (
                  <div key={key}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-body text-lios-gray-400">{label}</span>
                      <span className="text-xs font-subtitle text-white">{count} ({pct.toFixed(0)}%)</span>
                    </div>
                    <div className="h-2 bg-lios-surface-2 rounded-full overflow-hidden">
                      <div className={cn('h-full rounded-full', color)} style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Climatrônico levels */}
          <div className="rounded-xl border border-lios-border bg-lios-surface p-5">
            <h3 className="text-sm font-subtitle text-white mb-4">Nível Climatrônico</h3>
            <div className="space-y-3">
              {Object.entries(students.climatronicoLevels)
                .sort((a, b) => b[1] - a[1])
                .map(([level, count]) => {
                  const pct = students.total > 0 ? (count / students.total) * 100 : 0;
                  const color = level === 'Start' ? 'bg-lios-green' : level === 'Expert' ? 'bg-amber-500' : 'bg-lios-gray-400/30';
                  return (
                    <div key={level}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-body text-lios-gray-400">{level}</span>
                        <span className="text-xs font-subtitle text-white">{count}</span>
                      </div>
                      <div className="h-2 bg-lios-surface-2 rounded-full overflow-hidden">
                        <div className={cn('h-full rounded-full', color)} style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>

          {/* Payment methods */}
          <div className="rounded-xl border border-lios-border bg-lios-surface p-5">
            <h3 className="text-sm font-subtitle text-white mb-4">Formas de Pagamento</h3>
            <div className="space-y-3">
              {Object.entries(enrollments.paymentMethods)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 6)
                .map(([method, count]) => {
                  const pct = enrollments.total > 0 ? (count / enrollments.total) * 100 : 0;
                  return (
                    <div key={method}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-body text-lios-gray-400">{method}</span>
                        <span className="text-xs font-subtitle text-white">{count}</span>
                      </div>
                      <div className="h-2 bg-lios-surface-2 rounded-full overflow-hidden">
                        <div className="h-full rounded-full bg-blue-500" style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>
        </div>

        {/* Row 4: Top classes + Plans */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Top turmas */}
          <div className="rounded-xl border border-lios-border bg-lios-surface">
            <div className="flex items-center justify-between px-5 py-4 border-b border-lios-border">
              <h3 className="text-sm font-subtitle text-white">Top 10 Turmas</h3>
              <button onClick={() => navigate('/app/pedagogico/turmas')} className="text-xs font-subtitle text-lios-green hover:text-lios-green/80 transition-colors">
                Ver todas
              </button>
            </div>
            <div className="divide-y divide-lios-border">
              {classes.topClasses.map((cls, i) => (
                <button
                  key={cls.abbreviation}
                  onClick={() => navigate('/app/pedagogico/turmas')}
                  className="w-full flex items-center gap-3 px-5 py-3 hover:bg-white/5 transition-colors text-left"
                >
                  <span className="text-xs font-heading text-lios-gray-400 w-5">{i + 1}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-subtitle text-white truncate">
                      <span className="text-lios-green">[{cls.abbreviation}]</span> {cls.name}
                    </p>
                    <p className="text-xs font-body text-lios-gray-400">{cls.product_name}</p>
                  </div>
                  <span className="text-sm font-heading text-white">{cls.student_count}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Plan distribution */}
          <div className="rounded-xl border border-lios-border bg-lios-surface">
            <div className="px-5 py-4 border-b border-lios-border">
              <h3 className="text-sm font-subtitle text-white">Distribuição de Planos</h3>
            </div>
            <div className="p-5">
              <div className="space-y-3">
                {Object.entries(students.planDistribution)
                  .sort((a, b) => b[1] - a[1])
                  .slice(0, 8)
                  .map(([plan, count]) => {
                    const pct = students.total > 0 ? (count / students.total) * 100 : 0;
                    return (
                      <div key={plan}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-body text-lios-gray-400">{plan}</span>
                          <span className="text-xs font-subtitle text-white">{count} ({pct.toFixed(0)}%)</span>
                        </div>
                        <div className="h-2 bg-lios-surface-2 rounded-full overflow-hidden">
                          <div className="h-full rounded-full bg-purple-500" style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
