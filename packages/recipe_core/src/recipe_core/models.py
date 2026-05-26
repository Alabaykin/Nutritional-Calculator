from pydantic import BaseModel, Field, field_validator
from typing import List

class Ingredient(BaseModel):
    name: str
    weight_g: float = Field(ge=0.0)
    protein: float = Field(ge=0.0)
    fat: float = Field(ge=0.0)
    carbs: float = Field(ge=0.0)
    kcal: float = Field(ge=0.0)

class Recipe(BaseModel):
    recipe_name: str
    loss_coefficient: float
    ingredients: List[Ingredient]
