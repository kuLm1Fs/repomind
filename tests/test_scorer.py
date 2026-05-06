import unittest

from repomind.retrieval.chunker import CodeChunk
from repomind.retrieval.scorer import extract_keywords, score_chunk


class TestScorer(unittest.TestCase):
    def test_extracts_english_keywords(self):
        keywords = extract_keywords("how does jwt login work")

        self.assertIn("jwt", keywords)
        self.assertIn("login", keywords)

    def test_expands_chinese_login_query(self):
        keywords = extract_keywords("登录功能是怎么实现的？")

        self.assertIn("login", keywords)
        self.assertIn("auth", keywords)
        self.assertIn("jwt", keywords)

    def test_scores_content_matches(self):
        chunk = CodeChunk(
            path="src/service.py",
            start_line=1,
            end_line=3,
            content="def login():\n    return jwt_token",
        )

        score = score_chunk("login jwt", chunk)

        self.assertGreater(score, 0)

    def test_path_match_scores_higher_than_content_match(self):
        path_chunk = CodeChunk(
            path="src/auth/service.py",
            start_line=1,
            end_line=1,
            content="nothing relevant",
        )
        content_chunk = CodeChunk(
            path="src/service.py",
            start_line=1,
            end_line=1,
            content="auth",
        )

        self.assertGreater(
            score_chunk("auth", path_chunk),
            score_chunk("auth", content_chunk),
        )
