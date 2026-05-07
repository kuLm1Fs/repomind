# run_tools(repo_path: str, question: str) -> list[ToolResult]

from dataclasses import dataclass
from repomind.retrieval.scorer import extract_keywords
from repomind.tools.rg_tool import rg_search as rg
from repomind.tools.read_file_tool import read_file_range

@dataclass
class ToolResult:
    tool_name: str
    path: str
    start_line: int
    end_line: int
    content: str

def run_tools(repo_path: str
              , question: str
              , max_results: int =3) -> list[ToolResult]:
              keywords = extract_keywords(question)

              results: list[ToolResult] =[]
              seen = set()

              for keyword in keywords:
                    matches = rg.search(repo_path, keyword, limit = max_results)

                    for match in matches:
                        key = (match.path, match.line_number)