#!/usr/bin/env python3
"""Auth module for handling authentication
"""
import bcrypt


def _hash_password(password: str) -> str:
    """Hash a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
