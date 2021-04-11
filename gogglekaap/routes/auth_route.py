from flask import Blueprint, render_template, redirect, url_for, flash, session, request, g
from gogglekaap.forms.auth_form import LoginForm, RegisterForm
from gogglekaap.models.user import User as UserModel
from werkzeug import security

NAME = 'auth'
bp = Blueprint(NAME, __name__, url_prefix='/auth')


@bp.before_app_request
def before_app_request():
    g.user = None
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            g.user = user
        else:
            session.pop('user_id', None)

@bp.route('/')
def index():
    return redirect(url_for(f'{NAME}.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # POST, validate OK!
    if form.validate_on_submit():
        user_id = form.data.get('user_id')
        password = form.data.get('password')
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            if not security.check_password_hash(user.password, password):
                flash('Password is not valid.')
            else:
                session['user_id'] = user.user_id
                return redirect(url_for('base.index'))
        else:
            flash('User ID is not exists.')
    else:
        flash_form_errors(form)
    return render_template(f'{NAME}/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = form.data.get('user_id')
        user_name = form.data.get('user_name')
        password = form.data.get('password')
        repassword = form.data.get('repassword')
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            flash('User Id is already exists.')
            return redirect(request.path)
        else:
            g.db.add(
                UserModel(
                    user_id=user_id,
                    user_name=user_name,
                    password=security.generate_password_hash(password)
                )
            )
            g.db.commit()
            session['user_id'] = user_id
            return redirect(url_for('base.index'))

        return f'{user_id}, {user_name}, {password}, {repassword}'
    else:
        flash_form_errors(form)
    return render_template(f'{NAME}/register.html', form=form)

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for(f'{NAME}.login'))

def flash_form_errors(form):
    for _, errors in form.errors.items():
        for e in errors:
            flash(e)