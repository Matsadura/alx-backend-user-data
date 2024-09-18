#!/usr/bin/env python3
"""Basic auth class"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # nopep8
        """Returns the user email and password from the base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        idx = decoded_base64_authorization_header.find(':')
        email = decoded_base64_authorization_header[: idx]
        pwd = decoded_base64_authorization_header[idx + 1:]
        return email, pwd
        # cred = decoded_base64_authorization_header.split(':')
        # return cred[0], cred[1]

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # nopep8
        """ Return the User instance based on his email and password """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if not user or len(user) == 0:
            return None
        if not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request"""
        data = self.authorization_header(request)
        if not data:
            return None
        b64 = self.extract_base64_authorization_header(data)
        decoded = self.decode_base64_authorization_header(b64)
        email, pwd = self.extract_user_credentials(decoded)
        current_u = self.user_object_from_credentials(email, pwd)
        return current_u
