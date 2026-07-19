import os
import sys
from unittest.mock import MagicMock, AsyncMock
import pytest

# Set environment variables before any imports
os.environ["API_KEY"] = "test-key"
os.environ["MONGO_URL"] = "mongodb://localhost:27017"
os.environ["OLLAMA_URL"] = "http://test"
os.environ["MODEL"] = "test-model"

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope="session", autouse=True)
def mock_db_client():
    """Mock the database client to avoid real MongoDB connection during tests."""
    with pytest.MonkeyPatch().context() as mp:
        # Mock the db.client to a MagicMock
        mock_client = MagicMock()
        # Mock the database and collection
        mock_db = MagicMock()
        mock_collection = AsyncMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_client.__getitem__.return_value = mock_db
        
        # Patch the global db.client
        import app.core.database as database_module
        mp.setattr(database_module.db, "client", mock_client)
        yield mock_client

@pytest.fixture(scope="session")
def test_app():
    """Create TestClient after mocks are in place."""
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)