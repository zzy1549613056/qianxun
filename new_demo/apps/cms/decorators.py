from flask import session,redirect,url_for
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args,**kw):
        if session.get('cms_user_id'):
            return func(*args,**kw)
        return redirect(url_for('cms.login'))
    return wrapper