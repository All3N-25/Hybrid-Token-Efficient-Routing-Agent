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
