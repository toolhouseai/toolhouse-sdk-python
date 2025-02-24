from typing import Dict, List, Literal, Type, TypedDict, Union, cast

from llama_index.core.tools import FunctionTool
from pydantic import create_model
from pydantic.fields import FieldInfo

from toolhouse.models.GenericToolCall import GenericToolCall
from toolhouse.models.GenericTools import GenericTools
from toolhouse.models.GetToolsRequest import GetToolsRequest
from toolhouse.models.Provider import Provider
from toolhouse.models.RunToolsRequest import RunToolsRequest
from toolhouse.services.tools import Tools

ArrayFieldType = Union[
    Type[List[str]],
    Type[List[float]],
    Type[List[bool]],
    Type[List[int]],
]


class ListItems(TypedDict):
    """ListItems"""

    type: Literal["string", "number", "boolean"]


class LlamaIndex:
    """LlamaIndex"""

    def __init__(self, service: Tools):
        self.service = service

    def get_tools(self, tools: List[GenericTools], request: GetToolsRequest) -> List[FunctionTool]:
        """Get all tools from Toolhouse"""
        llama_tools = []
        for tool in tools:
            llama_tool = self.generate_tool(tool, request)
            llama_tools.append(llama_tool)
        return llama_tools

    def generate_tool(self, tool, request):
        """Generate a tool for LlamaIndex"""
        arguments = tool["arguments"]
        schema = self._generate_tool_schema(arguments)
        model = self._create_model(tool["name"], schema)
        return FunctionTool.from_defaults(
            fn=self._generate_function(tool["name"], request),
            name=tool["name"],
            description=tool["description"],
            return_direct=True,
            fn_schema=model,
        )

    def _generate_function(self, tool_name: str, request: GetToolsRequest):
        def wrapper(*args, **kwargs):
            tool = GenericToolCall(kwargs, tool_name)
            run_tools_request = RunToolsRequest(tool, Provider.LLAMAINDEX, request.metadata, request.bundle)
            run_response = self.service.run_tools(run_tools_request)
            return run_response.content

        return wrapper

    def _generate_tool_schema(self, args: List[Dict]):
        """Generate a tool schema for a given list of arguments"""
        field_definitions = {}

        for argument in args:
            field_type = self._resolve_field_type(argument)
            field_info = self._create_field_info(argument)
            field_definitions[argument["name"]] = (field_type, field_info)

        return field_definitions

    def _resolve_field_type(self, argument: Dict):
        """Resolve the field type based on the argument definition"""
        if self._is_array_type(argument):
            return self._get_array_field_type(argument["items"])
        return self._get_basic_field_type(argument["type"])

    def _is_array_type(self, argument: Dict) -> bool:
        """Check if the argument is an array type with items definition"""
        return argument["type"].lower() == "array" and "items" in argument

    def _get_array_field_type(self, items: ListItems) -> ArrayFieldType:
        """Get the field type for array items"""
        type_mapping = {
            "string": List[str],
            "number": List[float],
            "boolean": List[bool],
            "integer": List[int],
        }

        return cast(ArrayFieldType, type_mapping.get(items["type"].lower(), List[str]))

    def _get_basic_field_type(self, type_str: str):
        """Convert basic string type to actual type"""
        type_mapping = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        return type_mapping.get(type_str.lower(), str)

    def _create_field_info(self, argument: Dict) -> FieldInfo:
        """Create a FieldInfo instance based on argument definition"""
        if argument["required"]:
            return FieldInfo(description=argument["description"])
        return FieldInfo(description=argument["description"], default=None)

    def _create_model(self, name: str, schema: dict):
        return create_model(name, **schema)
