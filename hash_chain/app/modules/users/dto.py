from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('users', description='user related operations')
    user_list = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'public_id': fields.String(description='user Identifier'),
        "admin": fields.Boolean,
        "registered_on": fields.String(attribute="registered_on_str"),
    })

    user_create = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        "admin": fields.Boolean,
    })
