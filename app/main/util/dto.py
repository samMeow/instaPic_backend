from flask_restplus import Namespace, fields
from werkzeug.datastructures import FileStorage

# pylint: disable=too-few-public-methods

class UserDto:
    """
    User Data model
    """
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.Integer(description='user id'),
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
    user_search = api.parser()
    user_search.add_argument('username', location='args', type=str)


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

class PostDto:
    """
    Post data model
    """
    api = Namespace('post', description="post related operations")
    post = api.model('post', {
        'id': fields.Integer(description='post id'),
        'description': fields.String(
            required=True,
            description='Post short description',
            max_length=4000,
        ),
        'media': fields.String(description='post image path'),
        'user_id': fields.Integer(description='post creator'),
        'create_time': fields.DateTime(),
    })

    upload_post = api.parser()
    upload_post.bundle_errors = True
    upload_post.add_argument('description', location='form', type=str, required=True)
    upload_post.add_argument('media', location='files', type=FileStorage)

class MediaDto:
    """
    Image operation
    """
    api = Namespace('media', description="Media related operation")
