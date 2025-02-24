import unittest
from unittest.mock import patch

from toolhouse.models.GetToolsRequest import GetToolsRequest
from toolhouse.sdk import MissingDependencyError, Toolhouse
from toolhouse.services.tools import Tools

# Test data
arg_string = {"name": "code_str", "type": "string", "description": "The code to execute.", "required": True}
arg_array = {
    "name": "tags",
    "type": "array",
    "items": {"type": "string"},
    "description": "List of tags",
    "required": True,
}
tool_string = {
    "name": "code_interpreter",
    "title": "Code interpreter",
    "description": "Runs code.",
    "arguments": [arg_string],
}
tool_array = {
    "name": "tag_processor",
    "title": "Tag Processor",
    "description": "Process tags.",
    "arguments": [arg_array],
}


class TestLlamaIndex(unittest.TestCase):

    def setUp(self):
        """Set up a LlamaIndex instance for testing."""
        self.tools = Tools(api_key="testkey")
        from toolhouse.services.llamaindex import LlamaIndex

        self.runner = LlamaIndex(service=self.tools)

    def test_generate_tool(self):
        """Test generating a tool with string argument."""
        request = GetToolsRequest(provider="llamaindex", metadata={}, bundle="default")
        llama_tool = self.runner.generate_tool(tool_string, request)
        from llama_index.core.tools import FunctionTool

        self.assertIsInstance(llama_tool, FunctionTool)

    def test_generate_tool_with_array(self):
        """Test generating a tool with array argument."""
        request = GetToolsRequest(provider="llamaindex", metadata={}, bundle="default")
        llama_tool = self.runner.generate_tool(tool_array, request)
        from llama_index.core.tools import FunctionTool

        self.assertIsInstance(llama_tool, FunctionTool)
        # Verify the array parameter is properly defined
        schema = llama_tool.metadata.fn_schema.model_json_schema()
        self.assertIn("tags", schema["properties"])
        self.assertEqual(schema["properties"]["tags"]["type"], "array")
        self.assertEqual(schema["properties"]["tags"]["items"]["type"], "string")

    def test_generate_tools(self):
        """Test generating multiple tools."""
        request = GetToolsRequest(provider="llamaindex", metadata={}, bundle="default")
        llama_tools = self.runner.get_tools([tool_string, tool_array], request)
        from llama_index.core.tools import FunctionTool

        self.assertIsInstance(llama_tools, list)
        self.assertEqual(len(llama_tools), 2)
        self.assertIsInstance(llama_tools[0], FunctionTool)
        self.assertIsInstance(llama_tools[1], FunctionTool)


if __name__ == "__main__":
    unittest.main()
