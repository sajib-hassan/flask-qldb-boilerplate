import datetime
import uuid
from http import HTTPStatus

from hash_chain.app.extensions import db
from hash_chain.app.extensions.api.api import create_auth_successful_response
from hash_chain.app.modules.users.models import User


def save_new_user(data):
    user = User.find_by_email(data['email'])
    if user:
        response_object = {
            'status': 'fail',
            'message': f"{data['email']} is already registered",
        }
        return response_object, HTTPStatus.CONFLICT

    new_user = User(
        public_id=str(uuid.uuid4()),
        email=data['email'],
        username=data['username'],
        password=data['password'],
        registered_on=datetime.datetime.utcnow(),
        admin=data['admin']
    )
    save_changes(new_user)
    return generate_token(new_user)


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.find_by_public_id(public_id)


def generate_token(user):
    try:
        # generate the auth token
        access_token = user.encode_access_token()
        return create_auth_successful_response(
            token=access_token.decode(),
            status_code=HTTPStatus.CREATED,
            message="Successfully registered.",
        )
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, HTTPStatus.UNPROCESSABLE_ENTITY


def save_changes(data):
    db.session.add(data)
    db.session.commit()
