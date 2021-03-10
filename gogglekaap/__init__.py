from flask import Flask, render_template

# db = 'database'

# flask run -> create_app()
def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    @app.route('/')
    def index():
        # app.logger.info('Run HelloWorld!')
        return render_template('index.html')

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404.html'), 404

    # ''' === Method & Request context Practice === '''
    # from flask import request
    # @app.route('/test/method/', defaults={'id': 1}, methods=['GET', 'POST', 'DELETE', 'PUT'])
    # @app.route('/test/method/<int:id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
    # def method_test(id):
        # return jsonify({
            # 'id': id,
            # 'request.args': request.args,
            # 'request.form': request.form,
            # 'request.json': request.json
        # })


    # ''' === Routing Practice === '''
    # from flask import jsonify, redirect, url_for
    # from markupsafe import escape

    # @app.route('/test/name/<name>')
    # def name(name):
        # return f'Name is {name}, {escape(type(name))}'

    # @app.route('/test/id/<int:id>')
    # def id(id):
        # return 'Id: %d' % id

    # @app.route('/test/path/<path:subpath>')
    # def path(subpath):
        # return subpath

    # @app.route('/test/json')
    # def json():
        # return jsonify({'hello': 'world'})

    # @app.route('/test/redirect/<path:subpath>')
    # def redirect_url(subpath):
        # return redirect(subpath)

    # @app.route('/test/urlfor/<path:subpath>')
    # def urlfor(subpath):
        # return redirect(url_for('path', subpath=subpath))

    # ''' === Request hook, Context controll  === '''
    # # https://flask.palletsprojects.com/en/1.1.x/api/
    # from flask import g, current_app
    # @app.before_first_request
    # def before_first_request():
        # app.logger.info('BEFORE_FIRST_REQUEST')

    # @app.before_request
    # def before_request():
        # g.test = True
        # app.logger.info('BEFORE_REQUEST')

    # @app.after_request
    # def after_request(response):
        # app.logger.info(f"g.test: {g.test}")
        # app.logger.info(f"current_app.config: {current_app.config}")
        # app.logger.info("AFTER_REQUEST")
        # return response

    # @app.teardown_request
    # def teardown_request(exception):
        # app.logger.info('TEARDOWN_REQUEST')

    # @app.teardown_appcontext
    # def teardown_appcontext(exception):
        # app.logger.info('TEARDOWN_CONTEXT')

    return app
