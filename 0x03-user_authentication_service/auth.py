#!/usr/bin/env python3
"""imports method to return hashed password"""

from typing import Union
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

    def create_session(self, email: str) -> str:
        """ method to find a email of a user,
        generate a new uuid, store it and returns the
        session ID"""
        try:
            user = self._db.find_user_by(email=email)
            new_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=new_uuid)
            return new_uuid
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """returns the corresponding User or None"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ method takes a single user_id integer
        argument and returns None"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return user.session_id
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """method to update the user's reset token in the database"""
        try:
            user = self._db.find_user_by(email=email)
            new_uuid = _generate_uuid()
            self._db.update_user(user_id=user.id,
                                 reset_token=new_uuid)
            return new_uuid
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates the user's password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_password = _hash_password(password=password)
            self._db.update_user(user_id=user.id, reset_token=None,
                                 hashed_password=new_password)
            return user.reset_token
        except NoResultFound:
            raise ValueError
