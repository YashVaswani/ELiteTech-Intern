import { type RefObject, useEffect, useRef, useState } from 'react'
import { WS_STREAM_URL } from '../api/client'
import type { PredictionResponse } from '../types'

export type StreamStatus = 'idle' | 'connecting' | 'open' | 'closed' | 'error'

const FRAME_INTERVAL_MS = 150
const JPEG_QUALITY = 0.7

export function useGestureStream(
  videoRef: RefObject<HTMLVideoElement | null>,
  active: boolean,
) {
  const [status, setStatus] = useState<StreamStatus>('idle')
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null)
  const canvasRef = useRef<HTMLCanvasElement>(document.createElement('canvas'))
  const waitingForReplyRef = useRef(false)

  useEffect(() => {
    if (!active) return
    setStatus('connecting')

    const ws = new WebSocket(WS_STREAM_URL)

    ws.onopen = () => setStatus('open')
    ws.onerror = () => setStatus('error')
    ws.onclose = () => setStatus('closed')
    ws.onmessage = (event) => {
      waitingForReplyRef.current = false
      setPrediction(JSON.parse(event.data) as PredictionResponse)
    }

    const intervalId = window.setInterval(() => {
      const video = videoRef.current
      if (!video || video.readyState < 2) return
      if (ws.readyState !== WebSocket.OPEN) return
      if (waitingForReplyRef.current) return // backpressure: skip until previous frame is answered

      const canvas = canvasRef.current
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      const ctx = canvas.getContext('2d')
      if (!ctx) return
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

      canvas.toBlob(
        (blob) => {
          if (blob && ws.readyState === WebSocket.OPEN) {
            waitingForReplyRef.current = true
            ws.send(blob)
          }
        },
        'image/jpeg',
        JPEG_QUALITY,
      )
    }, FRAME_INTERVAL_MS)

    return () => {
      window.clearInterval(intervalId)
      ws.close()
    }
  }, [active, videoRef])

  return { status, prediction }
}
