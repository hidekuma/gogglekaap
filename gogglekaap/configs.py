import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    """Flask Config"""

    SECRET_KEY = 'secret'
    SESSION_COOKIE_NAME = 'gogglekaap'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/gogglekaap?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    USER_STATIC_BASE_DIR = 'user_images'

    def __init__(self):
        db_env = os.environ.get('SQLALCHEMY_DATABASE_URI')
        if db_env:
            self.SQLALCHEMY_DATABASE_URI = db_env

class DevelopmentConfig(Config):
    """Flask Config for Dev"""
    DEBUG=True
    SEND_FILE_MAX_AGE_DEFAULT = 1
    TEMPLATES_AUTO_RELOAD = True
    WTF_CSRF_ENABLED = False

class TestingConfig(DevelopmentConfig):
    __test__ = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "sqlite_test.db")}'

class ProductionConfig(Config):
    """Flask Config for Production"""
    pass
