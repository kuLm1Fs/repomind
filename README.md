# RepoMind

RepoMind is a local codebase analysis agent runtime.

It scans a local repository, chunks source files, retrieves relevant code, uses an OpenAI-compatible LLM to answer questions, evaluates the answer, retries once when needed, and saves a runtime trace.

## Usage

Create `.env`:

```env
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini

TOP_K=5
CHUNK_SIZE=80
CHUNK_OVERLAP=10
MAX_RETRY=1
TRACE_DIR=.repomind/traces
```
# Run:
```bash
uv run repomind ask ./demo-repo "登录功能是怎么实现的？"
```

OpenAI-Compatible Providers
DeepSeek example:
```
OPENAI_API_KEY=your-deepseek-key
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-v4-flash
``` 

# Current Capabilities
- Scan local repositories
- Ignore common dependency/build - directories
- Chunk files by line range
- Keyword/path-based retrieval
- rg search tool
- file range read tool
- OpenAI-compatible LLM answer generation
- rule-based answer evaluation
- one retry
- runtime trace JSON
# Not Included Yet
- LangGraph
- vector database
- embeddings
- Redis
- MCP
- Docker sandbox
- UI
- multi-agent workflow

# TRACE
Runtime traces are saved to: 
`.repomind/traces/`