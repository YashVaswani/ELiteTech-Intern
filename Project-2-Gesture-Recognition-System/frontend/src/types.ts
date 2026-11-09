export interface Landmark {
  x: number
  y: number
  z: number
}

export interface PredictionResponse {
  gesture: string | null
  confidence: number | null
  landmarks: Landmark[] | null
}
