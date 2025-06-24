"""Unit tests for chat service logic."""

from api.services.chat_service import get_chatbot_reply
from api.models.schemas import ChatResponse

def test_get_chatbot_reply_success(
    mock_get_session,
    mock_retrieve_context,
    mock_prompt_builder,
    mock_llm_provider,
    mocker
):
    """Test response of get_chatbot_reply for a valid chat session."""
    mock_chat_memory = mocker.MagicMock()
    mock_session = mock_get_session.return_value
    mock_session.chat_memory = mock_chat_memory

    mock_retrieve_context.return_value = "Context to answer"
    mock_prompt_builder.return_value = "Built prompt"
    mock_llm_provider.generate.return_value = "LLM answers to the query"

    response = get_chatbot_reply("session-id", "Query for the LLM")

    assert isinstance(response, ChatResponse)
    assert response.reply == "LLM answers to the query"
    mock_chat_memory.add_user_message.assert_called_once_with("Query for the LLM")
    mock_chat_memory.add_ai_message.assert_called_once_with("LLM answers to the query")
