from flask import Blueprint, render_template, session, redirect, url_for, \
     request, flash, g, jsonify, abort
from backend.utils import check_password, hash_password
from backend.database import  db_session, User

mod = Blueprint('auth', __name__, root_path='/auth')

@mod.route('/api-login', methods=["POST"])
def api_login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user: User = User.query.filter_by(email=email).first()
    if user:
        if check_password(password, user.password):
            g.user = user
            token = user.encode_auth_token(user.id)
            if isinstance (token, str):
                return {
                    'token': user.encode_auth_token(user.id),
                    'username': user.name,
                    'email': user.email,
                    'id': user.id,
                    'success': True,
                    'message': "sign up successful"
                }
            
    return {
        'token': None,
        'success': False,
        'message': "The email and password do not match",
    }

@mod.route('/api-signup', methods=["POST"])
def api_signup():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    user: User = User.query.filter_by(email=email).first()

    user: User = User(name=name, email=email, password=hash_password(password))
    db_session.add(user)
    db_session.commit()
    token = user.encode_auth_token(user.id)
    if isinstance(token, str):
        return {
            'token': token,
            'success': True,
            'name': user.name,
            'email': user.email,
            'id': user.id,
            'message': "Sign Up successful",
        }
    return {
        'token': None,
        'success': False,
        'message': 'Sign up was unsuccessful.'
    }
