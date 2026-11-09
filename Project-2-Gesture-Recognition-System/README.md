# Hand Gesture Recognition System

Real-time hand gesture recognition for intuitive human-computer interaction:
a webcam frame goes in, a gesture label and confidence come out, over a REST
or WebSocket API, with a live React UI on top.

100% free and open-source — every dependency (FastAPI, MediaPipe,
scikit-learn, React) is MIT/BSD/Apache-2.0 licensed, no paid APIs or
metered cloud services required.

## How it works

```
 Webcam frame
      │
      ▼
 MediaPipe HandLandmarker   →  21 (x, y, z) hand landmarks
      │
      ▼
 Feature normalization      →  wrist-relative, scale-invariant 63-dim vector
 (app/ml/features.py)          (shared by training AND inference — no drift)
      │
      ▼
 scikit-learn classifier    →  gesture label + confidence
 (RandomForestClassifier)
```

Supported gestures: `open_palm`, `fist`, `thumbs_up`, `thumbs_down`, `peace`,
`ok`, `pointing`.

> **Note on the shipped model:** the classifier committed in
> `backend/app/ml/artifacts/` is trained on a **synthetic**, procedurally
> generated landmark dataset (see `backend/training/hand_model.py`) so the
> whole system works out of the box with zero setup. It's a reasonable demo
> but was never shown a real hand. For real accuracy, collect a few minutes
> of your own webcam data with the included tool and retrain — see
> [`backend/training/README.md`](backend/training/README.md).

## Tech stack

| Layer          | Choice                                                    |
| -------------- | ----------------------------------------------------------- |
| Hand tracking  | [MediaPipe](https://ai.google.dev/edge/mediapipe) HandLandmarker (Apache-2.0) |
| Classifier     | scikit-learn `RandomForestClassifier` on normalized landmarks |
| Backend        | FastAPI (REST + WebSocket), Python 3.11                     |
| Frontend       | React 19, TypeScript, Vite, Tailwind CSS 4                  |
| Packaging      | Docker Compose                                               |
| CI             | GitHub Actions (lint + test, both apps)                     |

This project follows a **"lazy senior dev"** rule — minimum code, prefer
standard library / well-known OSS over custom code, no speculative
abstraction. See [`CLAUDE.md`](CLAUDE.md).

## Project structure

```
backend/
  app/
    api/routes/       REST + WebSocket endpoints
    ml/                landmark extraction, feature normalization, classifier
    ml/artifacts/       shipped model files (hand_landmarker.task, gesture_classifier.joblib)
    schemas/            pydantic request/response models
    services/           glue between ML layer and API layer
  training/            standalone scripts: synthetic data, webcam collection, training
  tests/               pytest suite
frontend/
  src/
    hooks/              webcam access, WebSocket streaming
    components/          webcam view w/ landmark overlay, prediction panel
    api/                 backend client
docker-compose.yml
.github/workflows/ci.yml
```

## Quick start (Docker Compose)

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000 (docs at `/docs`)

## Quick start (manual)

Requires Python 3.10–3.12 (MediaPipe doesn't yet ship wheels for newer
Python) and Node 20+.

**Backend:**

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements-dev.txt
python -m app.ml.download_model   # one-time: ~8MB MediaPipe model
uvicorn app.main:app --reload
```

The repo already ships a trained classifier, so the API works immediately.
To retrain (recommended for real accuracy), see
[`backend/training/README.md`](backend/training/README.md).

**Frontend:**

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open the printed local URL and allow camera access.

## API

| Method | Path                     | Description                                      |
| ------ | ------------------------ | ------------------------------------------------- |
| GET    | `/health`                | Liveness check                                     |
| GET    | `/api/v1/gestures`       | List supported gesture labels                      |
| POST   | `/api/v1/predict/image`  | Multipart image upload → `PredictionResponse`      |
| WS     | `/api/v1/predict/stream` | Send JPEG/PNG bytes per frame, receive one `PredictionResponse` JSON per frame |

```json
// PredictionResponse
{
  "gesture": "thumbs_up",
  "confidence": 0.94,
  "landmarks": [{ "x": 0.42, "y": 0.61, "z": -0.01 }, "... 21 total"]
}
```

Interactive docs (Swagger UI) at `/docs` once the backend is running.

## Testing

```bash
cd backend && ruff check . && ruff format --check . && pytest
cd frontend && npm run lint && npm run build
```

Both run in CI on every push/PR — see [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Deployment notes

- The WebSocket endpoint has no built-in auth/rate limiting — put it behind
  your own reverse proxy (nginx, Caddy) or auth layer for a public deployment.
- `HandLandmarker` is not thread-safe per instance; `PredictionService`
  serializes access with a lock, so throughput on a single backend instance
  is bounded by single-threaded MediaPipe inference (~30-60 fps on a modern
  CPU for one hand). Scale horizontally (more backend replicas) for more
  concurrent users, not more threads per instance.
- Gesture frames are processed in memory only and never written to disk.

## License

[MIT](LICENSE) — see [`SECURITY.md`](SECURITY.md) for reporting
vulnerabilities and [`CONTRIBUTING.md`](CONTRIBUTING.md) to contribute.
