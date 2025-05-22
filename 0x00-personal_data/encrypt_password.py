#!/usr/bin/env python3
"""
Password hashing utility.
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
    # Convert string to bytes
    password_bytes = password.encode('utf-8')
    # Generate salt and hash password
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed
