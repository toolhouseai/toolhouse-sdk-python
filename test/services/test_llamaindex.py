import unittest
from toolhouse.services.llamaindex import LlamaIndex
from toolhouse.models.GenericTools import GenericTools, GenericArgument
from llama_index.core.tools import FunctionTool
from toolhouse import Toolhouse

arg = GenericArgument(**{'name': 'code_str', 'type': 'string', 'description': 'The code to execute. Only Python is supported at the moment.', 'required': True})
tool = GenericTools(**{'name': 'code_interpreter', 'title': 'Code interpreter', 'description': 'Allows you to run the code you generate.', 'arguments': [arg]})


class TestLlamaIndex(unittest.TestCase):

    def setUp(self):
        """Set up a LlamaIndex instance for testing."""
        self.runner = LlamaIndex()
        self.th = Toolhouse(api_key="testkey")

    def test_generate_tool_schema(self):
        """Test registering and running a local tool."""
        llama_tool = self.runner.generate_tool(self.th, tool)
        print(llama_tool)

if __name__ == "__main__":
    unittest.main()
