import { useState, useCallback } from 'react';
import { supabase } from '../../../lib/supabase';
import type { CtVideo, CtInsights } from '../types';

interface UseContentStudioReturn {
  videos: CtVideo[];
  insights: CtInsights | null;
  totalVideos: number;
  totalComments: number;
  lastUpdated: string | null;
  loading: boolean;
  error: string | null;
  fetchVideos: (params?: { search?: string }) => Promise<void>;
  fetchInsights: () => Promise<void>;
}

export function useContentStudio(): UseContentStudioReturn {
  const [videos, setVideos] = useState<CtVideo[]>([]);
  const [insights, setInsights] = useState<CtInsights | null>(null);
  const [totalVideos, setTotalVideos] = useState(0);
  const [totalComments, setTotalComments] = useState(0);
  const [lastUpdated, setLastUpdated] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchVideos = useCallback(async (params?: { search?: string }) => {
    setLoading(true);
    setError(null);

    let query = supabase
      .from('ct_videos')
      .select('*', { count: 'exact' })
      .order('lesson_number', { ascending: false, nullsFirst: false });

    if (params?.search) {
      query = query.ilike('title', `%${params.search}%`);
    }

    const { data, error: dbError, count } = await query;

    if (dbError) {
      setError(dbError.message);
      setLoading(false);
      return;
    }

    setVideos(data ?? []);
    setTotalVideos(count ?? 0);

    // Get total comments count
    const { count: commentsCount } = await supabase
      .from('ct_comments')
      .select('*', { count: 'exact', head: true });

    setTotalComments(commentsCount ?? 0);

    // Get last updated from most recent video updated_at
    if (data && data.length > 0) {
      const latest = data.reduce((a, b) =>
        new Date(a.updated_at) > new Date(b.updated_at) ? a : b
      );
      setLastUpdated(latest.updated_at);
    }

    setLoading(false);
  }, []);

  const fetchInsights = useCallback(async () => {
    const { data, error: dbError } = await supabase
      .from('ct_insights')
      .select('*')
      .eq('type', 'content_ideas')
      .single();

    if (dbError) {
      // Not an error if no row found
      if (dbError.code !== 'PGRST116') {
        setError(dbError.message);
      }
      return;
    }

    setInsights(data);
  }, []);

  return {
    videos,
    insights,
    totalVideos,
    totalComments,
    lastUpdated,
    loading,
    error,
    fetchVideos,
    fetchInsights,
  };
}
