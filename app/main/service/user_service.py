from app.main import db
from app.main.model.user import User


def save_new_user(data):
    """
    Create User
    """
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        new_user = User(
            username=data['username'],
            password=data['password']
        )
        save_changes(new_user)
        return generate_token(new_user)
    response_object = {
        'status': 'fail',
        'message': 'User already exists. Please Log in.',
    }
    return response_object, 409

def search_user(username='', limit=5):
    """
    search by allowed filters
    """
    query = User.query
    if username:
        search = "{}%".format(username.replace('%', r'\%'))
        query = query.filter(User.username.like(search))
    return query.limit(limit).all()

def get_a_user(user_id):
    """
    one user
    """
    return User.query.filter_by(id=user_id).first()


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
