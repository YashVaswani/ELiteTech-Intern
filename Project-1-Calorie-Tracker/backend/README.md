# Calorie Tracker — Backend

FastAPI service that recognizes food from photos (pretrained open-source ViT) and estimates calories/macros. See the [repo root README](../README.md) for the full project overview.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

The first call to `/api/predict` downloads the ~350MB `nateraw/food` checkpoint from Hugging Face and caches it under `~/.cache/huggingface`.

## Configuration

All settings are environment variables (see `.env.example`), loaded via `pydantic-settings`. Notably:

- `DATABASE_URL` — SQLite by default, or a Postgres URL for production
- `SECRET_KEY` — JWT signing key; **must** be changed and kept secret in production
- `ML_MODEL_ID` — Hugging Face model id or local path for the classifier

## Testing

```bash
pytest -v
```

Prediction endpoint tests monkeypatch `predict_food` so the suite doesn't need to download model weights. Everything else runs against a real (temporary, per-test) SQLite database.

## Linting & formatting

```bash
ruff check .
black .
```

## Improving nutrition accuracy

The bundled `app/data/nutrition.json` contains estimated values for demo purposes. To replace them with real USDA data:

```bash
python scripts/import_usda.py --usda-dir /path/to/unzipped/usda/csv
```

See the docstring in that script for where to download the (free, no API key) USDA export.
