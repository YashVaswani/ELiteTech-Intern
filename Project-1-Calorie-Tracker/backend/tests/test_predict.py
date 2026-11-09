import io

from app.schemas.food import NutritionInfo, PredictionCandidate, PredictionResult


def _fake_prediction(image_bytes: bytes, serving_grams: float | None = None) -> PredictionResult:
    return PredictionResult(
        top_prediction=PredictionCandidate(food_name="pizza", confidence=0.92),
        alternatives=[PredictionCandidate(food_name="lasagna", confidence=0.05)],
        nutrition=NutritionInfo(
            food_name="pizza",
            serving_grams=150.0,
            calories=399.0,
            protein_g=16.5,
            carbs_g=49.5,
            fat_g=15.0,
        ),
    )


def test_predict_returns_top_food(client, monkeypatch):
    monkeypatch.setattr("app.api.routes.predict.predict_food", _fake_prediction)

    fake_image = io.BytesIO(b"not-a-real-jpeg-but-fine-for-mocked-inference")
    response = client.post(
        "/api/predict",
        files={"image": ("food.jpg", fake_image, "image/jpeg")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["top_prediction"]["food_name"] == "pizza"
    assert body["nutrition"]["calories"] == 399.0


def test_predict_rejects_unsupported_content_type(client):
    fake_file = io.BytesIO(b"not an image")
    response = client.post(
        "/api/predict",
        files={"image": ("food.txt", fake_file, "text/plain")},
    )
    assert response.status_code == 415
