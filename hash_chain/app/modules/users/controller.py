from http import HTTPStatus

from flask import request
from flask_restx import Resource

from hash_chain.app.modules.auth.decorators import admin_token_required
from hash_chain.app.modules.users.dto import UserDto
from hash_chain.app.modules.users.services import get_all_users, save_new_user, get_a_user

api = UserDto.api
_user_list = UserDto.user_list
_user_create = UserDto.user_create


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.doc(security='jwt_token')
    @admin_token_required
    @api.marshal_list_with(_user_list, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.doc('create a new user')
    @api.doc(security='jwt_token')
    @admin_token_required
    @api.expect(_user_create, validate=True)
    @api.response(int(HTTPStatus.CREATED), 'User successfully created.')
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @admin_token_required
    @api.doc(security='jwt_token')
    @api.marshal_with(_user_list)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user
