#!/usr/bin/env python3
"""Contains Auth related"""
import re
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """A class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require_auth method """
        if not path or not excluded_paths:
            return True
        clean_path = re.escape(path)
        for ex_path in excluded_paths:
            if ex_path.endswith("*"):
                new_path = ex_path[:-1]
                if re.search(f"^{new_path}", clean_path):
                    return False
            elif re.match(f"^{clean_path}/?$", ex_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization_header public method"""
        if request is None:
            return None
        data = request.headers
        if "Authorization" not in data:
            return None
        return data['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Current_user public method"""
        return None

    def session_cookie(self, request=None):
        """ Return a cookie form a request """
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        cookie = request.cookies.get(cookie_name)
        return cookie
