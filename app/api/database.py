import time
import psycopg
from psycopg.rows import dict_row
from . import settings

def get_db_connection():
    return psycopg.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        dbname=settings.DB_NAME,
        row_factory=dict_row
    )

def init_db():
    for _ in range(10):
        try:
            conn = psycopg.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
                dbname="postgres",
                autocommit=True
            )
            with conn.cursor() as cur:
                cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{settings.DB_NAME}'")
                if not cur.fetchone():
                    cur.execute(f"CREATE DATABASE {settings.DB_NAME}")
            conn.close()
            break
        except Exception:
            time.sleep(1)

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id SERIAL PRIMARY KEY,
                recipe_name VARCHAR(255) NOT NULL,
                total_weight_raw DOUBLE PRECISION NOT NULL,
                final_weight DOUBLE PRECISION NOT NULL,
                total_protein DOUBLE PRECISION NOT NULL,
                total_fat DOUBLE PRECISION NOT NULL,
                total_carbs DOUBLE PRECISION NOT NULL,
                total_kcal DOUBLE PRECISION NOT NULL,
                protein_100g DOUBLE PRECISION NOT NULL,
                fat_100g DOUBLE PRECISION NOT NULL,
                carbs_100g DOUBLE PRECISION NOT NULL,
                kcal_100g DOUBLE PRECISION NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    conn.close()

def save_recipe_calculation(res):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO recipes (
                recipe_name, total_weight_raw, final_weight,
                total_protein, total_fat, total_carbs, total_kcal,
                protein_100g, fat_100g, carbs_100g, kcal_100g
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            res.recipe_name, res.total_weight_raw, res.final_weight,
            res.total_protein, res.total_fat, res.total_carbs, res.total_kcal,
            res.protein_100g, res.fat_100g, res.carbs_100g, res.kcal_100g
        ))
        row_id = cur.fetchone()["id"]
        conn.commit()
    conn.close()
    return row_id

def get_recipe_history():
    conn = get_db_connection()
    with conn.cursor() as cur: