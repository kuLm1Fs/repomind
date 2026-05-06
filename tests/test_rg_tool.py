import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from repomind.tools.rg_tool import rg_search


class TestRgTool(unittest.TestCase):
    def test_empty_query_returns_empty_list(self):
        with TemporaryDirectory() as tmp:
            results = rg_search(tmp, "")

            self.assertEqual(results, [])

    def test_search_finds_matching_line(self):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "auth.py").write_text(
                "def login():\n    return 'token'\n",
                encoding="utf-8",
            )

            results = rg_search(str(repo), "login")

            self.assertGreaterEqual(len(results), 1)
            self.assertEqual(results[0].path, "auth.py")
            self.assertEqual(results[0].line_number, 1)
            self.assertIn("login", results[0].line)
