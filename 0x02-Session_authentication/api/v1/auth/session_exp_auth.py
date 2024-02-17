#!/usr/bin/env python3
""" Module of session views with expiring session
"""
from api.v1.session_auth import SessionAuth
import os
import time

class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __inti__(self):
        """Constructor"""
        self.session_duration = (
            int(os.getenv("SESSION_DURATION"))
            if os.getenv("SESSION_DURATION") and 
            os.getenv("SESSION_DURATION").isdigit()
            else 0
        )

    def create_session(self, user_id: str = None) -> str:
        """create_session"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": time.time(),
        }
        return session_id
    def user_id_for_session_id(self, session_id: str = None) -> str:
