from repomind.retrieval.repo_loader import load_repo
from repomind.retrieval.chunker import chunk_files
from repomind.retrieval.retriever import retrieve
from repomind.agents.answer_agent import generate_answer
from repomind.agents.evaluator_agent import evaluate_answer
from repomind.runtime.trace import save_trace
from repomind.tools.runtime import run_tools
from repomind.runtime.state import RuntimeState, state_to_trace_data


def ask(repo_path: str, question: str, settings) -> str:
    state = RuntimeState(
        repo_path=repo_path,
        question=question    
    )

    state.files = load_repo(repo_path)
    state.chunks = chunk_files(
        state.files,
        chunk_size=settings.CHUNK_SIZE,
        overlap=settings.CHUNK_OVERLAP,
    )

    top_k = settings.TOP_K
    retry_count = 0

    # First pass: tool context is independent of retry; retry only expands top_k.
    tool_results = run_tools(repo_path=repo_path, question=question)
    state.tool_results = tool_results

    while True:
        retrieved_chunks = retrieve(
            question,
            chunks=state.chunks,
            top_k=top_k,
        )
        state.retrieved_chunks = retrieved_chunks

        if not retrieved_chunks:
            save_trace(settings.TRACE_DIR, state)
            return "没有找到相关代码片段"

        answer = generate_answer(
            question,
            state.retrieved_chunks,
            settings,
            tool_results=state.tool_results,
        )
        state.answer = answer
        evaluation = evaluate_answer(answer)
        state.evaluation = evaluation

        if evaluation.passed:
            save_trace(settings.TRACE_DIR, state_to_trace_data(state))
            return answer

        if retry_count >= settings.MAX_RETRY:
            save_trace(settings.TRACE_DIR, state_to_trace_data(state))
            return answer

        retry_count += 1
        state.retry_count = retry_count
        top_k += settings.TOP_K
