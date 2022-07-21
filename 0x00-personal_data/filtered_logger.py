#!/usr/bin/env python3
"""
Main file to write a function that log obfuscated
"""

from typing import List
import logging
import mysql.connector
import os
import re


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')

os.environ['PERSONAL_DATA_DB_USERNAME'] = 'root'
os.environ['PERSONAL_DATA_DB_PASSWORD'] = ''
os.environ['PERSONAL_DATA_DB_HOST'] = 'localhost'
os.environ['PERSONAL_DATA_DB_NAME'] = 'holberton'


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
    logging.Logger(name='user_data')
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    log.addHandler(ch)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    connection = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST'),
        database=os.getenv('PERSONAL_DATA_DB_NAME'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD')
    )
    if connection.is_connected():
        return connection


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
