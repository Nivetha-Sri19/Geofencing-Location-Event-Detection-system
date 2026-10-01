import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { authApi } from '../api/auth'
import type { User } from '../types/api'

interface AuthContextValue {
  user: User | null
  loading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const raw = localStorage.getItem('geofence_user')
    return raw ? JSON.parse(raw) : null
  })
  const [loading, setLoading] = useState(true)

  const refreshUser = async () => {
    try {
      const next = await authApi.me()
      setUser(next)
      localStorage.setItem('geofence_user', JSON.stringify(next))
    } catch {
      setUser(null)
      localStorage.removeItem('geofence_user')
    }
  }

  useEffect(() => {
    if (localStorage.getItem('geofence_token')) refreshUser().finally(() => setLoading(false))
    else setLoading(false)
  }, [])

  const login = async (username: string, password: string) => {
    const token = await authApi.login({ username, password })
    localStorage.setItem('geofence_token', token.access_token)
    await refreshUser()
  }

  const logout = () => {
    localStorage.removeItem('geofence_token')
    localStorage.removeItem('geofence_user')
    setUser(null)
  }

  const value = useMemo(() => ({ user, loading, login, logout, refreshUser }), [user, loading])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used inside AuthProvider')
  return context
}
