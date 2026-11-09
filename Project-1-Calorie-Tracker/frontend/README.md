# Calorie Tracker — Frontend

React + TypeScript + Vite single-page app. Talks to the FastAPI backend in [`../backend`](../backend).

## Setup

```bash
npm install
cp .env.example .env
npm run dev
```

Runs at http://localhost:5173. Requires the backend running at the URL set in `VITE_API_BASE_URL` (default `http://localhost:8000`).

## Scripts

- `npm run dev` — start the Vite dev server
- `npm run build` — type-check and build for production
- `npm run preview` — preview the production build locally
- `npm run lint` — run oxlint

## Structure

```
src/
  api/        typed API client functions (axios)
  components/ shared UI components
  context/    React context (auth)
  hooks/      custom hooks
  pages/      route-level pages
  types/      shared TypeScript types matching backend schemas
```
