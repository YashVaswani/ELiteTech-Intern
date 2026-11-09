import pytest

from app.services.nutrition_service import (
    get_nutrition_for_grams,
    is_known_food,
    normalize_food_name,
)


def test_normalize_food_name_handles_spaces_and_case():
    assert normalize_food_name("Chicken Wings") == "chicken_wings"
    assert normalize_food_name("french-fries") == "french_fries"


def test_is_known_food():
    assert is_known_food("Sushi") is True
    assert is_known_food("not_a_real_food") is False


def test_get_nutrition_for_grams_scales_linearly():
    result = get_nutrition_for_grams("hamburger", 300)
    assert result.calories == 810.0  # 270 kcal/100g * 3


def test_get_nutrition_for_unknown_food_raises():
    with pytest.raises(KeyError):
        get_nutrition_for_grams("not_a_real_food", 100)
