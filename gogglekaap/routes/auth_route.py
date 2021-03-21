from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect
)
from gogglekaap.forms.auth_form import LoginForm, RegisterForm

NAME = 'auth'
bp = Blueprint(NAME, __name__, url_prefix='/auth')

@bp.route('/')
def index():
    return redirect(url_for(f'{NAME}.login'))


@bp.route('/login', methods=['GET', 'POST'])
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
        f'{NAME}/login.html',
        form=form
    )

@bp.route('/logout')
def logout():
    # TODO: 유저 세션 제거
    return 'logout'

@bp.route('/register', methods=['GET', 'POST'])
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
        f'{NAME}/register.html',
        form=form
    )

