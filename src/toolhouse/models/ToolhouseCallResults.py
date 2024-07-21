# This file was generated by liblab | https://liblab.com/

from __future__ import annotations
from .base import BaseModel
from typing import Union
from enum import Enum
from .AnthropicToolCallResults import AnthropicToolCallResults
from .OpenAiToolCallResults import OpenAiToolCallResults
from .OpenAiToolAssistantsCallResults import OpenAiToolAssistantsCallResults


def returnAnthropicToolCallResults(input_data):
    return AnthropicToolCallResults(**input_data)


def returnOpenAiToolCallResults(input_data):
    return OpenAiToolCallResults(**input_data)


def returnOpenAiToolAssistantsCallResults(input_data):
    return OpenAiToolAssistantsCallResults(**input_data)


class ContentGuard(BaseModel):
    required_lists = {
        "AnthropicToolCallResults": ["tool_use_id", "content", "type"],
        "OpenAiToolCallResults": ["role", "tool_call_id", "name", "content"],
        "OpenAiToolAssistantsCallResults": ["tool_call_id", "output"],
    }
    optional_lists = {
        "AnthropicToolCallResults": [],
        "OpenAiToolCallResults": [],
        "OpenAiToolAssistantsCallResults": [],
    }
    class_list = {
        "AnthropicToolCallResults": returnAnthropicToolCallResults,
        "OpenAiToolCallResults": returnOpenAiToolCallResults,
        "OpenAiToolAssistantsCallResults": returnOpenAiToolAssistantsCallResults,
    }

    @classmethod
    def return_one_of(cls, raw_input):
        return cls._one_of(
            cls.required_lists, cls.optional_lists, cls.class_list, raw_input
        )


Content = Union[
    AnthropicToolCallResults, OpenAiToolCallResults, OpenAiToolAssistantsCallResults
]


class Provider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OPENAI_ASSISTANTS = "openai_assistants"

    def list():
        return list(map(lambda x: x.value, Provider._member_map_.values()))


class ToolhouseCallResults(BaseModel):
    """
    Represents the results of a tool call for Toolhouse.
    """

    def __init__(self, content: Content, provider: Provider, **kwargs):
        """
        Initialize ToolhouseCallResults
        Parameters:
        ----------
            content: Content
            provider: str
        """
        self.content = content
        self.provider = self._enum_matching(provider, Provider.list(), "provider")
