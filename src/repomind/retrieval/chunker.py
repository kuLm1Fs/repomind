from dataclasses import dataclass
from repomind.retrieval.repo_loader import RepoFile
from pathlib import Path

@dataclass
class CodeChunk:
    path: str           # 文件相对路径
    start_line: int     # chunk 起始行号，从 1 开始
    end_line: int       # chunk结束行号
    content: str        # chunk文本内容

def chunk_file(file: RepoFile, chunk_size: int = 80, overlap: int = 10) -> list[CodeChunk]:
    lines = file.content.splitlines()

    if not lines:
        return []
    
    chunks : list[CodeChunk] = []
    step = chunk_size - overlap

    start = 0

    while start < len(lines):
        end = min(start + chunk_size, len(lines))
        chunk_lines = lines[start:end]

        chunks.append(
                CodeChunk(
                    path=file.path,
                    start_line=start + 1,
                    end_line=end,
                    content="\n".join(chunk_lines),
                    )
            )
        if end == len(lines):
            break

        start += step
    
    return chunks

def chunk_files(files: list[RepoFile]
                , chunk_size: int = 80
                , overlap: int = 10) -> list[CodeChunk]:
    chunks : list[CodeChunk] = []

    for file in files:
        chunks.extend(chunk_file(file, chunk_size, overlap))

    return chunks