#!/usr/bin/env python3
"""
Password hashing and validation utility.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt with automatic salting.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted and hashed password.
    """
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if a provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain text password to validate.

    Returns:
        bool: True if password matches hashed_password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
