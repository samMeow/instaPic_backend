from flask_restplus import Resource
from flask import request

from ..util.dto import PostDto
from ..service.auth_helper import Auth
from ..service.post_service import PostService
from ..service.media_helper import MediaHelper
from ..util.decorator import token_required

api = PostDto.api
_post = PostDto.post
_upload_post = PostDto.upload_post

@api.route('')
class PostList(Resource):
    # pylint: disable=no-self-use
    """
    Post list route
    """
    @api.doc('list all post')
    @api.marshal_list_with(_post, envelope='data')
    def get(self):
        """List all registered users"""
        return PostService.list_post(20, 0)

    @token_required
    @api.response(201, 'Post successfully created.')
    @api.doc('create a new post')
    @api.expect(_upload_post, validate=True)
    @api.marshal_with(_post, envelope='data')
    def post(self):
        """Creates a new post"""
        args = _upload_post.parse_args()
        file = args['media']
        # if user does not select file, browser also
        # submit an empty part without filename
        err = PostService.validate_post(args)
        if err:
            api.abort(400, message='Invalid request', errors=err)
        media_url = MediaHelper.save_file(file)
        if not media_url:
            api.abort(400, message='Fail to save media')
        post = PostService.create_post(
            description=args['description'],
            media=media_url,
            user_id=Auth.get_current_user(request)
        )
        return post, 201
