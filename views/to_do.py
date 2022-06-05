# todo
from utils.decorators import login_required
from flask import Blueprint, render_template, request, url_for, redirect, session, flash

from utils.models import Todo, db

to_do = Blueprint('to_do', __name__)


@to_do.route('/')
@login_required
def index():
    username = session['username']
    todo_list = Todo.query.filter_by(user_id=username)
    return render_template('todo/index.html', todo_list=todo_list)


@to_do.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    username = session['username']
    new_todo = Todo(title=title, complete=False, user_id=username)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('to_do.index'))


@to_do.route('/update/<int:todo_id>')
@login_required
def update(todo_id):
    username = session['username']
    todo = Todo.query.filter_by(id=todo_id, user_id=username).first()
    if not todo:
        flash('沒有這個項目')
    else:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for('to_do.index'))


@to_do.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    username = session['username']
    todo = Todo.query.filter_by(id=todo_id, user_id=username).first()
    if not todo:
        flash('沒有這個項目')
    else:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('to_do.index'))

