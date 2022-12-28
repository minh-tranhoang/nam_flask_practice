import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config(object):
    """Base config."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    STATIC_FOLDER = 'app/static'
    TEMPLATES_FOLDER = 'app/templates'


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    DATABASE_URI = ""


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    DATABASE_URI = ""
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://<username>:<password>@localhost/<db_name>'


class TestingConfig(Config):
    FLASK_ENV = 'test'
    DEBUG = True
    TESTING = True
    DATABASE_URI = ""
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")
