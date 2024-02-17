#!/usr/bin/env python3
""" user session module
"""
from models.base import Base


class UserSession(Base):
    """UserSession class"""

    def __init__(self, *args: list, **kwargs: dict):
        """Constructor"""
        self.user_id =""
        self.session_id = ""
        super().__init__(*args, **kwargs)
