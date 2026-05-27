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
