from app import *


if __name__ == "__main__":
    database_folder()
    construct_datebase('scripts/devices.sql')
    register('test', 'password', 'privileged1')
    login('test', 'password')
    delete_user('username')
    # app.run(host='0.0.0.0', port=5000, debug=False, use_evalex=False)
