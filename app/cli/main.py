import json
import sys
import os
from recipe_core.models import Recipe, Ingredient
from recipe_core.calculator import calculate_recipe
from recipe_core.exceptions import RecipeError

def fix_windows_encoding():
    if sys.platform.startswith("win"):
        try:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
        except Exception:
            pass