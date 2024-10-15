from typing import List
from pydantic import create_model
from pydantic.fields import FieldInfo
from llama_index.core.tools import FunctionTool
from toolhouse.services.tools import Tools
from toolhouse.models.GenericTools import GenericTools, GenericArgument
from toolhouse.models.RunToolsRequest import RunToolsRequest
from toolhouse.models.GenericToolCall import GenericToolCall, Input
from toolhouse.models.Provider import Provider
from toolhouse.models.GetToolsRequest import GetToolsRequest


class LlamaIndex():
    """LlamaIndex"""
    def __init__(self, service: Tools):
        self.service = service

    def get_tools(self, tools: List[GenericTools], request: GetToolsRequest) -> List[FunctionTool]:
        """Get all tools from Toolhouse"""
        llama_tools = []
        for tool in tools:
            llama_tool = self.generate_tool(self.service, tool, request)
            llama_tools.append(llama_tool)
        return llama_tools

    def generate_tool(self, service: Tools, tool: GenericTools, request: GetToolsRequest):
        """Generate a tool for LlamaIndex"""
        arguments = tool["arguments"]
        schema = self._generate_tool_schema(arguments)
        model = self._create_model(tool["name"], schema)
        return FunctionTool.from_defaults(
            fn=self._generate_function(service, tool["name"], request, arguments),
            name=tool["name"],
            description=tool["description"],
            return_direct=True,
            fn_schema=model
        )

    def _generate_function(self, service: Tools, tool_name: str, request: GetToolsRequest, arguments: List[GenericArgument]):
        def wrapper(*args, **kwargs):
            tool = GenericToolCall(kwargs, tool_name)
            run_tools_request = RunToolsRequest(tool, Provider.LLAMAINDEX, request.metadata, request.bundle)
            run_response = service.run_tools(run_tools_request)
            return run_response.content
        return wrapper

    def _generate_tool_schema(self, args: List[GenericArgument]):
        """Generate a tool schema for a given list of arguments"""
        field_definitions = {}

        for argument in args:
            field_type = self._get_field_type(argument["type"])
            
            if argument["required"]:
                field_info = FieldInfo(
                    description=argument["description"]
                )
                field_definitions[argument["name"]] = (field_type, field_info)
            else:
                field_info = FieldInfo(
                    description=argument["description"],
                    default=None
                )
                field_definitions[argument["name"]] = (field_type, field_info)

        return field_definitions

    def _get_field_type(self, type_str: str):
        """Convert string type to actual type"""
        type_mapping = {
            "string": str,
            "integer": int,
            "float": float,
            "boolean": bool,
            "array": list,
            "object": dict,
            # Add more type mappings as needed
        }
        return type_mapping.get(type_str.lower(), str)  # Default to str if type is not recognized

    def _create_model(self, name: str, schema: dict):
        return create_model(name, **schema)
