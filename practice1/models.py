import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy() #모델을 만들기도 하고 데이터를 만들기도 함

class Fcuser(db.Model):
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))

