# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
this project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-09-20

### Added

- FastAPI backend: REST `POST /api/v1/predict/image` and
  `WS /api/v1/predict/stream` endpoints for gesture prediction.
- MediaPipe Hands landmark extraction + scikit-learn gesture classifier
  (7 classes: open_palm, fist, thumbs_up, thumbs_down, peace, ok, pointing).
- Training pipeline: synthetic bootstrap dataset generator, webcam data
  collection tool, train/evaluate script.
- React + TypeScript + Vite + Tailwind frontend with live webcam gesture
  recognition and landmark overlay.
- Docker Compose setup, GitHub Actions CI, pre-commit hooks, and standard
  open-source project files.
