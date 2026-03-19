import { useEffect, useState } from 'react';
import { useAuth } from '../../../contexts/AuthContext';
import { useUsers } from '../hooks/useUsers';
import { ROLE_LABELS, ROLE_COLORS } from '../types';
import type { UserItem } from '../types';
import { cn } from '../../../lib/utils';
import {
  Plus,
  Pencil,
  Trash2,
  Ban,
  CheckCircle,
  KeyRound,
  X,
  Eye,
  EyeOff,
  Shield,
} from 'lucide-react';

type ModalType = 'create' | 'edit' | 'password' | 'delete' | 'permissions' | null;

export default function UsersPage() {
  const { user: currentUser } = useAuth();
  const {
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
  } = useUsers();

  const [modal, setModal] = useState<ModalType>(null);
  const [selectedUser, setSelectedUser] = useState<UserItem | null>(null);
  const [saving, setSaving] = useState(false);

  // Form states
  const [formEmail, setFormEmail] = useState('');
  const [formName, setFormName] = useState('');
  const [formPassword, setFormPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [formRoles, setFormRoles] = useState<string[]>([]);

  useEffect(() => {
    fetchUsers();
    fetchRoles();
    fetchPermissions();
  }, [fetchUsers, fetchRoles, fetchPermissions]);

  function openCreate() {
    setFormEmail('');
    setFormName('');
    setFormPassword('');
    setFormRoles([]);
    setShowPassword(false);
    setError(null);
    setModal('create');
  }

  function openEdit(u: UserItem) {
    setSelectedUser(u);
    setFormEmail(u.email);
    setFormName(u.full_name);
    setFormRoles(u.roles.map(r => r.id));
    setError(null);
    setModal('edit');
  }

  function openPassword(u: UserItem) {
    setSelectedUser(u);
    setFormPassword('');
    setShowPassword(false);
    setError(null);
    setModal('password');
  }

  function openDelete(u: UserItem) {
    setSelectedUser(u);
    setError(null);
    setModal('delete');
  }

  function openPermissions() {
    setError(null);
    setModal('permissions');
  }

  function closeModal() {
    setModal(null);
    setSelectedUser(null);
    setError(null);
  }

  function toggleRole(roleId: string) {
    setFormRoles(prev =>
      prev.includes(roleId) ? prev.filter(r => r !== roleId) : [...prev, roleId]
    );
  }

  async function handleCreate() {
    setSaving(true);
    const ok = await createUser({ email: formEmail, password: formPassword, full_name: formName, role_ids: formRoles });
    setSaving(false);
    if (ok) {
      closeModal();
      fetchUsers();
    }
  }

  async function handleEdit() {
    if (!selectedUser) return;
    setSaving(true);
    const ok = await updateUser(selectedUser.id, { email: formEmail, full_name: formName, role_ids: formRoles });
    setSaving(false);
    if (ok) {
      closeModal();
      fetchUsers();
    }
  }

  async function handleResetPassword() {
    if (!selectedUser) return;
    setSaving(true);
    const ok = await resetPassword(selectedUser.id, formPassword);
    setSaving(false);
    if (ok) {
      closeModal();
    }
  }

  async function handleToggleBan(u: UserItem) {
    const ok = await toggleBan(u.id, !u.banned);
    if (ok) fetchUsers();
  }

  async function handleDelete() {
    if (!selectedUser) return;
    setSaving(true);
    const ok = await deleteUser(selectedUser.id);
    setSaving(false);
    if (ok) {
      closeModal();
      fetchUsers();
    }
  }

  // Group permissions by module for the permissions view
  const permissionsByModule = permissions.reduce<Record<string, typeof permissions>>((acc, p) => {
    if (!acc[p.module]) acc[p.module] = [];
    acc[p.module].push(p);
    return acc;
  }, {});

  function roleHasPermission(roleId: string, permId: string) {
    return rolePermissions.some(rp => rp.role_id === roleId && rp.permission_id === permId);
  }

  return (
    <div className="px-6 py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-heading text-white">Usuários</h2>
            <p className="text-sm font-body text-lios-gray-400 mt-1">
              {users.length} usuário{users.length !== 1 ? 's' : ''} cadastrado{users.length !== 1 ? 's' : ''}
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={openPermissions}
              className="flex items-center gap-2 px-3 py-2 rounded-lg bg-lios-surface-2 text-sm font-subtitle text-lios-gray-300 hover:bg-white/10 transition-colors"
            >
              <Shield size={14} /> Permissões
            </button>
            <button
              onClick={openCreate}
              className="flex items-center gap-2 px-3 py-2 rounded-lg bg-amber-500/15 text-sm font-subtitle text-amber-400 hover:bg-amber-500/25 transition-colors"
            >
              <Plus size={14} /> Novo Usuário
            </button>
          </div>
        </div>

        {/* Error banner */}
        {error && !modal && (
          <div className="mb-4 px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/20 text-sm font-body text-red-400">
            {error}
          </div>
        )}

        {/* Table */}
        <div className="rounded-xl border border-lios-border bg-lios-surface overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b border-lios-border">
                  <th className="px-5 py-3 text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider">Usuário</th>
                  <th className="px-5 py-3 text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider hidden sm:table-cell">Roles</th>
                  <th className="px-5 py-3 text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider hidden md:table-cell">Último acesso</th>
                  <th className="px-5 py-3 text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider">Status</th>
                  <th className="px-5 py-3 text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider text-right">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-lios-border">
                {loading ? (
                  [1, 2, 3].map(i => (
                    <tr key={i}>
                      <td colSpan={5} className="px-5 py-4"><div className="h-5 bg-lios-surface-2 rounded animate-pulse" /></td>
                    </tr>
                  ))
                ) : users.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-5 py-10 text-center">
                      <p className="text-sm font-body text-lios-gray-400">Nenhum usuário encontrado</p>
                    </td>
                  </tr>
                ) : (
                  users.map(u => {
                    const isSelf = u.id === currentUser?.id;

                    return (
                      <tr key={u.id} className="hover:bg-white/5 transition-colors">
                        <td className="px-5 py-3">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-lios-surface-2 flex items-center justify-center shrink-0">
                              <span className="text-xs font-subtitle text-lios-gray-300">
                                {u.email.substring(0, 2).toUpperCase()}
                              </span>
                            </div>
                            <div className="min-w-0">
                              <p className="text-sm font-subtitle text-white truncate">
                                {u.full_name || u.email.split('@')[0]}
                                {isSelf && <span className="ml-2 text-[10px] text-amber-400">(você)</span>}
                              </p>
                              <p className="text-xs font-body text-lios-gray-400 truncate">{u.email}</p>
                            </div>
                          </div>
                        </td>
                        <td className="px-5 py-3 hidden sm:table-cell">
                          <div className="flex flex-wrap gap-1">
                            {u.roles.length === 0 ? (
                              <span className="text-xs font-caption text-lios-gray-400">Sem role</span>
                            ) : (
                              u.roles.map(r => (
                                <span
                                  key={r.id}
                                  className={cn(
                                    'text-[10px] font-caption px-2 py-0.5 rounded-full',
                                    ROLE_COLORS[r.name]?.bg ?? 'bg-gray-500/15',
                                    ROLE_COLORS[r.name]?.text ?? 'text-gray-400'
                                  )}
                                >
                                  {ROLE_LABELS[r.name] ?? r.name}
                                </span>
                              ))
                            )}
                          </div>
                        </td>
                        <td className="px-5 py-3 text-sm font-body text-lios-gray-300 hidden md:table-cell">
                          {u.last_sign_in_at
                            ? new Date(u.last_sign_in_at).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
                            : '—'}
                        </td>
                        <td className="px-5 py-3">
                          {u.banned ? (
                            <span className="text-[10px] font-caption px-2 py-0.5 rounded-full bg-red-500/15 text-red-400">
                              Desativado
                            </span>
                          ) : (
                            <span className="text-[10px] font-caption px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400">
                              Ativo
                            </span>
                          )}
                        </td>
                        <td className="px-5 py-3">
                          <div className="flex items-center justify-end gap-1">
                            <button
                              onClick={() => openEdit(u)}
                              title="Editar"
                              className="p-1.5 rounded-lg text-lios-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                            >
                              <Pencil size={14} />
                            </button>
                            <button
                              onClick={() => openPassword(u)}
                              title="Resetar senha"
                              className="p-1.5 rounded-lg text-lios-gray-400 hover:text-white hover:bg-white/10 transition-colors"
                            >
                              <KeyRound size={14} />
                            </button>
                            {!isSelf && (
                              <>
                                <button
                                  onClick={() => handleToggleBan(u)}
                                  title={u.banned ? 'Reativar' : 'Desativar'}
                                  className={cn(
                                    'p-1.5 rounded-lg transition-colors',
                                    u.banned
                                      ? 'text-emerald-400 hover:bg-emerald-500/10'
                                      : 'text-lios-gray-400 hover:text-amber-400 hover:bg-amber-500/10'
                                  )}
                                >
                                  {u.banned ? <CheckCircle size={14} /> : <Ban size={14} />}
                                </button>
                                <button
                                  onClick={() => openDelete(u)}
                                  title="Deletar"
                                  className="p-1.5 rounded-lg text-lios-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                                >
                                  <Trash2 size={14} />
                                </button>
                              </>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* ─── Modal Overlay ─── */}
      {modal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={closeModal}>
          <div
            className="bg-lios-surface border border-lios-border rounded-xl w-full max-w-lg mx-4 max-h-[85vh] overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            {/* ─── Create User Modal ─── */}
            {modal === 'create' && (
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-heading text-white">Novo Usuário</h3>
                  <button onClick={closeModal} className="text-lios-gray-400 hover:text-white"><X size={18} /></button>
                </div>

                {error && (
                  <div className="mb-4 px-3 py-2 rounded-lg bg-red-500/10 border border-red-500/20 text-sm font-body text-red-400">
                    {error}
                  </div>
                )}

                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider mb-1.5">
                      Email *
                    </label>
                    <input
                      type="email"
                      value={formEmail}
                      onChange={(e) => setFormEmail(e.target.value)}
                      placeholder="usuario@email.com"
                      className="w-full px-3 py-2.5 rounded-lg bg-lios-surface-2 border border-lios-border text-sm font-body text-white placeholder:text-lios-gray-400 focus:outline-none focus:border-amber-500/50"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider mb-1.5">
                      Nome completo
                    </label>
                    <input
                      type="text"
                      value={formName}
                      onChange={(e) => setFormName(e.target.value)}
                      placeholder="Nome do usuário"
                      className="w-full px-3 py-2.5 rounded-lg bg-lios-surface-2 border border-lios-border text-sm font-body text-white placeholder:text-lios-gray-400 focus:outline-none focus:border-amber-500/50"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider mb-1.5">
                      Senha *
                    </label>
                    <div className="relative">
                      <input
                        type={showPassword ? 'text' : 'password'}
                        value={formPassword}
                        onChange={(e) => setFormPassword(e.target.value)}
                        placeholder="Mínimo 6 caracteres"
                        className="w-full px-3 py-2.5 pr-10 rounded-lg bg-lios-surface-2 border border-lios-border text-sm font-body text-white placeholder:text-lios-gray-400 focus:outline-none focus:border-amber-500/50"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-lios-gray-400 hover:text-white"
                      >
                        {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                      </button>
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider mb-2">
                      Roles
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {roles.map(role => (
                        <button
                          key={role.id}
                          onClick={() => toggleRole(role.id)}
                          className={cn(
                            'px-3 py-1.5 rounded-lg text-sm font-subtitle border transition-colors',
                            formRoles.includes(role.id)
                              ? cn(ROLE_COLORS[role.name]?.bg ?? 'bg-white/10', ROLE_COLORS[role.name]?.text ?? 'text-white', 'border-transparent')
                              : 'border-lios-border text-lios-gray-400 hover:border-lios-gray-400/50'
                          )}
                        >
                          {ROLE_LABELS[role.name] ?? role.name}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-lios-border">
                  <button
                    onClick={closeModal}
                    className="px-4 py-2 rounded-lg text-sm font-subtitle text-lios-gray-400 hover:text-white transition-colors"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handleCreate}
                    disabled={saving || !formEmail || !formPassword}
                    className="px-4 py-2 rounded-lg bg-amber-500/15 text-sm font-subtitle text-amber-400 hover:bg-amber-500/25 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    {saving ? 'Criando...' : 'Criar Usuário'}
                  </button>
                </div>
              </div>
            )}

            {/* ─── Edit User Modal ─── */}
            {modal === 'edit' && selectedUser && (
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-heading text-white">Editar Usuário</h3>
                  <button onClick={closeModal} className="text-lios-gray-400 hover:text-white"><X size={18} /></button>
                </div>

                {error && (
                  <div className="mb-4 px-3 py-2 rounded-lg bg-red-500/10 border border-red-500/20 text-sm font-body text-red-400">
                    {error}
                  </div>
                )}

                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider mb-1.5">
                      Email
                    </label>
                    <input
                      type="email"
                      value={formEmail}
                      onChange={(e) => setFormEmail(e.target.value)}
                      className="w-full px-3 py-2.5 rounded-lg bg-lios-surface-2 border border-lios-border text-sm font-body text-white focus:outline-none focus:border-amber-500/50"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider mb-1.5">
                      Nome completo
                    </label>
                    <input
                      type="text"
                      value={formName}
                      onChange={(e) => setFormName(e.target.value)}
                      className="w-full px-3 py-2.5 rounded-lg bg-lios-surface-2 border border-lios-border text-sm font-body text-white focus:outline-none focus:border-amber-500/50"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-subtitle text-lios-gray-400 uppercase tracking-wider mb-2">
                      Roles
                    </label>
                    <div className="flex flex-wrap gap-2">
                      {roles.map(role => (
                        <button
                          key={role.id}
                          onClick={() => toggleRole(role.id)}
                          className={cn(
                            'px-3 py-1.5 rounded-lg text-sm font-subtitle border transition-colors',
                            formRoles.includes(role.id)
                              ? cn(ROLE_COLORS[role.name]?.bg ?? 'bg-white/10', ROLE_COLORS[role.name]?.text ?? 'text-white', 'border-transparent')
                              : 'border-lios-border text-lios-gray-400 hover:border-lios-gray-400/50'
                          )}
                        >
                          {ROLE_LABELS[role.name] ?? role.name}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-lios-border">
                  <button
                    onClick={closeModal}
                    className="px-4 py-2 rounded-lg text-sm font-subtitle text-lios-gray-400 hover:text-white transition-colors"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handleEdit}
                    disabled={saving || !formEmail}
                    className="px-4 py-2 rounded-lg bg-amber-500/15 text-sm font-subtitle text-amber-400 hover:bg-amber-500/25 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    {saving ? 'Salvando...' : 'Salvar'}
                  </button>
                </div>
              </div>
            )}

            {/* ─── Reset Password Modal ─── */}
            {modal === 'password' && selectedUser && (
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-heading text-white">Resetar Senha</h3>
                  <button onClick={closeModal} className="text-lios-gray-400 hover:text-white"><X size={18} /></button>
                </div>

                <p className="text-sm font-body text-lios-gray-400 mb-4">
                  Definir nova senha para <span className="text-white font-subtitle">{selectedUser.email}</span>
                </p>

                {error && (
                  <div className="mb-4 px-3 py-2 rounded-lg bg-red-500/10 border border-red-500/20 text-sm font-body text-red-400">
                    {error}
                  </div>
                )}

                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={formPassword}
                    onChange={(e) => setFormPassword(e.target.value)}
                    placeholder="Nova senha (mínimo 6 caracteres)"
                    className="w-full px-3 py-2.5 pr-10 rounded-lg bg-lios-surface-2 border border-lios-border text-sm font-body text-white placeholder:text-lios-gray-400 focus:outline-none focus:border-amber-500/50"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-lios-gray-400 hover:text-white"
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>

                <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-lios-border">
                  <button
                    onClick={closeModal}
                    className="px-4 py-2 rounded-lg text-sm font-subtitle text-lios-gray-400 hover:text-white transition-colors"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handleResetPassword}
                    disabled={saving || !formPassword || formPassword.length < 6}
                    className="px-4 py-2 rounded-lg bg-amber-500/15 text-sm font-subtitle text-amber-400 hover:bg-amber-500/25 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    {saving ? 'Salvando...' : 'Resetar Senha'}
                  </button>
                </div>
              </div>
            )}

            {/* ─── Delete Confirmation Modal ─── */}
            {modal === 'delete' && selectedUser && (
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-heading text-white">Deletar Usuário</h3>
                  <button onClick={closeModal} className="text-lios-gray-400 hover:text-white"><X size={18} /></button>
                </div>

                {error && (
                  <div className="mb-4 px-3 py-2 rounded-lg bg-red-500/10 border border-red-500/20 text-sm font-body text-red-400">
                    {error}
                  </div>
                )}

                <div className="px-4 py-3 rounded-lg bg-red-500/10 border border-red-500/20 mb-4">
                  <p className="text-sm font-body text-red-400">
                    Esta ação é <strong>irreversível</strong>. O usuário <span className="text-white font-subtitle">{selectedUser.email}</span> será permanentemente removido do sistema.
                  </p>
                </div>

                <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-lios-border">
                  <button
                    onClick={closeModal}
                    className="px-4 py-2 rounded-lg text-sm font-subtitle text-lios-gray-400 hover:text-white transition-colors"
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={handleDelete}
                    disabled={saving}
                    className="px-4 py-2 rounded-lg bg-red-500/15 text-sm font-subtitle text-red-400 hover:bg-red-500/25 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    {saving ? 'Deletando...' : 'Deletar Permanentemente'}
                  </button>
                </div>
              </div>
            )}

            {/* ─── Permissions Matrix Modal ─── */}
            {modal === 'permissions' && (
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-lg font-heading text-white">Matriz de Permissões</h3>
                  <button onClick={closeModal} className="text-lios-gray-400 hover:text-white"><X size={18} /></button>
                </div>

                <p className="text-sm font-body text-lios-gray-400 mb-4">
                  Visão geral das permissões atribuídas a cada role. Admin tem acesso total automaticamente.
                </p>

                <div className="rounded-lg border border-lios-border overflow-hidden">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="border-b border-lios-border bg-lios-surface-2">
                        <th className="px-4 py-2 text-xs font-subtitle text-lios-gray-400 uppercase">Permissão</th>
                        {roles.map(r => (
                          <th key={r.id} className="px-4 py-2 text-xs font-subtitle text-lios-gray-400 uppercase text-center">
                            {ROLE_LABELS[r.name] ?? r.name}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-lios-border">
                      {Object.entries(permissionsByModule).map(([mod, perms]) => (
                        perms.map((perm, i) => (
                          <tr key={perm.id} className="hover:bg-white/5">
                            <td className="px-4 py-2">
                              {i === 0 && (
                                <span className="text-[10px] font-caption text-lios-gray-400 uppercase block mb-0.5">{mod}</span>
                              )}
                              <span className="text-sm font-body text-white">{perm.action}</span>
                              {perm.description && (
                                <span className="text-xs font-body text-lios-gray-400 ml-2">— {perm.description}</span>
                              )}
                            </td>
                            {roles.map(r => (
                              <td key={r.id} className="px-4 py-2 text-center">
                                {r.name === 'admin' ? (
                                  <CheckCircle size={14} className="inline text-amber-400" />
                                ) : roleHasPermission(r.id, perm.id) ? (
                                  <CheckCircle size={14} className="inline text-emerald-400" />
                                ) : (
                                  <span className="text-lios-gray-400/30">—</span>
                                )}
                              </td>
                            ))}
                          </tr>
                        ))
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="flex justify-end mt-6 pt-4 border-t border-lios-border">
                  <button
                    onClick={closeModal}
                    className="px-4 py-2 rounded-lg text-sm font-subtitle text-lios-gray-400 hover:text-white transition-colors"
                  >
                    Fechar
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
