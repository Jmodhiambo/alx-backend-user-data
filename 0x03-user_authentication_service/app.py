#!/usr/bin/env python3
"""Basic Flask App."""

from flask import Flask, jsonify, request, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'])
def home() -> dict:
    """Home page."""
    return jsonify(message="Bienvenue"), 200


@app.route("/users", methods=["POST"])
def registering_user():
    """Registers user from the form input.
        Form fields:
            - email
            - password
    """
    email: str = request.form.get("email")
    password: str = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify(email=email, message="user created")
    except ValueError:
        return jsonify(message="email already registered"), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Creates a session for valid users."""
    email: str = request.form.get("email")
    password: str = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Destroys the session using passed in cookie."""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
