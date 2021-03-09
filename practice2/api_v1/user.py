from flask import jsonify
from flask import request
from models import Fcuser, db
from . import api

@api.route('/users', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # header에 contentname이 명시되어 있는데, from을 사용하면 아래와 같이 표현이 된다
        # userid = request.form.get('userid')
        # username = request.form.get('username')
        # password = request.form.get('password')
        # re_password = request.form.get('re_password')

        #하지만 json으로 받게 되면 data로 받아야 한다
        data = request.get_json()
        userid = data.get('userid')
        username = data.get('username')
        password = data.get('password')
        re_password = data.get('re_password')
        print(data)

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
    
    #1. 직접 리스트는 반복문을 돌면서 추가하면 됨
    #2. 모델안에다가 직렬화 함수를 만들어두고 리스트를 만들어냄
    return jsonify([user.serialize for user in users])

@api.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(uid):
    # header에 contentname이 명시되어 있는데, api를 사용하면 
    if request.method == 'GET':
        user = Fcuser.query.filter(Fcuser.id == uid).first()
        return jsonify(user.serialize)

    elif request.method == 'DELETE':
        Fuser.query.delete(Fcuser.id == uid)
        return jsonify(), 204 # no context 
    
    # put -> 전체를 업데이트 할 때 
    data = request.get_json()

    # userid = data.get('userid')
    # username = data.get('username')
    # password = data.get('password')

    # updated_Data = {}
    # if userid:
    #     updated_data['userid'] = userid
    # if username:
    #     updated_data['username'] = username
    # if password:
    #     updated_data['password'] = password

    Fcuser.query.filter(Fcuser.id == uid).update(data) # 업데이트 정보를 가지고 와서
    user = Fcuser.query.filter(Fcuser.id == uid).first() # 넣는다

    return jsonify(user.serialize)  


