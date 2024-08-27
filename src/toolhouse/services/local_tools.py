from typing import Union, List
from functools import wraps
import json
from anthropic.types import ToolUseBlock
from openai.types.chat import ChatCompletionMessageToolCall
from groq.types.chat import ChatCompletionMessageToolCall as GroqChatCompletionMessageToolCall
from ..models.RunLocalTools import AnthropicToolResponse, OpenAIToolResponse

SupportedTools = Union[
    ChatCompletionMessageToolCall,
    GroqChatCompletionMessageToolCall,
    ToolUseBlock]


class LocalTools():
    """Local Runner"""
    def __init__(self):
        self.local_tools = {}

    def get_registered_tools(self) -> List[str]:
        """Get List of registered tools"""
        return self.local_tools.keys()

    def register_local_tool(self, local_tool):
        """Register a new local tool runner"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not isinstance(result, str):
                    raise TypeError(
                        f"The function '{local_tool}' did not return a string. Returned type: {type(result).__name__}"
                        )
                return result
            # Add the function to the routes dictionary with the given name
            self.local_tools[local_tool] = wrapper
            return wrapper
        return decorator

    def _run_local_tools(self, local_tool, *args, **kwargs) -> str:
        """execute tool"""
        if local_tool in self.local_tools:
            return self.local_tools[local_tool](*args, **kwargs)
        else:
            raise ValueError(
                f"The LLM attempted to call a tool named {local_tool}, but there wasn't a registered local tool to respond to it."
                f"Make sure that you have a function that can handle this tool and decorate it with @register_local_tool(\"{local_tool}\")."
            )

    def run_tools(self, tool: SupportedTools) -> Union[AnthropicToolResponse, OpenAIToolResponse]:
        """_summary_

        Args:
            provider (Provider): _description_
            tool (_type_): _description_

        Returns:
            str: _description_
        """
        if isinstance(tool, ToolUseBlock):
            tool_input = tool.input if isinstance(tool.input, dict) else {}
            content = self._run_local_tools(local_tool=tool.name, **tool_input)
            return AnthropicToolResponse(type="tool_result", content=content, tool_use_id=tool.id)
        elif isinstance(tool, ChatCompletionMessageToolCall) or isinstance(tool, GroqChatCompletionMessageToolCall):
            content = self._run_local_tools(tool.function.name, **json.loads(tool.function.arguments))
            return OpenAIToolResponse(tool_call_id=tool.id, name=tool.function.name, content=content, role="tool")
        else:
            raise ValueError("Provider not suppoted")
