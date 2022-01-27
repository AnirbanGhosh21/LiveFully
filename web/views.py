from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Log
from . import db
from sqlalchemy import desc
from .functions import sentenceEvaluation, getSentimentPara

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        text = request.form.get('newLog')
        if text[-1] != '.' or text[-1] != '?':
            text += '.'
        polarity, subjectivity = getSentimentPara(text)
        tags = sentenceEvaluation(text)
        log = Log(text=text, author=current_user.id,
                  polarity=polarity, subjectivity=subjectivity, tags=tags)
        db.session.add(log)
        db.session.commit()
    return render_template('home.html', user=current_user)


@views.route('/view-logs')
@login_required
def create_log():
    logs = Log.query.filter_by(
        author=current_user.id).order_by(desc(Log.dateCreated))
    return render_template('logs.html', user=current_user, logs=logs)


@views.route('/delete/<int:id>')
@login_required
def delete(id):
    log_to_delete = Log.query.get_or_404(id)
    try:
        db.session.delete(log_to_delete)
        db.session.commit()
        logs = Log.query.filter_by(
            author=current_user.id).order_by(desc(Log.dateCreated))
        return render_template('logs.html', user=current_user, logs=logs)
    except:
        flash("Delete Failed")
        return render_template('home.html', user=current_user)


@ views.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    log_to_update = Log.query.get_or_404(id)
    if request.method == 'POST':
        log_to_update.text = request.form['newLog']
        try:
            db.session.commit()
            logs = Log.query.filter_by(
                author=current_user.id).order_by(desc(Log.dateCreated))
            return render_template('logs.html', user=current_user, logs=logs)
        except:
            flash('Update Error')
            return render_template('home.html', user=current_user)
    else:
        return render_template('update.html', user=current_user, log=log_to_update)


# @views.route('/create-log', methods=['GET', 'POST'])
# @login_required
# def create_log():
#     if request.method == 'POST':
#         text = request.form.get('newLog')
#         log = Log(text=text, author=current_user.id)
#         db.session.add(log)
#         db.session.commit()

#     return render_template('Journal.html', user=current_user)
