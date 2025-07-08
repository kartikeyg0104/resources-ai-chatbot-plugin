"""Fixtures for integration tests."""

import pytest
from fastapi import FastAPI
from api.routes.chatbot import router

@pytest.fixture
def fastapi_app() -> FastAPI:
    """Fixture to create FastAPI app instance with routes."""
    app = FastAPI()
    app.include_router(router)
    return app
