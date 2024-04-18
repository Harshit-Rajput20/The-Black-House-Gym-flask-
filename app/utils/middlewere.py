from flask import session, redirect, url_for, flash
from functools import wraps
from models.user import User
from models.sessions import Session
from models.user import AdminRole

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'session_token' in session:
            session_token = session['session_token']
            session_data = Session.query.filter_by(sid=session_token).first()
            if session_data:
                user_id = session_data.user_id
                user = User.query.get(user_id)
                if user:
                    # You can do additional checks here if needed
                    return func(*args, **kwargs)
        flash('Login required to access this page.', 'warning')
        return redirect(url_for('login.login'))
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'session_token' in session:
            session_token = session['session_token']
            session_data = Session.query.filter_by(sid=session_token).first()
            if session_data:
                user_id = session_data.user_id
                user = User.query.get(user_id)
                if user and user.is_admin:
                    return func(*args, **kwargs)
        flash('Admin privileges required to access this page.', 'warning')
        return redirect(url_for('login.login'))
    return wrapper


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'session_token' in session:
                session_token = session['session_token']
                session_data = Session.query.filter_by(sid=session_token).first()
                if session_data:
                    user_id = session_data.user_id
                    user = User.query.get(user_id)
                    if user and user.is_admin:
                        # If the user is an admin, check admin permissions
                        admin_role = AdminRole.query.get(user.admin_role_id)
                        if getattr(admin_role, permission):
                            return func(*args, **kwargs)
            flash('Insufficient permissions to access this page.', 'warning')
            return redirect(url_for('login.login'))
        return wrapper
    return decorator
