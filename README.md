# Hybrid Token-Efficient Routing Agent

The agent reads prompts from `/input/tasks.json`, routes each task to either the bundled Qwen3-8B model or Fireworks AI, and writes answers to `/output/results.json`.

## Run the Docker image

### 1. Pull the image

```bash
docker pull all3n25/hybrid-routing-agent:latest
```

### 2. Create the input and output directories

```bash
mkdir -p input output
```

Create `input/tasks.json`:

```json
[
  {
    "task_id": "task-1",
    "prompt": "What is the capital of the Philippines?"
  }
]
```

### 3. Configure Fireworks AI

Create a `.env` file using the values supplied by the evaluation environment:

```dotenv
FIREWORKS_API_KEY=your-api-key
FIREWORKS_BASE_URL=your-fireworks-endpoint
ALLOWED_MODELS=minimax-m3,kimi-k2p7-code,gemma-4-31b-it,gemma-4-26b-a4b-it,gemma-4-31b-it-nvfp4
```

### 4. Run the agent

```bash
docker run --rm \
  --env-file .env \
  -v "$PWD/input:/input:ro" \
  -v "$PWD/output:/output" \
  all3n25/hybrid-routing-agent:latest
```

The container exits after processing every task. A successful run returns exit code `0`.

### 5. Read the results

```bash
cat output/results.json
```

Example output:

```json
[
  {
    "task_id": "task-1",
    "answer": "Manila."
  }
]
```