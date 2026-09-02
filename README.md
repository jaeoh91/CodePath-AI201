# Applied AI Engineering Portfolio

Projects from [CodePath AI201](https://www.codepath.org/): a hands-on course in building production-ready LLM applications. 

This README contains a high-level overview, open each project's README for architecture, technical decisions, and runnable demos.

> **Course completed — September 2026.** 7 weeks · 7 projects · full stack covered: RAG pipelines → multi-tool agents → fine-tuning → detection backends → service-layer debugging → simulated OSS code review → AI safety red-teaming.

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

### `Week-3`: Fine-Tuned Text Classification

#### `Project-3` : [TakeMeter](./Week-3/Project-3/)

| | |
|---|---|
| **About** | Fine-tuned DistilBERT classifier that labels Hacker News comments as `technical_insight`, `opinion_or_critique`, or `joke_or_meta`, with a zero-shot LLaMA-3.3-70B baseline for comparison and a Gradio web UI for live classification |
| **Technical concepts** | Fine-tuning `distilbert-base-uncased` for 3-class sequence classification · stratified train/val/test split (70/15/15) · class-weighted cross-entropy loss via custom `WeightedTrainer` · β-sweep for weight-strength selection on validation macro-F1 · `load_best_model_at_end` with macro-F1 as model-selection metric · zero-shot baseline (LLaMA-3.3-70B, Groq API) · complementarity analysis (same accuracy, only 13/30 shared predictions) · dataset curation: label audit, 7 dropped no-fit rows, 16 synthetic boundary examples (train-only) |
| **Stack** | Python 3.12 · HuggingFace Transformers + `distilbert-base-uncased` · Groq / `llama-3.3-70b-versatile` (baseline) · scikit-learn · uv · Gradio |

---

### `Week-4`: AI-Content Detection Backend

#### `Project-4` : [Provenance Guard](./Week-4/Project-4/)

| | |
|---|---|
| **About** | Flask backend that classifies submitted creative text as likely AI-generated, likely human-written, or uncertain — with confidence scoring, a transparency label, an appeals workflow, rate limiting, and a structured audit log |
| **Technical concepts** | Dual-signal detection (sentence-length-variation "burstiness" + MATTR lexical diversity/stock-phrase heuristic) that decides the label, plus a third LLM-read signal kept advisory-only so the core score stays deterministic · disagreement axis (`abs(signal_1 - signal_2)`) separating genuine middle-ground from conflicting evidence · ordered banding rule (guard fired → disagreement too high → mean bands) · rate limiting via Flask-Limiter (10/min, 100/day) · appeals workflow (file → reviewer queue → resolve) reusing the submission store · structured JSONL audit logging · calibration against a hand-labeled fixture set that surfaced a counter-intuitive result (MATTR ran backwards vs. the original hypothesis on modern LLM output) |
| **Stack** | Python 3.11+ · Flask · Flask-Limiter · Groq / `llama-3.3-70b-versatile` (advisory signal) · uv · pytest |

---

### `Week-5`: Debugging a Flask + SQLAlchemy Service

#### `Lab-5` : [BookClub](./Week-5/Lab-5/)

| | |
|---|---|
| **About** | Reading-list starter app where club members track books, log reading progress, and view stats (streak, books finished this month, total pages read) |
| **Technical concepts** | Flask app-factory pattern · SQLAlchemy models & relationships (`User`, `Book`, `ReadingEvent`) · thin routes / service-layer separation · streak and aggregate-stats calculation over event history |
| **Stack** | Python · Flask · Flask-SQLAlchemy · SQLite |

#### `Project-5` : [Mixtape Bug Hunt](./Week-5/Project-5/)

| | |
|---|---|
| **About** | Debugging exercise on a Flask + SQLAlchemy social music API (share songs, build playlists, track listening streaks) — reproduced, root-caused, and fixed all five reported service-layer bugs with one conventional commit per fix and full RCA write-ups |
| **Technical concepts** | Bug reproduction discipline (symptom → route → service → root cause) before editing · SQLAlchemy query literacy (join-caused row multiplication, ORM uniquing vs. raw row counts) · calendar/streak and recency-window boundary reasoning (off-by-one and cutoff bugs) · intentional side effects (notifications on write paths) · pytest regression coverage per fix (13 passing) · RCA-style technical writing |
| **Stack** | Python · Flask · Flask-SQLAlchemy · pytest · SQLite |

---

### `Week-6`: Simulated Open-Source Code Review

#### `Project-6` : [CineLog](./Week-6/Project-6/)

| | |
|---|---|
| **About** | Flask + SQLAlchemy film-tracking API (collection + watchlist); simulated an open-source contribution by taking a half-finished watchlist feature through maintainer review feedback, a UUID-migration rebase, commit-history cleanup, and a merge to `main` |
| **Technical concepts** | Responding to real code-review feedback (naming conventions, duplicate-entry protection, test coverage, design tradeoffs) · rebasing a feature branch onto a moving `main` and resolving conflicts · interactive rebase (`reword`/`edit`/split) with `--force-with-lease` · service-layer design decisions owned and documented (default visibility, sort order) · pytest fixtures over in-memory SQLite, including error-path assertions |
| **Stack** | Python 3.14 · Flask · Flask-SQLAlchemy · pytest · SQLite |

---

### `Week-7`: AI Safety Red-Teaming (Tier 3 OSS Contribution)

#### `Project-7` : [PathReview — Prompt Injection Red-Team Suite](./Week-7/Project-7/)

| | |
|---|---|
| **About** | Tier 3 open-source contribution to [ascherj/pathreview](https://github.com/ascherj/pathreview) — an AI-powered portfolio review assistant. Authored a curated 31-fixture red-team corpus for the existing `PromptDefense` safety layer, a parametrized `tests/security/` test suite, and a new unconditional `test-security` CI job, so future changes to `safety/` can't silently weaken the injection defense. ([PR #1016](https://github.com/ascherj/pathreview/pull/1016)) |
| **Technical concepts** | White-box fixture design (regex-driven case selection, boundary probing, whitespace/case variants) · threat-model-driven corpus sourcing (attacks styled as PathReview's real ingestion surfaces: resume fields, README snippets, GitHub bios) · `pytest.mark.parametrize` with deterministic sorted-glob fixture discovery · `known_gaps` fixtures that explicitly document a real leading-`\n` detection bypass rather than hiding it · extending GitHub Actions CI with a path-independent security job · investigative findings: `PromptDefense` is fully tested but never wired into the live app (documented, not fixed, per issue scope) |
| **Stack** | Python 3.11 · pytest · GitHub Actions · `safety/prompt_defense.py` (PathReview upstream) · pre-commit (`ruff`, `black`, `mypy`) |

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
├── Week-2/
│   ├── Lab-2/        # Plant Advisor — multi-tool agent
│   └── Project-2/    # FitFindr — thrift-shopping planning-loop agent
│
├── Week-3/
│   └── Project-3/    # TakeMeter — Hacker News discourse classifier (fine-tuned DistilBERT)
│
├── Week-4/
│   └── Project-4/    # Provenance Guard — AI-content detection backend
│
├── Week-5/
│   ├── Lab-5/        # BookClub — Flask + SQLAlchemy reading tracker
│   └── Project-5/    # Mixtape Bug Hunt — service-layer debugging exercise
│
├── Week-6/
│   └── Project-6/    # CineLog — simulated OSS code review (watchlist feature)
│
└── Week-7/
    └── Project-7/    # PathReview — AI safety red-team suite (Tier 3 OSS contribution)
```

---

