from pathlib import Path

parser_path = Path('utils/json_parser.py')
text = parser_path.read_text(encoding='utf-8')
old = '''def try_parse_json(text: str) -> Optional[dict]:
    """
    Locate and parse the first complete JSON object in an AI response string.

    Returns a dict on success, or None if no valid JSON is found.
    """
    if not text or not isinstance(text, str):
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
        return None
'''
new = '''def try_parse_json(text: str) -> Optional[dict]:
    """
    Locate and parse the first JSON object in an AI response string.

    Returns a dict on success, or None if no valid JSON is found.
    """
    if not text or not isinstance(text, str):
        return None

    # Try direct JSON first.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

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

    # Try cleanup for some AI output formats.
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
'''
text = text.replace(old, new)
parser_path.write_text(text, encoding='utf-8')
print('parser block replaced')
