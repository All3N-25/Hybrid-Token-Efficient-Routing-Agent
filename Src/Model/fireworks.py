"""
Generate answers with the Fireworks API.
"""

import json
import os

from urllib.error import URLError
from urllib.request import Request, urlopen
from aiohttp.web_exceptions import HTTPError

import fireworks.client

fireworks.client.api_key = os.environ["FIREWORKS_API_KEY"]
api_key    = os.environ["FIREWORKS_API_KEY"]
base_url   = os.environ["FIREWORKS_BASE_URL"]
models     = os.environ["ALLOWED_MODELS"].split(",")

CATEGORY_MODEL_MAP = {
    "minimax-m3":       {"Factual Knowledge", "Mathematical Reasoning", "Logical/Deductive Reasoning", "Text Summarisation"},
    "kimi-k2p7-code":   {"Code Debugging", "Code Generation", "Sentiment Classification", "Named Entity Recognition"},
}
DEFAULT_MODEL = "minimax-m3"

fireworks_tokens_used = 0

def select_model(categories: list[str]) -> str:
    # Only selects the model that matches the first category.
    cat_set = set(categories)
    for model_name, model_categories in CATEGORY_MODEL_MAP.items():
        if cat_set & model_categories:
            if model_name not in models:
                raise RuntimeError(f"{model_name} not in ALLOWED_MODELS")
            return model_name
    return DEFAULT_MODEL

def generate(prompt: str, categories: list[str]) -> dict[str, str]:
    global fireworks_tokens_used
    if not models:
        raise RuntimeError("ALLOWED_MODELS is empty")

    model = select_model(categories)

    payload = {
        "model": f"accounts/fireworks/models/{model}",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Answer accurately and concisely. Return only the requested "
                    "answer. Avoid unnecessary Markdown headings, bold text, "
                    "LaTeX, explanations, or routing metadata because they "
                    "consume Fireworks tokens. Code answers may contain normal "
                    "source code with newline characters inside the string."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 8192,
    }
    if "minimax-m3" in model:
        payload["thinking"] = {"type": "disabled"}
        
    print("MODEL SELECTED:", payload["model"])
    
    request = Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            body = json.load(response)
    except HTTPError as e:          # must come BEFORE URLError
        err_body = e.read().decode(errors="replace")
        raise RuntimeError(f"Fireworks API error {e.code}: {err_body}") from e
    except URLError as e:
        raise RuntimeError(f"Failed to reach Fireworks API: {e.reason}") from e

    choice = body["choices"][0]
    answer = choice["message"].get("content")
    usage = body.get("usage", {})
    fireworks_tokens_used += int(usage.get("total_tokens", 0))
    print("FIREWORKS TOKEN USAGE:", usage)
    print("TOTAL FIREWORKS TOKENS USED:", fireworks_tokens_used)

    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError(
            f"Fireworks returned no final answer (finish_reason={choice.get('finish_reason')})"
        )
    return {
        "answer": answer.strip(),
        "model": model,
        "provider": "fireworks",
    }
