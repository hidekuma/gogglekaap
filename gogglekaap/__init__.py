from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SESSION_COOKIE_NAME'] = 'gogglekaap'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/gogglekaap?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if app.config['DEBUG']:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

    '''DB INIT'''
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    '''Routes INIT'''
    from gogglekaap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)

    '''CSRF INIT'''
    csrf.init_app(app)

    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html'), 404

    return app