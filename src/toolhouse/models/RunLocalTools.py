from typing import Literal
from pydantic import BaseModel


class AnthropicToolResponse(BaseModel):
    """Represents the results of a tool call for Anthropic."""

    tool_use_id: str
    """The ID of the tool call."""

    content: str
    """Result of the tool call."""

    type: Literal["tool_result"]
    """The type of tool call the output is required for."""


class OpenAIToolResponse(BaseModel):
    """Represents the results of a tool call for OpenAI."""

    role: Literal['tool']

    tool_call_id: str
    """The ID of the tool call."""

    name: str
    """tool_function_name"""

    content: str
    """Result of the tool call."""
