export interface User {
  id: number
  email: string
  daily_calorie_goal: number
}

export interface NutritionInfo {
  food_name: string
  serving_grams: number
  calories: number
  protein_g: number
  carbs_g: number
  fat_g: number
}

export interface PredictionCandidate {
  food_name: string
  confidence: number
}

export interface PredictionResult {
  top_prediction: PredictionCandidate
  alternatives: PredictionCandidate[]
  nutrition: NutritionInfo
}

export interface FoodItem {
  food_name: string
  calories_per_100g: number
  protein_per_100g: number
  carbs_per_100g: number
  fat_per_100g: number
}

export interface FoodLog {
  id: number
  food_name: string
  serving_grams: number
  calories: number
  protein_g: number
  carbs_g: number
  fat_g: number
  confidence: number | null
  logged_at: string
}

export interface DailySummary {
  date: string
  total_calories: number
  total_protein_g: number
  total_carbs_g: number
  total_fat_g: number
  goal_calories: number
  entries: FoodLog[]
}
