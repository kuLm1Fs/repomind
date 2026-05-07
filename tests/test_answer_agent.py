import unittest
from unittest.mock import patch

from repomind.agents.answer_agent import generate_answer
from repomind.retrieval.chunker import CodeChunk
from repomind.retrieval.retriever import RetrievedChunk
from repomind.tools.runtime import ToolResult


class FakeSettings:
    pass


class TestAnswerAgent(unittest.TestCase):
    @patch("repomind.agents.answer_agent.complete")
    def test_generate_answer_uses_retrieved_context(self, complete_mock):
        complete_mock.return_value = "涉及文件：\n- auth.py"

        retrieved_chunks = [
            RetrievedChunk(
                chunk=CodeChunk(
                    path="auth.py",
                    start_line=1,
                    end_line=2,
                    content="def login():\n    return 'token'",
                ),
                score=3,
            )
        ]

        answer = generate_answer(
            "登录功能是如何实现的？",
            retrieved_chunks,
            FakeSettings(),
        )

        self.assertIn("auth.py", answer)

        messages = complete_mock.call_args.args[0]
        user_message = messages[1]["content"]

        self.assertIn("登录功能是如何实现的？", user_message)
        self.assertIn("auth.py", user_message)
        self.assertIn("def login()", user_message)

@patch("repomind.agents.answer_agent.complete")
def test_generate_answer_includes_tool_context(self, complete_mock):
    complete_mock.return_value = "answer"

    retrieved_chunks = [
        RetrievedChunk(
            chunk=CodeChunk(
                path="auth.py",
                start_line=1,
                end_line=2,
                content="def login(): pass",
            ),
            score=3,
        )
    ]

    tool_results = [
        ToolResult(
            tool_name="rg_read_file",
            path="auth.py",
            start_line=1,
            end_line=2,
            content="def login():\n    return 'token'",
        )
    ]

    generate_answer(
        "登录功能是如何实现的？",
        retrieved_chunks,
        FakeSettings(),
        tool_results=tool_results,
    )

    messages = complete_mock.call_args.args[0]
    user_message = messages[1]["content"]

    self.assertIn("工具补充上下文", user_message)
    self.assertIn("rg_read_file", user_message)
    self.assertIn("return 'token'", user_message)
