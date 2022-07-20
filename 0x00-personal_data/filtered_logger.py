#!/usr/bin/env python3
"""
Main file to write a function that log obfuscated
"""

import logging
from typing import Union, List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns a function that log obfuscated"""
    for field in fields:
        val = field + '=[^{}]*'.format(separator)
        message = re.sub(val, field + '=' + redaction, message)

    return (message)
