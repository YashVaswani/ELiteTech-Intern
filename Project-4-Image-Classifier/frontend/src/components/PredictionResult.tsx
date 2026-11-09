import type { PredictionResponse } from '../api'

const LABEL_EMOJI: Record<string, string> = { cat: '🐱', dog: '🐶' }

export function PredictionResult({ label, confidence, probabilities }: PredictionResponse) {
  const sortedProbabilities = Object.entries(probabilities).sort(([, a], [, b]) => b - a)

  return (
    <div className="w-full rounded-xl border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-900">
      <p className="text-center text-3xl font-semibold capitalize">
        {LABEL_EMOJI[label] ?? ''} It's a {label}!
      </p>
      <p className="mt-1 text-center text-sm text-slate-500 dark:text-slate-400">
        {(confidence * 100).toFixed(1)}% confident
      </p>

      <div className="mt-5 space-y-3">
        {sortedProbabilities.map(([className, probability]) => (
          <div key={className}>
            <div className="mb-1 flex justify-between text-sm capitalize">
              <span>{className}</span>
              <span>{(probability * 100).toFixed(1)}%</span>
            </div>
            <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
              <div
                className="h-full rounded-full bg-indigo-500"
                style={{ width: `${probability * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
