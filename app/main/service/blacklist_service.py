
from app.main import db

from app.main.model.blacklist import BlacklistToken


def save_token(token):
    # pylint: disable=no-member, broad-except
    """
    save expired JWT token
    """
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200
    except Exception as err:
        response_object = {
            'status': 'fail',
            'message': err
        }
        return response_object, 200
