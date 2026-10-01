import api from './client'
import type { Geofence, EventRules, Point } from '../types/api'

export interface GeofencePayload {
  name: string
  description?: string | null
  geofence_type: 'circle' | 'polygon'
  center_latitude?: number | null
  center_longitude?: number | null
  radius_meters?: number | null
  boundary_tolerance_meters: number
  points: Point[]
  event_rules: EventRules
  is_active: boolean
}

export const geofencesApi = {
  list: () => api.get<Geofence[]>('/geofences').then(r => r.data),
  get: (id: number) => api.get<Geofence>(`/geofences/${id}`).then(r => r.data),
  create: (payload: GeofencePayload) => api.post<Geofence>('/geofences', payload).then(r => r.data),
  update: (id: number, payload: Partial<GeofencePayload>) => api.patch<Geofence>(`/geofences/${id}`, payload).then(r => r.data),
  remove: (id: number) => api.delete(`/geofences/${id}`),
}
