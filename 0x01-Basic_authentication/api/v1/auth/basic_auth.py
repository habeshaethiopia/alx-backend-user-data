#!/usr/bin/env python3
"""
auth module for the API
"""
from flask import jsonify, abort, request
from typing import List, TypeVar


class BasicAuth:
    """basic auth class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """extract_base64_authorization_header"""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
        
