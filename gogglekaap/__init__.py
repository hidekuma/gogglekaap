from flask import Flask

db = 'database'

def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    @app.route('/')
    def index():
        app.logger.info('RUN HELLOWORLD!')
        return "Hello World and Python!"


    ''' === Routing Practices === '''
    from markupsafe import escape
    from flask import redirect, jsonify, url_for

    @app.route('/test/name/<string:name>')
    def name(name):
        return f'My name is {name}, {escape(type(name))}'

    @app.route('/test/id/<int:id>')
    def id(id):
        return 'ID is %d' % id

    @app.route('/test/path/<path:subpath>')
    def path(subpath):
        return subpath

    @app.route('/test/json')
    def json():
        return jsonify([{'Hello': 'world'}])

    @app.route('/test/redirect/<path:subpath>')
    def redirect_url(subpath):
        return redirect(subpath)

    @app.route('/test/urlfor')
    def urlfor():
        return redirect(url_for('name', name='hidekuma'))

    ''' === Request hook, Context controll === '''
    from flask import g, current_app

    @app.before_first_request
    def before_first_request():
        app.logger.info('BEFORE_FIRST_REQUEST')

    @app.before_request
    def before_request():
        g.test = True
        app.logger.info("BEFORE_REQUEST")

    @app.after_request
    def after_request(response):
        print(g.test)
        print('mode:', current_app.config['DEBUG'])
        print(app.config['DEBUG'])
        g.test = False
        app.logger.info('AFTER_REQUEST')
        return response

    @app.teardown_request
    def teardown_request(exception):
        print(g.test)
        app.logger.info('TEARDOWN_REQUEST')

    @app.teardown_appcontext
    def teardown_appcontext(exception):
        app.logger.info('TEARDOWN_APPCONTEXT')



    return app
