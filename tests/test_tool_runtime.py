import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from repomind.tools.runtime import run_tools


class TestToolRuntime(unittest.TestCase):
    def test_run_tools_reads_rg_matches(self):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "auth.py").write_text(
                "def login():\n    return 'token'\n",
                encoding="utf-8",
            )

            results = run_tools(str(repo), "login", max_results=1)

            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].path, "auth.py")
            self.assertIn("def login()", results[0].content)
