#!/usr/bin/env python3
"""imports method to return hashed password"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """function that returns a salted,
    hashed password, which is a byte string"""

    passwd = password.encode()

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed

def _generate_uuid() -> str:
    """ returns a string rep of a new UUID"""
    new_uuid = str(uuid.uuid4())
    return new_uuid


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
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ returns a bool if user passowrd matches the bcrypt password"""
        try:
            locate_user = self._db.find_user_by(email=email)
            password = password.encode()
            return bcrypt.checkpw(password, locate_user.hashed_password)
        except NoResultFound:
            return False
