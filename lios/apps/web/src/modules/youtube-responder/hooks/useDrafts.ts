import { useState, useCallback } from 'react';
import { api } from '../../../lib/api';
import type { YtDraft, DraftStatus } from '../types';

interface DraftsParams {
  status?: DraftStatus;
  limit?: number;
  offset?: number;
}

interface DraftsResponse {
  data: YtDraft[];
  total: number;
}

interface UpdateDraftPayload {
  status: DraftStatus;
  edited_text?: string;
}

interface UseDraftsReturn {
  drafts: YtDraft[];
  total: number;
  loading: boolean;
  error: string | null;
  fetchDrafts: (params?: DraftsParams) => Promise<void>;
  updateDraft: (id: string, payload: UpdateDraftPayload) => Promise<boolean>;
}

export function useDrafts(): UseDraftsReturn {
  const [drafts, setDrafts] = useState<YtDraft[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDrafts = useCallback(async (params: DraftsParams = {}) => {
    setLoading(true);
    setError(null);

    const qs = new URLSearchParams();
    if (params.status)               qs.set('status', params.status);
    if (params.limit !== undefined)  qs.set('limit', String(params.limit));
    if (params.offset !== undefined) qs.set('offset', String(params.offset));

    const path = `/api/v1/youtube/drafts${qs.toString() ? `?${qs.toString()}` : ''}`;
    const { data, error: apiError } = await api.get<DraftsResponse>(path);

    setLoading(false);

    if (apiError) {
      setError(apiError.message);
      return;
    }

    if (data) {
      setDrafts(data.data);
      setTotal(data.total);
    }
  }, []);

  const updateDraft = useCallback(async (
    id: string,
    payload: UpdateDraftPayload
  ): Promise<boolean> => {
    const { error: apiError, data } = await api.patch<YtDraft>(
      `/api/v1/youtube/drafts/${id}`,
      payload
    );

    if (apiError) {
      setError(apiError.message);
      return false;
    }

    if (data) {
      setDrafts((prev) =>
        prev.map((d) => (d.id === id ? { ...d, ...data } : d))
      );
    }

    return true;
  }, []);

  return { drafts, total, loading, error, fetchDrafts, updateDraft };
}
