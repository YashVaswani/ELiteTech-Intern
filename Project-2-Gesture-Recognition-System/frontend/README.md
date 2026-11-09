# Frontend

React + TypeScript + Vite + Tailwind CSS. Captures webcam frames, streams
them to the backend over WebSocket, and renders the live gesture prediction
with a landmark skeleton overlay.

See the [repo root README](../README.md) for the full quick start. Summary:

```bash
npm install
cp .env.example .env   # set VITE_API_BASE_URL if the backend isn't on :8000
npm run dev
```

- `npm run lint` — oxlint
- `npm run build` — type-check (`tsc -b`) + production build

## Structure

- `src/hooks/useWebcam.ts` — requests camera access, exposes a `<video>` ref
- `src/hooks/useGestureStream.ts` — grabs frames onto a canvas, sends JPEG
  blobs over the WebSocket, applies simple backpressure (skip a frame if the
  previous one hasn't been answered yet)
- `src/components/WebcamView.tsx` — video + landmark skeleton overlay
- `src/components/GesturePanel.tsx` — current gesture, confidence, history
- `src/api/client.ts` — backend base URL / WS URL resolution
