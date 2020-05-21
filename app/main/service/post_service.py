import magic
from sqlalchemy.orm import lazyload

from ..model.post import Post
from .. import db

class PostService:
    """
    post related business logic
    """
    @staticmethod
    def validate_post(data):
        """
        Validate Post request
        """
        errors = {}
        if len(data['description']) > 4000:
            errors['description'] = 'Description too long (>4000 character)'
        if data['media'] and data['media'].filename == '':
            errors['media'] = 'Media should have a valid filename'
        else:
            file = data['media']
            buffer = file.read(1024)
            file.seek(0)
            mime = magic.from_buffer(buffer, mime=True)
            if not mime.startswith('video/') and not mime.startswith('image/'):
                errors['media'] = 'Media can only be image / video'
        return errors

    @staticmethod
    def list_post(filters=None, limit=None, offset=None, sort=None, order=None):
        """search post"""
        query = Post.query
        if filters:
            if filters['user_ids']:
                query = query.filter(Post.user_id.in_(filters['user_ids']))

        allowed_sort = {
            'create_time': Post.create_time
        }
        if sort:
            sort = allowed_sort[sort]
            if order == 'desc':
                sort = sort.desc()
            query = query.order_by(sort)

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.limit(offset)

        return query.options(lazyload('user')).all()

    @staticmethod
    def create_post(description, media, user_id):
        """create new post"""
        new_post = Post(
            description=description,
            media=media,
            user_id=user_id,
        )
        PostService.save_changes(new_post)
        return new_post

    @staticmethod
    def save_changes(data):
        """
        Commit user data to db
        """
        db.session.add(data)
        db.session.commit()
