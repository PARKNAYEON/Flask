from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from .. import db
from pybo.models import Question
from ..forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required


bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1) # get 방식으로 요청한 URL에서 page값 5를 가져올 때 사용
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)


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