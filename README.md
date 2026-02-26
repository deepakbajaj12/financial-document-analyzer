# Financial Document Analyzer

A multi-agent AI system built with **CrewAI** and **FastAPI** that analyzes financial PDF documents (e.g., 10-K filings, quarterly reports) to provide investment insights, risk assessments, and document verification.

## Features

- **Multi-Agent System** — Four specialized AI agents working sequentially:
  - **Document Verifier** — Validates the uploaded PDF is a real financial report
  - **Financial Analyst** — Extracts key metrics and answers user queries
  - **Investment Advisor** — Provides actionable investment recommendations
  - **Risk Assessor** — Identifies and rates potential risks
- **PDF Processing** — Extracts text from uploaded financial documents using `pypdf`
- **REST API** — Clean FastAPI interface with Swagger docs at `/docs`
- **LLM Flexibility** — Supports Google Gemini (preferred) or OpenAI GPT as the backing LLM

## Prerequisites

- **Python 3.10 or 3.11** (3.11 recommended; CrewAI is unstable on 3.13+)
- A valid **Google Gemini API key** or **OpenAI API key**

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd financial-document-analyzer-debug
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Copy `.env.example` to `.env` and fill in your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_API_KEY=your_serper_api_key_here
   ```
   - If `GOOGLE_API_KEY` is set → uses **Gemini 1.5 Flash**
   - Otherwise falls back to **OpenAI GPT-3.5 Turbo**

## Usage

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```
   Server runs at `http://127.0.0.1:8000`

2. **Analyze a document** via Swagger UI:
   - Open `http://127.0.0.1:8000/docs`
   - Use the `POST /analyze` endpoint
   - Upload a PDF and optionally provide a query

3. **Analyze via cURL**:
   ```bash
   curl -X POST http://127.0.0.1:8000/analyze \
     -F "file=@data/TSLA-Q2-2025-Update.pdf" \
     -F "query=What are the key financial risks?"
   ```

## API Documentation

### `GET /`
Health check endpoint.
```json
{"message": "Financial Document Analyzer API is running"}
```

### `POST /analyze`
Analyze a financial PDF document.

| Parameter | Type       | Required | Description                                    |
|-----------|------------|----------|------------------------------------------------|
| `file`    | File (PDF) | Yes      | The financial document to analyze              |
| `query`   | String     | No       | Specific question (default: general analysis)  |

**Response** (200):
```json
{
  "status": "success",
  "query": "What are the key financial risks?",
  "analysis": "...(detailed multi-agent analysis)...",
  "file_processed": "TSLA-Q2-2025-Update.pdf"
}
```

**Error** (500):
```json
{
  "detail": "Error processing financial document: ..."
}
```

---

## Bugs Found and Fixes

### Deterministic Bugs

| # | File | Bug | Fix |
|---|------|-----|-----|
| 1 | `tools.py` | **Double-escaped newline** — `"\\n"` produced literal `\n` text instead of actual newlines when reading PDF pages | Changed to `"\n"` so extracted text has proper line breaks |
| 2 | `tools.py` | **Wrong `tool` import** — `from crewai_tools import tool` was commented out; fallback used `langchain_core.tools.tool` which creates `StructuredTool` objects incompatible with CrewAI's `Agent` pydantic model (`ValidationError: Input should be a valid dictionary or instance of BaseTool`) | Changed to `from crewai.tools import tool` which produces CrewAI-compatible tool objects |
| 3 | `tools.py` | **SerperDevTool replaced with broken stub** — the original import was commented out and replaced with a dummy class that returned static strings | Restored proper `from crewai_tools import SerperDevTool` with graceful fallback |
| 4 | `agents.py` | **Missing spaces in string concatenation** — adjacent string literals like `"strategies."` `"You always"` became `"strategies.You always"` (no space) in all four agent backstories | Added trailing spaces to each string segment |
| 5 | `agents.py` | **LLM wrapper incompatibility** — used `langchain_openai.ChatOpenAI` / `langchain_google_genai.ChatGoogleGenerativeAI` which are LangChain wrappers not compatible with CrewAI v1.x agent model | Replaced with `crewai.LLM` which is CrewAI's native LLM wrapper |
| 6 | `task.py` | **Missing word in description** — `"at {file_path} provide"` was missing `"and"` → grammatically broken prompt sent to the LLM | Fixed to `"at {file_path} and provide"` |
| 7 | `main.py` | **Blocking async event loop** — `run_crew()` (synchronous, long-running) was called directly inside an `async` endpoint, freezing the entire server for all clients during analysis | Wrapped with `await asyncio.to_thread(run_crew, ...)` to run in a thread pool |
| 8 | `requirements.txt` | **Conflicting version pins** — strict pins like `crewai==0.130.0`, `pydantic==1.10.13`, `click==8.1.7` conflicted with each other, preventing installation | Replaced with minimum version constraints (e.g., `crewai>=1.9.0`) |
| 9 | `requirements.txt` | **Missing `google-genai` dependency** — CrewAI's native Gemini provider requires the `google-genai` package, which was not listed | Added `google-genai>=1.0.0` |

### Inefficient Prompts

| # | File | Issue | Fix |
|---|------|-------|-----|
| 1 | `agents.py` | Agent backstories were vague one-liners without clear behavioral instructions | Expanded backstories with specific expertise areas, working principles, and output expectations |
| 2 | `task.py` | Task descriptions lacked step-by-step instructions — LLM had no structured process to follow | Added numbered steps to each task description (e.g., "1. Read the document... 2. Extract key metrics...") |
| 3 | `task.py` | `expected_output` fields were generic ("A detailed answer") with no format guidance | Made expected outputs specific (e.g., "Include specific numbers, percentages, and data points from the document") |
| 4 | `task.py` | Verification task was defined last but should run first in the sequential pipeline | Reordered task definitions to match execution order: verification → analysis → investment → risk |

## Project Structure

```
financial-document-analyzer-debug/
├── .env                 # API keys (not committed)
├── .env.example         # Template for .env
├── agents.py            # CrewAI agent definitions (4 agents)
├── task.py              # CrewAI task definitions (4 tasks)
├── tools.py             # Custom tools (PDF reader, search, etc.)
├── main.py              # FastAPI application & crew orchestration
├── requirements.txt     # Python dependencies
├── data/                # Sample financial documents
│   └── TSLA-Q2-2025-Update.pdf
└── outputs/             # Analysis output directory
```

## License

MIT
