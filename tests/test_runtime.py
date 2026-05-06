import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from repomind.runtime import ask


class FakeSettings:
    CHUNK_SIZE = 80
    CHUNK_OVERLAP = 10
    TOP_K = 5


class TestRuntime(unittest.TestCase):
    def test_ask_returns_retrieved_code_chunks(self):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "auth.py").write_text(
                "def login():\n    return 'token'\n",
                encoding="utf-8",
            )

            answer = ask(str(repo), "登录功能是如何实现的？", FakeSettings())

            self.assertIn("涉及代码片段", answer)
            self.assertIn("auth.py:1-2", answer)
            self.assertIn("def login()", answer)
