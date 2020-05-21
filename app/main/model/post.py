from sqlalchemy.sql import func
from sqlalchemy import ForeignKeyConstraint, Index
from .. import db

# pylint: disable=too-few-public-methods
class Post(db.Model):
    # pylint: disable=no-member
    """
    Post table
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text, nullable=False)
    media = db.Column(db.String(255))
    user_id = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, server_default=func.now())
    user = db.relationship('User', lazy='selectin')

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'], ['users.id'],
            name='fk_posts_user_id'
        ),
        # sort by time
        Index('idx_posts_create_time', 'create_time'),
        # use for filter and sort by create time
        Index('idx_posts_user_id_create_time', 'user_id', 'create_time')
    )
