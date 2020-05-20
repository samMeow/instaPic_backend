import magic

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
    def list_post(limit, offset):
        """search post"""
        data = Post.query.limit(limit).offset(offset).all()
        return data

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
