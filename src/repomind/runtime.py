from repomind.retrieval.repo_loader import load_repo
from repomind.retrieval.chunker import chunk_files
from repomind.retrieval.retriever import retrieve
from repomind.agents.answer_agent import generate_answer
from repomind.agents.evaluator_agent import evaluate_answer

def ask(repo_path: str, question: str, settings) -> str:
    files = load_repo(repo_path)
    chunks = chunk_files(
        files,
        chunk_size=settings.CHUNK_SIZE,
        overlap=settings.CHUNK_OVERLAP,
    )

    top_k = settings.TOP_K
    retry_count = 0

    while True:
        retrieved_chunks = retrieve(
            question,
            chunks=chunks,
            top_k=settings.TOP_K,
        )

        if not retrieved_chunks:
            return "没有找到相关代码片段"

        answer = generate_answer(question, retrieved_chunks, settings)
        evaluation = evaluate_answer(answer)

        if evaluation.passed:
            return answer

        if retry_count >= settings.MAX_RETRY:
            return answer
        
        retry_count += 1
        top_k += settings.TOP_K