from functools import wraps

from flask import session, url_for, redirect


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        else:
            return f(*args, **kwargs)
    return wrap