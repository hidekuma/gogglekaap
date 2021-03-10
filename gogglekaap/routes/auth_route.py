from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    request,
    session,
    flash
)
from gogglekaap.forms.auth_form import LoginForm, RegisterForm
from werkzeug import security

NAME = 'auth'
bp = Blueprint(NAME, __name__, url_prefix='/auth')


''' === only for testing === '''
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

USERS.append(User('hidekuma', 'hidekuma', security.generate_password_hash('hidekuma')))
USERS.append(User('tester', 'tester', security.generate_password_hash('tester')))
USERS.append(User('admin', 'admin', security.generate_password_hash('admin')))

@bp.route('/')
def index():
    return redirect(url_for(f'{NAME}.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # TODO
        # 1) 유저조회
        # 2) 존재하는 유저 인지 체크
        # 3) 패스워드 정합확인
        # 3) 로그인 유지(세션)
        user_id = form.data.get('user_id')
        user = [user for user in USERS if user.user_id == user_id]
        if user:
            user = user[0]
            if not security.check_password_hash(
                user.password,
                form.password.data
            ):
                flash('Password is not valid.')
            else:
                session['user_id'] = user_id
                return redirect(url_for('base.index'))
        else:
            flash('User ID is not exists.')
        return redirect(request.path)
    else:
        flash_form_errors(form)

    if session.get("user_id"):
        return redirect(url_for('base.index'))
    return render_template(f'{NAME}/login.html', form=form)

@bp.route('/logout')
def logout():
    # TODO: 로그아웃 제거(세션)
    session.pop('user_id', None)
    return redirect(url_for(f'{NAME}.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # TODO
        # 1) 유저조회
        # 2) 유저 이미 존재하는지 체크
        # 3) 없으면 유저 생성
        # 4) 로그인 유지(세션)
        user_id = form.data.get('user_id')
        user = [user for user in USERS if user.user_id == user_id]
        if user:
            flash('User ID is already exsits.')
            return redirect(request.path)
        else:
            USERS.append(User(
                user_id = user_id,
                user_name = form.user_name.data,
                password = security.generate_password_hash(form.password.data)
            ))
            session['user_id'] = user_id
        return redirect(url_for('base.index'))
    else:
        flash_form_errors(form)

    if session.get('user_id'):
        return redirect(url_for('base.index'))
    return render_template(f'{NAME}/register.html', form=form)

def flash_form_errors(form):
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)
