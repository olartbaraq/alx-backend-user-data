#!/usr/bin/env python3

"""creating a new authentication mechanism"""

from api.v1.auth.auth import Auth
from api.v1.views.users import User
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

        session_id = str(uuid.uuid4())
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
        if session_id is not None:
            userID = self.user_id_by_session_id.get(session_id)
            return userID

    def current_user(self, request=None):
        """ that returns a User instance based on a cookie value"""
        session_cookie_val = self.session_cookie(request)
        user_session_id = self.user_id_for_session_id(session_cookie_val)
        user_instance = User.get(user_session_id)
        return user_instance

    def destroy_session(self, request=None):
        """ that deletes the user session / logout"""
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_by_session_id.get(session_id)
        if user_id:
            self.user_id_by_session_id.pop(session_id)
            return True
        return False
