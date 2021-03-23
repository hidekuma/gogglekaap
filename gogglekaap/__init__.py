from flask import Flask, render_template, g
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'
    app.config['SESSION_COOKIE_NAME'] = 'gogglekaap'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/gogglekaap?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'

    if app.config['DEBUG'] == True:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
        # TODO: 환경분리 및 Front 호출시 토큰삽입 처리
        app.config['WTF_CSRF_ENABLED'] = False

    ''' === CSRF Init === '''
    csrf.init_app(app)

    """ === Database Init === """
    db.init_app(app)
    migrate.init_app(app, db)

    """ === RestX Init === """
    from .apis import blueprint as api
    app.register_blueprint(api)

    """ === Routes Init === """
    from gogglekaap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)

    ''' === Request Hook === '''
    @app.before_request
    def before_request():
        # app.logger.info('BEFORE_REQUEST')
        g.db = db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404.html'), 404

    return app
