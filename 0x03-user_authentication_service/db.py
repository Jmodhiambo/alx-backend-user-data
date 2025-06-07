#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import logging
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
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
        """Saves user to the databases with hashed password."""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()  # Commits the changes to the database.

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Returns the first row found in the users table as filtered by
        the method’s input arguments."""

        session = self._session

        if not kwargs:
            raise InvalidRequestError

        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound
        except Exception:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates the user’s attributes as passed in the method’s arguments"""
        user = self.find_user_by(id=user_id)
        session = self._session
        for attr, val in kwargs.items():
            if not hasattr(user, attr):
                raise ValueError
            setattr(user, attr, val)
        session.commit()
