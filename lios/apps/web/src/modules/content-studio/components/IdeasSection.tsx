import { cn } from '../../../lib/utils';
import { Lightbulb, MessageSquareText } from 'lucide-react';
import type { ContentIdea } from '../types';
import { PRIORITY_LABELS, PRIORITY_COLORS } from '../types';

interface IdeasSectionProps {
  ideas: ContentIdea[];
  generatedAt: string | null;
}

export default function IdeasSection({ ideas, generatedAt }: IdeasSectionProps) {
  if (ideas.length === 0) {
    return (
      <div className="text-center py-12 text-lios-gray-400 font-body">
        Nenhuma ideia gerada ainda. Rode o script de atualização para gerar ideias.
      </div>
    );
  }

  return (
    <div>
      {generatedAt && (
        <p className="text-xs text-lios-gray-400 font-body mb-4">
          Geradas em {new Date(generatedAt).toLocaleDateString('pt-BR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      )}

      <div className="space-y-3">
        {ideas.map((idea, i) => {
          const prioColors = PRIORITY_COLORS[idea.priority];
          return (
            <div
              key={i}
              className="bg-lios-surface rounded-lg border border-lios-border p-4 hover:border-lios-green/30 transition-colors"
            >
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-lg bg-lios-green/15 flex items-center justify-center shrink-0">
                  <Lightbulb size={16} className="text-lios-green" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-start justify-between gap-3">
                    <h3 className="text-sm font-subtitle text-white leading-snug">
                      {idea.title}
                    </h3>
                    <span className={cn(
                      'text-[10px] font-caption px-2 py-0.5 rounded shrink-0',
                      prioColors.bg,
                      prioColors.text
                    )}>
                      {PRIORITY_LABELS[idea.priority]}
                    </span>
                  </div>

                  <p className="text-xs text-lios-gray-400 font-body mt-1.5 leading-relaxed">
                    {idea.justification}
                  </p>

                  {idea.source_comments.length > 0 && (
                    <div className="mt-2.5 space-y-1">
                      {idea.source_comments.slice(0, 2).map((comment, j) => (
                        <div
                          key={j}
                          className="flex items-start gap-1.5 text-[11px] text-lios-gray-400/70"
                        >
                          <MessageSquareText size={11} className="shrink-0 mt-0.5" />
                          <span className="line-clamp-1 italic">"{comment}"</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
