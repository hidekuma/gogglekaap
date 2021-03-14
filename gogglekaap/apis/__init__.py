from flask import Blueprint, g, abort
from flask_restx import Api
from functools import wraps

from .user import ns as UserNamespace
from .memo import ns as MemoNamespace
from .label import ns as LabelNamespace

def check_session(func):
    @wraps(func)
    def __wrapper(*args, **kwargs):
        if not g.user:
            abort(401)
        return func(*args, **kwargs)
    return __wrapper

blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/api'
)

api = Api(
    blueprint,
    title='Goggle Kaap API',
    version='1.0',
    doc='/docs',
    decorators=[check_session],
    description='Welcome My API docs',
)

api.add_namespace(UserNamespace)
api.add_namespace(MemoNamespace)
api.add_namespace(LabelNamespace)
