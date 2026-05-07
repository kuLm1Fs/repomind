#from typer.testing import CliRunner

#from repomind.main import app

#runner = CliRunner()

#def test_ask_command_runs_with_repo_and_question():
#    result = runner.invoke(app, ["ask", ".", "登录功能是如何实现的？"])
#
#    assert result.exit_code == 0
#    assert "登录功能是怎么实现的？" in result.output
#    assert "Repomind runtime is not implemented yet." in result.output
#
import unittest
from unittest.mock import patch
from typer.testing import CliRunner

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

if __name__ == "__main__":
    unittest.main()
