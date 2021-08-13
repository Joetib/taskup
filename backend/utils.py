import re
from datetime import datetime, timedelta
from functools import wraps
from flask import g, url_for, flash, abort, request, redirect, Markup
from backend.database import User
import hashlib


_ws_split_re = re.compile(r'(\s+)')


TIMEDELTA_UNITS = (
    ('year',   3600 * 24 * 365),
    ('month',  3600 * 24 * 30),
    ('week',   3600 * 24 * 7),
    ('day',    3600 * 24),
    ('hour',   3600),
    ('minute', 60),
    ('second', 1)
)

def hash_password(password: str):
    password = password.encode()
    return hashlib.sha256(password).hexdigest()

def check_password(password: str, hash:str) -> bool:
    return hash_password(password) == hash


def has_project_permission(project, user):
    permission =  project.manager == user or user in project.contributors
    if not permission:
        abort(404, {
            'success': False,
            'message': f"Permission denied.",
        } )
    return permission
    

def requires_api_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                if user:
                    g.user = user
                    return f(*args, **kwargs)
        return redirect(url_for('auth.api_login', next=request.path))
    return decorated_function

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('general.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def format_datetime(dt):
    return dt.strftime('%Y-%m-%d @ %H:%M')


def format_date(dt):
    return dt.strftime('%Y-%m-%d')


def format_timedelta(delta, granularity='second', threshold=.85):
    if isinstance(delta, datetime):
        delta = datetime.utcnow() - delta
    if isinstance(delta, timedelta):
        seconds = int((delta.days * 86400) + delta.seconds)
    else:
        seconds = delta

    for unit, secs_per_unit in TIMEDELTA_UNITS:
        value = abs(seconds) / secs_per_unit
        if value >= threshold or unit == granularity:
            if unit == granularity and value > 0:
                value = max(1, value)
            value = int(round(value))
            rv = u'%s %s' % (value, unit)
            if value != 1:
                rv += u's'
            return rv
    return u''
