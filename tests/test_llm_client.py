import unittest
from unittest.mock import Mock, patch

from repomind.llm.client import complete


class FakeSettings:
    OPENAI_API_KEY = "test-key"
    OPENAI_BASE_URL = "https://example.com/v1"
    OPENAI_MODEL = "test-model"



class TestLlmClient(unittest.TestCase):
    @patch("repomind.llm.client.OpenAI")
    def test_complete_returns_message_content(self, openai_mock):
        fake_client = Mock()
        fake_response = Mock()
        fake_response.choices = [
            Mock(message=Mock(content="hello from model"))
        ]

        fake_client.chat.completions.create.return_value = fake_response
        openai_mock.return_value = fake_client

        result = complete(
            [{"role": "user", "content": "hello"}],
            FakeSettings(),
        )

        self.assertEqual(result, "hello from model")
        fake_client.chat.completions.create.assert_called_once_with(
            model="test-model",
            messages=[{"role": "user", "content": "hello"}],
        )
