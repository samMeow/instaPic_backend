from app.main import db
from app.main.model.user import User

# pylint: disable=too-few-public-methods
class UserService:
    """User related Operation"""
    @staticmethod
    def save_new_user(data):
        """
        Create User
        """
        user = User.query.filter_by(username=data['username']).first()
        if user:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return response_object, 409
        new_user = User(
            username=data['username'],
            password=data['password']
        )
        UserService.save_changes(new_user)
        return new_user, 201


    @staticmethod
    def search_user(username='', limit=5):
        """
        search by allowed filters
        """
        query = User.query
        if username:
            search = "{}%".format(username.replace('%', r'\%'))
            query = query.filter(User.username.like(search))
        return query.limit(limit).all()

    @staticmethod
    def get_a_user(user_id):
        """
        one user
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def save_changes(data):
        """
        Commit user data to db
        """
        db.session.add(data)
        db.session.commit()
