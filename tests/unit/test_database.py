import pytest
from unittest.mock import patch, MagicMock, call
from app.api.database import get_db_connection, init_db, save_recipe_calculation, get_recipe_history
from recipe_core.calculator import RecipeCalculationResult

@patch("app.api.database.psycopg.connect")
def test_get_db_connection(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    
    conn = get_db_connection()
    
    assert conn == mock_conn
    mock_connect.assert_called_once()
    kwargs = mock_connect.call_args[1]
    assert "row_factory" in kwargs

@patch("app.api.database.time.sleep")
@patch("app.api.database.get_db_connection")
@patch("app.api.database.psycopg.connect")
def test_init_db_success(mock_connect, mock_get_db_conn, mock_sleep):
    mock_conn_postgres = MagicMock()
    mock_cursor_postgres = MagicMock()
    mock_cursor_postgres.fetchone.return_value = None
    mock_conn_postgres.cursor.return_value.__enter__.return_value = mock_cursor_postgres
    mock_connect.return_value = mock_conn_postgres
    
    mock_conn_recipe = MagicMock()
    mock_cursor_recipe = MagicMock()
    mock_conn_recipe.cursor.return_value.__enter__.return_value = mock_cursor_recipe
    mock_get_db_conn.return_value = mock_conn_recipe
    
    init_db()
    
    mock_cursor_postgres.execute.assert_has_calls([
        call("SELECT 1 FROM pg_database WHERE datname = 'recipe_db'"),
        call("CREATE DATABASE recipe_db")
    ])
    
    assert mock_cursor_recipe.execute.call_count == 1
    assert "CREATE TABLE IF NOT EXISTS recipes" in mock_cursor_recipe.execute.call_args[0][0]
    mock_conn_recipe.commit.assert_called_once()

@patch("app.api.database.time.sleep")
@patch("app.api.database.get_db_connection")
@patch("app.api.database.psycopg.connect")
def test_init_db_retry_then_success(mock_connect, mock_get_db_conn, mock_sleep):
    mock_conn_postgres = MagicMock()
    mock_cursor_postgres = MagicMock()
    mock_cursor_postgres.fetchone.return_value = True
    mock_conn_postgres.cursor.return_value.__enter__.return_value = mock_cursor_postgres
    
    mock_connect.side_effect = [
        Exception("Postgres starting..."),
        Exception("Postgres starting..."),
        mock_conn_postgres
    ]
    
    mock_conn_recipe = MagicMock()
    mock_cursor_recipe = MagicMock()
    mock_conn_recipe.cursor.return_value.__enter__.return_value = mock_cursor_recipe
    mock_get_db_conn.return_value = mock_conn_recipe
    
    init_db()
    
    assert mock_sleep.call_count == 2
    assert mock_connect.call_count == 3
    mock_conn_recipe.commit.assert_called_once()

@patch("app.api.database.get_db_connection")
def test_save_recipe_calculation(mock_get_db_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {"id": 99}
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_conn.return_value = mock_conn
    
    res = RecipeCalculationResult(
        recipe_name="Салат",
        total_weight_raw=100.0,
        final_weight=90.0,
        total_protein=1.0,
        total_fat=2.0,
        total_carbs=3.0,
        total_kcal=34.0,
        protein_100g=1.1,
        fat_100g=2.2,
        carbs_100g=3.3,
        kcal_100g=37.7
    )
    
    row_id = save_recipe_calculation(res)
    
    assert row_id == 99
    assert mock_cursor.execute.call_count == 1
    assert "INSERT INTO recipes" in mock_cursor.execute.call_args[0][0]
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

@patch("app.api.database.get_db_connection")
def test_get_recipe_history(mock_get_db_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{"id": 1, "recipe_name": "Суп"}]
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_conn.return_value = mock_conn
    
    history = get_recipe_history()
    
    assert history == [{"id": 1, "recipe_name": "Суп"}]
    mock_cursor.execute.assert_called_once_with("SELECT * FROM recipes ORDER BY id DESC")
    mock_conn.close.assert_called_once()


