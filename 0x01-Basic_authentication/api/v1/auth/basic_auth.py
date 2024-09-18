#!/usr/bin/env python3
"""Basic auth class"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:   # nopep8
        """Returns the decoded value as UTF8 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_byes = base64.b64decode(base64_authorization_header)
            decoded = decoded_byes.decode('utf-8')
        except Exception as e:
            return None
        return decoded
