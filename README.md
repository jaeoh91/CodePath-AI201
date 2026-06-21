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

#### `Project-1` : [GT F-1 Visa Policy Assistant](./Week-1/Project-1/)

| | |
|---|---|
| **About** | RAG assistant that answers F-1 visa policy questions for Georgia Tech international students, grounded in 25 official GT ISSS policy documents with inline Markdown citations linking to source pages |
| **Technical concepts** | Structure-aware HTML scraping (tag-by-tag to preserve heading/paragraph boundaries) · recursive character chunking with orphaned-heading post-processing · cosine distance threshold gating · citation injection via `Source` + `URL` chunk headers · grounded system prompt with strict refusal fallback · retrieval tracing & failure case analysis (AVR exception miss, chunk boundary gap) |
| **Stack** | Python 3.12 · ChromaDB · `sentence-transformers` (`all-MiniLM-L6-v2`) · Groq / `llama-3.3-70b-versatile` · `langchain-text-splitters` · Gradio |

### `Week-2`: Multi-Tool Agents

#### `Lab-2` : [Plant Advisor](./Week-2/Lab-2/)

| | |
|---|---|
| **About** | Multi-tool agent that looks up plant care data and seasonal context, then synthesizes grounded houseplant advice |
| **Technical concepts** | Tool-calling agent architecture (when to use agents vs. RAG) · OpenAI-compatible function schema design · multi-turn agent orchestration loops · tool dispatch & result message protocol · structured JSON data retrieval · production loop safeguards (`MAX_TOOL_ROUNDS`) · graceful degradation for missing data |
| **Stack** | Python 3.12 · Groq / `llama-3.3-70b-versatile` (tool calling) · structured JSON data (`plants.json`, `seasons.json`) · Gradio |

#### `Project-2` : [FitFindr](./Week-2/Project-2/)

| | |
|---|---|
| **About** | Thrift-shopping agent that takes a natural-language request (e.g. *"vintage graphic tee under $30"*), finds a matching secondhand listing from a mock 40-item dataset, suggests a complete outfit paired with the user's wardrobe, and writes a shareable Instagram/TikTok caption for the look |
| **Technical concepts** | Gated linear planning loop with early-return branch on empty search results · session state management (pure tools, state threaded through a single shared dict) · LLM query parsing with regex fallback for offline resilience · keyword-ranked listing search · tool isolation (each tool is a pure function — no session coupling) |
| **Stack** | Python 3.12 · Groq / `llama-3.3-70b-versatile` (query parsing, outfit suggestion, fit-card generation) · mock JSON dataset (40 listings + wardrobe) · pytest (offline tool tests with Groq stub) · Gradio |


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
│   └── Project-1/    # GT F-1 Visa Policy Assistant — domain RAG with citations
│
└── Week-2/
    ├── Lab-2/        # Plant Advisor — multi-tool agent
    └── Project-2/    # FitFindr — thrift-shopping planning-loop agent
```

---

