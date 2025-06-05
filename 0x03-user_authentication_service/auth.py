#!/usr/bin/env python3
"""Encrpyting password using bcrypt."""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Encrypts a password using bcrypt."""
    password = password.encode()  # Convert password to bytes

    # Generate salt
    salt: bytes = bcrypt.gensalt()

    # Hashing
    hashed_pwd: bytes = bcrypt.hashpw(password, salt)

    return hashed_pwd
