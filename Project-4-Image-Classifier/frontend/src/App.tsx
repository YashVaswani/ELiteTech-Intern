import { useEffect, useMemo, useState } from 'react'
import { ApiError, predictImage, type PredictionResponse } from './api'
import { ImageUploader } from './components/ImageUploader'
import { PredictionResult } from './components/PredictionResult'

type Status = 'idle' | 'loading' | 'success' | 'error'

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<Status>('idle')
  const [result, setResult] = useState<PredictionResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const previewUrl = useMemo(() => (file ? URL.createObjectURL(file) : null), [file])
  useEffect(() => () => (previewUrl ? URL.revokeObjectURL(previewUrl) : undefined), [previewUrl])

  const handleFileSelected = (selected: File) => {
    setFile(selected)
    setResult(null)
    setError(null)
    setStatus('idle')
  }

  const handleClassify = async () => {
    if (!file) return
    setStatus('loading')
    setError(null)
    try {
      const prediction = await predictImage(file)
      setResult(prediction)
      setStatus('success')
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Something went wrong. Please try again.')
      setStatus('error')
    }
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-xl flex-col items-center px-4 py-12">
      <h1 className="text-3xl font-bold">Cat vs Dog Classifier</h1>
      <p className="mt-2 text-center text-slate-500 dark:text-slate-400">
        A classical SVM (HOG + colour-histogram features) trained on the Kaggle
        "Dogs vs Cats" dataset.
      </p>

      <div className="mt-8 w-full space-y-4">
        <ImageUploader
          onFileSelected={handleFileSelected}
          previewUrl={previewUrl}
          disabled={status === 'loading'}
        />

        <button
          type="button"
          onClick={handleClassify}
          disabled={!file || status === 'loading'}
          className="w-full rounded-lg bg-indigo-600 py-3 font-medium text-white transition-colors hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300 dark:disabled:bg-slate-700"
        >
          {status === 'loading' ? 'Classifying…' : 'Classify image'}
        </button>

        {error && (
          <p
            role="alert"
            className="rounded-lg bg-red-50 p-3 text-sm text-red-700 dark:bg-red-950/40 dark:text-red-300"
          >
            {error}
          </p>
        )}

        {result && status === 'success' && <PredictionResult {...result} />}
      </div>
    </div>
  )
}

export default App
