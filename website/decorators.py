from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if not current_user.is_authenticated or not current_user.is_admin:
        #     abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            return redirect(url_for("views.dashboard"))
        return f(*args, **kwargs)
    return decorated_function
