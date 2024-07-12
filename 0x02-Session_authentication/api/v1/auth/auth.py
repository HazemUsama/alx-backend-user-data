#!/usr/bin/env python3
""" Authentication module.
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """ Authentication class.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require authentication.
        Parameters:
            - path: path to check.
            - excluded_paths: list of paths excluded from authentication.
        Returns:
            - True if authentication is required, False otherwise.
        """
        if path is None or not excluded_paths:
            return True
        if path[-1] != '/':
            path = path + '/'

        with_astericks = [s[:-1] for s in excluded_paths if s[-1] == '*']
        for s in with_astericks:
            if path.startswith(s):
                return False
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ Authorization header.
        Parameters:
            - request: request object.
        Returns:
            - Authorization header value.
        """
        if request is None:
            return None
        header_key = request.headers.get('Authorization')
        return header_key

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user.
        Parameters:
            - request: request object.
        Returns:
            - None.
        """
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
