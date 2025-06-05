#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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

    def find_user_by(self, email=None) -> User:
        """
        Returns the first row found in the users table as filtered by
        the method’s input arguments."""

       session = self._session

        if not kwargs:
            raise InvalidRequestError

        try:
            user = session.query(User).filter_by(email=email).first()
            return user
        except NoResultFound:
            raise NoResultFound
        except Exception:
            raise InvalidRequestError
