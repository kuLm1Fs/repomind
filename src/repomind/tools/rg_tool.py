from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess

@dataclass
class RgMatch:
    path: str
    line_number: int
    line: str

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "target",
    "dist",
    "__pycache__",
}

def rg_search(repo_path: str, query: str, limit: int = 20) -> list[RgMatch]:
    if not query.strip():
        return []
    
    root = Path(repo_path)
    
    if not root.exists():
        raise FileNotFoundError(repo_path)
    
    if not root.is_dir():
        raise NotADirectoryError(repo_path)
    
    if shutil.which("rg") is None:
        return python_search(root, query, limit)
    
    completed = subprocess.run(
        [
            "rg",
            "--line-number",
            "--no-heading",
            "--color",
            "never",
            query,
            str(root),
        ],
        capture_output=True,
        text=True,
        check=False,
        )
    
    if completed.returncode not in (0,1):
        return []
    
    matches: list[RgMatch] = []

    for line in completed.stdout.splitlines():
        parts = line.split(":", 2)

        if len(parts) != 3:
            continue

        path_text, line_number_text, matched_line = parts

        try:
            line_number = int(line_number_text)
        except ValueError:
            continue

        relative_path = Path(path_text).relative_to(root).as_posix()

        matches.append(
            RgMatch(
                path=relative_path,
                line_number=line_number,
                line=matched_line,
                )
            )
        
        if len(matches) >= limit:
            break

    return matches

def python_search(root: Path, query: str, limit: int) -> list[RgMatch]:
    matches: list[RgMatch] = []
    normalized_query = query.lower()

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in IGNORED_DIRS for part in path.parts):
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(lines, start=1):
            if normalized_query not in line.lower():
                continue

            relative_path = path.relative_to(root).as_posix()

            matches.append(
                RgMatch(
                    path = relative_path,
                    line_number=line_number,
                    line=line    
                )    
            )

            if len(matches) >= limit:
                return matches
    return matches