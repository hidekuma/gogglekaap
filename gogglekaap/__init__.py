from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
# db = 'database'

# flask run -> create_app()
def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'

    if app.config['DEBUG'] == True:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
        app.config['TEMPLATES_AUTO_RELOAD'] = True

    """ === CSRF Init === """
    csrf.init_app(app)

    """ === Routes Init === """
    from gogglekaap.routes import base_route
    app.register_blueprint(base_route.bp)

    from gogglekaap.forms.auth_form import LoginForm, RegisterForm
    @app.route('/auth/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            # TODO
            # 1) 유저조회
            # 2) 존재하는 유저 인지 체크
            # 3) 패스워드 정합확인
            # 3) 로그인 유지(세션)
            user_id = form.data.get('user_id')
            password = form.data.get('password')
            return f'{user_id}, {password}'
        else:
            # TODO: 에러컨트롤
            pass
        return render_template('login.html', form=form)

    @app.route('/auth/logout')
    def logout():
        # TODO: 로그아웃 제거(세션)
        return 'logout'

    @app.route('/auth/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            # TODO
            # 1) 유저조회
            # 2) 유저 이미 존재하는지 체크
            # 3) 없으면 유저 생성
            # 4) 로그인 유지(세션)
            user_id = form.data.get('user_id')
            password = form.data.get('password')
            repassword = form.data.get('repassword')
            user_name = form.data.get('user_name')
            return f'{user_id}, {password}, {repassword}, {user_name}'
        else:
            # TODO: 에러컨트롤
            pass
        return render_template('register.html', form=form)

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
