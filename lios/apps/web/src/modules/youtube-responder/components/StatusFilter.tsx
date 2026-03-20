import { cn } from '../../../lib/utils';
import { STATUS_LABELS, STATUS_COLORS } from '../types';
import type { DraftStatus } from '../types';

const ALL_STATUSES = Object.keys(STATUS_LABELS) as DraftStatus[];

interface StatusFilterProps {
  selected: DraftStatus | null;
  onChange: (status: DraftStatus | null) => void;
  counts?: Record<string, number>;
}

export function StatusFilter({ selected, onChange, counts }: StatusFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      <button
        onClick={() => onChange(null)}
        className={cn(
          'px-3 py-1.5 rounded-lg text-xs font-subtitle transition-colors border',
          selected === null
            ? 'bg-lios-green/20 text-lios-green border-lios-green/40'
            : 'bg-lios-surface text-lios-gray-400 border-lios-border hover:text-white hover:border-lios-border/60'
        )}
      >
        Todos
        {counts && (
          <span className="ml-1.5 opacity-70">
            {Object.values(counts).reduce((a, b) => a + b, 0)}
          </span>
        )}
      </button>

      {ALL_STATUSES.map((status) => {
        const colors = STATUS_COLORS[status];
        const isSelected = selected === status;
        const count = counts?.[status];

        return (
          <button
            key={status}
            onClick={() => onChange(isSelected ? null : status)}
            className={cn(
              'px-3 py-1.5 rounded-lg text-xs font-subtitle transition-colors border',
              isSelected
                ? cn(colors.bg, colors.text, 'border-current/30')
                : 'bg-lios-surface text-lios-gray-400 border-lios-border hover:text-white hover:border-lios-border/60'
            )}
          >
            {STATUS_LABELS[status]}
            {count !== undefined && (
              <span className="ml-1.5 opacity-70">{count}</span>
            )}
          </button>
        );
      })}
    </div>
  );
}
