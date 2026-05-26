class RecipeError(Exception):
    """Base exception for recipe core."""
    pass

class NegativeWeightError(RecipeError):
    """Raised when an ingredient weight is negative."""
    pass

class EmptyRecipeError(RecipeError):
    """Raised when a recipe contains no ingredients."""
    pass
