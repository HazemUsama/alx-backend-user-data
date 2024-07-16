#!/usr/bin/env python3
"""Auth module for handling authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login
        """
        try:
            user = self._db.find_user_by(email=email)
            encoded_pass = password.encode('utf-8')
            encoded_hash = user.hashed_password.encode('utf-8')
            return bcrypt.checkpw(encoded_pass, encoded_hash)
        except NoResultFound:
            return False


def _hash_password(password: str) -> str:
    """Hash a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def _generate_uuid() -> str:
    """Generate a UUID
    """
    return str(uuid.uuid4())
