import pytest
from unittest.mock import patch, MagicMock
from app.api.database import get_db_connection

@patch("app.api.database.psycopg.connect")
def test_get_db_connection(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    
    conn = get_db_connection()
    
    assert conn == mock_conn
    mock_connect.assert_called_once()
    kwargs = mock_connect.call_args[1]
    assert "row_factory" in kwargs
