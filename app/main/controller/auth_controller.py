from flask import request
from flask_restplus import Resource

from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto

api = AuthDto.api
user_auth = AuthDto.user_auth
auth_response = AuthDto.auth_response


@api.route('/login')
class UserLogin(Resource):
    # pylint: disable=no-self-use
    """
     User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    @api.marshal_with(auth_response, skip_none=True)
    def post(self):
        """get the post data"""
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    # pylint: disable=no-self-use
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        """get auth token"""
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
