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