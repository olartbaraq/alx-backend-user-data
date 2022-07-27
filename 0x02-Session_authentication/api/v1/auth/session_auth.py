#!/usr/bin/env python3

"""creating a new authentication mechanism"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """class session auth that inherits from base Auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session ID for a user_id"""
        if user_id is None:
            return None

        if type(user_id) is not str:
            return None

        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self,
                               session_id: str = None
                               ) -> str:
        """that returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None

        userID = self.user_id_by_session_id.get(session_id)
        return userID
