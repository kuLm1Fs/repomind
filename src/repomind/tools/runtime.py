from dataclasses import dataclass

from repomind.retrieval.scorer import extract_keywords
from repomind.tools.read_file_tool import read_file_range
from repomind.tools.rg_tool import rg_search


@dataclass
class ToolResult:
    tool_name: str
    path: str
    start_line: int
    end_line: int
    content: str


def run_tools(
    repo_path: str,
    question: str,
    max_results: int = 3,
) -> list[ToolResult]:
    keywords = extract_keywords(question)

    results: list[ToolResult] = []
    seen = set()

    for keyword in keywords:
        matches = rg_search(repo_path, keyword, limit=max_results)

        for match in matches:
            key = (match.path, match.line_number)

            if key in seen:
                continue

            seen.add(key)

            start_line = max(1, match.line_number - 10)
            end_line = match.line_number + 10

            file_slice = read_file_range(
                repo_path,
                match.path,
                start_line,
                end_line,
            )

            results.append(
                ToolResult(
                    tool_name="rg_read_file",
                    path=file_slice.path,
                    start_line=file_slice.start_line,
                    end_line=file_slice.end_line,
                    content=file_slice.content,
                )
            )

            if len(results) >= max_results:
                return results

    return results
