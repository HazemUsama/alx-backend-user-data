#!/usr/bin/env python3
""" Basic auth module.
"""
from api.v1.auth.auth import Auth
import base64
import binascii


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
