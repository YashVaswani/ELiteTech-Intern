from functools import lru_cache
from io import BytesIO

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

from app.core.config import get_settings


class FoodClassifier:
    """Thin wrapper around a pretrained Hugging Face image-classification model.

    Defaults to a ViT checkpoint fine-tuned on the Food-101 dataset
    (https://huggingface.co/nateraw/food, Apache-2.0), so no custom training
    or GPU is required to get a working classifier out of the box.
    """

    def __init__(self, model_id: str) -> None:
        self.processor = AutoImageProcessor.from_pretrained(model_id)
        self.model = AutoModelForImageClassification.from_pretrained(model_id)
        self.model.eval()

    @torch.inference_mode()
    def predict(self, image_bytes: bytes, top_k: int = 3) -> list[tuple[str, float]]:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        logits = self.model(**inputs).logits[0]
        probs = torch.softmax(logits, dim=-1)
        top_probs, top_indices = torch.topk(probs, k=min(top_k, probs.shape[-1]))

        return [
            (self.model.config.id2label[idx.item()], prob.item())
            for prob, idx in zip(top_probs, top_indices, strict=False)
        ]


@lru_cache
def get_classifier() -> FoodClassifier:
    settings = get_settings()
    return FoodClassifier(settings.ml_model_id)
