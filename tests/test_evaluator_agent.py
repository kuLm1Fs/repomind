import unittest

from repomind.agents.evaluator_agent import evaluate_answer


class TestEvaluatorAgent(unittest.TestCase):
    def test_passes_answer_with_required_sections(self):
        answer = """
涉及文件：
- auth.py

实现流程：
1. 接收登录请求
2. 生成 token

证据：
- auth.py:1-10
"""

        result = evaluate_answer(answer)

        self.assertTrue(result.passed)
        self.assertEqual(result.reasons, [])

    def test_fails_answer_missing_required_sections(self):
        answer = "登录逻辑在 auth.py 里。"

        result = evaluate_answer(answer)

        self.assertFalse(result.passed)
        self.assertIn("missing involved files section", result.reasons)
        self.assertIn("missing implementation flow section", result.reasons)
        self.assertIn("missing evidence section", result.reasons)

    def test_fails_answer_without_concrete_file_reference(self):
        answer = """
涉及文件：
- 无

实现流程：
1. 不清楚

证据：
- 无
"""

        result = evaluate_answer(answer)

        self.assertFalse(result.passed)
        self.assertIn("missing concrete file reference", result.reasons)
        self.assertIn("missing line evidence", result.reasons)

    def test_fails_answer_that_says_context_is_insufficient(self):
        answer = """
涉及文件：
- auth.py

实现流程：
1. 上下文不足，无法判断

证据：
- auth.py:1-2
"""

        result = evaluate_answer(answer)

        self.assertFalse(result.passed)
        self.assertIn("answer says context is insufficient", result.reasons)
