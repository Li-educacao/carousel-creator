import { useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, ChevronRight } from 'lucide-react';
import { useClasses } from '../hooks/useClasses';
import { STATUS_LABELS, STATUS_COLORS } from '../types';
import type { PedClass } from '../types';
import { cn } from '../../../lib/utils';

function formatDate(date: string | null) {
  if (!date) return '—';
  return new Date(date + 'T00:00:00').toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' });
}


export default function ClassesPage() {
  const navigate = useNavigate();
  const { classes, loading, fetchClasses } = useClasses();

  useEffect(() => {
    fetchClasses();
  }, [fetchClasses]);

  // Group by product_name
  const grouped = useMemo(() => {
    const groups: Record<string, PedClass[]> = {};
    for (const cls of classes) {
      const key = cls.product_name || 'Outros';
      if (!groups[key]) groups[key] = [];
      groups[key].push(cls);
    }
    // Sort groups: largest first
    return Object.entries(groups).sort((a, b) => b[1].length - a[1].length);
  }, [classes]);

  const totalStudents = classes.reduce((sum, c) => sum + (c.student_count ?? 0), 0);

  return (
    <div className="px-6 py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-heading text-white">Turmas</h2>
            <p className="text-sm font-body text-lios-gray-400 mt-1">
              {classes.length} turmas · {totalStudents} matrículas
            </p>
          </div>
        </div>

        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="rounded-xl border border-lios-border bg-lios-surface h-20 animate-pulse" />
            ))}
          </div>
        ) : classes.length === 0 ? (
          <div className="rounded-xl border border-lios-border bg-lios-surface p-10 text-center">
            <p className="text-sm font-body text-lios-gray-400">Nenhuma turma criada ainda</p>
          </div>
        ) : (
          <div className="space-y-8">
            {grouped.map(([productName, productClasses]) => (
              <div key={productName}>
                {/* Product group header */}
                <div className="flex items-center gap-3 mb-3">
                  <h3 className="text-sm font-subtitle text-lios-green uppercase tracking-wider">{productName}</h3>
                  <span className="text-xs font-caption text-lios-gray-400">
                    {productClasses.length} turmas · {productClasses.reduce((s, c) => s + (c.student_count ?? 0), 0)} alunos
                  </span>
                  <div className="flex-1 border-t border-lios-border" />
                </div>

                {/* Timeline list */}
                <div className="rounded-xl border border-lios-border bg-lios-surface overflow-hidden">
                  {productClasses.map((cls, i) => (
                    <button
                      key={cls.id}
                      onClick={() => navigate(`/app/pedagogico/turmas/${cls.id}`)}
                      className={cn(
                        'w-full flex items-center gap-4 px-5 py-3.5 text-left hover:bg-white/5 transition-colors group',
                        i > 0 && 'border-t border-lios-border'
                      )}
                    >
                      {/* Date column */}
                      <div className="w-20 shrink-0 text-center">
                        <p className="text-xs font-subtitle text-lios-gray-400">
                          {formatDate(cls.start_date)}
                        </p>
                      </div>

                      {/* Vertical line dot */}
                      <div className="flex flex-col items-center shrink-0">
                        <div className={cn(
                          'w-2.5 h-2.5 rounded-full',
                          cls.status === 'active' ? 'bg-lios-green' : 'bg-lios-gray-400/40'
                        )} />
                      </div>

                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-heading text-lios-green">{cls.abbreviation}</span>
                          <h4 className="text-sm font-subtitle text-white truncate group-hover:text-lios-green transition-colors">
                            {cls.name}
                          </h4>
                        </div>
                      </div>

                      {/* Stats */}
                      <div className="flex items-center gap-4 shrink-0">
                        <span className="flex items-center gap-1.5 text-xs font-body text-lios-gray-400">
                          <Users size={13} /> {cls.student_count ?? 0}
                        </span>
                        <span className={cn(
                          'text-[10px] font-caption px-2 py-0.5 rounded-full',
                          STATUS_COLORS[cls.status]?.bg, STATUS_COLORS[cls.status]?.text
                        )}>
                          {STATUS_LABELS[cls.status]}
                        </span>
                        <ChevronRight size={14} className="text-lios-gray-400/40 group-hover:text-lios-green transition-colors" />
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
