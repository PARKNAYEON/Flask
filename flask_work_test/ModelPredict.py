# coding:utf-8

import re
import sys
import json
from pathlib import Path

import flask
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort

module_path = Path(__file__).parent.parent 
sys.path.append(str(module_path))

from comm.ConfigInit import ConfigInit
from neuralnets.Starspace import Starspace
from data_process.DocPreprocess import DocPreprocess
from data_process.StarspaceData import StarspaceData
from wordnets.RelatedKeyword import RelatedKeyword

def nullable_string(val):
    if not val:
        return None
    return val

parser = reqparse.RequestParser()

class KeywordPredictor(Resource):
    ''' 키워드 모델 API

    '''

    parser.add_argument('input_keyword',
        type = nullable_string
    )
    
    def post(self, domain_id):
        ''' 키워드 모델의 domain_id를 받아서 해당 도메인의 저장된 모델을 불러옴
            /keyword/<domain_id> 형식으로 post 요청을 보내면, 학습된 해당된 모델이 있을 경우에 모델을 load

            Args :
                domain_id : 도메인 id
            Returns :
                boolean : 성공하면 True를 반환
        '''

        all_models["keyword"][domain_id] = self._load_model(domain_id)
        return True

    def get(self, domain_id):
        ''' domain_id를 받아서 해당 도메인에 load된 모델이 있을 경우, 예측
            /keyword/<domain_id>?input_keyword="" 형식으로 get 요청을 보내면, 해당 input_keyword값을 모델에 넣어서 예측

            Args :
                domain_id : 도메인 id
                input_keyword : 요청으로 들어온 모델의 input으로 넣을 string
            Returns :
                predict_result [json] : 성공하면 True를 반환
        '''

        if domain_id in all_models["keyword"]:
            data = parser.parse_args()
            if data["input_keyword"] is not None:
                input_keyword = data["input_keyword"].replace('"', '').replace("'", '')

            if input_keyword:
                model = all_models["keyword"][domain_id]
                if not model:
                    model = self._load_model(domain_id)
                    all_models["keyword"][domain_id] = model

                predicts = model.predict(data["input_keyword"]) 
                return jsonify({'predict_result': predicts}) 
            else:
                return jsonify({'predict_result': ""})

    def _load_model(self, domain_id):
        ''' 특정 domain_id에 해당하는 config를 초기화하고, RelatedKeyword를 해당 domain_id 모델을 로드

            Args :
                domain_id : 도메인 id
            Returns :
                model [model] : 로드된 모델
        '''

        conf_files = get_config_paths("/project/aidoc/02.02/airflow_dags/configs")
        conf_path = [path for path in conf_files if re.findall(r"\d+",path.stem)[0] == domain_id][0]
        comm_init_module = ConfigInit(domain_id  = domain_id, conf_path = conf_path)
        model = RelatedKeyword(comm_init_module) # model_path <- domain_id
        model.load_model()

        return model

class DocumentPredictor(Resource):

    def post(self, domain_id):
        ''' 문서 모델의 domain_id를 받아서 해당 도메인의 저장된 모델을 불러옴
            /document/<domain_id> 형식으로 post 요청을 보내면, 학습된 해당된 모델이 있을 경우에 모델을 load

            Args :
                domain_id : 도메인 id
            Returns :
                boolean : 성공하면 True를 반환
        '''

        all_models["document"][domain_id] = self._load_model(domain_id)
        return True

    def get(self, domain_id):
        ''' domain_id를 받아서 해당 도메인에 load된 모델이 있을 경우, 예측
            /document/<domain_id>?is_from_file=True 형식으로 get 요청을 보내면, 저장된 csv파일들을 읽어서 벡터를 업데이트
            /document/<domain_id>?is_from_file=False&contents="" 형식으로 get 요청을 보내면, contents를 전처리를 진행후 model에 넣어서 vector 반환

            Args :
                domain_id : 도메인 id
                is_from_file : 파일에서 읽을 것인지 여부
                contents : is_from_file가 False라면 처리할 문서내용
            Returns :
                result [json] : is_from_file=True 인 경우엔 성공여부 반환. is_from_file=False 인 경우엔 문서 모델에서 처리한 vector 반환
        '''
        
        if domain_id in all_models["document"]:
            
            parser.add_argument('is_from_file')
            parser.add_argument('contents')
            args = parser.parse_args()
            
            is_from_file = args["is_from_file"]
            contents = args["contents"] # 192.168.1.42:8786/document/1?contents="~~~~~~~"

            model = all_models["document"][domain_id]
            if not model:
                model = self._load_model(domain_id)
                all_models["document"][domain_id] = model

            if is_from_file == "TRUE":
                # csv 파일 목록을 읽어서 엘라스틱서치에 업데이트
                model_result = model.update_embedding_from_files()
                # return jsonify({'result': True})
                return model_result
            elif is_from_file == "FALSE" and contents:
                
                self.doc_pre.set_doc_data(contents)
                self.doc_pre.process_doc()
                self.star_pre.set_doc_data(self.doc_pre.get_doc_data())
                self.star_pre.apply_preprocess()
                processed_out = self.star_pre.get_doc_data() # contents 

                predicts = model.predict(processed_out) # vector
                return jsonify({'result': predicts}) # result: (400) result

    def _load_model(self, domain_id) :
        ''' 특정 domain_id에 해당하는 config를 초기화하고, Starspace를 해당 domain_id 모델을 로드

            Args :
                domain_id : 도메인 id
            Returns :
                model [model] : 로드된 모델
        '''
        
        conf_files = get_config_paths("/project/aidoc/03.22/dl-model/airflow_dags/configs")
        conf_path = [path for path in conf_files if re.findall(r"\d+",path.stem)[0] == domain_id][0]
        comm_init_module = ConfigInit(domain_id  = domain_id, conf_path = conf_path)
        model = Starspace(comm_init_module, model_save_time = None, is_init = False)
        model.load_model()

        return model

def get_config_paths(path) :
    # "/project/feature/airflow_test/configs"
    conf_path = Path(path)
    conf_files = list(conf_path.glob("*.json"))

    return conf_files

all_models = {"keyword" : {}, "document" : {}}

if __name__ == '__main__':
    
    app = flask.Flask(__name__)
    api = Api(app)
    
    parser.add_argument('domain_id')

    api.add_resource(KeywordPredictor, '/keyword/<domain_id>')
    api.add_resource(DocumentPredictor, '/document/<domain_id>')

    app.run(debug=True, port=8786, host='0.0.0.0')

    