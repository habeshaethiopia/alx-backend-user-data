#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from user import User

from user import Base

import bcrypt


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, user) -> None:
        """Add a user to the database"""
        self._session.add(user)
        self._session.commit()

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given attribute"""
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound
            return user
        except InvalidRequestError:
            return None

    def update_user(self, user_id, **kwargs) -> None:
        """Update a user in the database"""

        user = self.find_user_by(id=user_id)
        if not user:
            raise ValueError("No user found with the given id")

        for key, value in kwargs.items():
            setattr(user, key, value)
        self._session.commit()