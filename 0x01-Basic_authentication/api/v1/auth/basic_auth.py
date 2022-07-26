#!/usr/bin/env python3

"""text file class basicAuth that
inherits from base class"""

from api.v1.auth.auth import Auth


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
