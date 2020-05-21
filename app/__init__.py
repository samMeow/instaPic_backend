from flask_restplus import Api
from flask import Blueprint, request

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.post_controller import api as post_ns
from .main.util.error_handler import init_error_handler
from .main.config import Config

blueprint = Blueprint('api', __name__)


api = Api(
    blueprint,
    title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
    version='1.0',
    description='a boilerplate for flask restplus web service',
    doc='/docs/'
)
init_error_handler(blueprint)
api.add_namespace(user_ns, path='/users')
api.add_namespace(post_ns, path='/posts')
api.add_namespace(auth_ns)

@blueprint.after_request
def after_request(response):
    """
    add cors header
    """
    allowed = Config.ALLOWED_ORIGIN.split(',')
    origin = request.environ.get('HTTP_ORIGIN', None)
    if origin and origin in allowed:
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
    return response
