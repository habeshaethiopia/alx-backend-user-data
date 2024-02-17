#!/usr/bin/env python3
""" Module of session views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
import os


@app_views.route("auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /api/v1/auth_session/login
    Return:
      - the status of the API
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    from models.user import User

    user = User.search({"email": email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    SESSION_NAME = os.getenv("SESSION_NAME")
    response.set_cookie(SESSION_NAME, session_id)
    return response


@app_views.route(
    "auth_session/logout", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /api/v1/auth_session/logout
    Return:
      - the status of the API
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
