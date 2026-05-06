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
from typer.testing import CliRunner

from repomind.main import app


class TestCli(unittest.TestCase):
    def test_ask_command_runs_with_repo_and_question(self):
        runner = CliRunner()

        result = runner.invoke(app, ["ask", ".", "登录功能是如何实现的？"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("登录功能是如何实现的？", result.output)
        self.assertIn("RepoMind runtime is not implemented yet.", result.output)


if __name__ == "__main__":
    unittest.main()
