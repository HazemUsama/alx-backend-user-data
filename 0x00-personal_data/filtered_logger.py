#!/usr/bin/env python3
"""filtered_logger module
"""
import re


def filter_datum(fields: str, redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated
    Args:
        - fields: a list of strings representing all fields to obfuscate
        - redaction: a string representing by what the field will be obfuscated
        - message: a string representing the log line
        - separator: a string representing which character separates fields
    Returns:
        - the log message obfuscated
    """
    for field in fields:
        message = re.sub(rf'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message
