# Architecture

## Request flow: scanning a meal

```
┌──────────┐   photo    ┌──────────────┐   image bytes   ┌────────────────┐
│  React   │ ─────────▶ │ POST         │ ──────────────▶ │ FoodClassifier │
│ frontend │            │ /api/predict │                 │ (ViT, pretrained│
└──────────┘            └──────────────┘                 │  on Food-101)  │
     ▲                         │                          └────────────────┘
     │                         │ label + confidence               │
     │                         ▼                                  │
     │                  ┌──────────────┐                          │
     │                  │ nutrition    │ ◀────────────────────────┘
     │                  │ lookup table │
     │                  │ (JSON, per   │
     │                  │  100g)       │
     │                  └──────────────┘
     │                         │ scaled nutrition
     │◀────────────────────────┘
     │ JSON: { top_prediction, alternatives, nutrition }
```

The classifier and nutrition table are decoupled: the model only outputs a
food label (e.g. `"pizza"`); a separate lookup maps that label to
calories/macros. This means swapping the model (different checkpoint, or one
you fine-tuned yourself) only requires the new model's labels to exist in
`backend/app/data/nutrition.json` — no code changes.

## Backend layout

```
backend/app/
├── main.py              FastAPI app, CORS, router registration, table creation
├── api/routes/          One module per resource: auth, predict, foods, logs
├── core/                Settings (pydantic-settings) and JWT/password helpers
├── db/                  SQLAlchemy models (User, FoodLog) and session/engine
├── ml/model.py          Thin wrapper around the Hugging Face classifier
├── services/            Business logic: nutrition lookup, prediction orchestration
├── schemas/             Pydantic request/response models
└── data/nutrition.json  Bundled nutrition table (101 Food-101 categories)
```

Routes stay thin — they validate input, call a service function, and shape
the HTTP response. Business logic (nutrition math, prediction orchestration)
lives in `services/`, independent of FastAPI, so it's directly unit-testable.

## Why these choices

- **`Base.metadata.create_all()` instead of Alembic migrations.** This is a
  fresh schema with no prior versions to migrate from; a single line does the
  job. Add Alembic when the schema needs versioned migrations across
  deployed environments.
- **SQLite by default, Postgres in Docker Compose.** Zero-setup local dev,
  production-grade database in the containerized stack — same SQLAlchemy
  code either way via `DATABASE_URL`.
- **JWT bearer tokens, not sessions.** Stateless, works cleanly with a
  separately-deployed SPA frontend, and `python-jose`/`passlib` are the
  standard, well-audited libraries for it — no custom crypto.
- **Model and nutrition data are both swappable via config/files**, not
  hardcoded, so accuracy can be improved (fine-tuned model, real USDA import)
  without touching application code.

## Frontend layout

```
frontend/src/
├── api/        Typed functions wrapping each backend endpoint (axios)
├── components/ Presentational + form components (Navbar, AuthForm, etc.)
├── context/    AuthContext — holds the current user, login/register/logout
├── hooks/      useAuth()
├── pages/      One component per route (Dashboard, Scan, Foods, Login, Register)
└── types/      TypeScript interfaces mirroring backend Pydantic schemas
```

Auth state lives in React Context; the JWT itself is persisted to
`localStorage` and attached to requests via an axios interceptor.
`ProtectedRoute` redirects to `/login` when there's no authenticated user.
