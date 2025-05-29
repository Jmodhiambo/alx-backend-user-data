#!/usr/bin/env python3
"""
BasicAuth module
"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Returns the Base64 part of the Authorization header
        for a Basic Authentication."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Returns the decoded value of a Base64 string."""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        # Determinig if the header is a valid Base64
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header,
                                             validate=True)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        colon_position = decoded_base64_authorization_header.find(":")

        username: str = decoded_base64_authorization_header[:colon_position]
        passwd: str = decoded_base64_authorization_header[colon_position + 1:]

        return (username, passwd)

    def user_object_from_credentials(self, user_email: str, user_pwd: str):
        """Returns the User instance based on email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users or len(users) == 0:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request."""
        # Step 1: Get the authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Step 2: Extract the Base64 part
        base64_part = self.extract_base64_authorization_header(auth_header)
        if base64_part is None:
            return None

        # Step 3: Decode the Base64 string
        decoded = self.decode_base64_authorization_header(base64_part)
        if decoded is None:
            return None

        # Step 4: Extract user credentials
        email, password = self.extract_user_credentials(decoded)
        if email is None or password is None:
            return None

        # Step 5: Get user from credentials
        user = self.user_object_from_credentials(email, password)
        return user
