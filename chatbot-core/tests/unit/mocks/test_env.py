"""Fixtures for unit tests."""

import pytest

@pytest.fixture
def mock_get_session(mocker):
    """Mock the memory.get_session function."""
    return mocker.patch("api.services.chat_service.get_session")

@pytest.fixture
def mock_retrieve_context(mocker):
    """Mock the retrieve_context function."""
    return mocker.patch("api.services.chat_service.retrieve_context")

@pytest.fixture
def mock_prompt_builder(mocker):
    """Mock the build_prompt function."""
    return mocker.patch("api.services.chat_service.build_prompt")

@pytest.fixture
def mock_llm_provider(mocker):
    """Mock the LLM provider generate function."""
    return mocker.patch("api.services.chat_service.llm_provider")
