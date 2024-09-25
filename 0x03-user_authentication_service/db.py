#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user"""
        session = self._session
        new_user = User()
        new_user.email = email
        new_user.hashed_password = hashed_password
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs: dict) -> User:
        """Find a user"""
        session = self._session
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError
            found = session.query(User).filter(getattr(User,
                                               key) == value).first()
        if not found:
            raise NoResultFound
        return found
