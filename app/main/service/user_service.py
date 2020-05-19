import uuid
import datetime

from app.main import db
from app.main.model.user import User


def save_new_user(data):
    """
    Create User
    """
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    response_object = {
        'status': 'fail',
        'message': 'User already exists. Please Log in.',
    }
    return response_object, 409


def get_all_users():
    """
    All user list
    """
    return User.query.all()


def get_a_user(public_id):
    """
    one user
    """
    return User.query.filter_by(public_id=public_id).first()


def generate_token(user):
    # pylint: disable=broad-except
    """
    Get JWT token
    """
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data):
    """
    Commit user data to db
    """
    db.session.add(data)
    db.session.commit()
