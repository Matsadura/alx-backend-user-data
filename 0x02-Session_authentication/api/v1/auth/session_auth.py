#!/usr/bin/env python3
"""Handles session authenthication"""
import os
from typing import TypeVar
import uuid
from api.v1.auth.auth import Auth
from api.v1.views.users import User


class SessionAuth(Auth):
    """SessionAuth Class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """Return a User instance based on a cookie value"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Delete the user session/logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
