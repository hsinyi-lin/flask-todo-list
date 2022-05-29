import os
from datetime import timedelta
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# session settings
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=1)

# path to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)
    return wrap


@app.route('/')
@login_required
def index():
    todo_list = Todo.query.all()
    return render_template('todo.html', todo_list=todo_list)


@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:todo_id>')
@login_required
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>')
@login_required
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return '<h1>找不到網頁</h1>', 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login_form.html')
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user:
        check_pw = bcrypt.check_password_hash(user.password, password)
        if check_pw:
            session['username'] = username
            session.permanent = True
            return redirect(url_for('index'))
        else:
            flash('帳號或密碼錯誤')
            return redirect(url_for('login'))
    else:
        flash('沒有這個帳號')
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register_form.html')

    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']

    user = User.query.filter_by(username=username)
    if user.count() > 0:
        flash('此帳號已被註冊')
        return redirect(url_for('register'))
    if password1 != password2:
        flash('密碼不一致')
        return redirect(url_for('register'))

    pw_hash = bcrypt.generate_password_hash(password1)
    new_user = User(username=username, password=pw_hash)
    db.session.add(new_user)
    db.session.commit()
    flash('註冊成功')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
