#!/usr/bin/env python3
"""Auth module for handling authentication
"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(email: str, password: str) -> User:
        """Register a new user
        """
        if self._db.find_user_by(email=email):
            raise ValueError(f"User {email} already exists")
        hashed_password = _hash_password(password)
        return self._db.add_user(email, hashed_password)


def _hash_password(password: str) -> str:
    """Hash a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
