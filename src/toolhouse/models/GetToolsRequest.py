# This file was generated by liblab | https://liblab.com/

from __future__ import annotations
from typing import Any
from .base import BaseModel
from .Provider import Provider


class GetToolsRequest(BaseModel):
    """
    Represents a tool call for Toolhouse.
    """

    def __init__(self, provider: Provider, metadata: Any, bundle: str):
        """
        Initialize RunToolsRequest
        Parameters:
        ----------
            provider: str
            metadata
            bundle: str
        """
        self.provider = self._enum_matching(provider, Provider.list(), "provider")
        self.metadata = metadata
        self.bundle = bundle
