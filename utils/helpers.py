"""
Helper utilities.
"""

import re
import json


def parse_json(text: str) -> dict:
    """Extract and parse JSON from text."""
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return {}


def truncate(text: str, max_len: int = 500) -> str:
    """Truncate text to max length."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."
