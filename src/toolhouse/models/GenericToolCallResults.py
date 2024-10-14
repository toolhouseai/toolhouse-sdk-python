# This file was generated by liblab | https://liblab.com/

from .base import BaseModel


class GenericToolCallResults(BaseModel):
    """
    Represents the results of a tool call for Generic.
    """

    def __init__(self, content: str, **kwargs):
        """
        Initialize GenericToolCallResults
        Parameters:
        ----------
            content: str
        """
        self.content = content
