from flask import send_from_directory
from flask_restplus import Resource

from ..config import Config
from ..util.dto import MediaDto

api = MediaDto.api

@api.route('/<filename>')
class Media(Resource):
    # pylint: disable=no-self-use
    """static serve files"""
    def get(self, filename):
        """serve file"""
        return send_from_directory(Config.UPLOAD_DIR, filename)
