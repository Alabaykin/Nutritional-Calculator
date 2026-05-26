import pytest
from pydantic import ValidationError
from recipe_core.models import Recipe, Ingredient
from recipe_core.calculator import calculate_recipe
from recipe_core.exceptions import NegativeWeightError, EmptyRecipeError

def test_calculate_recipe_success():
    ingredients = [
        Ingredient(name="Курица", weight_g=200, protein=20, fat=5, carbs=0, kcal=125),
        Ingredient(name="Масло", weight_g=10, protein=0.5, fat=82.5, carbs=0.8, kcal=748)
    ]
    recipe = Recipe(recipe_name="Жареная курица", loss_coefficient=0.8, ingredients=ingredients)
    result = calculate_recipe(recipe)
    
    assert result.recipe_name == "Жареная курица"
    assert result.total_weight_raw == 210
    assert result.final_weight == 210 * 0.8
    assert result.total_protein == (20 * 200 / 100) + (0.5 * 10 / 100)
    assert result.total_fat == (5 * 200 / 100) + (82.5 * 10 / 100)
    assert result.total_carbs == (0 * 200 / 100) + (0.8 * 10 / 100)
    assert result.total_kcal == (125 * 200 / 100) + (748 * 10 / 100)
    
    assert result.protein_100g == pytest.approx((result.total_protein / result.final_weight) * 100)
    assert result.fat_100g == pytest.approx((result.total_fat / result.final_weight) * 100)
    assert result.carbs_100g == pytest.approx((result.total_carbs / result.final_weight) * 100)
    assert result.kcal_100g == pytest.approx((result.total_kcal / result.final_weight) * 100)

def test_negative_weight_validation():
    with pytest.raises(ValidationError):
        Ingredient(name="Курица", weight_g=-5, protein=20, fat=5, carbs=0, kcal=125)

def test_empty_ingredients_validation():
    with pytest.raises(ValidationError):
        Recipe(recipe_name="Пустой", loss_coefficient=0.8, ingredients=[])

def test_invalid_loss_coefficient_validation():
    ingredients = [Ingredient(name="Курица", weight_g=200, protein=20, fat=5, carbs=0, kcal=125)]