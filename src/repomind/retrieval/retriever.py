from dataclasses import dataclass

from repomind.retrieval.chunker import CodeChunk
from repomind.retrieval.scorer import score_chunk

@dataclass
class RetrievedChunk:
    chunk: CodeChunk
    score: int

def retrieve(
        question: str,
        chunks: list[CodeChunk],
        top_k: int = 5,
        )-> list[RetrievedChunk]:
    results: list[RetrievedChunk] = []

    for chunk in chunks:
        score = score_chunk(question, chunk)

        if score <= 0:
            continue
    
        results.append(RetrievedChunk(chunk=chunk,score=score))

    results.sort(key = lambda result: result.score, reverse= True)

    return results[:top_k]