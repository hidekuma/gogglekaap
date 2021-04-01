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

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        db_env = os.environ.get('SQLALCHEMY_DATABASE_URI')
        if db_env:
            return db_env
        return self.SQLALCHEMY_DATABASE_URI

class DevelopmentConfig(Config):
    """Flask Config for Dev"""
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 1
    WTF_CSRF_ENABLED = False

class TestingConfig(DevelopmentConfig):
    """Flask Config for Testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "sqlite_test.db")}'

class ProductionConfig(Config):
    """Flask Confir Production"""
    pass
