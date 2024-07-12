#!/usr/bin/env python3
""" SessionDBAuth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """

    def create_session(self, user_id=None):
        """ Create session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ User ID for session ID
        """
        if session_id is None:
            return None
        session_dictionary = UserSession.search({'session_id': session_id})
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None
        if (datetime.now() - created_at).seconds > self.session_duration:
            return None
        return session_dictionary.get('user_id')

    def destroy_session(self, request=None):
        """ Destroy session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if user_session is None:
            return False
        user_session.remove()
        return True
