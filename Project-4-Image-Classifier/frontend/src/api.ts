const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export interface PredictionResponse {
  label: string
  confidence: number
  probabilities: Record<string, number>
}

export class ApiError extends Error {}

export async function predictImage(file: File): Promise<PredictionResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new ApiError(body?.detail ?? `Request failed with status ${response.status}`)
  }

  return response.json()
}
