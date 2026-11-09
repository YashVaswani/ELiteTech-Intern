import { apiClient } from './client'
import type { DailySummary, FoodLog } from '../types'

export async function createLog(
  foodName: string,
  servingGrams: number,
  confidence?: number,
): Promise<FoodLog> {
  const { data } = await apiClient.post<FoodLog>('/api/logs', {
    food_name: foodName,
    serving_grams: servingGrams,
    confidence,
  })
  return data
}

export async function listLogs(): Promise<FoodLog[]> {
  const { data } = await apiClient.get<FoodLog[]>('/api/logs')
  return data
}

export async function deleteLog(logId: number): Promise<void> {
  await apiClient.delete(`/api/logs/${logId}`)
}

export async function getDailySummary(date: string): Promise<DailySummary> {
  const { data } = await apiClient.get<DailySummary>(`/api/logs/summary/${date}`)
  return data
}
