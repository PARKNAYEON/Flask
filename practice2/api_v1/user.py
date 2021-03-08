from flask import jsonify
from flask import request
from models import Fcuser, db
from . import api

@api.route('/users', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        userid = request.form.get('userid')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        if not (userid and username and password and re_password):
            return jsonify({'error': 'No arguments'}), 400 # 404 붙여서 에러 뜨게 할 수 있다
        
        if password != re_password:
            return jsonify({'error': 'Wrong password'}), 400


        fcuser = Fcuser()
        fcuser.userid = userid

        fcuser.username = username
        fcuser.password = password

        db.session.add(fcuser)
        db.session.commit()
        
        return jsonify(), 201

    users = Fcuser.query.all()
    print("user show wwww me")
    #1. 직접 리스트는 반복문을 돌면서 추가하면 됨
    #2. 모델안에다가 직렬화 함수를 만들어두고 리스트를 만들어냄
    return jsonify([user.serialize for user in users])


