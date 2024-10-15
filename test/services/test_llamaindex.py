import unittest
from toolhouse.services.llamaindex import LlamaIndex
from llama_index.core.tools import FunctionTool
from toolhouse.services.tools import Tools
from toolhouse.models.GetToolsRequest import GetToolsRequest
arg = {'name': 'code_str', 'type': 'string', 'description': 'The code to execute. Only Python is supported at the moment.', 'required': True}
tool = {'name': 'code_interpreter', 'title': 'Code interpreter', 'description': 'Allows you to run the code you generate.', 'arguments': [arg]}


class TestLlamaIndex(unittest.TestCase):

    def setUp(self):
        """Set up a LlamaIndex instance for testing."""
        self.runner = LlamaIndex(service=Tools(api_key="testkey"))

    def test_generate_tool(self):
        """Test registering and running a local tool."""
        request = GetToolsRequest(provider="llamaindex", metadata={}, bundle="default")
        llama_tool = self.runner.generate_tool(tool, request)
        assert isinstance(llama_tool, FunctionTool)
        
    def test_generate_tools(self):
        """Test registering and running a local tool."""
        request = GetToolsRequest(provider="llamaindex", metadata={}, bundle="default")
        llama_tools = self.runner.get_tools([tool], request)
        assert isinstance(llama_tools, list)
        assert isinstance(llama_tools[0], FunctionTool)


if __name__ == "__main__":
    unittest.main()
