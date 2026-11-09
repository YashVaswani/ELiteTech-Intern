# Contributing

Thanks for considering a contribution. This project follows a **"lazy senior
dev"** philosophy — see [`CLAUDE.md`](CLAUDE.md) for the full rule, but in
short: minimum code, prefer standard/library solutions over custom ones, no
speculative abstraction.

## Getting set up

See [`README.md`](README.md) → Quick start for backend + frontend setup.

## Workflow

1. Fork the repo and create a branch: `git checkout -b feat/short-description`.
2. Install pre-commit hooks once: `pip install pre-commit && pre-commit install`.
3. Make your change, keeping it as small as solves the problem.
4. Run checks before pushing:
   - Backend: `cd backend && ruff check . && ruff format --check . && pytest`
   - Frontend: `cd frontend && npm run lint && npm run build`
5. Open a pull request using the PR template. Link any related issue.

## Commit messages

Use short, imperative subject lines (`Add websocket reconnect backoff`, not
`Added` or `Adds`). Explain *why* in the body when it isn't obvious from the
diff.

## Adding a new gesture class

1. Add the label to `backend/app/ml/gestures.py`.
2. Regenerate/collect landmark data for it (`backend/training/README.md`).
3. Re-run `backend/training/train.py` and check the accuracy/confusion matrix
   in `backend/training/outputs/`.
4. Commit the updated `backend/app/ml/artifacts/` model files.

## Reporting bugs / requesting features

Use the GitHub issue templates under `.github/ISSUE_TEMPLATE/`.
