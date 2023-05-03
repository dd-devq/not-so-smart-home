from os import mkdir
from os.path import exists
from flask import jsonify


def response(message):
    return jsonify({'message': message})


def database_folder():
    match exists("database"):
        case True:
            pass
        case False:
            mkdir("database")
