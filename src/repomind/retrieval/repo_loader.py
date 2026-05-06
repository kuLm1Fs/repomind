"""
repo_path = "./demo-repo"

输出
[
    RepoFile(
        path = "src/auth/service.py",
        absolute_path = "/xxx/demo-repo/src/auth/service.py",
        content="..."
"""
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".go",
    ".js",
    ".ts",
    ".md",
    ".yml",
    ".yaml",
}

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "target",
    "dist",
    "__pycache__",
}

@dataclass
class RepoFile:
    path: str
    content: str

def load_repo(repo_path: str) -> list[RepoFile]:
    root = Path(repo_path)

    #检查仓库路径是否存在：
    if not root.exists():
        raise FileNotFoundError(repo_path)

    files: list[RepoFile] = []

    # 递归便利整个目录所有文件
    for path in root.rglob("*"):
        # 跳过非文件
        if not path.is_file():
            continue

        # 跳过忽略目录
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        
        # 跳过非指定后缀的文件
        if path.suffix not in SUPPORTED_EXTENSIONS:
            continue

        # 把绝对路径转成相对路径
        relative_path = path.relative_to(root).as_posix()
        content = path.read_text(encoding="utf-8")

        files.append(RepoFile(path=relative_path, content=content))

    return files
