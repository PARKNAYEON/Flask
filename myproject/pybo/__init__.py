from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config) # 환경변수로 부르기 위해

    #ORM db와 migrate를 객체로 만든 다음 함수 안에서 메서드를 이용해서 초기화 -> 이렇게 하지 않으면 다른 모듈에서 불러오지 못하기 때문이다
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models # migrate 객체가 models.py 파일을 참조하게 함


    #blueprint
    from .views import main_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp) # 객체 등록!
    app.register_blueprint(answer_views.bp)


    return app