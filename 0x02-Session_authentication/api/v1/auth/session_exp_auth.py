#!/usr/bin/env python3
""" Session expiration authentication module
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime
from os import getenv


class SessionExpAuth(SessionAuth):
    """ Session expiration Authentication class
    """

    def __init__(self):
        """ Constructor
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a new session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.utcnow()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Get a user ID from a session ID
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None
        if (datetime.utcnow() - created_at).seconds > self.session_duration:
            return None
        return session_dictionary.get('user_id')
