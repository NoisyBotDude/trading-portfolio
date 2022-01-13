from flask import flash, session, redirect, url_for
from functools import wraps

def logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            flash('You need to login first', 'danger')
            return redirect(url_for('user.login_page'))
    return wrapper