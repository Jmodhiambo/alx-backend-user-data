#!/usr/bin/env python3
"""UserSession model to persist sessions"""

from models.base import Base


class UserSession(Base):
    """Class to persist session ID <-> user ID"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize UserSession with user_id and session_id"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
