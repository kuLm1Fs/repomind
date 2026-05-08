import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from repomind.runtime.service import ask
from repomind.tools.runtime import ToolResult


class FakeSettings:
    CHUNK_SIZE = 80
    CHUNK_OVERLAP = 10
    TOP_K = 1
    MAX_RETRY = 1

    def __init__(self, trace_dir):
        self.TRACE_DIR = trace_dir


class TestRuntime(unittest.TestCase):
    @patch("repomind.runtime.service.run_tools")
    @patch("repomind.runtime.service.generate_answer")
    def test_ask_returns_generated_answer_when_evaluation_passes(
        self,
        generate_answer_mock,
        run_tools_mock,
    ):
        generate_answer_mock.return_value = """
涉及文件：
- auth.py

实现流程：
1. login 返回 token

证据：
- auth.py:1-2
"""
        run_tools_mock.return_value = [
            ToolResult(
                tool_name="rg_read_file",
                path="auth.py",
                start_line=1,
                end_line=2,
                content="def login():\n    return 'token'",
            )
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
            trace_files = list(trace_dir.glob("*.json"))
            self.assertEqual(len(trace_files), 1)

            trace_data = json.loads(trace_files[0].read_text(encoding="utf-8"))
            self.assertEqual(trace_data["question"], "登录功能是如何实现的？")
            self.assertEqual(trace_data["retry_count"], 0)
            self.assertTrue(trace_data["evaluation"]["passed"])
            self.assertEqual(trace_data["tool_results"][0]["path"], "auth.py")
            self.assertEqual(
                trace_data["retrieved_chunks"][0]["chunk"]["path"],
                "auth.py",
            )

        self.assertEqual(generate_answer_mock.call_count, 1)
        self.assertEqual(run_tools_mock.call_count, 1)
        self.assertEqual(
            generate_answer_mock.call_args.kwargs["tool_results"],
            run_tools_mock.return_value,
        )

    @patch("repomind.runtime.service.run_tools")
    @patch("repomind.runtime.service.generate_answer")
    def test_ask_retries_when_evaluation_fails(
        self,
        generate_answer_mock,
        run_tools_mock,
    ):
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
        run_tools_mock.return_value = []

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
            trace_files = list(trace_dir.glob("*.json"))
            self.assertEqual(len(trace_files), 1)

            trace_data = json.loads(trace_files[0].read_text(encoding="utf-8"))
            self.assertEqual(trace_data["retry_count"], 1)
            self.assertTrue(trace_data["evaluation"]["passed"])

        self.assertEqual(generate_answer_mock.call_count, 2)
        self.assertEqual(run_tools_mock.call_count, 1)

    @patch("repomind.runtime.service.run_tools")
    @patch("repomind.runtime.service.generate_answer")
    def test_ask_returns_message_and_saves_trace_when_no_chunks_match(
        self,
        generate_answer_mock,
        run_tools_mock,
    ):
        run_tools_mock.return_value = []

        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "notes.md").write_text(
                "This file is about deployment only.\n",
                encoding="utf-8",
            )

            trace_dir = repo / ".traces"
            settings = FakeSettings(trace_dir=str(trace_dir))

            answer = ask(str(repo), "登录功能是如何实现的？", settings)

            self.assertEqual(answer, "没有找到相关代码片段")
            trace_files = list(trace_dir.glob("*.json"))
            self.assertEqual(len(trace_files), 1)

            trace_data = json.loads(trace_files[0].read_text(encoding="utf-8"))
            self.assertEqual(trace_data["question"], "登录功能是如何实现的？")
            self.assertEqual(trace_data["retrieved_chunks"], [])
            self.assertEqual(trace_data["tool_results"], [])
            self.assertIsNone(trace_data["evaluation"])
            self.assertEqual(trace_data["retry_count"], 0)

        generate_answer_mock.assert_not_called()
        self.assertEqual(run_tools_mock.call_count, 1)
