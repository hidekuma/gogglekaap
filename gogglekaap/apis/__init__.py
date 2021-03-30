from flask import Blueprint, g, abort
from flask_restx import Api
from .user import ns as UserNamespace
from .memo import ns as MemoNamespace
from .label import ns as LabelNamespace
from functools import wraps

blueprint = Blueprint('api', __name__, url_prefix='/api')

def check_session(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        if not g.user:
            abort(401)
        return func(*args, **kwargs)
    return __wrapper

api = Api(
    blueprint,
    version='1.0',
    title='Goggle Kaap APIs',
    description='Goggle Kaap Apis for front-end developer',
    decorators=[check_session],
    doc='/docs'
)


api.add_namespace(UserNamespace)
api.add_namespace(MemoNamespace)
api.add_namespace(LabelNamespace)
