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

def numeric_list(value):
    """
    parse CSV to numeric integer
    """
    if not value:
        return None
    temp = value.split(',')
    if not all([v.isnumeric() for v in temp]):
        raise ValueError('Unable to parse as integer list')
    return [int(v) for v in temp]

numeric_list.__schema__ = {'type': 'string', 'format': 'comma separate integer'}
class PostDto:
    """
    Post data model
    """
    api = Namespace('post', description="post related operations")
    post_media = api.model('post_media', {
        'id': fields.Integer(description='post media id'),
        'post_id': fields.Integer(description='parent post id'),
        'media_type': fields.String(description='media type video / image'),
        'path': fields.String(description='public url to access media'),
        'create_time': fields.DateTime(description='create date time')
    })
    post = api.model('post', {
        'id': fields.Integer(description='post id'),
        'description': fields.String(
            required=True,
            description='Post short description',
            max_length=4000,
        ),
        'medias': fields.List(fields.Nested(post_media), description='all medias'),
        'user_id': fields.Integer(description='post creator'),
        'create_time': fields.DateTime(description='create time'),
        'user': fields.Nested(UserDto.user, description='user from user_id'),
    })
    meta = api.model('meta', {
        'has_next_page': fields.Boolean(description='has next page')
    })
    post_list = api.model('post_list', {
        'data': fields.List(fields.Nested(post), description='list of post'),
        'meta': fields.Nested(meta, description='Metadata')
    })

    upload_post = api.parser()
    upload_post.bundle_errors = True
    upload_post.add_argument('description', location='form', type=str, required=True)
    upload_post.add_argument('media', location='files', type=FileStorage)

    post_search = api.parser()
    post_search.bundle_errors = True
    post_search.add_argument(
        'sort',
        location='args', type=str, default='create_time', choices=('create_time')
    )
    post_search.add_argument(
        'order',
        location='args', type=str, default='desc', choices=('asc', 'desc')
    )
    post_search.add_argument(
        'filters[user_ids]',
        location='args', type=numeric_list
    )
    post_search.add_argument(
        'page[number]',
        location='args', type=int, default=0
    )
    post_search.add_argument(
        'page[size]',
        location='args', type=int, default=20
    )
