from fastapi import FastAPI, HTTPException
from typing import List
from recipe_core.models import Recipe
from recipe_core.calculator import calculate_recipe
from recipe_core.exceptions import RecipeError
from . import database

app = FastAPI(title="Recipe KBZhU Calculator API")

@app.on_event("startup")
def startup_event():
    try:
        database.init_db()
    except Exception as e:
        print(f"Database initialization failed: {e}")

@app.get("/health")
def health_check():
    try:
        conn = database.get_db_connection()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": f"error: {str(e)}"}

@app.post("/calculate")
def calculate(recipe: Recipe):
    try:
        res = calculate_recipe(recipe)
        try:
            row_id = database.save_recipe_calculation(res)
            result_dict = res.to_dict()
            result_dict["id"] = row_id
            return result_dict
        except Exception as e:
            result_dict = res.to_dict()
            result_dict["id"] = None
            result_dict["warning"] = f"Failed to save in DB: {str(e)}"
            return result_dict
    except RecipeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/recipes")
def get_recipes():
    try:
        return database.get_recipe_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
