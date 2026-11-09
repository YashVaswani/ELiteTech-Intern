# Cat vs Dog Classifier

A production-structured, fully open-source image classifier that tells cats
from dogs using a **Support Vector Machine** — not a neural network. Classical
computer-vision features (HOG + colour histograms) are extracted from each
image and fed to a scikit-learn `SVC`. It's served through a FastAPI backend
and a React + TypeScript frontend.

Everything here is free and open source: no paid APIs, no paid cloud services,
no proprietary datasets required beyond the free Kaggle download.

## How it works

```
                 ┌─────────────────────┐
  image  ──────► │ resize to 128×128   │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ HOG features        │
                 │ + RGB colour        │──► feature vector (≈8200-d)
                 │   histograms        │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ StandardScaler      │
                 │ + SVC (RBF kernel)  │──► "cat" / "dog" + confidence
                 └─────────────────────┘
```

Feature extraction (`backend/ml/features.py`) is shared by both training and
serving, so what the model was trained on is exactly what it sees in
production.

## Project layout

```
backend/
  app/            FastAPI application (HTTP layer)
  ml/             Feature extraction, dataset loading, training script
  tests/          pytest suite
  data/raw/       Your local dataset goes here (gitignored) — see data/README.md
  models/         Trained model + metrics land here (gitignored)
frontend/
  src/            React + TypeScript single-page app
scripts/
  organize_dataset.py   Turns a raw Kaggle download into the layout ml/dataset.py expects
```

## Prerequisites

- Python 3.10+ (3.10–3.12 recommended for best scikit-learn/scikit-image wheel support)
- Node.js 20+
- A free [Kaggle](https://www.kaggle.com/) account (only needed to download the dataset)
- Docker + Docker Compose (optional, for the containerized setup)

## 1. Get the dataset

The dataset isn't in this repo — see [backend/data/README.md](backend/data/README.md)
for exact commands. Short version:

```bash
pip install kaggle
kaggle competitions download -c dogs-vs-cats -p backend/data/kaggle-download
unzip backend/data/kaggle-download/*.zip -d backend/data/kaggle-download/extracted
python scripts/organize_dataset.py --source backend/data/kaggle-download/extracted/train --dest backend/data/raw
```

## 2. Train the model

```bash
cd backend
python -m venv .venv
./.venv/Scripts/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python -m ml.train
```

This runs a small grid search over the SVM's `C`/`gamma`, prints a
classification report, and writes `backend/models/model.joblib` +
`backend/models/metrics.json`.

## 3. Run the backend API

```bash
cd backend
python -m uvicorn app.main:app --reload
```

- `GET /health` → `{"status": "ok", "model_loaded": true}`
- `POST /predict` (multipart form, field `file`) → `{"label": "cat", "confidence": 0.97, "probabilities": {...}}`
- Interactive API docs: http://localhost:8000/docs

## 4. Run the frontend

```bash
cd frontend
npm install
cp .env.example .env.local   # points the UI at the local backend
npm run dev
```

Open http://localhost:5173, drop in a photo, and click **Classify image**.

## Running everything with Docker Compose

Once you've trained a model (`backend/models/model.joblib` must exist —
Compose bakes it into the backend image read-only):

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## Tests & linting

```bash
# Backend
cd backend
ruff check .
ruff format --check .
pytest -q

# Frontend
cd frontend
npm run lint
npx tsc -b --noEmit
npm run test
```

Both suites run automatically in CI on every push/PR — see
[.github/workflows/ci.yml](.github/workflows/ci.yml).

To run the same checks automatically before every commit:

```bash
pip install pre-commit
pre-commit install
```

## Why an SVM (and not a CNN)?

This project is a classical machine-learning exercise: the point is to show
that a well-chosen feature representation (HOG for shape/edges, colour
histograms for colour distribution) plus a kernel SVM can separate cats from
dogs reasonably well without deep learning. It also keeps the whole stack
CPU-only and dependency-light — no GPU, no PyTorch/TensorFlow, nothing to pay
for.

## Tech stack

| Layer | Choice | Why |
|---|---|---|
| ML | scikit-learn `SVC` + scikit-image `hog` | Standard, free, no GPU needed |
| Backend | FastAPI + Uvicorn | Async, automatic OpenAPI docs, minimal boilerplate |
| Frontend | React 19 + TypeScript + Vite | Fast dev loop, typed, zero-config Tailwind v4 plugin |
| Styling | Tailwind CSS v4 | Utility classes instead of hand-written CSS |
| Lint/format | ruff (Python), oxlint (TypeScript) | Single fast tool each, near-zero config |
| CI | GitHub Actions | Free for public repos |
| Containers | Docker + Docker Compose | Free, runs anywhere |

## License

[MIT](LICENSE).
