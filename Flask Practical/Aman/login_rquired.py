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

def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'authenticated' in session and 'role':
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('user_blueprint.admin_login'))

    return wrap