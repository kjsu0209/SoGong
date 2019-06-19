import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        userid = request.form['id']
        pw = request.form['pw']
        name = request.form['name']
        phone = request.form['phone']
        age = request.form['age']
        gender = request.form['gender']

        db = get_db()
        error = None

        if not userid:
            error = '아이디를 입력하세요'
        elif not pw:
            error = '비밀번호를 입력하세요'
        elif db.execute(\
            'SELECT id FROM USER_sp WHERE name = ?', (name,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(name)

        if error is None:
            db.execute(
                'INSERT INTO USER_sp (name, utype, id, pw, phone, age, sex, accid) VALUES (?, ?,?,?,?,?,?,?)',
                (name, 0, userid, generate_password_hash(pw), phone, age, gender, 1)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pw']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user_sp WHERE id = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['pw'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user_sp WHERE id = ?', (user_id,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view