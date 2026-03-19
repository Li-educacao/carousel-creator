import { useState, useCallback } from 'react';
import { api } from '../../../lib/api';
import type { UserItem, Role, CreateUserPayload, UpdateUserPayload, Permission, RolePermission } from '../types';

interface UsersResponse {
  data: UserItem[];
  total: number;
}

interface RolesResponse {
  data: Role[];
}

interface PermissionsResponse {
  data: {
    permissions: Permission[];
    role_permissions: RolePermission[];
  };
}

export function useUsers() {
  const [users, setUsers] = useState<UserItem[]>([]);
  const [roles, setRoles] = useState<Role[]>([]);
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const [rolePermissions, setRolePermissions] = useState<RolePermission[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError(null);

    const { data, error: apiError } = await api.get<UsersResponse>('/api/v1/admin/users');

    setLoading(false);
    if (apiError) {
      setError(apiError.message);
      return;
    }
    if (data) {
      setUsers(data.data);
    }
  }, []);

  const fetchRoles = useCallback(async () => {
    const { data, error: apiError } = await api.get<RolesResponse>('/api/v1/admin/users/roles');
    if (apiError) {
      setError(apiError.message);
      return;
    }
    if (data) {
      setRoles(data.data);
    }
  }, []);

  const fetchPermissions = useCallback(async () => {
    const { data, error: apiError } = await api.get<PermissionsResponse>('/api/v1/admin/users/permissions');
    if (apiError) {
      setError(apiError.message);
      return;
    }
    if (data) {
      setPermissions(data.data.permissions);
      setRolePermissions(data.data.role_permissions);
    }
  }, []);

  const createUser = useCallback(async (payload: CreateUserPayload): Promise<boolean> => {
    const { error: apiError } = await api.post('/api/v1/admin/users', payload);
    if (apiError) {
      setError(apiError.message);
      return false;
    }
    return true;
  }, []);

  const updateUser = useCallback(async (id: string, payload: UpdateUserPayload): Promise<boolean> => {
    const { error: apiError } = await api.patch(`/api/v1/admin/users/${id}`, payload);
    if (apiError) {
      setError(apiError.message);
      return false;
    }
    return true;
  }, []);

  const resetPassword = useCallback(async (id: string, password: string): Promise<boolean> => {
    const { error: apiError } = await api.post(`/api/v1/admin/users/${id}/reset-password`, { password });
    if (apiError) {
      setError(apiError.message);
      return false;
    }
    return true;
  }, []);

  const toggleBan = useCallback(async (id: string, ban: boolean): Promise<boolean> => {
    const { error: apiError } = await api.post(`/api/v1/admin/users/${id}/toggle-ban`, { ban });
    if (apiError) {
      setError(apiError.message);
      return false;
    }
    return true;
  }, []);

  const deleteUser = useCallback(async (id: string): Promise<boolean> => {
    const { error: apiError } = await api.delete(`/api/v1/admin/users/${id}`);
    if (apiError) {
      setError(apiError.message);
      return false;
    }
    return true;
  }, []);

  return {
    users,
    roles,
    permissions,
    rolePermissions,
    loading,
    error,
    setError,
    fetchUsers,
    fetchRoles,
    fetchPermissions,
    createUser,
    updateUser,
    resetPassword,
    toggleBan,
    deleteUser,
  };
}
