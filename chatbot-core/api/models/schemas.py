"""
Schemas for the chatbot API.

This module defines the request and response data models exchanged between
clients and the chatbot API endpoints.
"""

from enum import Enum
from pydantic import BaseModel, field_validator


class ChatRequest(BaseModel):
    """
    Represents a user message submitted to the chatbot.

    Fields:
        message (str): The user's input message.

    Validation:
        - Rejects messages that are empty.
    """
    message: str

    @field_validator("message")
    def message_must_not_be_empty(cls, v): # pylint: disable=no-self-argument
        """Validator that checks that a message is not empty."""
        if not v.strip():
            raise ValueError("Message cannot be empty.")
        return v

class ChatResponse(BaseModel):
    """
    Represents the chatbot's reply.
    """
    reply: str

class SessionResponse(BaseModel):
    """
    Response model when a new chat session is created.
    """
    session_id: str

class DeleteResponse(BaseModel):
    """
    Response model when a session is successfully deleted.
    """
    message: str

class QueryType(Enum):
    """
    Enum that represents the possible query types:
        - MULTI  -> Represents a multi-question query.
        - SIMPLE -> Represents a single scope query.
    """
    MULTI = 'MULTI'
    SIMPLE = 'SIMPLE'

def is_valid_query_type(input_str: str) -> bool:
    """
    Check if the given string is a valid member of the QueryType enum.

    Args:
        input_str (str): The string to validate.

    Returns:
        bool: True if the string is a valid QueryType member, False otherwise.
    """
    return input_str in QueryType.__members__

def str_to_query_type(input_str: str) -> QueryType:
    """
    Convert a string to its corresponding QueryType enum member.

    Args:
        input_str (str): The string representation of a QueryType.

    Returns:
        QueryType: The corresponding enum member.

    Raises:
        ValueError: If the input string is not a valid QueryType.
    """
    try:
        return QueryType[input_str]
    except KeyError as e:
        raise ValueError(f"Invalid query type: {input_str}") from e
