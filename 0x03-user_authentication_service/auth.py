#!/usr/bin/env python3
"""imports method to return hashed password"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """function that returns a salted,
    hashed password, which is a byte string"""

    passwd = password.encode()

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed
