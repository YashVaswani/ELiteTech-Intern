# Training pipeline

The API ships with a working default classifier trained on a **synthetic**
bootstrap dataset (a procedural hand-pose model, see `hand_model.py`) so the
project runs end to end with no setup. It recognizes the shape of each
gesture reasonably well but was never shown a real hand — expect it to be
noticeably less accurate than a model trained on real recordings. Retraining
on your own webcam data closes that gap and takes a few minutes.

## 1. Install training extras

```bash
cd backend
pip install -r training/requirements.txt
python -m app.ml.download_model   # one-time: fetches the MediaPipe hand model
```

## 2. Get landmark data

**Synthetic (default, already generated):**

```bash
python -m training.generate_synthetic_dataset --samples-per-class 300
```

**Real, from your webcam (recommended for real accuracy):**

```bash
python -m training.collect_webcam_data
```

A window opens showing your webcam feed with detected landmarks. Hold a
gesture in frame and press its number key (see the printed key legend) to
save a labeled sample; aim for 50-100+ per gesture from varied angles/
distances/lighting. Press `q` when done. Samples append to
`data/processed/collected.csv` and are combined with the synthetic set
automatically.

## 3. Train

```bash
python -m training.train
```

This trains a `RandomForestClassifier` on wrist-relative, scale-normalized
landmark features (`app/ml/features.py` — the exact same normalization the
API uses at inference time), prints a classification report, saves a
confusion matrix to `outputs/confusion_matrix.png`, and writes the trained
model to `app/ml/artifacts/gesture_classifier.joblib`, where the API loads
it from automatically on next restart.

## Adding a new gesture

1. Add the label to `app/ml/gestures.py`.
2. Add it to `GESTURE_FINGER_STATES` in `generate_synthetic_dataset.py`
   (optional, for a synthetic baseline) and/or collect real samples for it.
3. Re-run step 3.
