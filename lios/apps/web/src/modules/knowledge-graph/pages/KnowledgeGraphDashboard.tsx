import {
  Brain,
  Network,
  Users,
  GraduationCap,
  RefreshCw,
  Link2,
  MessageCircle,
  BookOpen,
} from 'lucide-react';
import { useKgMetrics } from '../hooks/useKgMetrics';
import { cn } from '../../../lib/utils';

const TYPE_LABELS: Record<string, string> = {
  student: 'Alunos',
  class: 'Turmas',
  telegram_group: 'Grupos Telegram',
  telegram_member: 'Membros Telegram',
  topic: 'Tópicos',
  course: 'Cursos',
  module: 'Módulos',
  campaign: 'Campanhas',
  product: 'Produtos',
};

const RELATION_LABELS: Record<string, string> = {
  matriculado_em: 'Matriculado em',
  participa_de: 'Participa de',
  especialista_em: 'Especialista em',
  comprou: 'Comprou',
  reclamou_de: 'Reclamou de',
  elogiou: 'Elogiou',
  mencionou: 'Mencionou',
  perguntou_sobre: 'Perguntou sobre',
  ensina: 'Ensina',
  monitora: 'Monitora',
};

function StatCard({ title, value, subtitle, icon: Icon, color }: {
  title: string;
  value: string;
  subtitle: string;
  icon: typeof Brain;
  color: string;
}) {
  return (
    <div className="bg-lios-surface rounded-xl border border-lios-border p-5 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <div className={cn('p-2.5 rounded-lg', color === 'blue' ? 'bg-lios-blue/10' : color === 'green' ? 'bg-lios-green/10' : 'bg-white/5')}>
          <Icon size={20} className={cn(color === 'blue' ? 'text-lios-blue' : color === 'green' ? 'text-lios-green' : 'text-lios-gray-300')} />
        </div>
      </div>
      <div>
        <p className="text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider">{title}</p>
        <p className="text-2xl font-heading text-white mt-1">{value}</p>
        <p className={cn('text-sm font-body mt-0.5', color === 'blue' ? 'text-lios-blue' : color === 'green' ? 'text-lios-green' : 'text-lios-gray-400')}>{subtitle}</p>
      </div>
    </div>
  );
}

export default function KnowledgeGraphDashboard() {
  const { loading, metrics, refresh } = useKgMetrics();

  if (loading) {
    return (
      <div className="p-6 max-w-7xl mx-auto">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-lios-surface rounded w-64" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="h-32 bg-lios-surface rounded-xl" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-2xl font-heading text-white">Grafo de Conhecimento</h1>
          <p className="text-sm font-body text-lios-gray-400 mt-1">Visão geral das entidades e relações do LIOS.</p>
        </div>
        <button
          onClick={refresh}
          className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-subtitle text-lios-gray-400 border border-lios-border hover:text-white hover:bg-white/5 transition-colors"
        >
          <RefreshCw size={16} /> Atualizar
        </button>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Entidades"
          value={metrics.totalNodes.toLocaleString('pt-BR')}
          subtitle={`${Object.keys(metrics.typeCounts).length} tipos`}
          icon={Brain}
          color="blue"
        />
        <StatCard
          title="Relações"
          value={metrics.totalEdges.toLocaleString('pt-BR')}
          subtitle={`${metrics.relationStats.length} tipos`}
          icon={Link2}
          color="blue"
        />
        <StatCard
          title="Alunos no Grafo"
          value={(metrics.typeCounts.student ?? 0).toLocaleString('pt-BR')}
          subtitle="com conexões mapeadas"
          icon={Users}
          color="green"
        />
        <StatCard
          title="Turmas"
          value={(metrics.typeCounts.class ?? 0).toLocaleString('pt-BR')}
          subtitle="mapeadas"
          icon={GraduationCap}
          color="green"
        />
      </div>

      {/* Distribution by Type */}
      <div className="bg-lios-surface rounded-xl border border-lios-border p-6">
        <h2 className="text-base font-subtitle text-white mb-4 flex items-center gap-2">
          <Network size={18} className="text-lios-blue" />
          Distribuição de Entidades
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {Object.entries(metrics.typeCounts)
            .sort(([, a], [, b]) => b - a)
            .map(([type, count]) => (
              <div key={type} className="bg-lios-surface-2 rounded-lg p-4">
                <p className="text-xs font-body text-lios-gray-400">{TYPE_LABELS[type] ?? type}</p>
                <p className="text-xl font-heading text-white mt-1">{count.toLocaleString('pt-BR')}</p>
              </div>
            ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Students */}
        <div className="bg-lios-surface rounded-xl border border-lios-border p-6">
          <h2 className="text-base font-subtitle text-white mb-4 flex items-center gap-2">
            <Users size={18} className="text-lios-green" />
            Alunos mais Conectados
          </h2>
          {metrics.topStudents.length === 0 ? (
            <p className="text-sm font-body text-lios-gray-400">Sem dados disponíveis.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-lios-border">
                    <th className="text-left py-2 font-subtitle text-lios-gray-400">Aluno</th>
                    <th className="text-right py-2 font-subtitle text-lios-gray-400">Total</th>
                    <th className="text-right py-2 font-subtitle text-lios-gray-400">Turmas</th>
                    <th className="text-right py-2 font-subtitle text-lios-gray-400">Grupos TG</th>
                  </tr>
                </thead>
                <tbody>
                  {metrics.topStudents.map((s, i) => (
                    <tr key={s.node_id} className={i % 2 === 0 ? 'bg-white/[0.02]' : ''}>
                      <td className="py-2 font-body text-white truncate max-w-[200px]">{s.name}</td>
                      <td className="py-2 text-right font-heading text-white">{s.total_connections}</td>
                      <td className="py-2 text-right font-body text-lios-green">{s.turmas}</td>
                      <td className="py-2 text-right font-body text-lios-blue">{s.grupos_telegram}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Top Classes */}
        <div className="bg-lios-surface rounded-xl border border-lios-border p-6">
          <h2 className="text-base font-subtitle text-white mb-4 flex items-center gap-2">
            <BookOpen size={18} className="text-lios-green" />
            Turmas com mais Alunos
          </h2>
          {metrics.topClasses.length === 0 ? (
            <p className="text-sm font-body text-lios-gray-400">Sem dados disponíveis.</p>
          ) : (
            <div className="space-y-3">
              {metrics.topClasses.map((c, i) => {
                const max = metrics.topClasses[0]?.total_alunos ?? 1;
                const pct = Math.round((c.total_alunos / max) * 100);
                return (
                  <div key={c.node_id}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="font-body text-lios-gray-300 truncate max-w-[250px]">
                        {i + 1}. {c.name}
                      </span>
                      <span className="font-heading text-white">{c.total_alunos} alunos</span>
                    </div>
                    <div className="w-full bg-lios-surface-2 rounded-full h-1.5">
                      <div
                        className="bg-lios-green h-1.5 rounded-full transition-all"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Telegram Members */}
      <div className="bg-lios-surface rounded-xl border border-lios-border p-6">
        <h2 className="text-base font-subtitle text-white mb-4 flex items-center gap-2">
          <MessageCircle size={18} className="text-lios-blue" />
          Membros Telegram mais Ativos
        </h2>
        {metrics.topTelegramMembers.length === 0 ? (
          <p className="text-sm font-body text-lios-gray-400">Sem dados disponíveis.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {metrics.topTelegramMembers.map(m => (
              <div key={m.node_id} className="bg-lios-surface-2 rounded-lg p-4">
                <p className="font-subtitle text-white text-sm">{m.name}</p>
                <div className="flex items-center gap-4 mt-2 text-xs font-body">
                  <span className="text-lios-blue">{m.topics} tópicos</span>
                  <span className="text-lios-green">{m.groups} grupos</span>
                  <span className="text-lios-gray-400">{m.total_relations} relações</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Relation Stats */}
      <div className="bg-lios-surface rounded-xl border border-lios-border p-6">
        <h2 className="text-base font-subtitle text-white mb-4 flex items-center gap-2">
          <Link2 size={18} className="text-lios-blue" />
          Tipos de Relação
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {metrics.relationStats.map(r => (
            <div key={r.relation} className="bg-lios-surface-2 rounded-lg p-4">
              <p className="text-xs font-body text-lios-gray-400">{RELATION_LABELS[r.relation] ?? r.relation}</p>
              <p className="text-xl font-heading text-white mt-1">{r.total.toLocaleString('pt-BR')}</p>
              <p className="text-xs font-body text-lios-gray-400/60 mt-0.5">peso médio: {r.avg_weight}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Last Ingestion */}
      {metrics.lastIngestion && (
        <p className="text-xs font-body text-lios-gray-400/60 text-center">
          Última ingestão: {new Date(metrics.lastIngestion.created_at).toLocaleString('pt-BR')} —
          {' '}{metrics.lastIngestion.nodes_created} nós, {metrics.lastIngestion.edges_created} arestas
        </p>
      )}
    </div>
  );
}
