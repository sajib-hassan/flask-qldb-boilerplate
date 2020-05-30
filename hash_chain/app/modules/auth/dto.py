from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    auth = api.model('auth', {
        'email': fields.String(required=True, nullable=False, description='The email address'),
        'password': fields.String(required=True, nullable=False, description='The user password '),
    })

    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        # 'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        "admin": fields.Boolean,
        "registered_on": fields.String(attribute="registered_on_str"),
        "token_expires_in": fields.String,
    })
