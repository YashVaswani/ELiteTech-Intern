export const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export const WS_STREAM_URL = `${API_BASE_URL.replace(/^http/, 'ws')}/api/v1/predict/stream`

export async function fetchGestureClasses(): Promise<string[]> {
  const res = await fetch(`${API_BASE_URL}/api/v1/gestures`)
  if (!res.ok) throw new Error(`Failed to fetch gesture list: ${res.status}`)
  const data = (await res.json()) as { gestures: string[] }
  return data.gestures
}
