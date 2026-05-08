import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from typer.testing import CliRunner

from repomind.config.settings import settings
from repomind.main import app


class TestCli(unittest.TestCase):
    @patch("repomind.main.runtime_ask")
    def test_ask_command_runs_with_repo_and_question(self, runtime_ask_mock):
        runtime_ask_mock.return_value = "fake answer"

        runner = CliRunner()

        result = runner.invoke(app, ["ask", ".", "登录功能是如何实现的？"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("fake answer", result.output)
        runtime_ask_mock.assert_called_once()

        args = runtime_ask_mock.call_args.args
        self.assertEqual(args[0], ".")
        self.assertEqual(args[1], "登录功能是如何实现的？")
        self.assertIs(args[2], settings)

    @patch("repomind.main.runtime_ask")
    def test_ask_command_rejects_missing_repo_path(self, runtime_ask_mock):
        runner = CliRunner()

        result = runner.invoke(app, ["ask", "/path/does/not/exist", "问题"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Repository path does not exist", result.output)
        runtime_ask_mock.assert_not_called()

    @patch("repomind.main.runtime_ask")
    def test_ask_command_rejects_file_path(self, runtime_ask_mock):
        runner = CliRunner()

        with TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "not-a-repo.py"
            file_path.write_text("print('hi')", encoding="utf-8")

            result = runner.invoke(app, ["ask", str(file_path), "问题"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Repository path must be a directory", result.output)
        runtime_ask_mock.assert_not_called()

    @patch("repomind.main.runtime_ask")
    def test_ask_command_rejects_empty_question(self, runtime_ask_mock):
        runner = CliRunner()

        result = runner.invoke(app, ["ask", ".", "   "])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Question must not be empty", result.output)
        runtime_ask_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
