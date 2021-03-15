import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Fcuser(db.Model):
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))

    @property #변수처럼 사용할 수 있게 됨
    def serialize(self): 
        return {
            'id' : self.id,
            'password' : self.password,
            'userid' : self.userid,
            'username' : self.username
        }