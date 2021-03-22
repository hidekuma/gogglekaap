from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request,
    session,
    g
)
from gogglekaap.forms.auth_form import LoginForm, RegisterForm
from gogglekaap.models.user import User as UserModel
from gogglekaap import db
from werkzeug import security

NAME = 'auth'
bp = Blueprint(NAME, __name__, url_prefix='/auth')

@bp.before_app_request
def before_app_request():
    # from flask import current_app as app
    # app.logger.info('BEFORE_APP_REQUEST')
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
    if form.validate_on_submit():
        user_id = form.user_id.data
        password = form.password.data
        user = UserModel.find_one_by_user_id(user_id)
        if user:
            if not security.check_password_hash(user.password, password):
                flash('Password is not valid.')
            else:
                session['user_id'] = user.user_id
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

        user = UserModel.find_one_by_user_id(user_id)
        if user:
            flash('User ID is already exists.')
            return redirect(request.path)
        else:
            user = UserModel(
                user_id=user_id,
                user_name=user_name,
                password=security.generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.user_id

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
