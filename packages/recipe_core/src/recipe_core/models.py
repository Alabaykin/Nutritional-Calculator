from pydantic import BaseModel, Field, field_validator
from typing import List

class Ingredient(BaseModel):
    name: str = Field(min_length=1)
    weight_g: float = Field(ge=0.0)
    protein: float = Field(ge=0.0)
    fat: float = Field(ge=0.0)
    carbs: float = Field(ge=0.0)
    kcal: float = Field(ge=0.0)

class Recipe(BaseModel):
    recipe_name: str = Field(min_length=1)
    loss_coefficient: float = Field(gt=0.0, le=1.0)
    ingredients: List[Ingredient]

    @field_validator('ingredients')
    @classmethod
    def check_ingredients_not_empty(cls, v):
        if not v:
            raise ValueError('Recipe must contain ingredients')
        return v
