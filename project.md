# RepoMind — Codebase Agent Runtime

## 项目定位

### 一句话介绍

基于 Agent Workflow 的代码库分析 Runtime，支持 Repo Retrieval、Tool Calling、Answer Evaluation 与 Retry Workflow，实现对本地代码仓库的自动分析与上下文理解。

---

# 项目目标

输入：

```bash
repomind ask ./demo-repo "登录功能是怎么实现的？"

输出：

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
核心思想

RepoMind 并不是聊天机器人。

核心问题：

“LLM 如何理解大型代码仓库”

项目重点：

Retrieval Engineering
Context Engineering
Agent Workflow
Tool Runtime
Evaluation & Retry
Runtime Workflow
Question
    ↓
Repo Retrieval
    ↓
Tool Decision
    ↓
Tool Execution
    ↓
Answer Generation
    ↓
Answer Evaluation
    ↓
Retry / Final Output
核心模块
1. Repo Retrieval System
功能

根据用户问题：

“登录功能怎么实现？”

自动：

检索相关文件
找到关键函数
返回相关代码上下文
文件扫描

支持：

SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".go",
    ".js",
    ".ts",
    ".md",
    ".yml",
    ".yaml"
}

忽略：

.git
node_modules
.venv
target
dist
__pycache__
Chunking

采用：

80 行 chunk
10 行 overlap

Metadata：

{
    "path": "src/auth/service.py",
    "start_line": 1,
    "end_line": 80,
    "content": "..."
}
Retrieval Strategy

第一版：

Keyword Retrieval

Score：

score =
关键词命中次数
+
路径命中权重

例如：

auth/login/jwt

路径额外加分。

后续扩展
Hybrid Retrieval
Embedding Search
MMR
Rerank
Metadata Filter
2. Workflow Runtime

采用：

LangGraph
Workflow
Question
→ Retrieve
→ Tool
→ Generate
→ Evaluate
→ Retry
Graph State
class GraphState(TypedDict):
    repo_path: str
    question: str
    retrieved_chunks: list
    tool_results: list
    answer: str
    retry_count: int
Conditional Edge

例如：

如果 evaluator 判断回答不足
→ retry retrieval
3. Tool Runtime
核心思想

普通 RAG 不够。

Agent 需要：

动态获取上下文
Tool 设计
rg_tool
rg "jwt"

用于：

搜索 symbol
搜索关键字
定位文件
read_file_tool

读取：

指定文件 + 指定行范围
Tool Workflow
retrieval 不足
→ tool search
→ 补充上下文
→ 重新回答
4. Answer Evaluator
为什么需要

LLM 容易：

漏文件
漏流程
hallucination
Evaluator 检查

是否包含：

涉及文件
核心流程
代码证据
函数说明
Retry Workflow

如果失败：

扩大 topK
→ 重新 retrieval
→ regenerate
项目目录结构
repomind/
├── src/
│   └── repomind/
│       ├── main.py
│       ├── runtime.py
│       │
│       ├── retrieval/
│       │   ├── repo_loader.py
│       │   ├── chunker.py
│       │   ├── retriever.py
│       │   ├── scorer.py
│       │
│       ├── workflow/
│       │   ├── graph.py
│       │   ├── state.py
│       │
│       ├── tools/
│       │   ├── rg_tool.py
│       │   ├── read_file_tool.py
│       │
│       ├── agents/
│       │   ├── answer_agent.py
│       │   ├── evaluator_agent.py
│       │
│       ├── runtime/
│       │   ├── trace.py
│       │   ├── session.py
│       │
│       └── llm/
│           ├── client.py
│
├── .env
├── README.md
└── pyproject.toml
一周开发计划
Day1

CLI + Project Skeleton

实现：

repomind ask ./repo "问题"
Day2

Repo Loader + Chunking

实现：

仓库扫描
chunk overlap
metadata
Day3

Retrieval Runtime

实现：

keyword retrieval
path scoring
topK retrieval
Day4

LLM Generation

实现：

chunk prompt
structured answer
Day5

Tool Runtime

实现：

rg_tool
read_file_tool
Day6

Evaluator + Retry

实现：

answer validation
retry workflow
Day7

Trace + README + Polish

实现：

trace logging
workflow visualization
README
简历描述
项目亮点
1. Retrieval Engineering

解决：

代码仓库上下文噪音

采用：

keyword retrieval
path scoring
topK control
2. Context Engineering

解决：

token explosion

采用：

chunk overlap
retrieval filtering
limited topK
3. Tool Runtime

解决：

retrieval 不足

通过：

rg search
file reading

动态补充上下文。

4. Evaluation + Retry

解决：

LLM hallucination

采用：

answer evaluator
retry workflow
后续扩展方向
Retrieval
Hybrid Search
Embedding Retrieval
MMR
Rerank
Memory
Recent Memory
Semantic Memory
Deduplication
Runtime
Trace Visualization
Session Runtime
Async Workflow
Tooling
Git Tool
AST Parser
Dependency Graph
简历描述
RepoMind：代码库分析 Agent Runtime

- 基于 LangGraph 设计代码库分析 Agent Workflow，实现 Retrieval、Tool Calling、Evaluation 与 Retry Runtime
- 实现 Repo Retrieval System，支持代码 chunking、关键词检索与 path-aware scoring
- 设计 Tool Runtime，支持 ripgrep 搜索与局部文件读取，增强 Agent 动态上下文获取能力
- 引入 Evaluator + Retry Workflow，对缺少代码证据或流程说明的回答自动重试
- 实现 Runtime Trace Logging，记录 retrieval、tool call、retry 与 final answer，提升 Agent 可观测性
面试高频问题
1. 为什么不用纯向量检索？

代码仓库：

文件路径有语义
symbol 有语义
import 有语义

因此：

path-aware retrieval

优于纯 embedding retrieval。

2. 为什么需要 Tool Runtime？

静态 retrieval 不一定足够。

Agent 需要：

动态获取上下文

因此：

rg
read_file

用于补充 retrieval。

3. 为什么要 chunk overlap？

避免：

函数或逻辑被切断

导致上下文丢失。

4. 为什么 topK 不宜过大？

因为：

token budget
retrieval noise
Lost in the Middle
5. 为什么需要 evaluator？

LLM 回答可能：

漏文件
漏流程
hallucination

因此需要：

Answer Validation
项目体现的能力

本项目体现：

Agent Workflow
Retrieval Engineering
Tool Calling
Runtime Design
Context Engineering
LLM Evaluation
Retry Mechanism

而不仅仅是：

调用 OpenAI API