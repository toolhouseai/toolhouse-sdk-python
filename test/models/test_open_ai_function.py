# This file was generated by liblab | https://liblab.com/
# pylint: disable=C0116, C0115

import unittest
from src.toolhouse.models.OpenAiFunction import OpenAiFunction


class TestOpenAiFunctionModel(unittest.TestCase):
    def test_true(self):
        self.assertTrue(True)  # pylint: disable=W1503

    def test_open_ai_function(self):
        # Create OpenAiFunction class instance
        test_model = OpenAiFunction(name="earum", arguments="facere")
        self.assertEqual(test_model.name, "earum")
        self.assertEqual(test_model.arguments, "facere")

    def test_open_ai_function_required_fields_missing(self):
        # Assert OpenAiFunction class generation fails without required fields
        with self.assertRaises(TypeError):
            # pylint: disable=E1120, W0612            
            test_model = OpenAiFunction()  # noqa: F841


if __name__ == "__main__":
    unittest.main()
