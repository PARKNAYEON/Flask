from pybo import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True) # db.Column(속성의 데이터 타입 지정, 속서을 기본 키로 지정)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE')) # ForeginKey(연결할 기존 모델의 속성, 삭제 연동 설정)
    question = db.relationship('Question', backref=db.backref('answer_set',)) # -> relationship : 기존 모델 참조
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)