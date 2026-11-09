# ML: food image classification

## Default (no training required)

The backend loads a **pretrained, open-source** Vision Transformer fine-tuned on
[Food-101](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/)
from the Hugging Face Hub: [`nateraw/food`](https://huggingface.co/nateraw/food)
(Apache-2.0). It downloads automatically the first time the backend runs
(cached under `~/.cache/huggingface`) — no API key, no cost, no manual setup.

This covers the 101 Food-101 categories, which is also what
[`backend/app/data/nutrition.json`](../backend/app/data/nutrition.json) is
keyed on.

## Training your own model (optional)

If you want to fine-tune your own weights — e.g. on a larger/custom dataset,
or to improve accuracy — use [`train.py`](train.py):

```bash
pip install -r requirements.txt
python train.py --output_dir ./food101-vit --epochs 3
```

This fine-tunes `google/vit-base-patch16-224-in21k` on the open
[Food-101 dataset](https://huggingface.co/datasets/food101) using Hugging
Face's standard `Trainer` API (no custom training loop). A single epoch on a
free Google Colab GPU takes roughly 30–45 minutes.

To use the result, point the backend at it:

```bash
# backend/.env
ML_MODEL_ID=/absolute/path/to/food101-vit
# or, after `trainer.push_to_hub()` / manual upload:
ML_MODEL_ID=your-username/food101-vit
```

## Swapping in a different label set

If you fine-tune on different food categories, update
`backend/app/data/nutrition.json` to match — the backend looks up nutrition
by the model's predicted label name.
