import api from './client'
import type { Device } from '../types/api'

export const devicesApi = {
  list: () => api.get<Device[]>('/devices').then(r => r.data),
  create: (payload: { device_identifier: string; name: string; user_id?: number }) => api.post<Device>('/devices', payload).then(r => r.data),
  update: (id: number, payload: { name?: string; is_active?: boolean; user_id?: number }) => api.patch<Device>(`/devices/${id}`, payload).then(r => r.data),
}
