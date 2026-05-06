import unittest

from repomind.retrieval.chunker import CodeChunk
from repomind.retrieval.retriever import retrieve


class TestRetriever(unittest.TestCase):
    def test_returns_top_scoring_chunks(self):
        chunks = [
            CodeChunk("src/readme.md", 1, 1, "nothing"),
            CodeChunk("src/auth/service.py", 1, 2, "def login(): pass"),
            CodeChunk("src/payment/service.py", 1, 2, "def charge(): pass"),
        ]

        results = retrieve("login auth", chunks, top_k=1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].chunk.path, "src/auth/service.py")
        self.assertGreater(results[0].score, 0)

    def test_filters_zero_score_chunks(self):
        chunks = [
            CodeChunk("src/readme.md", 1, 1, "nothing"),
        ]

        results = retrieve("login", chunks, top_k=5)

        self.assertEqual(results, [])
