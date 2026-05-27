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
    assert response.status_code == 200
    assert response.json()["status"] == "unhealthy"

@patch("app.api.database.save_recipe_calculation")
def test_calculate_endpoint_success(mock_save):
    mock_save.return_value = 42
    payload = {
        "recipe_name": "Тестовый рецепт",
        "loss_coefficient": 0.9,
        "ingredients": [
            {"name": "Сахар", "weight_g": 50, "protein": 0, "fat": 0, "carbs": 100, "kcal": 400}
        ]
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["recipe_name"] == "Тестовый рецепт"
    assert data["id"] == 42
    assert data["final_weight"] == 45.0
    assert data["total_kcal"] == 200.0

def test_calculate_endpoint_validation_error():
    payload = {
        "recipe_name": "Тестовый рецепт",
        "loss_coefficient": -0.5,
        "ingredients": []
    }
    response = client.post("/calculate", json=payload)