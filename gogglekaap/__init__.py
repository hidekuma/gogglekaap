from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'

    if app.config['DEBUG'] == True:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

    ''' === CSRF Init === '''
    csrf.init_app(app)

    ''' === auth === '''
    from gogglekaap.forms.auth_form import LoginForm, RegisterForm
    @app.route('/auth/login', methods=['GET', 'POST'])
    def login():
        # TODO
        # 1) 존재하는지 유저 확인
        # 2) 패스워드 정합확인
        # 3) 로그인 유지 (세션)
        form = LoginForm()
        if form.validate_on_submit():
            user_id = form.user_id.data
            password = form.password.data
            return f'{user_id}, {password}'

        return render_template(
            'login.html',
            form=form
        )

    @app.route('/auth/logout')
    def logout():
        # TODO: 유저 세션 제거
        return 'logout'

    @app.route('/auth/register', methods=['GET', 'POST'])
    def register():
        # TODO
        # 1) 유저가 존재하는지 확인
        # 2) 없으면 유저 생성
        # 3) 로그인 유지 (세션)
        form = RegisterForm()
        if form.validate_on_submit():
            user_id = form.user_id.data
            user_name = form.user_name.data
            password = form.password.data
            repassword = form.repassword.data
            return f'{user_id}, {user_name}, {password}, {repassword}'
        return render_template(
            'register.html',
            form=form
        )

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404.html'), 404

    return app
