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
_post_search = PostDto.post_search
_post_list = PostDto.post_list

@api.route('')
class PostList(Resource):
    # pylint: disable=no-self-use
    """
    Post list route
    """
    @api.expect(_post_search, validate=True)
    @api.doc('list all post')
    @api.response(200, 'list of posts with pagination meta')
    @api.marshal_with(_post_list)
    def get(self):
        """List all registered users"""
        args = _post_search.parse_args()
        # not using sqlalchemy pagination as it use (slow) count query
        data = PostService.list_post(
            filters={
                'user_ids': args['filters[user_ids]']
            },
            limit=args['page[size]'] + 1,
            offset=args['page[number]'] * args['page[size]'],
            sort=args['sort'],
            order=args['order']
        )
        response = {
            'meta': {
                'has_next_page': len(data) == args['page[size]'] + 1
            },
            'data': data[0:args['page[size]']]
        }
        return response, 200

    @token_required
    @api.response(201, 'Post successfully created.')
    @api.doc('create a new post')
    @api.response(201, 'successfully create post')
    @api.response(400, 'validation error')
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
        media_type = PostService.determine_media_type(file)
        media_url = MediaHelper.save_file(file)
        if not media_url:
            api.abort(400, message='Fail to save media')
        post = PostService.create_post(
            description=args['description'],
            media_type=media_type,
            media_url=media_url,
            user_id=Auth.get_current_user(request)
        )
        return post, 201
