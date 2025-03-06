from .base import BaseModel
from enum import Enum


class Type(Enum):
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    OBJECT = "object"
    ARRAY = "array"
    BOOLEAN = "boolean"

    def list():
        """List of types"""
        return list(map(lambda x: x.value, Type._member_map_.values()))


class GenericArgument(BaseModel):
    """
    Generic Argument
    """

    def __init__(self, type: Type, required: bool, description: str, name: str, **kwargs):
        """
        Initialize GenericArgument
        Parameters:
        ----------
            type: str
            required: bool
            description: str
            name: str
        """
        self.type = self._enum_matching(type, Type.list(), "type")
        self.required = required
        self.description = description
        self.name = name
