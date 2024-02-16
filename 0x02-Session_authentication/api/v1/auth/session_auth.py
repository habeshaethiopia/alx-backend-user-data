#!/usr/bin/env python3
"""
session auth module for the API
"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """SessionAuth class"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """create_session"""
        if user_id is None or type(user_id) is not str:
            return None
        session_id = super().create_session(user_id)
        self.user_id_by_session_id[session_id] = user_id
        return session_id
