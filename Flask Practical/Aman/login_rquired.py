from flask import flash,session,redirect,url_for
from functools import wraps
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'authenticated' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('user_blueprint.login'))

    return wrap