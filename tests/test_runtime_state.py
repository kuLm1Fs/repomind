import unittest

from repomind.runtime.state import RuntimeState, state_to_trace_data


class TestRuntimeState(unittest.TestCase):
    def test_runtime_state_defaults(self):
        state = RuntimeState(
            repo_path="/tmp/repo",
            question="登录功能怎么实现？",
        )

        self.assertEqual(state.repo_path, "/tmp/repo")
        self.assertEqual(state.question, "登录功能怎么实现？")
        self.assertEqual(state.files, [])
        self.assertEqual(state.chunks, [])
        self.assertEqual(state.retrieved_chunks, [])
        self.assertEqual(state.tool_results, [])
        self.assertEqual(state.answer, "")
        self.assertIsNone(state.evaluation)
        self.assertEqual(state.retry_count, 0)

    def test_state_to_trace_data_exports_runtime_trace_fields(self):
        state = RuntimeState(
            repo_path="/tmp/repo",
            question="登录功能怎么实现？",
        )
        state.files = ["large file data"]
        state.chunks = ["large chunk data"]
        state.retrieved_chunks = ["retrieved"]
        state.tool_results = ["tool"]
        state.answer = "answer"
        state.evaluation = "evaluation"
        state.retry_count = 1

        trace_data = state_to_trace_data(state)

        self.assertEqual(
            trace_data,
            {
                "repo_path": "/tmp/repo",
                "question": "登录功能怎么实现？",
                "retrieved_chunks": ["retrieved"],
                "tool_results": ["tool"],
                "answer": "answer",
                "evaluation": "evaluation",
                "retry_count": 1,
            },
        )
        self.assertNotIn("files", trace_data)
        self.assertNotIn("chunks", trace_data)
