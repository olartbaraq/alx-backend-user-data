#!/usr/bin/env python3

"""
Main file
"""

from typing import Any
from xmlrpc.client import boolean
import bcrypt


def hash_password(password: str) -> bytes:
    """function that returns a salted,
    hashed password, which is a byte string"""

    passwd = password.encode()

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """function to validate that the provided password
    matches the hashed password."""
    password = password.encode()
    if bcrypt.checkpw(password, hashed_password):
        return True
    return False
