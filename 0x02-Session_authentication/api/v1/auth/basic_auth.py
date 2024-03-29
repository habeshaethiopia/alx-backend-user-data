#!/usr/bin/env python3
"""
auth module for the API
"""
from flask import jsonify, abort, request
from typing import List, TypeVar
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """basic auth class"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """extract_base64_authorization_header"""
        if authorization_header is None or type(
            authorization_header
        ) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """decode_base64_authorization_header"""
        if (
            base64_authorization_header is None
            or type(base64_authorization_header) is not str
        ):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header
            ).decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """extract_user_credentials"""
        if (
            decoded_base64_authorization_header is None
            or type(decoded_base64_authorization_header) is not str
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """user_object_from_credentials"""
        if (
            user_email is None
            or user_pwd is None
            or type(user_email) is not str
            or type(user_pwd) is not str
        ):
            return None
        try:
            from models.user import User

            users = User.search({"email": user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """current_user"""
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(b64_header)
        user_creds = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_creds[0], user_creds[1])
