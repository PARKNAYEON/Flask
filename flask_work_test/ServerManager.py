from werkzeug.serving import make_server
import flask
from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api, reqparse, abort

import logging as log
import threading

# from FlaskTest import KeywordPredictor, DocumentPredictor
try :
    from ModelPredict import KeywordPredictor, DocumentPredictor
except :
    from .ModelPredict import KeywordPredictor, DocumentPredictor
class ServerThread(threading.Thread):

    def __init__(self, app, host, port):
        ''' flask rest_api 서버를 구동하고 멈추는 등 동작을 담당

            Args :
                app : 구동할 어플리케이션을 지정
                host : host
                port : port
            Returns :
                None
        '''

        threading.Thread.__init__(self)
        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        ''' 서버를 구동

            Args :
                None
            Returns :
                None
        '''

        log.info('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        ''' 서버를 멈춤

            Args :
                None
            Returns :
                None
        '''

        self.srv.shutdown()

def start_server(host, port):
    global server
    global app
    global api

    parser = reqparse.RequestParser()
    parser.add_argument('domain_id')

    api.add_resource(KeywordPredictor, '/keyword/<domain_id>')
    api.add_resource(DocumentPredictor, '/document/<domain_id>')

    server = ServerThread(app, host, port)
    server.start()
    log.info('server started')
    print('server started')

app = flask.Flask('app')
api = Api(app)

server = None
target_port = 8786

# all_models = {"keyword" : {}, "document" : {}}
# start_server(host = "0.0.0.0", port = target_port)

from psutil import process_iter
from signal import SIGTERM # or SIGKILL

@app.route('/shutdown', methods=['POST'])
def stop_server():
    # global server
    # server.shutdown()
    # print('server stopped')
    global target_port

    shutdown_server()

    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == target_port:
                proc.send_signal(SIGTERM) # or SIGKILL
    
    return "Bye Bye"

from flask import request
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()
    
    return Response("Bye", mimetype='text/plain')
