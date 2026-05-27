import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

@patch("app.api.database.get_db_connection")
def test_health_endpoint_success(mock_get_conn):
    mock_conn = MagicMock()
    mock_get_conn.return_value = mock_conn
    
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"}

@patch("app.api.database.get_db_connection")
def test_health_endpoint_failure(mock_get_conn):
    mock_get_conn.side_effect = Exception("DB Connection Refused")
    
    response = client.get("/health")