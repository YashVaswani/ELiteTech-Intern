import { apiClient } from './client'
import type { User } from '../types'

export async function register(email: string, password: string): Promise<User> {
  const { data } = await apiClient.post<User>('/api/auth/register', { email, password })
  return data
}

export async function login(email: string, password: string): Promise<string> {
  const form = new URLSearchParams()
  form.set('username', email)
  form.set('password', password)
  const { data } = await apiClient.post<{ access_token: string }>('/api/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return data.access_token
}

export async function getCurrentUser(): Promise<User> {
  const { data } = await apiClient.get<User>('/api/auth/me')
  return data
}
