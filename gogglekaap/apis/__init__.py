from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    blueprint,
    version='1.0',
    title='Goggle Kaap APIs',
    description='Goggle Kaap Apis for front-end developer',
    doc='/docs'
)


# TODO: add namespace to blueprint
