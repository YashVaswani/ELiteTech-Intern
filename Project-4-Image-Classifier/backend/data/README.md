# Dataset setup

The dataset is not included in this repo (it's ~800MB and Kaggle requires
authentication to download it). Get it yourself with the Kaggle CLI:

```bash
pip install kaggle
# Get an API token from https://www.kaggle.com/settings -> "Create New Token"
# and place the downloaded kaggle.json at ~/.kaggle/kaggle.json
# (on Windows: C:\Users\<you>\.kaggle\kaggle.json)

kaggle competitions download -c dogs-vs-cats -p data/kaggle-download
# or, for the folder-per-class mirror:
# kaggle datasets download -d salader/dogs-vs-cats -p data/kaggle-download

unzip data/kaggle-download/*.zip -d data/kaggle-download/extracted
```

Then organize it into the layout this project expects:

```bash
python scripts/organize_dataset.py \
  --source data/kaggle-download/extracted/train \
  --dest backend/data/raw
```

This produces:

```
backend/data/raw/
    cat/   (thousands of .jpg files)
    dog/   (thousands of .jpg files)
```

Train the model against it (from `backend/`, with the venv active):

```bash
python -m ml.train
```

This writes `backend/models/model.joblib` (the trained pipeline) and
`backend/models/metrics.json` (accuracy + classification report). The API
loads `model.joblib` automatically the next time it starts.

Tip: pass `--limit 1000` to `organize_dataset.py` for a quick smoke-test
run on a subset before committing to training on the full ~25k images.
