#!/usr/bin/env python3
""" session db auth module for the API
"""
from api.v1.auth.session_auth import SessionAuth


class SessionDBAuth(SessionAuth):
    """session DB auth class"""

    def create_session(self, user_id=None):
        """create session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        from models.user_session import UserSession

        UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user_id_for_session_id"""
        if session_id is None:
            return None
        from models.user_session import UserSession

        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        user_session = user_session[0]
        from time import time

        if (time() - user_session.created_at) > self.session_duration:
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """destroy session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        from models.user_session import UserSession

        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session = user_session[0]
        user_session.remove()
        return True
