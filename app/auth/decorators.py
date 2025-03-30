from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("No autorizado", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def empleado_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'empleado']:
            flash("No autorizando", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def cliente_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'empleado', 'cliente']:
            flash("No autorizado", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function