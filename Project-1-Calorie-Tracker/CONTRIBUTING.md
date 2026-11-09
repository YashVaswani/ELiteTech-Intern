# Contributing

Thanks for considering a contribution. This project is a full-stack food recognition and calorie tracking app, built entirely on free, open-source tooling.

## Getting set up

See [README.md](README.md) for the full local setup (backend + frontend). In short:

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Before opening a pull request

1. Install pre-commit hooks once: `pip install pre-commit && pre-commit install` (run from the repo root).
2. Backend: `ruff check . && black --check . && pytest` (from `backend/`).
3. Frontend: `npm run lint && npm run build` (from `frontend/`).
4. Keep changes focused — one logical change per PR, with a clear description of *why*.

## Code style

- Python: [Black](https://black.readthedocs.io/) formatting, [Ruff](https://docs.astral.sh/ruff/) linting, type hints on new code.
- TypeScript/React: functional components, typed props, [oxlint](https://oxc.rs) clean.
- Prefer standard library / well-known packages over custom implementations — avoid adding a dependency or abstraction unless it earns its complexity.

## Reporting bugs

Open an issue using the bug report template with steps to reproduce, expected vs. actual behavior, and environment details.
