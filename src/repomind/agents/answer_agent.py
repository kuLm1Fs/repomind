from repomind.llm.client import complete


def build_context(retrieved_chunks) -> str:
    blocks = []

    for result in retrieved_chunks:
        chunk = result.chunk

        blocks.append(
            "\n".join(
                [
                    f"文件：{chunk.path}",
                    f"行号：{chunk.start_line}-{chunk.end_line}",
                    "代码：",
                    chunk.content,
                ]
            )
        )

    return "\n\n---\n\n".join(blocks)


def build_tool_context(tool_results) -> str:
    tool_results = tool_results or []
    blocks = []

    for result in tool_results:
        blocks.append(
            "\n".join(
                [
                    f"工具：{result.tool_name}",
                    f"文件：{result.path}",
                    f"行号：{result.start_line}-{result.end_line}",
                    "代码：",
                    result.content,
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)


def generate_answer(
    question: str,
    retrieved_chunks,
    settings,
    tool_results=None,
) -> str:
    context = build_context(retrieved_chunks)
    tool_context = build_tool_context(tool_results)

    messages = [
        {
            "role": "system",
            "content": (
                "你是 RepoMind，一个本地代码库分析 Agent。"
                "你只能基于提供的代码上下文回答问题。"
                "如果上下文不足，请明确说明。"
                "回答必须包含：涉及文件、实现流程、证据"
            ),
        },
        {
            "role": "user",
            "content": (
                f"问题：{question}\n\n"
                f"检索上下文：\n{context}\n\n"
                f"工具补充上下文：\n{tool_context}"
            ),
        },
    ]

    return complete(messages, settings)
