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
    pass
