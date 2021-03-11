import sys
sys.path.append('.')

from gogglekaap.configs import TestingConfig
from gogglekaap import create_app, db
from gogglekaap.models.user import User as UserModel
import pytest


@pytest.fixture
def user_data():
    yield dict(
        user_id='tester',
        user_name='tester',
        password='tester'
    )

@pytest.fixture
def app(user_data):
    app = create_app(TestingConfig())
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(UserModel(**user_data))
        db.session.commit()
    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client
