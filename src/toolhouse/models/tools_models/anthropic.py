from typing import Literal, List, Dict
from pydantic import BaseModel


ArgumentType = Literal["string", "number", "integer", "object", "array", "boolean"]


class Property(BaseModel):
    """Tool Property"""
    type: ArgumentType
    description: str


class InputSchema(BaseModel):
    """InputSchema"""
    type: Literal['object']
    properties: Dict[str, Property]
    required: List[str]


class Tool(BaseModel):
    """Anthropic Tools"""
    name: str
    description: str
    input_schema: InputSchema


class Tools(BaseModel):
    """ToolHouse"""
    tools: List[Tool]
