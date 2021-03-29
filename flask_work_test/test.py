# coding:utf-8

import re
import sys
import json
from pathlib import Path

import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask_jwt import JWT
from glob import glob
import os
import subprocess
from flask_restful import Resource, Api, reqparse, abort
from concurrent.futures import ProcessPoolExecutor
from time import sleep

module_path = Path(__file__).parent.parent 
sys.path.append(str(module_path))
os.chdir("C:/Users/netid/Desktop/git/Flask/flask_work_test")

parser = reqparse.RequestParser()
# 실행시킬 쉘 파일 이름
sh_file = "./test.sh"

class AnalCategory(Resource):
    '''
        카테고리 유사도 분석 통신
    '''

    parser.add_argument('Vector_flag', type=bool)

    def post(self, domain_id):

        args = parser.parse_args()
        vector_flag = args['Vector_flag']

        if vector_flag == True:
            try:
                result = os.system(sh_file + " " + domain_id)
                if 0 != result:
                    return jsonify({"status" : False, "message" : "shell file error"})
            except Exception as e:
                print("error")
                return jsonify({"message" : str(e), "status" : False})
            else:
                # 성공적이면 True 
                return jsonify({"message" : "success", "status" : True})

        return jsonify({"message" : "fail"})



if __name__ == '__main__':

    pool = ProcessPoolExecutor(3)

    future = pool.map()
    
    app = flask.Flask(__name__)
    api = Api(app)
    
    parser.add_argument('domain_id')

    api.add_resource(AnalCategory, '/category/<domain_id>')
   
    app.run(debug=True)
