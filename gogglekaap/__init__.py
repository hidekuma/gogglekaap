from flask import Flask, render_template, g
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config=None):
    print('run: create_app()')
    app = Flask(__name__)

    ''' === Flask Configuration === '''
    from .configs import DevelopmentConfig, ProductionConfig
    if not config:
        if app.config['DEBUG'] == True:
            config = DevelopmentConfig()
        else:
            config = ProductionConfig()

    print('run with: ', config)
    app.config.from_object(config)

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
