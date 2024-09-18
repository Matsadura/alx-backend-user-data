#!/usr/bin/env python3
"""Contains Auth related"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require_auth public method"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == '':
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
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
