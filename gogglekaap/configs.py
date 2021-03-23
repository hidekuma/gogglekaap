
class Config(object):
    """Flask Config"""
    SECRET_KEY = 'secret'
    SESSION_COOKIE_NAME = 'gogglekaap'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/gogglekaap?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_DOC_EXPANSION = 'list'


class DevelopmentConfig(Config):
    """Flask Config for Dev"""
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 1
    # TODO: 환경분리 및 Front 호출시 토큰삽입 처리
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Flask Confir Production"""
    pass
