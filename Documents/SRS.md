# 1. Introduction
- Build an AI agent that completes a fixed set of tasks autonomously by deciding in real time whether to use a local model or call a remote model via Fireworks AI credits. The goal: pick the cheapest option every time, without falling below the accuracy threshold.

### 1.1 Scope
- Read JSON inputs.
- Analyze prompts.
- Classify tasks.
- Estimate prompt complexity.
- Route each prompt to the appropriate model.
- Generate concise answers.
- Store results to Results.json.

---

# 2. Overall Description

The Hybrid Token-Efficient Routing Agent is a command-line AI system designed to process a collection of natural-language tasks autonomously. Its primary purpose is to reduce remote token usage while maintaining the level of answer accuracy required by the evaluation process. For every task, the system extracts the prompt, identifies its category, estimates its complexity, and selects an appropriate language model. Simple tasks are handled by a bundled local model whenever possible, avoiding remote token costs. Tasks that require stronger mathematical, logical, factual, or programming capabilities are routed to an allowed model through the Fireworks AI service. The system operates inside a Docker container, receives tasks through a structured JSON input file, and records concise answers in a JSON output file. Its routing rules are deterministic and inexpensive, allowing model selection without consuming additional language-model tokens. The application is intended to run without interactive user input and relies on environment variables for model availability, API access, file locations, and local inference settings. This hybrid approach balances answer quality, execution time, and token efficiency.

### 2.1 Product Perspective
- The system runs as a standalone Docker container.
- It reads tasks from `/input/tasks.json` and writes answers to `/output/results.json`.
- It uses rule-based prompt analysis for routing and language models for answer generation.
- It does not require a graphical interface, database, or web server.

### 2.2 User Characteristics
- The primary users are evaluators or operators who provide tasks in the required JSON format and configure the runtime through environment variables.
- Users are expected to understand basic JSON files, Docker execution, and API credential configuration.

### 2.3 Operating Environment
- The application runs on `linux/amd64` using Python 3.12.
- Local inference uses a bundled Qwen3-8B Q4_K_M GGUF model through `llama-cpp-python`.
- Remote inference requires network access to the configured Fireworks AI endpoint.

### 2.4 Constraints and Dependencies
- Only models listed in the `ALLOWED_MODELS` environment variable may be used remotely.
- All remote requests must use `FIREWORKS_BASE_URL` and a valid `FIREWORKS_API_KEY`.
- Tasks and results must follow the required JSON structures.
- The system must complete all tasks within the evaluation time limit while minimizing Fireworks token usage.

### 2.5 Assumptions
- Input files contain valid task identifiers and natural-language prompts.
- The local model file and required environment variables are available at runtime.
- The Fireworks AI service is reachable when a task is routed remotely.

--- 

# 3. Functional Requirements

### 3.1 Input Processing.
- Be able to read inputs on a JSON Structure. 

### 3.2 Prompt Extraction.
- Extract properties of the prompt.
- This will be used for Functional Requirement 3, to classify the prompt. 

### 3.3 Classify the Prompt.
- Classify the tasks based on the categories provided:
    - Factual Knowledge
    - Mathematical Reasoning
    - Sentiment Classification
    - Text Summarisation
    - Named Entity Recognition
    - Code Debugging
    - Logical / Deductive Reasoning
    - Code Generation

### 3.4 Estimate complexity.
- Use the outputs of FR 2-3 to determine the complexity of the prompt.
- Complexity Categorization:
    - Simple
    - Complex
- Use Rule Based To Classify.

### 3.5 Routing Decision.
- Be able to determine to use a local model or a Fireworks AI model.
- This can be based on:
    - Complexity
    - Classification
    - Accuracy/Confidence
    - Token Cost
### 3.6 Concise Answers.
- Use prompt engineering to make the answers more concise and simple.

---

# 4. Non-Functional Requirements

### 4.1 Performance.
- Should be able to provide a more accurate answer and reduce the token usage. 

---

# 5. System Architecture
```
                  Startup
                     │
                     ▼
        Read Environment Variables
                     │
                     ▼
          Load Allowed Models
                     │
                     ▼
        Read /input/tasks.json
                     │
                     ▼
         For each Prompt in Tasks
                     │
                     ▼
        Prompt Feature Extraction
                     │
                     ▼
         Capability Classifier
                     │
                     ▼
            Complexity Estimator
                     │
                     ▼
             Routing Decision
          ┌──────────┴──────────┐
          ▼                     ▼
    Local Model          Fireworks Model
          │                     │
          └──────────┬──────────┘
                     ▼
             Collect Responses
                     ▼
        Write /output/results.json
                     ▼
                 Exit(0)
```

---

# 6. Evaluation
- This is how the hackathon judges our work.
### 6.1 Accuracy.
- LLM-Judge evaluates each answer against the expected intent.
- Submissions below the accuracy threshold are excluded from the leaderboard.

### 6.2 Token Usage.
- submissions that pass the accuracy gate are ranked ascending by total tokens recorded by the judging proxy. 
- Fewer tokens = higher rank.

### 6.3 Waiting Time (Not Judged on the Hackathon).
- Not required but good to have.
- Reduce the thinking time of the model.
