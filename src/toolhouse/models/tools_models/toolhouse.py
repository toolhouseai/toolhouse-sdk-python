from typing import Literal, List
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl


ArgumentType = Literal["string", "number", "integer", "object", "array", "boolean"]
ArgumentFrom = Literal["llm", "user", "metadata"]
ToolType = Literal["local", "remote"]


class Argument(BaseModel):
    """Tool Arguments"""
    name: str
    type: ArgumentType
    source: ArgumentFrom
    label: str
    description: str
    required: bool


class ToolHouseTool(BaseModel):
    """ToolHouse Tools Configuration"""
    id: str
    publisher: str
    tool_type: ToolType = "remote"
    logo: str = Field(pattern=r'^data:image\/svg\+xml;base64,')
    title: str
    category: str
    short_description: str
    long_description: str
    price_per_execution: Decimal = Field(gt=0)
    star_rating: Decimal = Field(ge=0, le=5)
    executions: int
    url: HttpUrl
    description_for_model: str
    arguments: List[Argument]


class Tools(BaseModel):
    """ToolHouse"""
    tools: List[ToolHouseTool]
