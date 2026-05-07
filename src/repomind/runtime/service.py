from repomind.retrieval.repo_loader import load_repo
from repomind.retrieval.chunker import chunk_files
from repomind.retrieval.retriever import retrieve
from repomind.agents.answer_agent import generate_answer
from repomind.agents.evaluator_agent import evaluate_answer
from repomind.runtime.trace import save_trace
from repomind.tools.runtime import run_tools

def ask(repo_path: str, question: str, settings) -> str:
    trace_data = {
    "repo_path": repo_path,
    "question": question,
    "retrieved_chunks": [],
    "tool_results": [],
    "answer": "",
    "evaluation": None,
    "retry_count": 0,
    }
    files = load_repo(repo_path)
    chunks = chunk_files(
        files,
        chunk_size=settings.CHUNK_SIZE,
        overlap=settings.CHUNK_OVERLAP,
    )

    top_k = settings.TOP_K
    retry_count = 0
    # 第一版工具结果不用随 retry 变化，retry 只是扩大 `top_k`。所以工具上下文跑一次即可
    tool_results = run_tools(repo_path=repo_path, question=question)
    trace_data["tool_results"] = tool_results

    while True:
        retrieved_chunks = retrieve(
            question,
            chunks=chunks,
            top_k=top_k,
        )
        trace_data["retrieved_chunks"] = retrieved_chunks

        if not retrieved_chunks:
            save_trace(settings.TRACE_DIR, trace_data)
            return "没有找到相关代码片段"

        answer = generate_answer(question, 
                                 retrieved_chunks, 
                                 settings,
                                 tool_results=tool_results)
        trace_data["answer"] = answer
        evaluation = evaluate_answer(answer)
        trace_data["evaluation"] = evaluation

        if evaluation.passed:
            save_trace(settings.TRACE_DIR, trace_data)
            return answer

        if retry_count >= settings.MAX_RETRY:
            save_trace(settings.TRACE_DIR, trace_data)
            return answer
        
        retry_count += 1
        trace_data["retry_count"] = retry_count
        top_k += settings.TOP_K