import pytest
import os
from unittest.mock import MagicMock, AsyncMock, patch

# Set environment variables BEFORE importing the app
os.environ["API_KEY"] = "test-key"
os.environ["MONGO_URL"] = "mongodb://localhost:27017"
os.environ["OLLAMA_URL"] = "http://test"
os.environ["MODEL"] = "test-model"
# Use the test_app fixture provided by conftest
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from fastapi import HTTPException
# Import the app after env is set
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_unauthorized_access():
    # TestClient raises HTTPException for 403 responses
    with pytest.raises(Exception) as exc_info:
        client.get("/server/")
    # Verify the exception is our 403 error
    assert "403" in str(exc_info.value) or "Invalid or missing API key" in str(exc_info.value)
def test_authorized_get_server_info():
    # Mock the service method to return a predictable list
    mock_data = [{"id": "s1", "status": "online", "note": "test"}]
    # Patch the method on the service class
    with patch("app.services.server_service.ServerService.get_all_server_info", 
                return_value=mock_data):
        headers = {"X-API-KEY": "test-key"}
        response = client.get("/server/", headers=headers)
        assert response.status_code == 200
        assert response.json() == mock_data
def test_authorized_post_server_info():
    mock_return_id = "mocked-id-123"
    with patch("app.services.server_service.ServerService.add_server_info", 
                return_value=mock_return_id):
        payload = {"id": "new-server", "status": "offline", "note": "test note"}
        headers = {"X-API-KEY": "test-key"}
        response = client.post("/server/", json=payload, headers=headers)
        assert response.status_code == 200
        # add_server_info returns a string ID, so response is that string
        assert response.json() == mock_return_id
def test_chat_endpoint_requires_auth():
    # Mock the service method for chat (if we had one). Currently chat uses process_chat from service.
    # We'll mock the chat_service.process_chat function.
    mock_response = "Mocked AI response"
    with patch("app.clients.ollama_client.OllamaClient.generate",
                return_value=mock_response):
        payload = {"message": "Hello AI"}
        headers = {"X-API-KEY": "test-key"}
        response = client.post("/chat", json=payload, headers=headers)
        assert response.status_code == 200
        assert response.json() == {"response": mock_response}

