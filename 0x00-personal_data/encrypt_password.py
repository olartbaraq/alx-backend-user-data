#!/usr/bin/env python3

"""
Main file
"""

from typing import Any
import bcrypt


def hash_password(password: str) -> bytes:
    """function that returns a salted,
    hashed password, which is a byte string"""

    passwd = password.encode()

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed
