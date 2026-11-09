"""Fine-tune an image classifier on Food-101 (optional).

The backend works out of the box with the pretrained, open-source
`nateraw/food` checkpoint (see backend/app/ml/model.py) — running this
script is only needed if you want to train your own weights.

Uses the standard Hugging Face `Trainer` API rather than a hand-rolled
training loop, and torchvision's built-in Food-101 dataset loader rather
than a custom downloader — both free, open-source, and already battle-tested.

Usage:
    pip install -r requirements.txt
    python train.py --output_dir ./food101-vit --epochs 3

The resulting directory is a standard Hugging Face model folder: point
ML_MODEL_ID in backend/.env at its path (or push it to the HF Hub and use
the repo id) to swap it in for the default pretrained model.
"""

import argparse

import numpy as np
import torch
from datasets import load_dataset
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
    Trainer,
    TrainingArguments,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base_model", default="google/vit-base-patch16-224-in21k")
    parser.add_argument("--output_dir", default="./food101-vit")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--learning_rate", type=float, default=5e-5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    dataset = load_dataset("food101")
    labels = dataset["train"].features["label"].names

    processor = AutoImageProcessor.from_pretrained(args.base_model)

    def transform(batch):
        images = [img.convert("RGB") for img in batch["image"]]
        inputs = processor(images=images, return_tensors="pt")
        inputs["labels"] = batch["label"]
        return inputs

    dataset = dataset.with_transform(transform)

    model = AutoModelForImageClassification.from_pretrained(
        args.base_model,
        num_labels=len(labels),
        id2label=dict(enumerate(labels)),
        label2id={label: i for i, label in enumerate(labels)},
        ignore_mismatched_sizes=True,
    )

    def collate_fn(batch):
        return {
            "pixel_values": torch.stack([item["pixel_values"] for item in batch]),
            "labels": torch.tensor([item["labels"] for item in batch]),
        }

    def compute_metrics(eval_pred):
        predictions = np.argmax(eval_pred.predictions, axis=1)
        accuracy = (predictions == eval_pred.label_ids).mean()
        return {"accuracy": accuracy}

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_steps=50,
        remove_unused_columns=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        data_collator=collate_fn,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    processor.save_pretrained(args.output_dir)


if __name__ == "__main__":
    main()
