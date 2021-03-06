
import datetime
import jwt

from app.main.model.blacklist import BlacklistToken

from ..config import key
from .. import db, flask_bcrypt

class User(db.Model):
    # pylint: disable=no-member
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100))

    # no need to create index for username search
    # as it has unique idx

    @property
    def password(self):
        """
        Read password
        """
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        """
        password setter
        """
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        password check
        """
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        # pylint: disable=broad-except
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as err:
            return err

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)
