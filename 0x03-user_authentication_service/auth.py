#!/usr/bin/env python3
"""Handle auth"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a salted hash"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
