"""Generate answers with the Qwen3 model bundled in the container."""

import os
from functools import lru_cache

from llama_cpp import Llama


@lru_cache(maxsize=1)
def _model() -> Llama:
    return Llama(
        model_path=os.environ.get("LOCAL_MODEL_PATH", "/models/qwen3.gguf"),
        n_ctx=int(os.environ.get("LOCAL_MODEL_CONTEXT", "4096")),
        n_threads=int(os.environ.get("LOCAL_MODEL_THREADS", "4")),
        verbose=False,
    )


def generate(prompt: str) -> dict[str, str]:
    response = _model().create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer accurately and concisely. Return only the requested "
                    "answer. Avoid unnecessary Markdown headings, bold text, "
                    "LaTeX, explanations, or routing metadata because they "
                    "consume Fireworks tokens. Code answers may contain normal "
                    "source code with newline characters inside the string."
                ),
                "thinking": {"type": "disabled"}
            },
            {"role": "user", "content": f"{prompt}\n/no_think"},
        ],
        temperature=0,
    )
    answer = response["choices"][0]["message"]["content"]
    if not answer or not answer.strip():
        raise RuntimeError("Local model returned no answer")
    return {
        "answer": answer.strip(),
    }
