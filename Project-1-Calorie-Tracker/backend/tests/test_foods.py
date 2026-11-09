def test_list_foods_returns_all_categories(client):
    response = client.get("/api/foods")
    assert response.status_code == 200
    foods = response.json()
    assert len(foods) == 101
    assert any(f["food_name"] == "pizza" for f in foods)


def test_get_food_scales_by_grams(client):
    response = client.get("/api/foods/pizza", params={"grams": 200})
    assert response.status_code == 200
    data = response.json()
    assert data["serving_grams"] == 200
    assert data["calories"] == 532.0  # 266 kcal/100g * 2


def test_get_unknown_food_returns_404(client):
    response = client.get("/api/foods/not_a_real_food")
    assert response.status_code == 404
