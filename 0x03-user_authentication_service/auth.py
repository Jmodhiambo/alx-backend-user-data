#!/usr/bin/env python3
"""Authentication Module."""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user."""
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            return False
        if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return False
        return True


def _hash_password(password: str) -> bytes:
    """Encrypts a password using bcrypt."""
    password = password.encode('utf-8')  # Convert password to bytes

    # Generate salt
    salt: bytes = bcrypt.gensalt()

    # Hashing
    hashed_pwd: bytes = bcrypt.hashpw(password, salt)

    return hashed_pwd


def _generate_uuid() -> str:
    """Generates uuid4."""
    return str(uuid4)
