# encoding: utf-8
from http import HTTPStatus

from flask_restx import Resource

from hash_chain.app.modules.auth.decorators import token_required
from hash_chain.app.modules.auth.dto import AuthDto
from hash_chain.app.modules.auth.services import Auth

api = AuthDto.api
user_auth = AuthDto.auth
user_model = AuthDto.user


@api.route('/login')
class UserLogin(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/login."""

    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    @api.response(int(HTTPStatus.OK), "Login succeeded.")
    @api.response(int(HTTPStatus.UNAUTHORIZED), "email or password does not match")
    @api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Authenticate an existing user and return an access token."""
        return Auth.login_user()


@api.route("/user")
class GetUser(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/user."""

    @api.doc(security="jwt_token")
    @token_required
    @api.response(int(HTTPStatus.OK), "Token is currently valid.", user_model)
    @api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @api.marshal_with(user_model)
    def get(self):
        """Validate access token and return user info."""
        return Auth.get_logged_in_user()


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """

    @api.doc('logout a user')
    @api.doc(security='jwt_token')
    @api.response(int(HTTPStatus.OK), "Log out succeeded, token is no longer valid.")
    @api.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @api.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @api.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Add token to blacklist, deauthenticating the current user."""
        return Auth.logout_user()
