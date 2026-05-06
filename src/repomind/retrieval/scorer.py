from src.repomind.retrieval.chunker import CodeChunk
import re

QUERY_EXPANSIONS = {
    "登录": ["login", "auth", "authenticate", "jwt", "token"],
    "登陆": ["login", "auth", "authenticate", "jwt", "token"],
    "认证": ["auth", "authenticate", "authentication", "token", "jwt"],
    "鉴权": ["auth", "authorization", "permission", "token"],
    "用户": ["user", "account"],
    "接口": ["api", "controller", "route", "handler"],
    "配置": ["config", "settings", "env"],
    "数据库": ["db", "database", "sql", "model"],
}

def extract_keywords(question: str) -> list[str]:
    normalized = question.lower()

    keywords : list[str] = []

    # 提取英文代码常见词：login, jwt, auth_service, user123
    keywords.extend(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", normalized))

    # 中文问题很难直接和英文代码匹配，所以做少量人工扩展
    for chinese_word, expanded_words in QUERY_EXPANSIONS.items():
        if chinese_word in question:
            keywords.append(chinese_word)
            keywords.extend(expanded_words)

    # 去重，同时保留顺序
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        if keyword not in seen:
            seen.add(keyword)
            unique_keywords.append(keyword)

    return unique_keywords

def score_chunk(question: str, chunk: CodeChunk) -> int:
    keywords = extract_keywords(question)

    content = chunk.content.lower()
    path = chunk.path.lower()

    score = 0

    for keyword in keywords:
        normailized_keyword = keyword.lower()

        content_hits = content.count(normailized_keyword)
        path_hits = path.count(normailized_keyword)

        score += content_hits
        score += path_hits * 3

    return score