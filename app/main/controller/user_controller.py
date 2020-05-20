from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, search_user, get_a_user
from ..util.decorator import token_required

api = UserDto.api
_user = UserDto.user
_user_search = UserDto.user_search


@api.route('')
class UserList(Resource):
    # pylint: disable=no-self-use
    """
    User list route
    """
    @token_required
    @api.expect(_user_search, validate=True)
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        args = _user_search.parse_args()
        return search_user(username=args['username'])

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        """Creates a new User"""
        data = request.json
        return save_new_user(data=data)


@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    # pylint: disable=no-self-use
    """
    User detail Route
    """
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, user_id):
        """get a user given its identifier"""
        user = get_a_user(user_id)
        if not user:
            return api.abort(404)
        return user
