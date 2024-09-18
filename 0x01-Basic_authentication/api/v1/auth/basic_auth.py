#!/usr/bin/env python3
"""Basic auth class"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """A BasicAuth class that inherits from Auth"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # nopep8
        """Returns the Bae64 part of the Authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.strip('Basic ')
