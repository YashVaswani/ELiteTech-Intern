# Contributing

## Setup

See the [README](README.md) for full backend/frontend setup instructions.

## Code style

- **Backend (Python):** formatted and linted with [ruff](https://docs.astral.sh/ruff/). Run `ruff format .` and `ruff check --fix .` from `backend/` before committing.
- **Frontend (TypeScript):** linted with [oxlint](https://oxc.rs/docs/guide/usage/linter.html). Run `npm run lint` from `frontend/`.
- Install the git hooks once with `pre-commit install` (see `.pre-commit-config.yaml`) so both run automatically on commit.

## Guiding principle

Prefer the smallest correct change. Before adding a custom abstraction, a new
dependency, or a helper function, check whether the standard library, an
already-installed library, or a single inline expression already solves the
problem. Don't add configuration options, error handling, or generality for
cases that don't exist yet.

## Tests

- Backend: `pytest -q` from `backend/` (with the venv active).
- Frontend: `npm run test` from `frontend/`.

Both run in CI on every pull request (`.github/workflows/ci.yml`); please
keep them green.

## Commit messages

Short, imperative summary line (e.g. `Fix CORS header on image-decode errors`),
explaining *why* when it isn't obvious from the diff.
