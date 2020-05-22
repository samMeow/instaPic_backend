# pylint: disable=missing-class-docstring, too-few-public-methods
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', '')
    AWS_BUCKET_PATH = os.getenv('AWS_BUCKET_PATH', '')
    ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', '')

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL', '')
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    #     os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
