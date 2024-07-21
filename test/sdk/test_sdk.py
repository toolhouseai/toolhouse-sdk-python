# pylint: disable=C0116, C0115

import unittest
from src.toolhouse import Toolhouse, Provider


class TestSDK(unittest.TestCase):

    def test_true(self):
        self.assertTrue(True)  # pylint: disable=W1503

    def test_sdk(self):
        th = Toolhouse()
        assert th.provider == Provider.OPENAI

    def test_providers(self):
        th = Toolhouse(provider="anthropic")
        assert th.provider == "anthropic"
        th = Toolhouse(provider="openai")
        assert th.provider == "openai"
        th = Toolhouse(provider="openai_assistants")
        assert th.provider == "openai_assistants"


if __name__ == "__main__":
    unittest.main()
