from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST', )) # 답변 저장 템플릿에 있는 form 엘리먼트의 method값과 일치해야 함
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content'] # name 속성이 'content'인 값
        answer = Answer(content=content, create_date=datetime.now(), user=g.user) # g.user -> auth_views.py 파일의 @bp.before_app_request 애너테이션으로 만든 로그인한 사용자 정보
        question.answer_set.append(answer) # 질문에 대한 답변들
        db.session.commit()
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id = question_id), answer.id)) # 스크롤 저절로 이동
    
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit(): 
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            return redirect('{}#answer_{}'.format(url_for('question.detail', question_id = answer.question.id), answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
    