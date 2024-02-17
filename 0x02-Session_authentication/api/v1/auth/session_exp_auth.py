#!/usr/bin/env python3
""" Module of session views with expiring session
"""
from api.v1.auth.session_auth import SessionAuth
import os
import time


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __init__(self):
        """Constructor"""
        self.session_duration = 0
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            pass

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
        """user_id_for_session_id"""
        if session_id is None:
            print("session_id is None")
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            print("session_duration <= 0")
            return session_dict.get("user_id")
        if "created_at" not in session_dict:
            print("created_at not in session_dict")
            return None
        if (time.time() - session_dict.get("created_at")) > self.session_duration:
            print("time.time() - session_dict.get(created_at) > self.session_duration")
            return None
        # print("returning session_dict.get(user_id)",session_dict.get("user_id"))
        return session_dict.get("user_id")
