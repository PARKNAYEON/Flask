from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from .. import db
from sqlalchemy import func
from pybo.models import Question, Answer, User, question_voter
from ..forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required


bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    #입력 파라미터
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    if so == 'recommend':
        sub_query = db.session.query( # 질문별 추천 수를 알기 위해서
            question_voter.c.question_id, func.count('*').label('num_voter'))\
            .group_by(question_voter.c.question_id).subquery()  # 모델과 조인하고 /질문별 추천 수를/ 얻기
        question_list = Question.query\
            .outerjoin(sub_query, Question.id == sub_query.c.question_id)\
                .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())# 아우터조인, 추천수를 의미하는 것을 역순으로 정렬 -> 추천 수가 많은 질문으로 정렬되고, 추천 수가 같은 경우 작성일시 역순으로 정렬
    elif so == 'popular':
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer'))\
            .group_by(Answer.question_id).subquery()
        question_list = Question.query\
            .outerjoin(sub_query, Question.id == sub_query.c.question_id)\
                .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:
        question_list = Question.query.order_by(Question.create_date.desc())
        
    #조회
    
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username).join(User, Answer.user_id == User.id).subquery()
        question_list = question_list.join(User).outerjoin(sub_query, sub_query.c.question_id == Question.id).filter(Question.subject.ilike(search)|
            Question.content.ilike(search)|
            User.username.ilike(search)|
            sub_query.c.content.ilike(search)|
            sub_query.c.username.ilike(search)).distinct()

    #paging
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)



@bp.route('/detail/<int:question_id>/')
def detail(question_id): # 라우트 매핑 규칙에 사용한 <int:question_id> 전달 
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index')) # post 방식 요청이면 데이터 저장 후 질문 목록 페이지로 이동
    return render_template('question/question_form.html', form=form) # GET 방식 요청이면 질문 등록 페이지 렌더링

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required #로그인시 필요하니까
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다.') # 로그인한 사용자와 질문의 작성자가 다르면 수정할 수 없도록 flash 오류를 발생시킴
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST': # 질문 수정 화면에서 데이터를 수정한 다음 저장하기 버튼을 눌렀을 때
        form = QuestionForm()
        if form.validate_on_submit(): # 검증
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit() # 이상 없음, 저장
            return redirect(url_for('question.detail', question_id=question_id))
    else: # 질문 수정 버튼을 눌렀을 때 : 이미 수정할 질문에 해당하는 것들이 보이게 함
        form = QuestionForm(obj=question)
    return render_template('Question/question_form.html', form=form)


@bp.route('/delete/<int:question_id>')
@login_required # 로그인시 사용가능
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))



        