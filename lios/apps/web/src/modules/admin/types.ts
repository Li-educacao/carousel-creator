export interface Role {
  id: string;
  name: string;
  description: string;
}

export interface UserItem {
  id: string;
  email: string;
  full_name: string;
  avatar_url: string | null;
  roles: Role[];
  created_at: string;
  last_sign_in_at: string | null;
  banned: boolean;
}

export interface CreateUserPayload {
  email: string;
  password: string;
  full_name: string;
  role_ids: string[];
}

export interface UpdateUserPayload {
  email?: string;
  full_name?: string;
  role_ids?: string[];
}

export interface Permission {
  id: string;
  module: string;
  action: string;
  description: string;
}

export interface RolePermission {
  role_id: string;
  permission_id: string;
}

export const ROLE_LABELS: Record<string, string> = {
  admin: 'Administrador',
  marketing: 'Marketing',
  pedagogico: 'Pedagógico',
};

export const ROLE_COLORS: Record<string, { bg: string; text: string }> = {
  admin: { bg: 'bg-amber-500/15', text: 'text-amber-400' },
  marketing: { bg: 'bg-lios-blue/15', text: 'text-lios-blue' },
  pedagogico: { bg: 'bg-lios-green/15', text: 'text-lios-green' },
};
