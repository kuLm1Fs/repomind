# RepoMind — Codebase Agent Runtime

## 你的角色

你是这个项目的 coding agent。目标是在 1 周内实现一个最小可用的代码库分析 Agent Runtime。

不要做大而全，不要过度设计。优先完成可运行闭环。

---

## 项目定位

RepoMind 是一个本地代码库分析 Agent Runtime。

它不是普通聊天机器人，而是用于回答：

```bash
repomind ask ./demo-repo "登录功能是怎么实现的？"
```
期待输出
```
涉及文件：
- UserController.java
- AuthService.java
- JwtUtil.java

实现流程：
1. Controller 接收登录请求
2. Service 校验用户名密码
3. JwtUtil 生成 JWT
4. Interceptor 校验 token

证据：
- UserController.java:23-51
- AuthService.java:10-43
```

核心能力：

扫描本地代码仓库
对代码按行切 chunk
基于关键词和路径进行代码检索
调用 LLM 根据代码上下文回答问题
支持简单 Tool Runtime：rg 搜索、局部文件读取
支持 Answer Evaluator
支持一次 Retry
保存 runtime trace

技术栈
Python 3.12+
uv
typer
rich
pydantic
python-dotenv
openai
ripgrep，可选，作为外部命令 rg

暂时不要引入：

LangGraph
Milvus
pgvector
Redis
MCP
Docker Sandbox
UI
多 Agent

这些作为后续扩展写在 README 即可。

项目结构
```
repomind/
├── AGENTS.md
├── README.md
├── .env.example
├── pyproject.toml
├── src/
│   └── repomind/
│       ├── main.py
│       ├── runtime.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── llm/
│       │   ├── __init__.py
│       │   └── client.py
│       ├── retrieval/
│       │   ├── __init__.py
│       │   ├── repo_loader.py
│       │   ├── chunker.py
│       │   ├── retriever.py
│       │   └── scorer.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── rg_tool.py
│       │   └── read_file_tool.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── answer_agent.py
│       │   └── evaluator_agent.py
│       └── runtime/
│           ├── __init__.py
│           └── trace.py
└── tests/
```

.env 配置

创建 .env.example：

```
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini

TOP_K=5
CHUNK_SIZE=80
CHUNK_OVERLAP=10
MAX_RETRY=1
TRACE_DIR=.repomind/traces
```
src/repomind/config/settings.py 负责读取环境变量。


CLI 目标

实现命令：

uv run repomind ask ./demo-repo "登录功能是怎么实现的？"

main.py 使用 Typer。

CLI 参数：

repo_path: str
question: str