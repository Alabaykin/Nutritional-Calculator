import pytest
from pydantic import ValidationError
from recipe_core.models import Recipe, Ingredient
from recipe_core.exceptions import NegativeWeightError, EmptyRecipeError
from recipe_core.calculator import calculate_recipe

def test_calculate_recipe_success():
    chicken = Ingredient(
        name="Куриное филе",
        weight_g=200.0,
        protein=23.6,
        fat=1.9,
        carbs=0.4,
        kcal=113.0
    )
    buckwheat = Ingredient(
        name="Гречка",
        weight_g=100.0,
        protein=12.6,
        fat=3.3,
        carbs=62.1,
        kcal=313.0
    )
    recipe = Recipe(
        recipe_name="Тестовый рецепт",
        loss_coefficient=0.8,
        ingredients=[chicken, buckwheat]
    )
    
    result = calculate_recipe(recipe)
    
    assert result.recipe_name == "Тестовый рецепт"
    assert result.total_weight_raw == 300.0
    assert result.final_weight == 240.0
    
    assert pytest.approx(result.total_protein) == 59.8
    assert pytest.approx(result.total_fat) == 7.1
    assert pytest.approx(result.total_carbs) == 62.9
    assert pytest.approx(result.total_kcal) == 539.0
    
    assert pytest.approx(result.kcal_100g, 0.1) == 224.6
    assert pytest.approx(result.protein_100g, 0.1) == 24.9

def test_calculate_recipe_empty_ingredients():
    # Используем model_construct(), чтобы обойти Pydantic-валидацию на пустой список
    # и протестировать доменное исключение EmptyRecipeError бизнес-логики
    recipe = Recipe.model_construct(
        recipe_name="Пустой рецепт",
        loss_coefficient=1.0,
        ingredients=[]
    )
    with pytest.raises(EmptyRecipeError) as exc_info:
        calculate_recipe(recipe)
    assert "должен содержать ингредиенты" in str(exc_info.value)

def test_calculate_recipe_negative_weight():
    # Используем model_construct(), чтобы обойти Pydantic-валидацию отрицательного веса
    # и протестировать доменное исключение NegativeWeightError бизнес-логики
    bad_ingredient = Ingredient.model_construct(
        name="Вредный ингредиент",
        weight_g=-50.0,
        protein=10.0,
        fat=5.0,
        carbs=1.0,
        kcal=100.0
    )
    recipe = Recipe.model_construct(
        recipe_name="Плохой рецепт",
        loss_coefficient=1.0,
        ingredients=[bad_ingredient]
    )
    with pytest.raises(NegativeWeightError) as exc_info:
        calculate_recipe(recipe)
    assert "Вес не может быть отрицательным" in str(exc_info.value)

def test_recipe_pydantic_validation_zero_loss():
    chicken = Ingredient(
        name="Курица",
        weight_g=100.0,
        protein=20.0,
        fat=2.0,
        carbs=0.0,
        kcal=110.0
    )
    with pytest.raises(ValidationError) as exc_info:
        Recipe(
            recipe_name="Плохой рецепт",
            loss_coefficient=0.0,
            ingredients=[chicken]
        )
    assert "loss_coefficient" in str(exc_info.value)

def test_zero_weight_ingredients():
    # Проверка граничного случая с нулевым весом ингредиентов
    ingredients = [Ingredient(name="Вода", weight_g=0.0, protein=0, fat=0, carbs=0, kcal=0)]
    recipe = Recipe(recipe_name="Пустая вода", loss_coefficient=0.8, ingredients=ingredients)
    result = calculate_recipe(recipe)
    assert result.final_weight == 0.0
    assert result.protein_100g == 0.0
    assert result.fat_100g == 0.0
    assert result.carbs_100g == 0.0
    assert result.kcal_100g == 0.0
