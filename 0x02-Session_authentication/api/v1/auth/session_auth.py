#!/usr/bin/env python3
"""Class SessionAuth that inherits from Auth
"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """A class that inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a <user_id>."""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())  # Creates a session ID
        # Stores user_id by in the dictonary with session_id as key.
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id
