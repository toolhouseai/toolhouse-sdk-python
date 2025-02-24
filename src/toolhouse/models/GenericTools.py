from __future__ import annotations
from .base import BaseModel
from typing import List
from toolhouse.models.GenericArgument import GenericArgument


class GenericTools(BaseModel):
    """
    Generic Tools
    """

    def __init__(
        self,
        description: str,
        name: str,
        title: str,
        arguments: List[GenericArgument],
        **kwargs,
    ):
        """
        Initialize AntropicTools
        Parameters:
        ----------
            description: str
            name: str
            title: str
            arguments: List[GenericArguments]
        """
        self.description = description
        self.name = name
        self.title = title
        self.arguments = arguments