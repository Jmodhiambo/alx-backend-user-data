#!/usr/bin/env python3
"""
Class Auth
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return False (placeholder for auth logic)"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None (placeholder for header extraction logic)"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None (placeholder for user retrieval logic)"""
        return None
