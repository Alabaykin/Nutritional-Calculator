import pytest
from unittest.mock import patch, MagicMock, call
from app.api.database import get_db_connection, init_db

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

