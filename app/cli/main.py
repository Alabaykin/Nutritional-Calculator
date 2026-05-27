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

def main():
    fix_windows_encoding()

    if len(sys.argv) < 2:
        print("Ошибка: укажите путь к файлу рецепта.")
        print("Использование: python -m app.cli.main <recipe.json>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Ошибка: Файл {file_path} не найден.")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON.")
        sys.exit(1)

    try:
        recipe = Recipe(**data)
    except Exception as e:
        print(f"Ошибка валидации данных рецепта: {e}")
        sys.exit(1)

    try:
        res = calculate_recipe(recipe)
    except RecipeError as e:
        print(f"Ошибка расчета: {e}")
        sys.exit(1)

    print(f"Рецепт: {res.recipe_name}")
    print(f"Сырой вес: {res.total_weight_raw:.1f}г -> Вес готового блюда: {res.final_weight:.1f}г")
    print("-" * 30)
    print("Итого КБЖУ на все блюдо:")
    print(f"Калории: {res.total_kcal:.1f} ккал")