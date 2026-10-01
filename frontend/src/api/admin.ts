import api from './client'
import type { AuditLog, Role, User } from '../types/api'

export const adminApi = {
  users: () => api.get<User[]>('/users').then(r => r.data),
  role: (id: number, role: Role) => api.patch<User>(`/users/${id}/role`, { role }).then(r => r.data),
  status: (id: number, is_active: boolean) => api.patch<User>(`/users/${id}/status`, { is_active }).then(r => r.data),
  auditLogs: () => api.get<AuditLog[]>('/audit-logs', { params: { limit: 200 } }).then(r => r.data),
}
