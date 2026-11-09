import { useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createLog } from '../api/logs'
import { predictFood } from '../api/predict'
import type { PredictionResult } from '../types'

function formatFoodName(name: string): string {
  return name.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}

export function ScanPage() {
  const navigate = useNavigate()
  const fileInputRef = useRef<HTMLInputElement>(null)

  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [servingGrams, setServingGrams] = useState(150)
  const [isPredicting, setIsPredicting] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleFileChange(file: File | undefined) {
    if (!file) return
    setPreviewUrl(URL.createObjectURL(file))
    setResult(null)
    setError(null)
    setIsPredicting(true)
    try {
      const prediction = await predictFood(file)
      setResult(prediction)
      setServingGrams(prediction.nutrition.serving_grams)
    } catch {
      setError('Could not recognize this image. Try a clearer photo of a single dish.')
    } finally {
      setIsPredicting(false)
    }
  }

  async function handleLog() {
    if (!result) return
    setIsSaving(true)
    try {
      await createLog(result.top_prediction.food_name, servingGrams, result.top_prediction.confidence)
      navigate('/')
    } catch {
      setError('Could not save this entry. Please try again.')
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="mx-auto max-w-lg space-y-6 p-6">
      <h1 className="text-xl font-bold text-gray-900">Scan your food</h1>

      <div
        className="flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 bg-white p-8 text-center hover:border-brand-400"
        onClick={() => fileInputRef.current?.click()}
      >
        {previewUrl ? (
          <img src={previewUrl} alt="Selected food" className="max-h-64 rounded-lg object-cover" />
        ) : (
          <p className="text-gray-500">Tap to upload or take a photo of your meal</p>
        )}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          capture="environment"
          className="hidden"
          onChange={(e) => handleFileChange(e.target.files?.[0])}
        />
      </div>

      {isPredicting && <p className="text-center text-gray-500">Analyzing photo...</p>}
      {error && <p className="text-center text-red-500">{error}</p>}

      {result && (
        <div className="space-y-4 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <div>
            <p className="text-sm text-gray-500">Recognized as</p>
            <p className="text-lg font-semibold text-gray-900">
              {formatFoodName(result.top_prediction.food_name)}{' '}
              <span className="text-sm font-normal text-gray-400">
                ({Math.round(result.top_prediction.confidence * 100)}% confident)
              </span>
            </p>
          </div>

          {result.alternatives.length > 0 && (
            <p className="text-sm text-gray-500">
              Also considered: {result.alternatives.map((a) => formatFoodName(a.food_name)).join(', ')}
            </p>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700">Serving size (grams)</label>
            <input
              type="number"
              min={1}
              value={servingGrams}
              onChange={(e) => setServingGrams(Number(e.target.value))}
              className="mt-1 w-32 rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            />
          </div>

          <div className="grid grid-cols-4 gap-2 text-center text-sm">
            <div className="rounded-lg bg-gray-50 p-2">
              <p className="font-bold text-gray-900">
                {Math.round((result.nutrition.calories / result.nutrition.serving_grams) * servingGrams)}
              </p>
              <p className="text-gray-500">kcal</p>
            </div>
            <div className="rounded-lg bg-gray-50 p-2">
              <p className="font-bold text-gray-900">
                {Math.round((result.nutrition.protein_g / result.nutrition.serving_grams) * servingGrams)}g
              </p>
              <p className="text-gray-500">protein</p>
            </div>
            <div className="rounded-lg bg-gray-50 p-2">
              <p className="font-bold text-gray-900">
                {Math.round((result.nutrition.carbs_g / result.nutrition.serving_grams) * servingGrams)}g
              </p>
              <p className="text-gray-500">carbs</p>
            </div>
            <div className="rounded-lg bg-gray-50 p-2">
              <p className="font-bold text-gray-900">
                {Math.round((result.nutrition.fat_g / result.nutrition.serving_grams) * servingGrams)}g
              </p>
              <p className="text-gray-500">fat</p>
            </div>
          </div>

          <button
            onClick={handleLog}
            disabled={isSaving}
            className="w-full rounded-md bg-brand-600 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-50"
          >
            {isSaving ? 'Saving...' : 'Log this food'}
          </button>
        </div>
      )}
    </div>
  )
}
