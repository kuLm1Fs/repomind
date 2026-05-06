from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess

@dataclass
class RgMatch:
    path: str
    line_number: int
    line: str

def rg_search(repo_path: str, query: str, limit: int = 20) -> list[RgMatch]:
    if not query.strip():
        return []
    
    if shutil.which("rg") is None:
        return []
    
    root = Path(repo_path)
    
    if not root.exists():
        raise FileNotFoundError(repo_path)
    
    if not root.is_dir():
        raise NotADirectoryError(repo_path)
    
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