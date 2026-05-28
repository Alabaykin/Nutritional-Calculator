# 🍳 recipe-core

[![PyPI version](https://img.shields.io/badge/pypi-0.1.0-blue.svg)](https://pypi.org/project/recipe-core/)
[![Python versions](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

**recipe-core** — это легковесная, строго типизированная Python-библиотека для моделирования рецептов кулинарных блюд и точного расчета их итоговой пищевой и энергетической ценности (КБЖУ). 

Библиотека реализует независимый доменный слой по принципам Чистой Архитектуры, используя **Pydantic v2** для строгой валидации входящих данных на лету.

---

## ✨ Ключевые возможности

*   **🛡️ Валидация данных**: Автоматическая защита от создания ингредиентов с отрицательным весом или рецептов с некорректными коэффициентами уварки.
*   **📐 Точный расчет пищевой ценности**: Алгоритм учитывает общую массу сырого набора продуктов и коэффициент потери веса при термической обработке (ужарка/уварка/выпекание).
*   **📦 Zero-Dependency в runtime**: Зависит только от `pydantic`. Ничего лишнего!
*   **💻 100% Type-Safe**: Полная поддержка аннотаций типов для безупречной работы автодополнения в VS Code, PyCharm и других IDE.

---

## 🚀 Установка

Установите библиотеку из репозитория PyPI:
```bash
pip install recipe-core
```

---

## 📖 Быстрый старт и пример использования

Библиотека предоставляет три основных компонента: модель `Ingredient`, модель `Recipe` и функцию `calculate_recipe`.

Вот простой скрипт, показывающий полный цикл работы с библиотекой:

```python
import pytest
from recipe_core.models import Recipe, Ingredient
from recipe_core.calculator import calculate_recipe
from recipe_core.exceptions import NegativeWeightError, EmptyRecipeError

# 1. Создаем сырые ингредиенты
chicken = Ingredient(
    name="Куриное филе",
    weight_g=200.0,
    protein=23.6,
    fat=1.9,
    carbs=0.4,
    kcal=113.0
)

buckwheat = Ingredient(
    name="Гречневая крупа",
    weight_g=100.0,
    protein=12.6,
    fat=3.3,
    carbs=62.1,
    kcal=313.0
)

# 2. Собираем рецепт с коэффициентом ужарки/уварки (0.8 означает потерю 20% веса при готовке)
recipe = Recipe(
    recipe_name="Гречка с курицей",
    loss_coefficient=0.8,
    ingredients=[chicken, buckwheat]
)

# 3. Выполняем расчет пищевой ценности готового блюда
result = calculate_recipe(recipe)

# 4. Получаем результаты
print(f"Блюдо: {result.recipe_name}")
print(f"Вес сырых продуктов: {result.total_weight_raw} г")
print(f"Итоговый вес блюда: {result.final_weight} г")
print(f"Энергетическая ценность готового блюда на 100г: {result.kcal_100g:.1f} ккал")
print(f"БЖУ на 100г: Б={result.protein_100g:.1f}г, Ж={result.fat_100g:.1f}г, У={result.carbs_100g:.1f}г")
```

---

## 🛡️ Обработка ошибок

В библиотеке реализованы кастомные доменные исключения для контроля логики:

```python
from recipe_core.models import Recipe, Ingredient
from recipe_core.calculator import calculate_recipe
from recipe_core.exceptions import NegativeWeightError

# Попытка передать некорректные данные в обход стандартных конструкторов:
bad_ingredient = Ingredient.model_construct(
    name="Невалидный продукт",
    weight_g=-100.0,  # Отрицательный вес!
    protein=10.0, fat=2.0, carbs=0.0, kcal=58.0
)

recipe = Recipe.model_construct(
    recipe_name="Плохой рецепт",
    loss_coefficient=1.0,
    ingredients=[bad_ingredient]
)

try:
    calculate_recipe(recipe)
except NegativeWeightError as e:
    print(f"Ошибка расчета! {e}")
```

---

## 📄 Лицензия

Этот проект распространяется под свободной лицензией **MIT License**. Вы можете использовать его в своих коммерческих и некоммерческих целях.
