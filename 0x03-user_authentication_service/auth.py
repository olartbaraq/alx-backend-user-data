#!/usr/bin/env python3
"""imports method to return hashed password"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


def _hash_password(password: str) -> bytes:
    """function that returns a salted,
    hashed password, which is a byte string"""

    passwd = password.encode()

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """instantiation for the Auth class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """returns a user object"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            new_passwd = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=new_passwd)
            return User
