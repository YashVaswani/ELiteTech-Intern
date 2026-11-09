import { useEffect, useRef, useState } from 'react'
import { GesturePanel } from './components/GesturePanel'
import { StatusBadge } from './components/StatusBadge'
import { WebcamView } from './components/WebcamView'
import { useGestureStream } from './hooks/useGestureStream'
import { useWebcam } from './hooks/useWebcam'

const MAX_HISTORY = 8

function App() {
  const { videoRef, status: webcamStatus, error: webcamError } = useWebcam()
  const { status: streamStatus, prediction } = useGestureStream(
    videoRef,
    webcamStatus === 'active',
  )
  const [history, setHistory] = useState<string[]>([])
  const lastGesture = useRef<string | null>(null)

  useEffect(() => {
    const gesture = prediction?.gesture
    if (gesture && gesture !== lastGesture.current) {
      lastGesture.current = gesture
      setHistory((h) => [gesture, ...h].slice(0, MAX_HISTORY))
    }
  }, [prediction])

  return (
    <div className="mx-auto flex min-h-screen max-w-4xl flex-col items-center gap-6 px-4 py-8">
      <header className="text-center">
        <h1 className="text-2xl font-semibold">Hand Gesture Recognition</h1>
        <p className="mt-1 text-sm text-slate-400">
          Real-time gesture recognition powered by MediaPipe hand landmarks
        </p>
      </header>

      <StatusBadge webcamStatus={webcamStatus} streamStatus={streamStatus} />

      {webcamError && (
        <p className="rounded border border-red-800 bg-red-950 px-3 py-2 text-sm text-red-300">
          Camera error: {webcamError}. Allow camera access and reload.
        </p>
      )}

      <div className="flex w-full flex-col items-center gap-6 md:flex-row md:items-start md:justify-center">
        <WebcamView videoRef={videoRef} prediction={prediction} />
        <GesturePanel prediction={prediction} history={history} />
      </div>
    </div>
  )
}

export default App
