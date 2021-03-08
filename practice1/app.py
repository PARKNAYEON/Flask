import os
from flask import Flask
from flask import request
from flask import redirect
from flask import session
from flask import render_template
from models import db
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm
from forms import LoginForm

from models import Fcuser

app = Flask(__name__)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #login --> session
        session['userid'] = form.data.get('userid')  #원하는 정보를 추가 로그인이 안한 사람은 아무런 정보가 없다(userid라는 값이 없음)
        return redirect('/')

    return render_template('login.html', form=form)


# @app.route('/register') # get밖에 허용을 하지 않는다.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
    # if request.method == 'POST':
    #     # 회원정보 생성
    #     userid = request.form.get('userid')
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     re_password = request.form.get('re-password')
        #검증 단계
    #    if (userid and username and password and re_password) and password == re_password:
        # db에 넣겠다!
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = form.data.get('password')
        # fcuser.userid = userid
        # fcuser.username = username
        # fcuser.password = password

        db.session.add(fcuser)

         #이제 커밋을 해야해
        db.session.commit()
        print('Success!')
        return redirect('/')

    return render_template('register.html', form=form)


'''
teardown : 사용자의 요청의 끝
commit : commit하면 동작을 쌓아둔 것를 데이터베이스에 저장하는 것(실제로 반영하는 역할)
transaction
'''

'''
# 테이블 만들기
class Test(db.Model): 
    __tablename__ = 'test_table' #테이블 명
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

db.create_all()
'''

'''
탬플릿

'''

@app.route('/')
def hello():
    userid = session.get('userid', None)
    return render_template('hello.html', userid=userid) #controller view 구분할 수 있도록 html 바로 들고와서 사용자에게 전달할 수 있다 


#순환구조 방지하기 위해서(앱관련 설정 여기로 옮겨오기)
basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile # 한 줄로 표현 가능 -- connection
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True # tear down일 때 commit을 하겠다 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'adfdffadafagfgad'
# secret key를 기반으로 해서 암호화된 해시를 만들어냄 , 이를 가지고 검증을 함
csrf = CSRFProtect()
csrf.init_app(app)

db.init_app(app) #초기화
db.app = app #안에다가 넣기
db.create_all()

if __name__:"___main___":
    app.run(host='127.0.0.1', port=5000, debug=True)
