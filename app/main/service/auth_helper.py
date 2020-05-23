from app.main.model.user import User
from ..service.blacklist_service import save_token


class Auth:
    """
    Auth service
    """
    # pylint: disable=inconsistent-return-statements

    @staticmethod
    def login_user(data):
        # pylint: disable=broad-except
        """
        login a user
        """
        try:
            # fetch the user data
            user = User.query.filter_by(username=data.get('username')).first()
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode(),
                        'user': user,
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'username or password does not match.'
                }
                return response_object, 401

        except Exception as err:
            print(err)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        """
        Logout out user from request
        """
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        """
        Get user info from request
        """
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(remove_prefix(auth_token, 'Bearer '))
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'username': user.username
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return response_object, 401

    @staticmethod
    def get_current_user(new_request):
        """
        get current JWT user id
        """
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            return User.decode_auth_token(remove_prefix(auth_token, 'Bearer '))
        return None

def remove_prefix(text, prefix):
    """remove prefix helper"""
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
