#!/usr/bin/env python3
"""Authentication Module."""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user to the database if does not exists."""
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")


def _hash_password(password: str) -> bytes:
    """Encrypts a password using bcrypt."""
    password = password.encode()  # Convert password to bytes

    # Generate salt
    salt: bytes = bcrypt.gensalt()

    # Hashing
    hashed_pwd: bytes = bcrypt.hashpw(password, salt)

    return hashed_pwd
