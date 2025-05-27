#!/usr/bin/env python3
"""
BasicAuth module
"""

from api.v1.auth.auth import Auth
import base64


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
