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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(self.FORMAT)
        record.msg = filter_datum(list(self.fields), self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
