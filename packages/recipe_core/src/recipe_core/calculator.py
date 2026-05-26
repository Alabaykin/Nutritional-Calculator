from typing import Dict, Any
from .models import Recipe, Ingredient
from .exceptions import NegativeWeightError, EmptyRecipeError

class RecipeCalculationResult:
    def __init__(self, recipe_name: str, total_weight_raw: float, final_weight: float,
                 total_protein: float, total_fat: float, total_carbs: float, total_kcal: float,
                 protein_100g: float, fat_100g: float, carbs_100g: float, kcal_100g: float):
        self.recipe_name = recipe_name
        self.total_weight_raw = total_weight_raw
        self.final_weight = final_weight
        self.total_protein = total_protein
        self.total_fat = total_fat
        self.total_carbs = total_carbs
        self.total_kcal = total_kcal
        self.protein_100g = protein_100g
        self.fat_100g = fat_100g
        self.carbs_100g = carbs_100g
        self.kcal_100g = kcal_100g

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recipe_name": self.recipe_name,
            "total_weight_raw": self.total_weight_raw,
            "final_weight": self.final_weight,
            "total_protein": self.total_protein,
            "total_fat": self.total_fat,
            "total_carbs": self.total_carbs,
            "total_kcal": self.total_kcal,
            "protein_100g": self.protein_100g,
            "fat_100g": self.fat_100g,
            "carbs_100g": self.carbs_100g,
            "kcal_100g": self.kcal_100g
        }

def calculate_recipe(recipe: Recipe) -> RecipeCalculationResult:
    if not recipe.ingredients:
        raise EmptyRecipeError("Рецепт должен содержать ингредиенты")
    
    total_weight_raw = 0.0
    total_protein = 0.0
    total_fat = 0.0
    total_carbs = 0.0
    total_kcal = 0.0
    
    for i in recipe.ingredients:
        if i.weight_g < 0:
            raise NegativeWeightError("Вес не может быть отрицательным")
        total_weight_raw += i.weight_g
        total_protein += (i.protein * i.weight_g) / 100.0
        total_fat += (i.fat * i.weight_g) / 100.0
        total_carbs += (i.carbs * i.weight_g) / 100.0
        total_kcal += (i.kcal * i.weight_g) / 100.0
        
    final_weight = total_weight_raw * recipe.loss_coefficient
    
    if final_weight > 0:
        protein_100g = (total_protein / final_weight) * 100.0
        fat_100g = (total_fat / final_weight) * 100.0
        carbs_100g = (total_carbs / final_weight) * 100.0
        kcal_100g = (total_kcal / final_weight) * 100.0
    else:
        protein_100g = fat_100g = carbs_100g = kcal_100g = 0.0
        
    return RecipeCalculationResult(
        recipe_name=recipe.recipe_name,
        total_weight_raw=total_weight_raw,
        final_weight=final_weight,
        total_protein=total_protein,
        total_fat=total_fat,
        total_carbs=total_carbs,
        total_kcal=total_kcal,
        protein_100g=protein_100g,
        fat_100g=fat_100g,
        carbs_100g=carbs_100g,
        kcal_100g=kcal_100g
    )
