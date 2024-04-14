from functools import wraps
from flask import request, redirect, url_for, session

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function

def guest_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return decorated_function
