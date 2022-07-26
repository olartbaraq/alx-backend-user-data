#!/usr/bin/env python3

"""text file class basicAuth that
inherits from base class"""

from typing import Tuple, TypeVar

from flask_login import current_user
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """class basicAuth that inherits from base class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """method to return the Base64 of the Authorization"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        splited_basic = authorization_header.split(' ')
        if splited_basic[0] != 'Basic':
            return None
        return splited_basic[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """method to return the decoded value of a Base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            base64_bytes = base64.b64decode(base64_authorization_header)
            base64_message = base64_bytes.decode('utf-8')
            return base64_message
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ returns the user email and password from
        the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        splited_colon = decoded_base64_authorization_header.split(':')
        splited_name = splited_colon[0]
        splited_password = splited_colon[-1]
        if len(splited_colon) == 1:
            return (None, None)
        else:
            return (splited_name, splited_password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """ returns the User instance
        based on his email and password"""

        from models.user import User
        if type(user_email) is not str or user_email is None:
            return None
        if type(user_pwd) is not str or user_pwd is None:
            return None
        user = User()
        current_user = user.search({'email': user_email})
        if not current_user:
            return None
        valid_password = (current_user[0]).is_valid_password(user_pwd)
        if valid_password:
            return current_user[0]
        else:
            return None
