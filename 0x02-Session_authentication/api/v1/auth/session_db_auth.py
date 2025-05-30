#!/usr/bin/env python3
"""Session-based auth with DB persistence"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from typing import Optional
from datetime import datetime, timedelta
from flask import request


class SessionDBAuth(SessionExpAuth):
    """Session authentication that stores sessions in file"""

    def create_session(self, user_id: str = None) -> Optional[str]:
        """Creates and saves a UserSession"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        new_session = UserSession(user_id=user_id, session_id=session_id)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """Returns the user_id from a session_id"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None

        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id

        if not hasattr(session, 'created_at'):
            return None

        ex_time = session.created_at + timedelta(seconds=self.session_duration)
        if ex_time < datetime.utcnow():
            return None

        return session.user_id

    def destroy_session(self, request=None) -> bool:
        """Deletes the UserSession corresponding to the request"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        session = sessions[0]
        session.remove()
        return True
