import os
from flask import Flask
from flask import request, redirect, render_template
from models import db
from forms import RegisterForm
from api_v1 import api as api_v1

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1') #뷰를 분리할 때 사용

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html')

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile # 한 줄로 표현 가능 -- connection
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True # tear down일 때 commit을 하겠다 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'adfdffadafagfgad'

db.init_app(app)
db.app = app
db.create_all()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)