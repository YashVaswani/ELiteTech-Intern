import { apiClient } from './client'
import type { FoodItem, NutritionInfo } from '../types'

export async function listFoods(): Promise<FoodItem[]> {
  const { data } = await apiClient.get<FoodItem[]>('/api/foods')
  return data
}

export async function getFood(foodName: string, grams = 100): Promise<NutritionInfo> {
  const { data } = await apiClient.get<NutritionInfo>(`/api/foods/${encodeURIComponent(foodName)}`, {
    params: { grams },
  })
  return data
}
