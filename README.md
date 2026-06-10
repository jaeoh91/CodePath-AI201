# Applied AI Engineering Portfolio

Projects from [CodePath AI201](https://www.codepath.org/): a hands-on course in building production-ready LLM applications. 

This README contains a high-level overview, open each project's README for architecture, technical decisions, and runnable demos.

---

## Projects

### `Week-1`: Production-Ready RAG

#### `Lab-1` : [RulesBot](./Week-1/Lab-1/)

| | |
|---|---|
| **About** | RAG chatbot that answers board game rules from source documents, with citations and explicit refusal when context is missing |
| **Technical concepts** | End-to-end RAG pipeline design (ingest → retrieve → generate) · chunking tradeoffs (window size, overlap, noise filtering) · vector similarity search & cosine distance thresholds · fail-closed retrieval gating · prompt engineering for grounded, cited outputs · hybrid local embeddings + API inference · adversarial safety testing (jailbreaks, injection, citation integrity) |
| **Stack** | Python 3.12 · ChromaDB (persistent vector store) · `sentence-transformers` (`all-MiniLM-L6-v2`, local embeddings) · Groq / `llama-3.3-70b-versatile` · Gradio |

#### `Project-1` : *Coming soon*

| | |
|---|---|
| **About** | *Placeholder — personal project extending Week 1 concepts. Description TBD.* |
| **Technical concepts** | *Placeholder — e.g., advanced retrieval, evaluation pipelines, or production deployment.* |
| **Stack** | *Placeholder — TBD.* |

### `Week-2`: Multi-Tool Agents

#### `Lab-2` : [Plant Advisor](./Week-2/Lab-2/)

| | |
|---|---|
| **About** | Multi-tool agent that looks up plant care data and seasonal context, then synthesizes grounded houseplant advice |
| **Technical concepts** | Tool-calling agent architecture (when to use agents vs. RAG) · OpenAI-compatible function schema design · multi-turn agent orchestration loops · tool dispatch & result message protocol · structured JSON data retrieval · production loop safeguards (`MAX_TOOL_ROUNDS`) · graceful degradation for missing data |
| **Stack** | Python 3.12 · Groq / `llama-3.3-70b-versatile` (tool calling) · structured JSON data (`plants.json`, `seasons.json`) · Gradio |

#### `Project-2` : *Coming soon*

| | |
|---|---|
| **About** | *Placeholder — personal project extending Week 2 concepts. Description TBD.* |
| **Technical concepts** | *Placeholder — e.g., multi-agent workflows, memory, or external API integrations.* |
| **Stack** | *Placeholder — TBD.* |


---

## Quick Start

Each project is self-contained with its own `requirements.txt` and `.env.example`.

```bash
# Example: run RulesBot
cd Week-1/Lab-1
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add API keys
python app.py
```

---

## Repository Structure

```
CodePath AI201/
├── Week-1/
│   ├── Lab-1/        # RulesBot — production-ready RAG
│   └── Project-1/    # Coming soon
│
└── Week-2/
    ├── Lab-2/        # Plant Advisor — multi-tool agent
    └── Project-2/    # Coming soon
```

---

