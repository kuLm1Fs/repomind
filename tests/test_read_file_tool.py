import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from repomind.tools.read_file_tool import read_file_range


class TestReadFileTool(unittest.TestCase):
    def test_reads_requested_line_range(self):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "auth.py").write_text(
                "line1\nline2\nline3\nline4\n",
                encoding="utf-8",
            )

            result = read_file_range(str(repo), "auth.py", 2, 3)

            self.assertEqual(result.path, "auth.py")
            self.assertEqual(result.start_line, 2)
            self.assertEqual(result.end_line, 3)
            self.assertEqual(result.content, "line2\nline3")

    def test_missing_file_raises_error(self):
        with TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                read_file_range(str(tmp), "missing.py", 1, 2)

    def test_invalid_line_range_raises_error(self):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "auth.py").write_text("line1\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                read_file_range(str(repo), "auth.py", 0, 1)

            with self.assertRaises(ValueError):
                read_file_range(str(repo), "auth.py", 3, 2)
