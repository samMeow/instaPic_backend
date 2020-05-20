from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import boto3

from .config import config_by_name
from .util.handler import global_handler

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
s3 = boto3.client('s3')

def create_app(config_name):
    """
    main app
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    global_handler(app)

    return app
