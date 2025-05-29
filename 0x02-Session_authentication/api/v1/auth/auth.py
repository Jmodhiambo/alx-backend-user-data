#!/usr/bin/env python3
"""
Class Auth
file: api/v1/auth/auth.py
"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Return False (placeholder for auth logic)"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Normalize the path to ensure trailing slash
        if not path.endswith("/"):
            path += "/"

        # Normalize excluded paths
        for excluded in excluded_paths:
            if excluded.endswith('*'):
                # Wildcard path prefix match
                prefix = excluded[:-1]
                if path.startswith(prefix):
                    return False
            else:
                # Normalize to include trailing slash
                if not excluded.endswith('/'):
                    excluded += '/'
                if path == excluded:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """Retrieve the Authorization header from the request"""
        if request is None or "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None (placeholder for user retrieval logic)"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request."""
        if request is None:
            return None

        session_name = os.getenv("SESSION_NAME")
        if session_name is None:
            return None
        return request.cookies.get(session_name)
