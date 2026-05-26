from .models import Recipe
from pydantic import BaseModel

class RecipeCalculationResult(BaseModel):
    recipe_name: str
    total_weight_raw: float
    final_weight: float
    total_protein: float
    total_fat: float
    total_carbs: float
    total_kcal: float
    protein_100g: float
    fat_100g: float
    carbs_100g: float
    kcal_100g: float

def calculate_recipe(recipe: Recipe) -> RecipeCalculationResult:
    total_weight_raw = sum(i.weight_g for i in recipe.ingredients)
    from .exceptions import EmptyRecipeError, NegativeWeightError
    if not recipe.ingredients:
        raise EmptyRecipeError('Рецепт должен содержать ингредиенты')
    for i in recipe.ingredients:
        if i.weight_g < 0:
            raise NegativeWeightError('Вес не может быть отрицательным')
    
    final_weight = total_weight_raw * recipe.loss_coefficient
    total_protein = sum(i.protein * i.weight_g / 100.0 for i in recipe.ingredients)
    total_fat = sum(i.fat * i.weight_g / 100.0 for i in recipe.ingredients)
    total_carbs = sum(i.carbs * i.weight_g / 100.0 for i in recipe.ingredients)
    total_kcal = sum(i.kcal * i.weight_g / 100.0 for i in recipe.ingredients)
    pass
