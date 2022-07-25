#!/usr/bin/env python3

"""main file for api authentication"""

from flask import request
from typing import List, TypeVar


class Auth():
    """class to manage api authentication"""

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """returns a bool based on path and excluded_paths"""
        if not excluded_paths or not path:
            return True
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """returns the request status"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the request status object"""
        return None
