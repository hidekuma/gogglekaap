from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    print('run: create_app()')
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secretkey'

    if app.config['DEBUG']:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

    '''CSRF INIT'''
    csrf.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    from gogglekaap.forms.auth_form import LoginForm, RegisterForm
    @app.route('/auth/login')
    def login():
        form = LoginForm()
        return render_template('login.html', form=form)

    @app.route('/auth/register')
    def register():
        form = RegisterForm()
        return render_template('register.html', form=form)

    @app.route('/auth/logout')
    def logout():
        return 'logout'

    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html'), 404

    return app