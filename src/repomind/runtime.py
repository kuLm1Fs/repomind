from repomind.retrieval.repo_loader import load_repo
from repomind.retrieval.chunker import chunk_files
from repomind.retrieval.retriever import retrieve

def ask(repo_path: str, question: str, settings) -> str:
    files = load_repo(repo_path)
    chunks = chunk_files(
        files,
        chunk_size=settings.CHUNK_SIZE,
        overlap=settings.CHUNK_OVERLAP,
        )
    retrieved_chunks = retrieve(
        question,
        chunks,
        top_k=settings.TOP_K,
        )
    
    if not retrieved_chunks:
        return "没有找到相关代码片段"
    
    lines = ["涉及代码片段：", ""]

    for index, result in enumerate(retrieved_chunks, start=1):
        chunk = result.chunk

        lines.append(
            f"{index}.{chunk.path}:{chunk.start_line}-{chunk.end_line}"
            )
        lines.append(f"score: {result.score}")
        lines.append("")
        lines.append(chunk.content)
        lines.append("")

    return "\n".join(lines)