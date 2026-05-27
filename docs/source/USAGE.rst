Usage Examples
==============

Here is how you can use the core library:

.. code-block:: python

   from recipe_core.models import Recipe, Ingredient
   from recipe_core.calculator import calculate_recipe

   ingredient = Ingredient(name="Курица", weight_g=200, protein=20.0, fat=5.0, carbs=0.0, kcal=125.0)
   recipe = Recipe(recipe_name="Грудка", loss_coefficient=0.8, ingredients=[ingredient])
   result = calculate_recipe(recipe)
   print(result.final_weight)
