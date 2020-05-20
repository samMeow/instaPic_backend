import os
from flask import redirect, url_for, send_from_directory
from flask_restplus import Resource
from werkzeug.utils import secure_filename

from ..util.dto import PostDto
from ..config import Config

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

api = PostDto.api
_post = PostDto.post
_upload_post = PostDto.upload_post

def allowed_file(filename):
    """
    temp
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('')
class PostList(Resource):
    # pylint: disable=no-self-use
    """
    Post list route
    """
    @api.response(201, 'Post successfully created.')
    @api.doc('create a new post')
    @api.expect(_upload_post, validate=True)
    def post(self):
        """Creates a new post"""
        args = _upload_post.parse_args()
        file = args['media']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file is None or file.filename == '':
            return {'message': 'Missing file'}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Config.UPLOAD_DIR, filename))
            return redirect(url_for('api.post_post',
                                    filename=filename))
        return {'message': 'sth wrong'}, 400

@api.route('/<filename>')
class Post(Resource):
    # pylint: disable=no-self-use
    """
    post router
    """
    def get(self, filename):
        """
        serve file
        """
        return send_from_directory(Config.UPLOAD_DIR, filename)
