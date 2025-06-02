#!/usr/bin/env python3
"""
Route module for the API
File: api/v1/app.py
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
if auth_type == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


@app.before_request
def auth_handle() -> str:
    """auth handle."""
    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]

    request.current_user = None

    """if auth.require_auth(request.path, excluded_paths):
        if auth.authorization_header(request) is None:
            abort(401)

        if auth.session_cookie(request) is None:
            abort(401)

        user = auth.current_user(request)
        if user is None:
            abort(403)

        request.current_user = user
    if auth.require_auth(request.path, excluded_paths):
        user = None

        if auth.authorization_header(request):
            user = auth.current_user(request)
        elif auth.session_cookie(request):
            user = auth.current_user(request)

        if user is None:
            abort(401)

        request.current_user = user"""
    if auth.require_auth(request.path, excluded_paths):
        # 1) Grab whichever credential method is in use:
        auth_header = auth.authorization_header(request)
        session_id = auth.session_cookie(request)

        # 2) If neither header nor cookie is present → 401 Unauthorized
        if auth_header is None and session_id is None:
            abort(401)

        # 3) Try to get a user from whichever is present
        user = None
        if auth_header:
            user = auth.current_user(request)
        elif session_id:
            user = auth.current_user(request)

        # 4) If header/cookie was present but didn't map to a valid user
        if user is None:
            abort(403)

        # 5) Finally, stash the authenticated user on the request
        request.current_user = user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
