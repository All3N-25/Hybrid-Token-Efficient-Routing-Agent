# Hybrid Token Efficient Routing Agent Design

## Target Track

Track 1: General-Purpose AI Agent.

The agent reads unseen natural-language tasks, answers them in English, and minimizes recorded Fireworks token usage without falling below the accuracy gate.

## Runtime Contract

- Read input from `/input/tasks.json`.
- Write output to `/output/results.json`.
- Exit `0` on success and non-zero on failure.
- Finish all tasks within 10 minutes.
- Keep each task under 30 seconds.
- Do not hardcode answers, prompts, or model IDs.
- Use only model IDs from `ALLOWED_MODELS`.
- Route every Fireworks call through `FIREWORKS_BASE_URL`.

Input:

```json
[
  { "task_id": "t1", "prompt": "Summarise the following text in one sentence: ..." }
]
```

Output:

```json
[
  { "task_id": "t1", "answer": "..." }
]
```

## Minimal Architecture

```text
/input/tasks.json
      |
      v
load + validate tasks
      |
      v
cheap prompt analysis
      |
      v
rule-based route
      |
      +--> local small model / local rules
      |
      +--> Fireworks allowed model
      |
      v
/output/results.json
```

## Python Modules

```text
src/
  main.py        # orchestration and exit codes
  io.py          # read /input/tasks.json, write /output/results.json
  router.py      # classify, estimate risk, choose local or Fireworks
  local.py       # zero-token local handling
  fireworks.py   # env-driven Fireworks client
```

Skipped for MVP: database, web server, queues, plugin system, vector store, fine-tuning.

## Routing Policy

Use the cheapest path that is likely to pass the judge.

Local first:

- Sentiment classification.
- Named entity extraction.
- Very short factual prompts with obvious answers.
- Simple summaries with strict length constraints.
- Formatting-only transformations.

Fireworks:

- Math word problems.
- Code debugging.
- Code generation.
- Logic puzzles.
- Ambiguous factual questions.
- Long prompts where missing details could fail the judge.

If a prompt matches multiple categories, choose the riskier category. For example, code plus math routes as code/math, not summarisation.

## Prompt Signals

Cheap signals are enough for the first version:

- Prompt length.
- Presence of code fences or programming keywords.
- Math symbols, numbers, percentages, or "calculate".
- Entity extraction words like "extract", "person", "organization", "location".
- Sentiment words like "positive", "negative", "neutral", "sentiment".
- Summary words like "summarise", "summarize", "one sentence", "bullet".
- Logic words like "if", "must", "cannot", "exactly one", "who is".

## Fireworks Configuration

Read these at runtime:

```python
FIREWORKS_API_KEY
FIREWORKS_BASE_URL
ALLOWED_MODELS
```

Model choice should be simple:

- Prefer the cheapest/smallest allowed model for straightforward Fireworks calls.
- Use the strongest allowed model for code, math, and logic.
- If only one model is allowed, use it.

No model IDs belong in source code.

## Output Discipline

Return only the answer text required by the task. Do not include routing metadata in `/output/results.json`; extra fields may be ignored, but the required schema is safer.

## Build Plan

1. Implement JSON input/output exactly as required.
2. Add deterministic routing rules.
3. Add Fireworks calls using environment variables.
4. Add local handlers for sentiment, NER, and simple formatting.
5. Add a tiny smoke test using a local sample `tasks.json`.
6. Add Dockerfile for `linux/amd64`.

