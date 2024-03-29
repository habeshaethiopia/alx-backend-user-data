#!/usr/bin/env python3
"""
auth module for the API
"""
from flask import jsonify, abort, request
from typing import List, TypeVar
import os
import uuid

class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        for p in excluded_paths:
            if p.endswith("*") and path.startswith(p[:-1]):
                return False
        if path[-1] != "/":
            path += "/"
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def session_cookie(self, request=None):
        """session_cookie"""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)