import uuid

from flask import Flask, jsonify
from flask import abort
from flask import request

app = Flask(__name__)
jwt_secret = 'jwt_secret'

users = [
    {
        'id': uuid.uuid4(),
        'name': 'Robin Nagpal',
        'email': 'robinnagpal.tiet@gmail.com',
        'password': 'secret'
    },
    {
        'id': uuid.uuid4(),
        'name': 'Guneet Kaur',
        'email': '2013nibor@gmail.com',
        'password': 'secret'
    },
    {
        'id': uuid.uuid4(),
        'name': 'Joe',
        'email': 'joe@gmail.com',
        'password': 'secret'
    }
]


@app.route('/auth/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app.route('/auth/login', methods=['POST'])
def create_task():
    request_json = request.json
    if not request_json or not 'email' in request_json:
        abort(400)
    if not request_json or not 'password' in request_json:
        abort(400)
    user = find_user(request_json['email'])
    if not user:
        abort(400)
    if not request_json['password'] == user.password:
        abort(400)

    return jsonify(), 201


def find_user(email):
    for user in users:
        if user['email'] == email:
            return user


if __name__ == '__main__':
    app.run(debug=True)
