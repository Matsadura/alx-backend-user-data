#!/usr/bin/env python3
"""Contains Auth related"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class to manage the API authentication"""
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require_auth public method"""
        return False
    
    def authorization_header(self, request=None) -> str:
        """Authorization_header public method"""
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """Current_user public method"""
        return None
