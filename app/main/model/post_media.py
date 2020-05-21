from sqlalchemy.sql import func
from sqlalchemy import ForeignKeyConstraint, Index
from .. import db

# pylint: disable=too-few-public-methods
class PostMedia(db.Model):
    # pylint: disable=no-member
    """
    many to one post media (attachment)
    """
    __tablename__ = 'post_medias'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, nullable=False)
    media_type = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, server_default=func.now())

    post = db.relationship('Post', lazy='selectin')

    __table_args__ = (
        ForeignKeyConstraint(
            ['post_id'], ['posts.id'],
            name='fk_post_medias_post'
        ),
        Index('idx_post_medias_post_id_id', 'post_id', 'id'),
    )
