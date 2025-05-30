#!/usr/bin/env python3
"""Session expiration authentication"""

from datetime import datetime, timedelta
from os import getenv
from typing import Optional
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration"""

    def __init__(self) -> None:
        """Initialize with session duration from environment"""
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "0"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> Optional[str]:
        """Create a session and store creation timestamp"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """Return user_id if session is valid and not expired"""
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if not created_at or not isinstance(created_at, datetime):
            return None

        time = datetime.now()
        if time > created_at + timedelta(seconds=self.session_duration):
            return None

        return session_dict.get("user_id")
