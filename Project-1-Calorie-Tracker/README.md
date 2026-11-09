# Calorie Tracker

Recognize a food item from a photo and estimate its calories and macros — built end-to-end with **only free, open-source tools** (no paid APIs, no proprietary models).

> Internship project: *"Develop a model that can accurately recognize food items from images and estimate their calorie content, enabling users to track their dietary intake and make informed food choices."*

## How it works

1. User uploads/takes a photo of a meal in the React frontend.
2. FastAPI backend runs it through a pretrained, open-source Vision Transformer ([`nateraw/food`](https://huggingface.co/nateraw/food), Apache-2.0) fine-tuned on the [Food-101](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/) dataset — 101 food categories.
3. The predicted label is matched against a bundled nutrition lookup table (calories/protein/carbs/fat per 100g) and scaled to the chosen serving size.
4. The user can log the entry to their daily food diary and track progress against a calorie goal.

No paid nutrition API, no cloud ML service — the model runs locally/in your own container, and nutrition data ships in the repo (swappable for a full [USDA FoodData Central](https://fdc.nal.usda.gov/) import via `backend/scripts/import_usda.py`).

## Tech stack (all free & open source)

| Layer | Tech |
|---|---|
| ML | PyTorch, Hugging Face Transformers, pretrained ViT (Apache-2.0) |
| Backend | FastAPI, SQLAlchemy, Pydantic, JWT auth (python-jose + passlib) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, React Router, Axios |
| Infra | Docker, Docker Compose, GitHub Actions CI, pre-commit |

## Project structure

```
.
├── backend/          FastAPI app, ML inference, nutrition data, tests
├── frontend/         React + Vite + TypeScript SPA
├── ml/               Optional training script to fine-tune your own model
├── docs/             Architecture & API notes
├── docker-compose.yml
└── .github/          CI workflow, issue/PR templates
```

## Quick start (Docker)

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API docs (Swagger UI): http://localhost:8000/docs

The first prediction request downloads the ~350MB model checkpoint from Hugging Face and caches it in a Docker volume — subsequent requests are fast.

## Quick start (manual / local dev)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

App: http://localhost:5173

## Testing

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm run lint && npm run build
```

Prediction tests mock the ML model so the suite runs fast without downloading weights; run the app itself to exercise the real model.

## API overview

| Method | Path | Description |
|---|---|---|
| POST | `/api/auth/register` | Create an account |
| POST | `/api/auth/login` | Get a JWT access token |
| GET | `/api/auth/me` | Current user |
| POST | `/api/predict` | Upload an image, get food name + calorie/macro estimate |
| GET | `/api/foods` | Browse the full nutrition database |
| GET | `/api/foods/{name}` | Nutrition for one food, scaled by `grams` |
| POST | `/api/logs` | Log a food entry to your diary |
| GET | `/api/logs` | List your logged entries |
| DELETE | `/api/logs/{id}` | Remove a logged entry |
| GET | `/api/logs/summary/{date}` | Daily calorie/macro totals + entries |

Full interactive docs at `/docs` (Swagger) once the backend is running.

## Design notes

- **Minimal, standard-library-first code.** No custom auth framework, no custom ORM, no hand-rolled training loop — JWT via `python-jose`, SQLAlchemy for persistence, Hugging Face `Trainer` for optional fine-tuning. Standard tools before custom code, everywhere.
- **Works offline / zero-cost by default.** SQLite, a locally-run open-source model, and a bundled nutrition table mean the whole stack runs with no API keys and no recurring cost.
- **Swappable data sources.** `ML_MODEL_ID` env var swaps the model; `backend/scripts/import_usda.py` upgrades the bundled nutrition estimates to real USDA data.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for more detail, and [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

## License

[MIT](LICENSE)
