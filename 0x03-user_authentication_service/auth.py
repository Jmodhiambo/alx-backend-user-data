#!/usr/bin/env python3
"""Authentication Module."""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4
from typing import Optional


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

    def create_session(self, email: str) -> str:
        """Creates a session and returns session ID."""
        db = self._db
        try:
            user = db.find_user_by(email=email)
            session_id = _generate_uuid()
            db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Gets a user from the session ID."""
        if session_id is None:
            return None

        db = self._db
        try:
            user = db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset token for the user with the given email."""
        db = self._db
        try:
            user = db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session by updating session ID to None."""
        db = self._db
        db.update_user(user_id, session_id=None)


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
    return str(uuid4())
