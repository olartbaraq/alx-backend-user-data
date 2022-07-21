#!/usr/bin/env python3
"""
Main file to write a function that log obfuscated
"""

from cmath import log
import logging
from typing import Union, List
import re


PII_FIELDS = (['email', 'phone', 'ssn', 'password', 'ip'])


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns a function that log obfuscated"""
    for field in fields:
        val = field + '=[^{}]*'.format(separator)
        message = re.sub(val, field + '=' + redaction, message)

    return (message)


def get_logger() -> logging.Logger:
    """function that takes no arguments
    and returns a logging.Logger object."""
    log = logging.getLogger('user_data')
    log.setLevel(level=logging.INFO)

    RedactingFormatter = logging.Formatter(PII_FIELDS)

    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG)
    ch.setFormatter(RedactingFormatter)

    log.addHandler(ch)
    return log


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor Method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records using filter_datum """
        formatter = logging.Formatter(self.FORMAT)
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
