from flask import jsonify
from flask import request
from flask import Blueprint
from models import Todo, db
import requests
import datetime

from . import api

def send_slack(msg):
    res = requests.post('http://...... slack link.....', json={
            'text': msg
    }, headers={'Content-Type' : 'application/json'})

@api.route('/todos', methods=['GET', 'POST'])
def toods():
    if request.method == 'POST': # 내용을 전달한 데이터를 슬랙에 전달
        # 생성하는 코드
        # 알림
        send_slack('TODO가 생성되었습니다')# 사용자 정보, 할일 제목, 기한
    elif request.method == 'GET':
        pass

    data = request.get_json()
    return jsonify(data) 

@api.route('/slack/todos', methods=['POST'])
def slack_todos():
    # flasktodo create aaaaaa : 명령의 구분이 띄어쓰기로 나눠져 있음
    # flask list 
    res = request.form['text'].split(' ') # msg 와 cmd 구분하기
    cmd, *args = res 

    ret_msg = ''

    if cmd == 'create':
        todo_name = args[0]

        todo = Todo()
        todo.title = todo_name

        db.session.add(todo)
        db.session.commit()
        ret_msg = 'todo가 생성되었습니다'

        send_slack('[%s] %s 할일을 만들었습니다.' %(str(datetime.datetime.now()), todo_name)) 

    elif cmd == 'list':
        todos = Todo.query.all()
        for todo in enumerate(todos):
            ret_msg += '%d. %s (~ %s)'%(idx+1, todo.title, str(todo.tstamp))
        

    return jsonify(res)