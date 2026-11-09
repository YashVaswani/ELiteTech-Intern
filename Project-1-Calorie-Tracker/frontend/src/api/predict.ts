import { apiClient } from './client'
import type { PredictionResult } from '../types'

export async function predictFood(image: File, servingGrams?: number): Promise<PredictionResult> {
  const form = new FormData()
  form.append('image', image)
  if (servingGrams) {
    form.append('serving_grams', String(servingGrams))
  }
  const { data } = await apiClient.post<PredictionResult>('/api/predict', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}
