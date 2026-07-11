FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential cmake curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip wheel --no-cache-dir --wheel-dir /wheels \
        -r /tmp/requirements.txt llama-cpp-python==0.3.16

ARG MODEL_URL=https://huggingface.co/Qwen/Qwen2-7B-Instruct-GGUF/resolve/main/qwen2-7b-instruct-q4_k_m.gguf
ARG MODEL_SHA256=ed93dfc426f926451fa3ec7f996a787a31cfd97e55d7769568fbffc2d69861c2
RUN curl --fail --location --retry 3 "$MODEL_URL" --output /qwen2.gguf \
    && echo "$MODEL_SHA256  /qwen2.gguf" | sha256sum --check -

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

WORKDIR /app
COPY Src/ /app/
COPY --from=builder /qwen2.gguf /models/qwen2.gguf

ENV INPUT_PATH=/input/tasks.json \
    OUTPUT_PATH=/output/results.json \
    LOCAL_MODEL_PATH=/models/qwen2.gguf \
    LOCAL_MODEL_CONTEXT=4096 \
    LOCAL_MODEL_THREADS=4

CMD ["python", "main.py"]
