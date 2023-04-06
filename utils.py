from os import mkdir
from os.path import exists
from flask import jsonify
from functools import wraps


def response(message):
    return jsonify({'message': message})


def database_folder():
    match exists("database"):
        case True:
            pass
        case False:
            mkdir("database")


def isAuthenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = session.get('auth')

        if not token:
            return abort(401, 'Unauthorised access detected!')

        verifyJWT(token)

        return f(*args, **kwargs)

    return decorator
