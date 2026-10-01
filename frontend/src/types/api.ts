export type Role = 'admin' | 'operator' | 'viewer'
export type GeofenceType = 'circle' | 'polygon'
export type GeofenceState = 'inside' | 'outside'
export type EventType = 'enter' | 'exit' | 'inside' | 'outside'

export interface User {
  id: number
  username: string
  email: string
  role: Role
  is_active: boolean
}

export interface TokenResponse {
  access_token: string
  token_type: string
  expires_in: number
}

export interface Device {
  id: number
  user_id: number
  device_identifier: string
  name: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Point {
  sequence?: number
  latitude: number
  longitude: number
}

export interface EventRules {
  enter: boolean
  exit: boolean
  inside: boolean
  outside: boolean
}

export interface Geofence {
  id: number
  name: string
  description: string | null
  geofence_type: GeofenceType
  center_latitude: number | null
  center_longitude: number | null
  radius_meters: number | null
  boundary_tolerance_meters: number
  event_rules: EventRules
  is_active: boolean
  points: Point[]
}

export interface LocationEvent {
  id: number
  device_id: number
  latitude: number
  longitude: number
  recorded_at: string
  received_at: string
}

export interface EventHistoryItem {
  id: number
  device_id: number
  geofence_id: number
  location_event_id: number
  event_type: EventType
  previous_state: GeofenceState
  current_state: GeofenceState
  occurred_at: string
}

export interface ProcessingEvent {
  geofence_id: number
  geofence_name: string
  event_type: EventType
  previous_state: GeofenceState
  current_state: GeofenceState
  timestamp: string
}

export interface LocationProcessingResponse {
  location_event_id: number
  device_id: number
  latitude: number
  longitude: number
  timestamp: string
  events: ProcessingEvent[]
}

export interface AuditLog {
  id: number
  user_id: number | null
  action: string
  entity_type: string
  entity_id: number | null
  details: Record<string, unknown> | null
  created_at: string
}
