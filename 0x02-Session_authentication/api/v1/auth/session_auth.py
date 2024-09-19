#!/usr/bin/env python3
"""Handles session authenthication"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth Class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        u_id = uuid.uuid4()
        self.user_id_by_session_id[f"{u_id}"] = user_id
        return u_id
