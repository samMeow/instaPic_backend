from flask_restplus import Namespace, fields

# pylint: disable=too-few-public-methods

class UserDto:
    """
    User Data model
    """
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'username': fields.String(
            required=True,
            description='user username',
            min_length=6,
            max_length=255
        ),
        'password': fields.String(
            required=True,
            description='user password',
            min_length=6,
            max_length=255
        )
    })


class AuthDto:
    """
    Auth data model
    """
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'username': fields.String(
            required=True,
            description='The username',
            min_length=6,
            max_length=255
        ),
        'password': fields.String(
            required=True,
            description='The user password',
            min_length=6,
            max_length=255
        ),
    })
