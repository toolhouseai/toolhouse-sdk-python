# This file was generated by liblab | https://liblab.com/

from .base import BaseModel
from enum import Enum


class Role(Enum):
    TOOL = "tool"

    def list():
        return list(map(lambda x: x.value, Role._member_map_.values()))


class OpenAiToolCallResults(BaseModel):
    """
    Represents the results of a tool call for OpenAI.
    """

    def __init__(
        self, content: str, name: str, tool_call_id: str, role: Role, **kwargs
    ):
        """
        Initialize OpenAiToolCallResults
        Parameters:
        ----------
            content: str
            name: str
            tool_call_id: str
            role: str
        """
        self.content = content
        self.name = name
        self.tool_call_id = tool_call_id
        self.role = self._enum_matching(role, Role.list(), "role")
