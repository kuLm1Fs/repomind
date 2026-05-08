import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

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

    @patch("repomind.tools.rg_tool.shutil.which", return_value=None)
    def test_python_fallback_finds_matching_line_when_rg_is_missing(self, which_mock):
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
            which_mock.assert_called_once_with("rg")

    @patch("repomind.tools.rg_tool.shutil.which", return_value=None)
    def test_python_fallback_ignores_configured_directories(self, which_mock):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            ignored_dir = repo / "node_modules" / "pkg"
            ignored_dir.mkdir(parents=True)
            (ignored_dir / "auth.py").write_text("def login(): pass", encoding="utf-8")
            (repo / "auth.py").write_text("def login(): pass", encoding="utf-8")

            results = rg_search(str(repo), "login")

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].path, "auth.py")
            which_mock.assert_called_once_with("rg")

    @patch("repomind.tools.rg_tool.shutil.which", return_value=None)
    def test_python_fallback_respects_limit(self, which_mock):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "auth.py").write_text(
                "login one\nlogin two\nlogin three\n",
                encoding="utf-8",
            )

            results = rg_search(str(repo), "login", limit=2)

            self.assertEqual(len(results), 2)
            self.assertEqual([result.line_number for result in results], [1, 2])
            which_mock.assert_called_once_with("rg")
