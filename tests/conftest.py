"""
Pytest configuration for the To-Do List App test suite.

Fixtures
--------
client
    A FastAPI TestClient wired to the app.
    Storage is reset before EVERY test to guarantee isolation.
"""

import pytest
from fastapi.testclient import TestClient

import todo_app.storage as storage
from todo_app.main import app


@pytest.fixture(autouse=True)
def reset_storage():
    """Reset in-memory storage before each test. Runs automatically."""
    storage.reset()
    yield
    # Post-test cleanup (optional — pre-test reset is sufficient)
    storage.reset()


@pytest.fixture
def client() -> TestClient:
    """Return a TestClient for the To-Do app."""
    return TestClient(app)
