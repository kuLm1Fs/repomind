from dataclasses import dataclass, field
from typing import Any

@dataclass
class RuntimeState:
    repo_path: str
    question: str

    files: list[Any] = field(default_factory=list)
    chunks: list[Any] = field(default_factory=list)
    retrieved_chunks: list[Any] = field(default_factory=list)
    tool_results: list[Any] = field(default_factory=list)

    answer: str = ""
    evaluation: Any = None
    retry_count: int = 0

def state_to_trace_data(state: RuntimeState) -> dict:
    return {
        "repo_path": state.repo_path,
        "question": state.question,
        "retrieved_chunks": state.retrieved_chunks,
        "tool_results": state.tool_results,
        "answer": state.answer,
        "evaluation": state.evaluation,
        "retry_count": state.retry_count,
    }