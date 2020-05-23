from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import UserService
from ..util.decorator import token_required

api = UserDto.api
_user = UserDto.user
_user_request = UserDto.user_request
_user_search = UserDto.user_search


@api.route('')
class UserList(Resource):
    # pylint: disable=no-self-use
    """
    User list route
    """
    @token_required
    @api.expect(_user_search, validate=True)
    @api.doc('search user by username')
    @api.response(200, 'List of users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """search user by username"""
        args = _user_search.parse_args()
        return UserService.search_user(username=args['username'])

    @api.expect(_user_request, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.marshal_with(_user, skip_none=True)
    def post(self):
        """Creates a new User"""
        data = request.json
        response, status = UserService.save_new_user(data=data)
        if status != 201:
            api.abort(status, response['message'], status=response['status'])
        return response, 201



@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    # pylint: disable=no-self-use
    """
    User detail Route
    """
    @token_required
    @api.doc('get a user')
    @api.marshal_with(_user, skip_none=True)
    def get(self, user_id):
        """get a user given its identifier"""
        user = UserService.get_a_user(user_id)
        if not user:
            return api.abort(404)
        return user
