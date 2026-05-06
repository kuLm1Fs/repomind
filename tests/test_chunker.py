import unittest

from repomind.retrieval.chunker import chunk_file
from repomind.retrieval.repo_loader import RepoFile


class TestChunker(unittest.TestCase):
    def test_short_file_creates_one_chunk(self):
        file = RepoFile(
            path="main.py",
            content="line1\nline2\nline3",
        )

        chunks = chunk_file(file, chunk_size=80, overlap=10)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].path, "main.py")
        self.assertEqual(chunks[0].start_line, 1)
        self.assertEqual(chunks[0].end_line, 3)
        self.assertEqual(chunks[0].content, "line1\nline2\nline3")

    def test_long_file_creates_overlapping_chunks(self):
        content = "\n".join(f"line{i}" for i in range(1, 151))
        file = RepoFile(path="main.py", content=content)

        chunks = chunk_file(file, chunk_size=80, overlap=10)

        self.assertEqual(len(chunks), 2)

        self.assertEqual(chunks[0].start_line, 1)
        self.assertEqual(chunks[0].end_line, 80)

        self.assertEqual(chunks[1].start_line, 71)
        self.assertEqual(chunks[1].end_line, 150)
