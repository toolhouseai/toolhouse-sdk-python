# pylint: disable=C0116, C0115

import unittest
from unittest import mock
from src.toolhouse import Toolhouse, Provider, ToolhouseError
import os


class TestSDK(unittest.TestCase):

    def test_true(self):
        self.assertTrue(True)  # pylint: disable=W1503

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_sdk_api_exception(self):
        with self.assertRaises(ToolhouseError):
            Toolhouse()

    @mock.patch.dict(os.environ, {"TOOLHOUSE_API_KEY": "345"}, clear=True)
    def test_sdk(self):
        th = Toolhouse()
        assert th.provider == Provider.OPENAI

    @mock.patch.dict(os.environ, {"TOOLHOUSE_API_KEY": "345"}, clear=True)
    def test_providers(self):
        th = Toolhouse(provider="anthropic")
        assert th.provider == "anthropic"
        th = Toolhouse(provider="openai")
        assert th.provider == "openai"
        th = Toolhouse(provider="openai_assistants")
        assert th.provider == "openai_assistants"

    def test_access_token(self):
        th = Toolhouse(access_token="123")
        assert th.api_key == "123"
        
    def test_api_key(self):
        th = Toolhouse(api_key="123")
        assert th.api_key == "123"

    @mock.patch.dict(os.environ, {"TOOLHOUSE_API_KEY": "345"}, clear=True)
    def test_access_key_from_env(self):
        th = Toolhouse()
        assert th.api_key == "345"

    @mock.patch.dict(os.environ, {"TOOLHOUSE_API_KEY": "345"}, clear=True)
    def test_access_key_param_overrides_env(self):
        th = Toolhouse(access_token="123")
        assert th.api_key == "123"


if __name__ == "__main__":
    unittest.main()
