"""
utils/json_parser.py
────────────────────
Safely extract the first JSON object from an AI response string.
"""

import ast
import json
import re
from typing import Optional


def _strip_comments_and_fences(text: str) -> str:
    text = re.sub(r'```(?:json)?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    return text.strip()


def _remove_trailing_commas(text: str) -> str:
    text = re.sub(r',\s*([}\]])', r'\1', text)
    return text


def try_parse_json(text: str) -> Optional[dict]:
    """
    Locate and parse the first JSON object in an AI response string.

    Returns a dict on success, or None if no valid JSON is found.
    """
    if not text or not isinstance(text, str):
        return None

    cleaned = _strip_comments_and_fences(text)

    # Try direct JSON first.
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Try to recover a JSON-like object from the first brace pair.
    start = cleaned.find("{")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False
    end = None

    for idx in range(start, len(cleaned)):
        char = cleaned[idx]
        if char == "\\" and not escape:
            escape = True
            continue
        if char == '"' and not escape:
            in_string = not in_string
        if not in_string:
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = idx
                    break
        escape = False

    if end is None:
        return None

    candidate = cleaned[start : end + 1]
    candidate = _remove_trailing_commas(candidate)

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    try:
        return ast.literal_eval(candidate)
    except (ValueError, SyntaxError):
        pass

    return None

    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False
    end = None

    for idx in range(start, len(text)):
        char = text[idx]
        if char == "\\" and not escape:
            escape = True
            continue
        if char == '"' and not escape:
            in_string = not in_string
        if not in_string:
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end = idx
                    break
        escape = False

    if end is None:
        return None

    candidate = text[start : end + 1]

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    import re
    candidate = re.sub(r',\s*([}\]])', r'\1', candidate)
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    return None
