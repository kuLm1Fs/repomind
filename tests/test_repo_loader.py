import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from repomind.retrieval.repo_loader import load_repo


class TestRepoLoader(unittest.TestCase):
    def test_loads_supported_files(self):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "main.py").write_text("print('hi')", encoding="utf-8")
            (repo / "notes.txt").write_text("ignore me", encoding="utf-8")

            files = load_repo(str(repo))

            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].path, "main.py")
            self.assertEqual(files[0].content, "print('hi')")

    def test_ignores_configured_directories(self):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / ".git").mkdir()
            (repo / ".git" / "config.py").write_text("secret", encoding="utf-8")
            (repo / "app.py").write_text("print('app')", encoding="utf-8")

            files = load_repo(str(repo))

            paths = [file.path for file in files]
            self.assertEqual(paths, ["app.py"])

    def test_loads_nested_files_with_relative_posix_paths(self):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            nested_dir = repo / "src" / "auth"
            nested_dir.mkdir(parents=True)
            (nested_dir / "service.py").write_text("def login(): pass", encoding="utf-8")

            files = load_repo(str(repo))

            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].path, "src/auth/service.py")

    def test_ignores_supported_files_inside_ignored_directories(self):
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            ignored_dir = repo / "node_modules" / "pkg"
            ignored_dir.mkdir(parents=True)
            (ignored_dir / "index.ts").write_text("export const token = 1", encoding="utf-8")
            (repo / "app.ts").write_text("export const app = 1", encoding="utf-8")

            files = load_repo(str(repo))

            paths = [file.path for file in files]
            self.assertEqual(paths, ["app.ts"])

    def test_missing_repo_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            load_repo("/path/does/not/exist")

    def test_file_path_returns_empty_list(self):
        with TemporaryDirectory() as tmp:
            repo_file = Path(tmp) / "not-a-repo.py"
            repo_file.write_text("print('hi')", encoding="utf-8")

            files = load_repo(str(repo_file))

            self.assertEqual(files, [])
