from flask import Blueprint, render_template, request, session, redirect, send_file
from utils import response, isAuthenticated

web = Blueprint('web', __name__)
api = Blueprint('api', __name__)


@web.route('/')
def signIn():
    return render_template('login.html')


@web.route('/logout')
def logout():
    session['auth'] = None
    return redirect('/')


@api.route('/login', methods=['POST'])
def apiLogin():
    if not request.is_json:
        return response('Invalid JSON!'), 400

    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if not username or not password:
        return response('All fields are required!'), 401

    user = login(username, password)

    if user:
        session['auth'] = user
        return response('Success'), 200

    return response('Invalid credentials!'), 403
