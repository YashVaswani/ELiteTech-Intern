import { type RefObject, useEffect, useRef } from 'react'
import { HAND_CONNECTIONS } from '../handConnections'
import type { PredictionResponse } from '../types'

interface Props {
  videoRef: RefObject<HTMLVideoElement | null>
  prediction: PredictionResponse | null
}

export function WebcamView({ videoRef, prediction }: Props) {
  const overlayRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = overlayRef.current
    const video = videoRef.current
    if (!canvas || !video) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let rafId: number
    const draw = () => {
      canvas.width = video.clientWidth
      canvas.height = video.clientHeight
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      const landmarks = prediction?.landmarks
      if (landmarks) {
        ctx.strokeStyle = '#22d3ee'
        ctx.lineWidth = 2
        for (const [a, b] of HAND_CONNECTIONS) {
          const p1 = landmarks[a]
          const p2 = landmarks[b]
          ctx.beginPath()
          ctx.moveTo(p1.x * canvas.width, p1.y * canvas.height)
          ctx.lineTo(p2.x * canvas.width, p2.y * canvas.height)
          ctx.stroke()
        }
        ctx.fillStyle = '#facc15'
        for (const p of landmarks) {
          ctx.beginPath()
          ctx.arc(p.x * canvas.width, p.y * canvas.height, 3, 0, Math.PI * 2)
          ctx.fill()
        }
      }
      rafId = requestAnimationFrame(draw)
    }
    rafId = requestAnimationFrame(draw)
    return () => cancelAnimationFrame(rafId)
  }, [videoRef, prediction])

  return (
    <div className="relative w-full max-w-xl overflow-hidden rounded-xl border border-slate-800 bg-black">
      <video ref={videoRef} autoPlay playsInline muted className="w-full -scale-x-100" />
      <canvas ref={overlayRef} className="absolute inset-0 -scale-x-100" />
    </div>
  )
}
