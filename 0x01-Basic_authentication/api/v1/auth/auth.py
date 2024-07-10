#!/usr/bin/env python3
""" Authentication module.
"""
from flask import request
from typing import List, TypeVar


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
