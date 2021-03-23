from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask_jwt import JWT
from glob import glob
import os
import psutil

os.chdir("C:/Users/netid/Desktop/git/Flask/flask_work_test")
# 파일리스트  = glob( ) -> 통신할 py 파일을 나열

app = Flask(__name__)

host="127.0.0.1"

@app.route("/vector_model_train/<domain>/<parameter>", methods=['GET'])
def test(domain, parameter):
    if request.method == 'GET':
        try:
            exec(open("run_vector_upload.py").read())
        except Exception as e:
            # 파일에 에러가 있다
            print("other errorrr!~")
            x = str(e)
            return jsonify({"message" : str(e), "status" : False}), 404
        else:
            # 성공적이면 True 
            print("통신성공~~")
            print(jsonify({"status" : True}))
            # print(psutil.pids())
            return jsonify({"message" : "success", "status" : True}), 200

    return jsonify(),201
        
def run(self, host=None, port=None, debug=None, **options):
    from werkzeug.serving import run_simple
    if host is None:
        host = '127.0.0.1'
    if port is None:
        server_name = self.config['SERVER_NAME']
        if server_name and ':' in server_name:
            port = int(server_name.rsplit(':', 1)[1])
        else:
            port = 5000
    if debug is not None:
        self.debug = bool(debug)
    options.setdefault('use_reloader', self.debug)
    options.setdefault('use_debugger', self.debug)
    try:
        Run_simple (host, port, self, ** options) # enters this function
    finally:
        # reset the first request information if the development server
        # reset normally.  This makes it possible to restart the server
        # without reloader and that stuff from an interactive shell.
        self._got_first_request = False

if __name__ == '__main__':
    a = 5000
    app.run(debug=True)



