from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    g
)

NAME = 'base'
bp = Blueprint(NAME, __name__)

@bp.route('/')
def index():
    if not g.user:
        return redirect(url_for('auth.login'))
    return render_template('index.html')
