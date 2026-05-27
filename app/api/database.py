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