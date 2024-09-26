#!/usr/bin/env python3
"""Handle auth"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a salted hash"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Return str repr of a new UUID"""
    import uuid
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Check the validity of a password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return False
        return True

    def create_session(self, email: str) -> str:
        """Return session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        data = {'session_id': _generate_uuid()}
        self._db.update_user(user.id, **data)
        return data['session_id']

    def get_user_from_session_id(self, session_id: str) -> User:
        """Return the user or None"""
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user session"""
        return self._db.update_user(user_id, **{'session_id': None})
