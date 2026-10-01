import api from './client'
import type { TokenResponse, User } from '../types/api'

export const authApi = {
  login: (payload: { username: string; password: string }) => api.post<TokenResponse>('/auth/login', payload).then(r => r.data),
  register: (payload: { username: string; email: string; password: string }) => api.post<User>('/auth/register', payload).then(r => r.data),
  me: () => api.get<User>('/auth/me').then(r => r.data),
}
