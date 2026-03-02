from src.db.main import get_session
from unittest.mock import Mock
from src import app
import pytest
from fastapi.testclient import TestClient
from src.auth.dependencies import RoleChecker,AccessTokenBearer,RefreshTokenBearer

mock_session=Mock()
mock_user_service=Mock()
mock_shoe_service=Mock()

def get_mock_session():
    yield mock_session

role_checker=RoleChecker(["admin"])
access_token_bearer=AccessTokenBearer()
refresh_token_bearer=RefreshTokenBearer()

app.dependency_overrides[get_session]=get_mock_session
app.dependency_overrides[role_checker]=Mock()
app.dependency_overrides[access_token_bearer]=Mock()
app.dependency_overrides[refresh_token_bearer]=Mock()

@pytest.fixture
def fake_session():
    return mock_session

@pytest.fixture
def fake_user_service():
    return mock_user_service

@pytest.fixture
def fake_shoe_service():
    return mock_shoe_service

@pytest.fixture
def test_client():
    return TestClient(app)

