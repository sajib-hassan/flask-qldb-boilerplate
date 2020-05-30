from http import HTTPStatus

from flask import request

from hash_chain.app.extensions import db
from hash_chain.app.extensions.api.api import create_auth_successful_response
from hash_chain.app.modules.auth.models import BlacklistedToken
from hash_chain.app.modules.users.models import User
from hash_chain.app.util.datetime_util import format_timespan_digits, remaining_fromtimestamp
from hash_chain.app.util.exceptions import ApiUnauthorized


def save_token(token):
    blacklist_token = BlacklistedToken(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, 200


class Auth:

    @staticmethod
    def login_user():
        try:
            # fetch the user data
            data = request.json
            user = User.find_by_email(data.get('email'))
            if not user or not user.check_password(data.get('password')):
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, HTTPStatus.UNAUTHORIZED
            access_token = user.encode_access_token()
            return create_auth_successful_response(
                token=access_token.decode(),
                status_code=HTTPStatus.OK,
                message="Successfully logged in.",
            )
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, HTTPStatus.UNPROCESSABLE_ENTITY

    @staticmethod
    def check_access_token(admin_only=False):
        token = request.headers.get("Authorization")
        if not token:
            raise ApiUnauthorized(description="Unauthorized", admin_only=admin_only)
        result = User.decode_access_token(token)
        if result.failure:
            raise ApiUnauthorized(
                description=result.error,
                admin_only=admin_only,
                error="invalid_token",
                error_description=result.error,
            )
        return result.value

    @staticmethod
    def get_logged_in_user():
        _data = Auth.check_access_token()

        public_id = _data.get('public_id')
        user = User.find_by_public_id(public_id)
        if not user:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, HTTPStatus.UNAUTHORIZED

        expires_at = _data.get('expires_at')
        user.token_expires_in = format_timespan_digits(remaining_fromtimestamp(expires_at))
        return user

    @staticmethod
    def logout_user():
        _data = Auth.check_access_token()
        access_token = _data.get('token')
        expires_at = _data.get('expires_at')
        blacklisted_token = BlacklistedToken(access_token, expires_at)
        try:
            db.session.add(blacklisted_token)
            db.session.commit()
            response_dict = dict(status="success", message="Successfully logged out.")
            return response_dict, HTTPStatus.OK
        except Exception as e:
            response_dict = dict(status='fail', message=e)
            return response_dict, HTTPStatus.INTERNAL_SERVER_ERROR
