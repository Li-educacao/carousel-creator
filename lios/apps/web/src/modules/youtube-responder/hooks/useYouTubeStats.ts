import { useState, useCallback } from 'react';
import { api } from '../../../lib/api';
import type { YtStats } from '../types';

interface UseYouTubeStatsReturn {
  stats: YtStats | null;
  loading: boolean;
  error: string | null;
  fetchStats: () => Promise<void>;
}

export function useYouTubeStats(): UseYouTubeStatsReturn {
  const [stats, setStats] = useState<YtStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = useCallback(async () => {
    setLoading(true);
    setError(null);

    const { data, error: apiError } = await api.get<YtStats>('/api/v1/youtube/stats');

    setLoading(false);

    if (apiError) {
      setError(apiError.message);
      return;
    }

    if (data) {
      setStats(data);
    }
  }, []);

  return { stats, loading, error, fetchStats };
}
