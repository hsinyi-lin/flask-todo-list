# todo_list
from utils.decorators import login_required
from flask import Blueprint, render_template, request, url_for, redirect

from utils.models import Todo, db

to_do = Blueprint('to_do', __name__)


@to_do.route('/')
@login_required
def index():
    todo_list = Todo.query.all()
    return render_template('todo.html', todo_list=todo_list)


@to_do.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('to_do.index'))


@to_do.route('/update/<int:todo_id>')
@login_required
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('to_do.index'))


@to_do.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('to_do.index'))

