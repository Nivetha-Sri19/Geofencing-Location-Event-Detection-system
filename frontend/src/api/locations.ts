import api from './client'
import type { EventHistoryItem, EventType, LocationEvent, LocationProcessingResponse } from '../types/api'

export const locationsApi = {
  process: (payload: { device_id: number; latitude: number; longitude: number; timestamp: string }) => api.post<LocationProcessingResponse>('/locations/process', payload).then(r => r.data),
  events: (params?: { device_id?: number; geofence_id?: number; event_type?: EventType; limit?: number; offset?: number }) => api.get<EventHistoryItem[]>('/locations/events', { params }).then(r => r.data),
  history: (params?: { device_id?: number; limit?: number; offset?: number }) => api.get<LocationEvent[]>('/locations/history', { params }).then(r => r.data),
  current: () => api.get<LocationEvent[]>('/locations/current').then(r => r.data),
}
