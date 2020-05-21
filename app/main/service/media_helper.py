import os
import uuid

from botocore.exceptions import ClientError
from .. import s3
from ..config import Config

# pylint: disable=too-few-public-methods

# no need to gzip as it doesn't help much
# can consider image lossy compression
class MediaHelper:
    """Media Helping service"""

    @staticmethod
    def save_file(file):
        """Upload file"""
        _, ext = os.path.splitext(file.filename)
        object_name = str(uuid.uuid4()) + ext
        try:
            s3.upload_fileobj(file, Config.AWS_BUCKET_NAME, object_name)
        except ClientError as err:
            print(err)
            return None
        return Config.AWS_BUCKET_PATH + '/' + object_name

    @staticmethod
    def del_file(object_name):
        # pylint: disable=broad-except
        """DEL s3 object"""
        try:
            s3.delete_object(Bucket=Config.AWS_BUCKET_NAME, Key=object_name)
        except Exception as err:
            print(err)
            return False
        return True
