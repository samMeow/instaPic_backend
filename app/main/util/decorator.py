from functools import wraps

from flask import request

from app.main.service.auth_helper import Auth


def token_required(func):
    """
    JWT middleware
    """
    @wraps(func)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return func(*args, **kwargs)

    return decorated
