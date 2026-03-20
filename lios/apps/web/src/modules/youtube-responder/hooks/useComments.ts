import { useState, useCallback } from 'react';
import { api } from '../../../lib/api';
import type { YtComment, CommentCategory } from '../types';

interface CommentsParams {
  video_id?: string;
  category?: CommentCategory;
  has_response?: boolean;
  search?: string;
  limit?: number;
  offset?: number;
}

interface CommentsResponse {
  data: YtComment[];
  total: number;
}

interface UseCommentsReturn {
  comments: YtComment[];
  total: number;
  loading: boolean;
  error: string | null;
  fetchComments: (params?: CommentsParams) => Promise<void>;
}

export function useComments(): UseCommentsReturn {
  const [comments, setComments] = useState<YtComment[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchComments = useCallback(async (params: CommentsParams = {}) => {
    setLoading(true);
    setError(null);

    const qs = new URLSearchParams();
    if (params.video_id)               qs.set('video_id', params.video_id);
    if (params.category)               qs.set('category', params.category);
    if (params.has_response !== undefined) qs.set('has_response', String(params.has_response));
    if (params.search)                 qs.set('search', params.search);
    if (params.limit !== undefined)    qs.set('limit', String(params.limit));
    if (params.offset !== undefined)   qs.set('offset', String(params.offset));

    const path = `/api/v1/youtube/comments${qs.toString() ? `?${qs.toString()}` : ''}`;
    const { data, error: apiError } = await api.get<CommentsResponse>(path);

    setLoading(false);

    if (apiError) {
      setError(apiError.message);
      return;
    }

    if (data) {
      setComments(data.data);
      setTotal(data.total);
    }
  }, []);

  return { comments, total, loading, error, fetchComments };
}
