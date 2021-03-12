import sys
sys.path.append('.')

from gogglekaap.configs import TestingConfig
from gogglekaap import create_app, db
from gogglekaap.models.user import User as UserModel
from gogglekaap.models.memo import Memo as MemoModel
import pytest
import os
import shutil


@pytest.fixture(scope='session')
def user_data():
    yield dict(
        user_id='tester',
        user_name='tester',
        password='tester'
    )

@pytest.fixture(scope='session')
def memo_data():
    yield dict(
        title='title',
        content='content',
    )

@pytest.fixture(scope='session')
def app(user_data, memo_data):
    app = create_app(TestingConfig())
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = UserModel(**user_data)
        db.session.add(user)
        # flush()를 통해서, user 고유 아이디 조회
        db.session.flush()
        memo_data['user_id'] = user.id
        db.session.add(MemoModel(**memo_data))
        db.session.commit()
        yield app

        # 불필요 디비 정리 및 삭제
        path = os.path.join(
            app.static_folder,
            app.config['USER_STATIC_BASE_DIR'],
            'tester'
        )
        shutil.rmtree(path, True)
        db.drop_all()
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace(
            'sqlite:///',
            ''
        )
        if os.path.isfile(db_path):
            os.remove(db_path)


@pytest.fixture(scope='session')
def client(app, user_data):
    with app.test_client() as client:
        # NOTE: 세션 입혀기주기
        with client.session_transaction() as session:
            session['user_id'] = user_data['user_id']

        yield client
