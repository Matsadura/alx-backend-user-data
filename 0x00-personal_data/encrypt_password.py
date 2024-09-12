#!/usr/bin/env python3
"""Encrypting password"""


import bcrypt


def hash_password(password: str) -> bytes:
    """encrypt password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """this function expects 2 arguments and returns a boolean"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
