import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from repomind.runtime.service import ask


class FakeSettings:
    CHUNK_SIZE = 80
    CHUNK_OVERLAP = 10
    TOP_K = 1
    MAX_RETRY = 1

    def __init__(self, trace_dir):
        self.TRACE_DIR = trace_dir


class TestRuntime(unittest.TestCase):
    @patch("repomind.runtime.service.generate_answer")
    def test_ask_returns_generated_answer_when_evaluation_passes(
        self,
        generate_answer_mock,
    ):
        generate_answer_mock.return_value = """
涉及文件：
- auth.py

实现流程：
1. login 返回 token

证据：
- auth.py:1-2
"""

        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "auth.py").write_text(
                "def login():\n    return 'token'\n",
                encoding="utf-8",
            )

            trace_dir = repo / ".traces"
            settings = FakeSettings(trace_dir=str(trace_dir))

            answer = ask(str(repo), "登录功能是如何实现的？", settings)

            self.assertIn("涉及文件", answer)
            self.assertEqual(len(list(trace_dir.glob("*.json"))), 1)

        self.assertEqual(generate_answer_mock.call_count, 1)

    @patch("repomind.runtime.service.generate_answer")
    def test_ask_retries_when_evaluation_fails(self, generate_answer_mock):
        generate_answer_mock.side_effect = [
            "不完整回答",
            """
涉及文件：
- auth.py

实现流程：
1. login 返回 token

证据：
- auth.py:1-2
""",
        ]

        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "auth.py").write_text(
                "def login():\n    return 'token'\n",
                encoding="utf-8",
            )

            trace_dir = repo / ".traces"
            settings = FakeSettings(trace_dir=str(trace_dir))

            answer = ask(str(repo), "登录功能是如何实现的？", settings)

            self.assertIn("涉及文件", answer)
            self.assertEqual(len(list(trace_dir.glob("*.json"))), 1)

        self.assertEqual(generate_answer_mock.call_count, 2)
