from flask import jsonify
from flask import request
from flask import Blueprint
import requests

from . import api

@api.route('/todos', methods=['GET', 'POST'])
def toods():
    if request.method == 'POST': # 내용을 전달한 데이터를 슬랙에 전달
        res = requests.post('https://hooks.slack.com/services/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', json={
            'text': 'Hello world!'
        }, headers={'Content-Type' : 'application/json'})
    elif request.method == 'GET':
        pass

    data = request.get_json()

    return jsonify(data)

@api.route('/test', methods=['POST'])
def test():
    res = request.form['text']
    print(res)
    return jsonify(res)