import magic
from sqlalchemy.orm import lazyload

from ..model.post import Post
from ..model.post_media import PostMedia
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
        if len(data['description']) < 1:
            errors['description'] = 'Description too short (<1 characters)'
        if len(data['description']) > 4000:
            errors['description'] = 'Description too long (>4000 characters)'
        if data['media'] and data['media'].filename == '':
            errors['media'] = 'Media should have a valid filename'
        elif data['media']:
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
            query = query.offset(offset)

        return query.options(lazyload('user'), lazyload('medias')).all()

    # atomic
    @staticmethod
    def create_post(description, user_id, media_url=None, media_type=None):
        # pylint: disable=broad-except
        """create new post"""
        try:
            new_post = Post(
                description=description,
                # media=media,
                user_id=user_id,
            )
            db.session.add(new_post)
            db.session.flush()
            if media_url:
                new_media = PostMedia(
                    post_id=new_post.id,
                    path=media_url,
                    media_type=media_type
                )
                db.session.add(new_media)
            db.session.commit()
        except Exception as err:
            print(err)
            db.session.rollback()
            return None

        return new_post

    @staticmethod
    def determine_media_type(media):
        """
        guess media type
        """
        media.seek(0)
        buffer = media.read(1024)
        media.seek(0)
        mime = magic.from_buffer(buffer, mime=True)
        if mime.startswith('video/'):
            return 'video'
        if mime.startswith('image/'):
            return 'image'
        return 'unknown'
