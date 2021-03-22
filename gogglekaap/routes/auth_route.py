from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request,
    session
)
from gogglekaap.forms.auth_form import LoginForm, RegisterForm
from werkzeug import security

''' === login test === '''
from dataclasses import dataclass

USERS = []

@dataclass
class User:
    """
    class User:
        def __init__(self, user_id, user_name, password):
            self.user_id = user_id
            self.user_name = user_name
            self.password = password
    """
    user_id: str
    user_name: str
    password: str

USERS.append(User(
    'hidekuma',
    'hidekuma',
    security.generate_password_hash('1234')
))
USERS.append(User(
    'tester',
    'tester',
    security.generate_password_hash('1234')
))
USERS.append(User(
    'admin',
    'admin',
    security.generate_password_hash('1234')
))


NAME = 'auth'
bp = Blueprint(NAME, __name__, url_prefix='/auth')

@bp.route('/')
def index():
    return redirect(url_for(f'{NAME}.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        user = [user for user in USERS if user.user_id == user_id]
        if user:
            user = user[0]
            if not security.check_password_hash(user.password, password):
                flash('Password is not valid.')
            else:
                session['user_id'] = user_id
                return redirect(url_for('base.index'))
        else:
            flash('User ID is not exists.')

        return redirect(request.path)
    else:
        flash_form_errors(form)

    if session.get('user_id'):
        return redirect(url_for('base.index'))

    return render_template(
        f'{NAME}/login.html',
        form=form
    )

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for(f'{NAME}.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        user_name = form.user_name.data
        password = form.password.data

        user = [user for user in USERS if user.user_id == user_id]
        if user:
            flash('User ID is already exists.')
            return redirect(request.path)
        else:
            USERS.append(User(
                user_id=user_id,
                user_name=user_name,
                password=security.generate_password_hash(password)
            ))
            session['user_id'] = user_id

        return redirect(url_for('base.index'))
    else:
        flash_form_errors(form)

    if session.get('user_id'):
        return redirect(url_for('base.index'))

    return render_template(
        f'{NAME}/register.html',
        form=form
    )

def flash_form_errors(form):
    # {'password' : ['password must match']}
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)
