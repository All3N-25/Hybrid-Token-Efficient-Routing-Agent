"""Classify a prompt's categories and complexity."""

import re


_CODE_FENCE = re.compile(r"```")
_BARE_CODE_LINE = re.compile(r"(?m)^\s*(def |class |function |public |private |const |let |var )\w+")
_CODE_REQUEST = re.compile(r"\b(write|create|implement|generate)\b.{0,40}\b(function|class|script|program|code)\b")
_MATH_EXPR = re.compile(r"\d+\s*[-+*/%^=]\s*\d+")
_NUMBER = re.compile(r"\d")
_MCQ_OPTION = re.compile(r"(?m)^\s*\(?[A-Ea-e][).:]\s+\S")

_DEBUG_WORDS = (
    "debug", "bug", "fix this code", "fix the code", "error", "traceback",
    "what's wrong", "why does this fail", "doesn't work", "corrected version",
)
_CODE_WORDS = (
    "write a function", "write code", "implement a function", "create a function",
    "sql query", "algorithm", "return a function", "generate code",
)
_MATH_WORDS = (
    "calculate", "compute", "solve", "how many", "how much", "sum of",
    "product of", "percent", "average", "remainder", "divided by",
    "equation", "probability", "final price",
)
_LOGIC_WORDS = (
    "logic puzzle", "deduce", "deduction", "constraint", "exactly one",
    "must", "cannot", "only if", "if and only if", "who owns",
)
_NER_WORDS = (
    "named entities", "extract and label", "people mentioned", "organizations mentioned",
    "organisations mentioned", "locations mentioned", "dates mentioned",
    "companies mentioned",
)
_NER_ACTION_WORDS = ("extract", "list all", "identify")
_NER_ENTITY_WORDS = ("person", "organization", "organisation", "location", "date", "entity", "entities")
_SENTIMENT_WORDS = (
    "sentiment", "positive or negative", "positive, negative", "classify the review",
    "classify this review", "tone of", "opinion", "how does the author feel",
)
_SUMMARY_WORDS = (
    "summarize", "summarise", "summary", "tldr", "tl;dr", "condense",
    "one sentence", "briefly describe",
)


def _has_any(text, words):
    return any(word in text for word in words)


def classify_categories(prompt):
    text = prompt.lower()
    has_code = bool(_CODE_FENCE.search(prompt) or _BARE_CODE_LINE.search(prompt))
    categories = []

    if has_code and _has_any(text, _DEBUG_WORDS):
        categories.append("Code Debugging")
    if _CODE_REQUEST.search(text) or _has_any(text, _CODE_WORDS):
        categories.append("Code Generation")
    if _MATH_EXPR.search(prompt) or (not has_code and _NUMBER.search(prompt) and _has_any(text, _MATH_WORDS)):
        categories.append("Mathematical Reasoning")
    if _has_any(text, _LOGIC_WORDS):
        categories.append("Logical / Deductive Reasoning")
    if _has_any(text, _NER_WORDS) or (_has_any(text, _NER_ACTION_WORDS) and _has_any(text, _NER_ENTITY_WORDS)):
        categories.append("Named Entity Recognition")
    if _has_any(text, _SENTIMENT_WORDS):
        categories.append("Sentiment Classification")
    if _has_any(text, _SUMMARY_WORDS):
        categories.append("Text Summarisation")
    return categories or ["Factual Knowledge"]


def classify_complexity(prompt, categories=None):
    categories = categories or classify_categories(prompt)
    words = len(prompt.split())
    score = 0

    if words > 120:
        score += 1
    if words > 300:
        score += 1
    if any(category in {
        "Mathematical Reasoning",
        "Code Debugging",
        "Code Generation",
        "Logical / Deductive Reasoning",
    } for category in categories):
        score += 2
    if len(categories) > 1:
        score += 1
    if _CODE_FENCE.search(prompt) or _BARE_CODE_LINE.search(prompt):
        score += 1
    if _MATH_EXPR.search(prompt):
        score += 1
    if _MCQ_OPTION.search(prompt):
        score -= 1
    if _has_any(prompt.lower(), ("exactly", "must", "cannot", "only if", "format", "json", "table")):
        score += 1

    if score <= 5:
        return "Simple"
    return "Complex"


def classify_prompt(prompt):
    categories = classify_categories(prompt)
    return {
        "categories": categories,
        "complexity": classify_complexity(prompt, categories),
    }
