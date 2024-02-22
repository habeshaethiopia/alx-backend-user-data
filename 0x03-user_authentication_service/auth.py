#!/usr/bin/env python3
"""Auth module
"""
from db import DB
import bcrypt
from user import User


def _hash_password(password: str) -> str:
    """Hash a password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    @classmethod
    def register_user(cls, email: str, password: str) -> User:
        """Register a user with the database"""
        user = Auth._db.find_user_by(email=email)
        if user:
            raise ValueError("User {} already exists".format(email))
        hashed_password = self._db._hash_password(password)
        user = User(email=email, hashed_password=hashed_password)
        self._db.add_user(user)
        return user
