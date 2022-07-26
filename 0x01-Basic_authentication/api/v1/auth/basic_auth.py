#!/usr/bin/env python3

"""text file class basicAuth that
inherits from base class"""

from typing import Tuple
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
