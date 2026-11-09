# Self-hostable image serving both the API and the React UI from one process
# - no paid platform required.
# Build:  docker build -t retail-segmentation .
# Run:    docker run --rm -p 8000:8000 retail-segmentation

FROM node:22-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM python:3.12-slim
WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY api ./api
RUN pip install --no-cache-dir ".[api]"

COPY configs ./configs
COPY --from=frontend-build /frontend/dist ./frontend/dist

# Train once at image build time so the container serves ready-to-use data.
RUN retail-segment train

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
