from typing import Literal, List, Dict
from pydantic import BaseModel


ArgumentType = Literal["string", "number", "integer", "object", "array", "boolean"]


class Property(BaseModel):
    """Tool Property"""
    type: ArgumentType
    description: str


class Paramenters(BaseModel):
    """Parameters"""
    type: Literal["object"]
    properties: Dict[str, Property]


class Function(BaseModel):
    """InputSchema"""
    name: str
    description: str
    parameters: Paramenters
    required: List[str]


class Tool(BaseModel):
    """OpenAI Tools"""
    type: Literal["function"]
    function: Function


class Tools(BaseModel):
    """ToolHouse"""
    tools: List[Tool]
