#!/usr/bin/env python3
"""Handle auth"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a salted hash"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register an user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {user.email} already exists')
        except NoResultFound:
            hashed_pwd = _hash_password(password=password)
            user = self._db.add_user(email, hashed_pwd)
        return user
