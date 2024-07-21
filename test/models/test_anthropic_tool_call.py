# This file was generated by liblab | https://liblab.com/

import unittest
from src.toolhouse.models.AnthropicToolCall import AnthropicToolCall


class TestAnthropicToolCallModel(unittest.TestCase):
    def test_true(self):
        self.assertTrue(True)

    def test_anthropic_tool_call(self):
        # Create AnthropicToolCall class instance
        test_model = AnthropicToolCall(
            type="tool_use", input="foo", name="esse", id="pariatur"
        )
        self.assertEqual(test_model.type, "tool_use")
        self.assertEqual(test_model.input, "foo")
        self.assertEqual(test_model.name, "esse")
        self.assertEqual(test_model.id, "pariatur")

    def test_anthropic_tool_call_required_fields_missing(self):
        # Assert AnthropicToolCall class generation fails without required fields
        with self.assertRaises(TypeError):
            test_model = AnthropicToolCall()


if __name__ == "__main__":
    unittest.main()
