"""conftest for unit tests."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routes.chatbot import router

pytest_plugins = ["tests.unit.mocks.test_env"]

@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
def client(app: FastAPI):
    return TestClient(app)
