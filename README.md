# Hybrid Token Efficient Routing Agent Design (Expanded)

## 1. Target Track & Objective
**Track 1: General-Purpose AI Agent.**

The primary objective is to read unseen natural-language tasks, process them, and answer in English while **strictly minimizing recorded Fireworks token usage** without falling below the baseline accuracy gate. This requires a highly tuned, heuristic-based router that acts as a gatekeeper before any LLM API is invoked.

## 2. Runtime Contract & Constraints

### 2.1 I/O Specifications
- **Input:** Read from `/input/tasks.json`.
- **Output:** Write exclusively to `/output/results.json`.
- **Exit Codes:** Must exit `0` on absolute success. Any uncaught exceptions or validation failures must exit non-zero (e.g., `1` for IO errors, `2` for API failures).

### 2.2 Performance Limits
- **Total Execution:** Finish all tasks within 10 minutes.
- **Per-Task Limit:** Keep each task under 30 seconds.
- **Concurrency:** Ensure asynchronous processing (`asyncio`) or multithreading is used if tasks are batched, to prevent blocking I/O from breaching the 10-minute limit.

### 2.3 Hard Rules
- **No Hardcoding:** Do not hardcode answers, prompts, or model IDs.
- **Model Restrictions:** Use *only* model IDs provided in the `ALLOWED_MODELS` environment variable.
- **Network Routing:** Route every Fireworks API call strictly through `FIREWORKS_BASE_URL`.

---

## 3. Architecture & Data Flow

```text
[ /input/tasks.json ]
        |
        v
+-------------------------------+
| 1. Ingestion & Validation     | -> Drop invalid tasks, sanitize strings
+-------------------------------+
        |
        v
+-------------------------------+
| 2. Heuristic Analyzer         | -> Regex matching, length calculation, NLP rules
+-------------------------------+
        |
        v
+-------------------------------+
| 3. Routing Engine             | -> Decision Matrix (Local vs. Cloud)
+-------------------------------+
       /                 \
  [ LOCAL ]            [ FIREWORKS ]
      |                    |
+-------------+      +-------------------+
| Zero-Token  |      | Cost-Optimized    |
| NLP Scripts |      | LLM API Call      |
+-------------+      +-------------------+
       \                 /
        v               v
+-------------------------------+
| 4. Formatting & Persistence   | -> Ensure strict JSON schema compliance
+-------------------------------+
        |
        v
[ /output/results.json ]
```

## 4. Deep Dive: Routing Policy & Heuristics
The core of the cost-saving mechanism is the Routing Policy. Use the cheapest path that is statistically likely to pass the judge.

### 4.1 Local Handlers (Zero Token Cost)
Route to local, rule-based Python functions if the prompt matches these criteria:

Sentiment Classification: Looks for "positive, negative, or neutral". Uses simple keyword weighting or a lightweight local library like VADER or TextBlob (if allowed).

Named Entity Extraction (NER): Looks for "extract", "locations", "people". Uses RegEx or basic NLP tokenization for standard formats.

Simple Summaries: Looks for "TL;DR" or "one sentence" combined with low word counts.

Formatting: e.g., "Convert this CSV to JSON".

### 4.2 Fireworks Handlers (Token Intensive)
Route to the cloud if the risk of failure is high or reasoning is required:

Math & Logic: Presence of +, -, *, /, %, calculate, sum, deduce, logic.

Code Execution/Debugging: Presence of code blocks (```), def, class, debug, traceback.

Long Context: Any prompt exceeding ~150 words (too complex for reliable local heuristics).

### 4.3 Conflict Resolution
If a prompt triggers multiple heuristics (e.g., Code + Summarization), always default to the riskier/harder category (Fireworks). It is better to spend a few tokens than fail the accuracy gate entirely.

## 5. Configuration & Environment Variables
The agent must be entirely dynamically configured via OS environment variables.

Code snippet
# Required API Credentials
FIREWORKS_API_KEY=your_secure_api_key_here
FIREWORKS_BASE_URL=https://api.fireworks.ai/inference/v1

# Model Selection (Comma-separated list of allowed models)
ALLOWED_MODELS=accounts/fireworks/models/llama-v3-8b-instruct,accounts/fireworks/models/mixtral-8x7b-instruct

# File Paths (Defaults provided for local testing)
INPUT_PATH=/input/tasks.json
OUTPUT_PATH=/output/results.json
Selection Logic:

If ALLOWED_MODELS contains multiple options, map them to complexity tiers. Use the smallest parameter model (e.g., 8B) for standard queries, and the largest for Code/Math.

If only one model is provided, use it universally for all external calls.

## 6. Error Handling & Fallbacks
API Timeouts: If a Fireworks call approaches the 30-second task limit, catch the TimeoutError. Do not crash the entire run. Log the error and return a safe fallback string (e.g., "Unable to process task due to complexity.") to ensure subsequent tasks are still processed.

JSON Malformation: If the LLM returns broken JSON when JSON is requested, attempt one automatic repair (using local regex) before falling back.

Missing Keys: If ALLOWED_MODELS or FIREWORKS_API_KEY is missing on boot, exit immediately with a non-zero code to fail fast.

## 7. Execution & Build Plan
Phase 1: Local Setup
Implement standard Pydantic or Dataclass models for Task input/output.

Build the Regex Engine for prompt classification.

Phase 2: API Integration
Implement aiohttp or the standard requests library to interface with Fireworks.

Implement retry logic (e.g., Tenacity library) with exponential backoff for HTTP 429/500 errors.

Phase 3: Dockerization
Create a linux/amd64 compatible Dockerfile to ensure it runs on the grading servers.

Dockerfile
# Example Dockerfile
FROM python:3.11-slim-bookworm
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/

# Define default environment variables
ENV INPUT_PATH=/input/tasks.json
ENV OUTPUT_PATH=/output/results.json

# Run the orchestrator
CMD ["python", "-m", "src.main"]