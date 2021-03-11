from flask import Blueprint
from flask_restx import Api
# TODO: Add api namespace

# TODO: Session based authentication

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
    description='Welcome My API docs',
)

# TODO: Add namespace to Blueprint
