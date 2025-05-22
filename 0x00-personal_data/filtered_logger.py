#!/usr/bin/env python3
"""
The function filter_datum that returns the log message obfuscated
"""

import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns the log message with sensitive fields obfuscated."""
    return re.sub(
        f"({'|'.join(fields)})=.+?{separator}",
        lambda m: f"{m.group(1)}={redaction}{separator}",
        message
    )
