from flask import request, Blueprint, session, redirect, flash, url_for, render_template
from flask_bcrypt import Bcrypt

from utils.models import db, User

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()


@auth.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('to_do.index'))
        else:
            flash('帳號或密碼錯誤')
            return redirect(url_for('auth.login'))
    else:
        flash('沒有這個帳號')
        return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register_form.html')

    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']

    user = User.query.filter_by(username=username)
    if user.count() > 0:
        flash('此帳號已被註冊')
        return redirect(url_for('auth.register'))
    if password1 != password2:
        flash('密碼不一致')
        return redirect(url_for('auth.register'))

    pw_hash = bcrypt.generate_password_hash(password1)
    new_user = User(username=username, password=pw_hash)
    db.session.add(new_user)
    db.session.commit()
    flash('註冊成功')
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
