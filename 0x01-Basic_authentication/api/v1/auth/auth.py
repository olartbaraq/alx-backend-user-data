#!/usr/bin/env python3

"""main file for api authentication"""

from email import header
from wsgiref import headers
from flask import request
from typing import List, TypeVar
import re


class Auth():
    """class to manage api authentication"""

    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """returns a bool based on path and excluded_paths"""
        if not excluded_paths or not path:
            return True
        for ex_path in excluded_paths:
            if ex_path[-1] == '*':
                pat = ex_path.split('*')
                pat = pat[0] + '.*'
                match = re.search(pat, path)
                if match:
                    return False
        if path[-1] != '/':
            path = path + '/'
        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """returns the request status"""
        if request is None:
            return None
        if not request:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the request status object"""
        return None
