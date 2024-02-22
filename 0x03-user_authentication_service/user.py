#!/usr/bin/env python3
"""SQLAlchemy model"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """User class"""
    cnt=0
    def __init__(self, email: str, hashed_password: str):
        """Initialize a new User instance"""
        self.email = email
        self.hashed_password = hashed_password
        User.cnt += 1
        self.id = User.cnt
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    # def __str__(self):
    #     """String representation of the User object"""
    #     return "User: {} {}".format(self.first_name, self.last_name)
    # def __repr__(self):
    #     """String representation of the User object"""
    #     return "User: {} {}".format(self.first_name, self.last_name)
    # def to_dict(self):
    #     """Return a dictionary representation of the object"""
    #     return {
    #         "id": self.id,
    #         "email": self.email,
    #         "hashed_password": self.hashed_password,
    #         "reset_token": self.reset_token,
    #     }

    # def from_dict(self, data):
    #     """Set the object's attributes from a dictionary"""
    #     for key, value in data.items():
    #         setattr(self, key, value)
