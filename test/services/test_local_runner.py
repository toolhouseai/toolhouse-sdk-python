import json
import unittest
from anthropic.types import ToolUseBlock
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall, Function
from groq.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall as ChatCompletionMessageToolCallGroq, Function as FunctionGroq
from toolhouse.services.local_tools import LocalTools


class TestLocalRunner(unittest.TestCase):

    def setUp(self):
        """Set up a LocalRunner instance for testing."""
        self.runner = LocalTools()

    def test_register_a_tool(self):
        """Test registering and running a local tool."""

        @self.runner.register_local_tool("add")
        def add(a, b):
            return str(a + b)

        assert "add" in self.runner.local_tools
        assert self.runner.local_tools["add"] == add

    def test_anthropic_run_local(self):
        """Test registering and running a local tool Anthropic."""

        @self.runner.register_local_tool("add")
        def add(a, b):
            return str(a + b)

        tool = ToolUseBlock(id="id", input={'a': 3, 'b': 5}, name="add", type="tool_use")
        # Test the 'add' function
        result = self.runner.run_tools(tool)
        self.assertEqual(result.content, "8", "The add function did not return the expected result")

    def test_register_and_run_local_tool_openai(self):
        """Test registering and running a local tool."""

        @self.runner.register_local_tool("add")
        def add(a, b):
            return str(a + b)

        func = Function(arguments=json.dumps({'a': 3, 'b': 5}), name="add")
        tool = ChatCompletionMessageToolCall(id="id", function=func, type="function")
        # Test the 'add' function
        result = self.runner.run_tools(tool)
        self.assertEqual(result.content, "8", "The add function did not return the expected result")
        
    def test_register_and_run_local_tool_groq(self):
        """Test registering and running a local tool groq"""

        @self.runner.register_local_tool("add")
        def add(a, b):
            return str(a + b)

        func = FunctionGroq(arguments=json.dumps({'a': 3, 'b': 5}), name="add")
        tool = ChatCompletionMessageToolCallGroq(id="id", function=func, type="function")
        # Test the 'add' function
        result = self.runner.run_tools(tool)
        self.assertEqual(result.content, "8", "The add function did not return the expected result")

    def test_run_nonexistent_local_tool(self):
        """Test running a local tool that does not exist."""
        tool = ToolUseBlock(id="id", input={'a': 3, 'b': 5}, name="add", type="tool_use")
        with self.assertRaises(ValueError):
            self.runner.run_tools(tool)

    def test_function_return_type(self):
        """Test that the registered functions return a string."""

        @self.runner.register_local_tool("add")
        def add(a, b):
            return a + b  # This should raise a TypeError
        tool = ToolUseBlock(id="id", input={'a': 3, 'b': 5}, name="add", type="tool_use")

        with self.assertRaises(TypeError):
            self.runner.run_tools(tool)


if __name__ == "__main__":
    unittest.main()
