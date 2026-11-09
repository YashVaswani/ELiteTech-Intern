# Retail Customer Segmentation (K-means)

Segment a retail store's customers by purchase history using **RFM features
(Recency, Frequency, Monetary) + K-means clustering**, packaged as a real
production-shaped product: a tested Python ML pipeline, a FastAPI backend,
a React + TypeScript dashboard, CI, and a container image.

**100% open source, 100% free** - scikit-learn, pandas, FastAPI, React,
Tailwind, Recharts, pytest, vitest, ruff, Biome, Docker, GitHub Actions. No
paid API, no paid cloud service, no license key anywhere in this repo.

<!-- Replace `<owner>/<repo>` once this is pushed to GitHub for a live badge. -->
<!-- ![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg) -->

## Why RFM + K-means

- **Recency, Frequency, Monetary** are the three purchase-history signals
  that best predict future customer value, and they're derivable from a
  bare `(customer_id, invoice_date, amount)` transaction log - no need for
  demographic or browsing data most stores don't have.
- **K-means** is the standard, well-understood algorithm for this: fast,
  works well on the 2-3 continuous features RFM produces, and every stats
  team already knows how to read its output. This project uses
  scikit-learn's implementation rather than a hand-rolled one - it already
  does k-means++ initialization and multiple restarts correctly.
- **The number of clusters (`k`) is chosen automatically** via the elbow
  method and silhouette score, not hardcoded, so the pipeline stays correct
  if the underlying customer base changes.

## Architecture

```
┌─────────────────────┐      retail-segment train      ┌──────────────────────┐
│ retail_segmentation  │ ───────────────────────────────▶ │ models/*.joblib      │
│ (the ML library)     │                                 │ data/processed/*.csv │
└─────────────────────┘                                 │ reports/*            │
                                                          └──────────┬───────────┘
                                                                     │ read at startup
┌─────────────────────┐        GET/POST /api/*          ┌───────────▼──────────┐
│ React + TypeScript   │ ◀──────────────────────────────▶ │ FastAPI (api/)       │
│ frontend (Recharts,  │        (Vite dev proxy, or       │ - thin HTTP layer    │
│ Tailwind)             │        same-origin in prod)      │ - no ML logic here   │
└─────────────────────┘                                  └──────────────────────┘
```

The ML pipeline and the web layer are fully decoupled: `retail_segmentation`
has no knowledge of HTTP, and `api/` has no ML logic beyond calling into it.
That's what's unit-tested independently of the API in `tests/`.

## Results

Trained on the bundled synthetic dataset (2,000 customers):

| | |
|---|---|
| ![k selection](reports/figures/k_selection.png) | ![clusters](reports/figures/clusters_pca.png) |

| Segment | Customers | Avg. days since last order | Avg. orders | Avg. spend |
|---|---|---|---|---|
| Champions | 531 | 61.5 | 28.1 | $3,301.5 |
| Potential Loyalists | 1,103 | 480.8 | 9.1 | $546.4 |
| New Customers | 366 | 96.1 | 1.5 | $71.9 |

(Regenerate with `retail-segment train` - exact numbers depend on the data.)

## Project structure

```
.
├── src/retail_segmentation/   # the ML library (framework-agnostic)
│   ├── data.py                 # load real transactions, or generate synthetic ones
│   ├── features.py             # transactions -> RFM features
│   ├── model.py                # log-transform + scale + K-means pipeline
│   ├── evaluate.py             # elbow method + silhouette score for choosing k
│   ├── segments.py             # cluster id -> business-readable segment name
│   ├── insights.py             # shared PCA projection helper
│   ├── viz.py                  # static elbow/silhouette + PCA plots (for the README/notebook)
│   ├── config.py               # loads configs/config.yaml
│   └── cli.py                  # `retail-segment train` / `retail-segment predict`
├── api/                        # FastAPI serving layer (thin - no ML logic)
│   ├── main.py                  # endpoints, reads the trained artifacts once at startup
│   └── schemas.py                # request/response models
├── frontend/                   # React + TypeScript + Tailwind + Recharts dashboard
│   └── src/
│       ├── App.tsx               # tabs: Overview / Explore segments / Classify a customer
│       ├── api.ts                # typed fetch client for the backend
│       └── components/           # charts, tables, forms
├── tests/                      # pytest: unit tests + FastAPI integration tests
├── notebooks/                   # exploratory analysis notebook (mirrors the pipeline)
├── configs/config.yaml         # all tunable settings (paths, k range, random seed)
├── data/                        # raw + processed data (gitignored, regenerated on train)
├── models/                      # trained pipeline artifact (gitignored, regenerated)
├── reports/                     # generated plots + k-selection scores (gitignored, regenerated)
├── .github/workflows/ci.yml    # backend + frontend lint/test/build on every push
├── Dockerfile                    # multi-stage: builds the React app, serves it + the API from one process
└── .pre-commit-config.yaml     # auto lint/format on commit (Python side)
```

## Setup

Requires Python 3.10+ and Node.js 20+.

```bash
# Backend
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash / macOS / Linux: source .venv/bin/activate
pip install -e ".[api,dev]"

# Frontend
cd frontend && npm install && cd ..
```

## Usage

**1. Train the pipeline** (generates synthetic data on first run if
`data/raw/transactions.csv` doesn't exist, computes RFM features, picks the
best `k`, fits K-means, and saves the model + segmented customers + plots):

```bash
retail-segment train
```

**2. Run the backend API:**

```bash
uvicorn api.main:app --reload --port 8000
```

**3. Run the frontend** (in a second terminal - the Vite dev server proxies
`/api/*` to the backend, so no CORS setup is needed):

```bash
cd frontend && npm run dev
```

Open http://localhost:5173 for the dashboard (Overview with segment summary
and charts, per-segment drill-down with CSV export, and a form to classify
a new customer) or http://localhost:8000/docs for the interactive API docs.

**Classify a single customer** from the command line instead:

```bash
retail-segment predict --recency 15 --frequency 12 --monetary 850
```

**Use your own data** instead of the synthetic generator: drop a CSV with
columns `customer_id, invoice_date, amount` at `data/raw/transactions.csv`
before running `retail-segment train` (see `data/README.md`).

## Configuration

All tunable values live in [`configs/config.yaml`](configs/config.yaml) -
file paths, the number of synthetic customers, the `k` search range, and the
random seed. Edit the file; no code changes needed.

## Testing, linting, formatting

Backend:

```bash
pytest                # unit tests + FastAPI integration tests
ruff check .           # lint
ruff format .          # format
pre-commit install    # optional: run both automatically on every commit
```

Frontend:

```bash
cd frontend
npm run build          # type-check (tsc) + production build
npm test               # vitest + React Testing Library
npm run lint           # Biome (lint + import order)
npm run format          # Biome (format)
```

CI (`.github/workflows/ci.yml`) runs both suites - lint, tests, and a full
pipeline smoke test - on every push, using GitHub Actions' free tier.

## Running with Docker

```bash
docker build -t retail-segmentation .
docker run --rm -p 8000:8000 retail-segmentation
```

Then open http://localhost:8000. The image is a multi-stage build: it
compiles the React app, trains the model, and serves both the API and the
built frontend from a single FastAPI process - no external service, no API
key, no separate web server to configure.

## Design notes

- **No custom K-means implementation.** scikit-learn's is faster, tested,
  and handles edge cases (empty clusters, bad initialization) correctly.
- **The ML pipeline and the web layer are fully decoupled.** `api/` is a
  thin adapter over `retail_segmentation`, which has zero HTTP awareness
  and is tested entirely on its own.
- **One linter/formatter per language** - ruff for Python, Biome for
  TypeScript - instead of a black+isort+flake8 or eslint+prettier stack
  doing the same job with several configs instead of one.
- **`k` is data-driven, not hardcoded** - silhouette score picks it, so
  relabeling logic (`segments.py`) has to work for whatever `k` comes out,
  not just a specific number chosen in advance.
- **Same-origin in production.** The frontend build is served by FastAPI
  itself, so there's no CORS configuration to maintain and no second web
  server in the container.

## License

MIT - see [LICENSE](LICENSE).
