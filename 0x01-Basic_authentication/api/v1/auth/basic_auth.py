#!/usr/bin/env python3
""" Basic auth module.
"""
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar


class BasicAuth(Auth):
    """ BasicAuth class.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract base64 authorization header.
        Parameters:
            - authorization_header: authorization header.
        Returns:
            - Base64 authorization header.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Decode base64 authorization header.
        Parameters:
            - base64_authorization_header: base64 authorization header.
        Returns:
            - Decoded base64 authorization header.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user credentials.
        Parameters:
            - decoded_base64_authorization_header: decoded b64 auth header.
        Returns:
            - Tuple of user credentials.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ User object from credentials.
        Parameters:
            - user_email: user email.
            - user_pwd: user password.
        Returns:
            - User object.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        from models.user import User
        try:
            users = User.search({'email': user_email})
        except KeyError:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieve the User instance for a request.
        Parameters:
            - request: request object.
        Returns:
            - User instance.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        if b64_auth_header is None:
            return None
        decoded_b64_auth_header = self.decode_base64_authorization_header(
            b64_auth_header)
        if decoded_b64_auth_header is None:
            return None
        email, password = self.extract_user_credentials(
            decoded_b64_auth_header)
        if email is None or password is None:
            return None
        user = self.user_object_from_credentials(
                email, password)
        return user
