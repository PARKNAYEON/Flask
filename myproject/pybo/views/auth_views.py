from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    
    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit(): #POST 방식 요청에는 로그인을 수행 
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id # key, value
            return redirect(url_for('main.index'))
        flash(error)

    return render_template('auth/login.html', form=form) # GET 방식 요청에는 로그인 템플릿을 렌더링

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.before_app_request # 라우터 함수보다 먼저 실행
def load_logged_in_user(): # 함수에서 사용한 g는 플라스크가 제공하는 컨텍스트 변수
    user_id = session.get('user_id') # 세션 변수에 user_id값이 있으면 데이터베이스에서 이를 조회하여 g.user에 저장 -> 이렇게 하면 이후 사용자 로그인 검사를 할 때 session을 조사할 필요가 없다
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# 로그인이 필요함
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view