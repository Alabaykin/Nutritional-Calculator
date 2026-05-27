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