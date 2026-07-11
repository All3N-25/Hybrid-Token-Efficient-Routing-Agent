FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip wheel --no-cache-dir --wheel-dir /wheels \
        -r /tmp/requirements.txt llama-cpp-python==0.3.16

ARG MODEL_URL=https://huggingface.co/Qwen/Qwen3-8B-GGUF/resolve/main/Qwen3-8B-Q4_K_M.gguf
ARG MODEL_SHA256=d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785
RUN curl --fail --location --retry 3 "$MODEL_URL" --output /qwen3.gguf \
    && echo "$MODEL_SHA256  /qwen3.gguf" | sha256sum --check -

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

WORKDIR /app
COPY Src/ /app/
COPY --from=builder /qwen3.gguf /models/qwen3.gguf

ENV INPUT_PATH=/input/tasks.json \
    OUTPUT_PATH=/output/results.json \
    LOCAL_MODEL_PATH=/models/qwen3.gguf \
    LOCAL_MODEL_NAME=Qwen3-8B-Q4_K_M \
    LOCAL_MODEL_CONTEXT=4096 \
    LOCAL_MODEL_THREADS=4

CMD ["python", "main.py"]
