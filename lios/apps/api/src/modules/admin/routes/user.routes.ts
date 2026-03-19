import { Router, Request, Response } from 'express';
import { supabaseAdmin } from '../../../lib/supabase.js';
import type { AuthenticatedRequest } from '../../../middleware/auth.js';

const router = Router();

// GET /users — List all users with profiles and roles
router.get('/', async (_req: Request, res: Response): Promise<void> => {
  // Fetch all users from auth
  const { data: authData, error: authError } = await supabaseAdmin.auth.admin.listUsers();

  if (authError) {
    res.status(500).json({ error: { message: 'Erro ao listar usuários', code: 'LIST_ERROR' } });
    return;
  }

  const users = authData.users ?? [];

  // Fetch all profiles
  const { data: profiles } = await supabaseAdmin
    .from('core_profiles')
    .select('id, full_name, avatar_url');

  // Fetch all user-role assignments with role names
  const { data: userRoles } = await supabaseAdmin
    .from('core_user_roles')
    .select('user_id, role_id, core_roles(id, name, description)');

  // Build lookup maps
  const profileMap = new Map((profiles ?? []).map(p => [p.id, p]));
  const roleMap = new Map<string, { id: string; name: string; description: string }[]>();
  for (const ur of userRoles ?? []) {
    const role = ur.core_roles as unknown as { id: string; name: string; description: string };
    if (!roleMap.has(ur.user_id)) roleMap.set(ur.user_id, []);
    roleMap.get(ur.user_id)!.push(role);
  }

  const result = users.map(u => ({
    id: u.id,
    email: u.email,
    full_name: profileMap.get(u.id)?.full_name ?? '',
    avatar_url: profileMap.get(u.id)?.avatar_url ?? null,
    roles: roleMap.get(u.id) ?? [],
    created_at: u.created_at,
    last_sign_in_at: u.last_sign_in_at,
    banned: u.banned_until ? new Date(u.banned_until) > new Date() : false,
  }));

  res.json({ data: result, total: result.length });
});

// GET /users/roles — List all available roles
router.get('/roles', async (_req: Request, res: Response): Promise<void> => {
  const { data, error } = await supabaseAdmin
    .from('core_roles')
    .select('id, name, description')
    .order('name');

  if (error) {
    res.status(500).json({ error: { message: 'Erro ao listar roles', code: 'ROLES_ERROR' } });
    return;
  }

  res.json({ data });
});

// GET /users/permissions — List all permissions grouped by module
router.get('/permissions', async (_req: Request, res: Response): Promise<void> => {
  const { data, error } = await supabaseAdmin
    .from('core_permissions')
    .select('id, module, action, description')
    .order('module')
    .order('action');

  if (error) {
    res.status(500).json({ error: { message: 'Erro ao listar permissões', code: 'PERMS_ERROR' } });
    return;
  }

  // Also fetch role-permission assignments
  const { data: rolePerms } = await supabaseAdmin
    .from('core_role_permissions')
    .select('role_id, permission_id');

  res.json({ data: { permissions: data, role_permissions: rolePerms ?? [] } });
});

// POST /users — Create a new user
router.post('/', async (req: Request, res: Response): Promise<void> => {
  const { email, password, full_name, role_ids } = req.body;
  const adminUser = (req as AuthenticatedRequest).user;

  if (!email || !password) {
    res.status(400).json({ error: { message: 'Email e senha são obrigatórios', code: 'VALIDATION' } });
    return;
  }

  if (password.length < 6) {
    res.status(400).json({ error: { message: 'Senha deve ter no mínimo 6 caracteres', code: 'VALIDATION' } });
    return;
  }

  // Create user in Supabase Auth
  const { data: authData, error: authError } = await supabaseAdmin.auth.admin.createUser({
    email,
    password,
    email_confirm: true,
    user_metadata: { full_name: full_name || '' },
  });

  if (authError) {
    const msg = authError.message.includes('already been registered')
      ? 'Este email já está cadastrado'
      : `Erro ao criar usuário: ${authError.message}`;
    res.status(400).json({ error: { message: msg, code: 'CREATE_ERROR' } });
    return;
  }

  const newUserId = authData.user.id;

  // Profile is auto-created by trigger, but update full_name if provided
  if (full_name) {
    await supabaseAdmin
      .from('core_profiles')
      .update({ full_name })
      .eq('id', newUserId);
  }

  // Assign roles
  if (role_ids && Array.isArray(role_ids) && role_ids.length > 0) {
    const roleInserts = role_ids.map((role_id: string) => ({
      user_id: newUserId,
      role_id,
      assigned_by: adminUser.id,
    }));

    await supabaseAdmin.from('core_user_roles').insert(roleInserts);
  }

  res.status(201).json({ data: { id: newUserId, email } });
});

// PATCH /users/:id — Update user profile and roles
router.patch('/:id', async (req: Request, res: Response): Promise<void> => {
  const id = req.params.id as string;
  const { full_name, role_ids, email } = req.body;
  const adminUser = (req as AuthenticatedRequest).user;

  // Update email in Supabase Auth if changed
  if (email) {
    const { error } = await supabaseAdmin.auth.admin.updateUserById(id, { email });
    if (error) {
      res.status(400).json({ error: { message: `Erro ao atualizar email: ${error.message}`, code: 'UPDATE_ERROR' } });
      return;
    }
  }

  // Update profile
  if (full_name !== undefined) {
    await supabaseAdmin
      .from('core_profiles')
      .update({ full_name })
      .eq('id', id);

    await supabaseAdmin.auth.admin.updateUserById(id, {
      user_metadata: { full_name },
    });
  }

  // Update roles (replace all)
  if (role_ids !== undefined && Array.isArray(role_ids)) {
    // Remove existing roles
    await supabaseAdmin.from('core_user_roles').delete().eq('user_id', id);

    // Insert new roles
    if (role_ids.length > 0) {
      const roleInserts = role_ids.map((role_id: string) => ({
        user_id: id,
        role_id,
        assigned_by: adminUser.id,
      }));
      await supabaseAdmin.from('core_user_roles').insert(roleInserts);
    }
  }

  res.json({ data: { id } });
});

// POST /users/:id/reset-password — Reset user password
router.post('/:id/reset-password', async (req: Request, res: Response): Promise<void> => {
  const id = req.params.id as string;
  const { password } = req.body;

  if (!password || password.length < 6) {
    res.status(400).json({ error: { message: 'Senha deve ter no mínimo 6 caracteres', code: 'VALIDATION' } });
    return;
  }

  const { error } = await supabaseAdmin.auth.admin.updateUserById(id, { password });

  if (error) {
    res.status(400).json({ error: { message: `Erro ao resetar senha: ${error.message}`, code: 'RESET_ERROR' } });
    return;
  }

  res.json({ data: { success: true } });
});

// POST /users/:id/toggle-ban — Ban/unban user
router.post('/:id/toggle-ban', async (req: Request, res: Response): Promise<void> => {
  const id = req.params.id as string;
  const { ban } = req.body;

  if (ban) {
    // Ban for 100 years (effectively permanent)
    const banUntil = new Date();
    banUntil.setFullYear(banUntil.getFullYear() + 100);
    const { error } = await supabaseAdmin.auth.admin.updateUserById(id, {
      ban_duration: `${100 * 365 * 24}h`,
    });
    if (error) {
      res.status(400).json({ error: { message: `Erro ao desativar usuário: ${error.message}`, code: 'BAN_ERROR' } });
      return;
    }
  } else {
    const { error } = await supabaseAdmin.auth.admin.updateUserById(id, {
      ban_duration: 'none',
    });
    if (error) {
      res.status(400).json({ error: { message: `Erro ao reativar usuário: ${error.message}`, code: 'UNBAN_ERROR' } });
      return;
    }
  }

  res.json({ data: { banned: ban } });
});

// DELETE /users/:id — Permanently delete a user
router.delete('/:id', async (req: Request, res: Response): Promise<void> => {
  const id = req.params.id as string;
  const adminUser = (req as AuthenticatedRequest).user;

  // Prevent self-deletion
  if (id === adminUser.id) {
    res.status(400).json({ error: { message: 'Não é possível deletar a si mesmo', code: 'SELF_DELETE' } });
    return;
  }

  const { error } = await supabaseAdmin.auth.admin.deleteUser(id);

  if (error) {
    res.status(400).json({ error: { message: `Erro ao deletar usuário: ${error.message}`, code: 'DELETE_ERROR' } });
    return;
  }

  res.status(204).send();
});

export default router;
