import type { PredictionResponse } from '../types'

interface Props {
  prediction: PredictionResponse | null
  history: string[]
}

const GESTURE_EMOJI: Record<string, string> = {
  open_palm: '✋',
  fist: '✊',
  thumbs_up: '👍',
  thumbs_down: '👎',
  peace: '✌️',
  ok: '👌',
  pointing: '👆',
}

export function GesturePanel({ prediction, history }: Props) {
  const gesture = prediction?.gesture
  const confidence = prediction?.confidence

  return (
    <div className="flex w-full max-w-xs flex-col gap-4 rounded-xl border border-slate-800 bg-slate-900 p-5">
      <div className="text-center">
        <div className="text-6xl">{gesture ? (GESTURE_EMOJI[gesture] ?? '🖐️') : '—'}</div>
        <div className="mt-2 text-lg font-medium capitalize">
          {gesture ? gesture.replaceAll('_', ' ') : 'No hand detected'}
        </div>
        {confidence != null && (
          <div className="mt-3">
            <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full bg-cyan-400 transition-all"
                style={{ width: `${Math.round(confidence * 100)}%` }}
              />
            </div>
            <div className="mt-1 text-xs text-slate-400">
              {Math.round(confidence * 100)}% confidence
            </div>
          </div>
        )}
      </div>

      {history.length > 0 && (
        <div>
          <div className="mb-1 text-xs tracking-wide text-slate-500 uppercase">Recent</div>
          <div className="flex flex-wrap gap-1">
            {history.map((g, i) => (
              <span key={i} className="rounded bg-slate-800 px-2 py-1 text-xs capitalize">
                {g.replaceAll('_', ' ')}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
