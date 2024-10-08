# This file was generated by liblab | https://liblab.com/

import unittest
from src.toolhouse.models.AnthropicToolCallResults import AnthropicToolCallResults


class TestAnthropicToolCallResultsModel(unittest.TestCase):
    def test_true(self):
        self.assertTrue(True)

    def test_anthropic_tool_call_results(self):
        # Create AnthropicToolCallResults class instance
        test_model = AnthropicToolCallResults(
            type="tool_result", content="asperiores", tool_use_id="corrupti"
        )
        self.assertEqual(test_model.type, "tool_result")
        self.assertEqual(test_model.content, "asperiores")
        self.assertEqual(test_model.tool_use_id, "corrupti")

    def test_anthropic_tool_call_results_required_fields_missing(self):
        # Assert AnthropicToolCallResults class generation fails without required fields
        with self.assertRaises(TypeError):
            test_model = AnthropicToolCallResults()


if __name__ == "__main__":
    unittest.main()
