from dataclasses import dataclass
from pathlib import Path

@dataclass
class FileSlice:
    path: str
    start_line: int
    end_line: int
    content: str

def read_file_range(
        repo_path: str,
        relative_path: str,
        start_line: int,
        end_line: int,
        )->FileSlice:
    root = Path(repo_path)
    file_path = root / relative_path

    if not file_path.exists():
        raise FileNotFoundError(relative_path)
    
    if not file_path.is_file():
        raise IsADirectoryError(relative_path)
    
    if start_line < 1:
        raise ValueError("start_line must be greater than or equal to 1")

    if end_line < start_line:
        raise ValueError("end_line must be greater than or equal to start_line")

    lines = file_path.read_text(encoding="utf-8").splitlines()

    start_index = start_line - 1
    end_index = min(end_line, len(lines))

    selected_lines = lines[start_index:end_index]

    return FileSlice(
        path = relative_path,
        start_line=start_line,
        end_line=start_line + len(selected_lines) - 1,
        content="\n".join(selected_lines)
        )