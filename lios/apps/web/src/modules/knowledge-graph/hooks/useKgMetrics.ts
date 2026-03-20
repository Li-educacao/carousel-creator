import { useState, useEffect, useCallback } from 'react';
import { supabase } from '../../../lib/supabase';

interface KgOverview {
  totalNodes: number;
  totalEdges: number;
  typeCounts: Record<string, number>;
  lastIngestion: { created_at: string; nodes_created: number; edges_created: number } | null;
}

interface TopStudent {
  node_id: string;
  name: string;
  total_connections: number;
  turmas: number;
  grupos_telegram: number;
}

interface TopClass {
  node_id: string;
  name: string;
  total_alunos: number;
}

interface TopTelegramMember {
  node_id: string;
  name: string;
  total_relations: number;
  topics: number;
  groups: number;
}

interface RelationStat {
  relation: string;
  total: number;
  avg_weight: number;
}

export interface KgMetrics extends KgOverview {
  topStudents: TopStudent[];
  topClasses: TopClass[];
  topTelegramMembers: TopTelegramMember[];
  relationStats: RelationStat[];
}

export function useKgMetrics() {
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState<KgMetrics>({
    totalNodes: 0,
    totalEdges: 0,
    typeCounts: {},
    lastIngestion: null,
    topStudents: [],
    topClasses: [],
    topTelegramMembers: [],
    relationStats: [],
  });

  const fetchMetrics = useCallback(async () => {
    setLoading(true);
    try {
      const [nodesRes, edgesRes, logRes, typeData, topStudents, topClasses, topMembers, relStats] =
        await Promise.all([
          supabase.from('kg_nodes').select('type', { count: 'exact', head: true }),
          supabase.from('kg_edges').select('id', { count: 'exact', head: true }),
          supabase.from('kg_ingestion_log').select('created_at, nodes_created, edges_created')
            .order('created_at', { ascending: false }).limit(1),
          supabase.from('kg_nodes').select('type'),
          supabase.rpc('kg_top_students', { p_limit: 10 }),
          supabase.rpc('kg_top_classes', { p_limit: 10 }),
          supabase.rpc('kg_top_telegram_members', { p_limit: 10 }),
          supabase.from('kg_relation_stats').select('*'),
        ]);

      const typeCounts: Record<string, number> = {};
      (typeData.data ?? []).forEach((n: { type: string }) => {
        typeCounts[n.type] = (typeCounts[n.type] || 0) + 1;
      });

      setMetrics({
        totalNodes: nodesRes.count ?? 0,
        totalEdges: edgesRes.count ?? 0,
        typeCounts,
        lastIngestion: logRes.data?.[0] ?? null,
        topStudents: (topStudents.data ?? []) as TopStudent[],
        topClasses: (topClasses.data ?? []) as TopClass[],
        topTelegramMembers: (topMembers.data ?? []) as TopTelegramMember[],
        relationStats: (relStats.data ?? []) as RelationStat[],
      });
    } catch (error) {
      console.error('Error fetching KG metrics:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMetrics();
  }, [fetchMetrics]);

  return { loading, metrics, refresh: fetchMetrics };
}
