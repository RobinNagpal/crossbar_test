import json
import logging
import os
import uuid

import jwt
from flask import Flask, jsonify
from flask import abort
from flask import request
from flask_cors import CORS, cross_origin

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app, support_credentials=True)

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
@cross_origin()
def get_users():
    return jsonify({'users': users})


@app.route('/auth/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_task():
    request_json = json.loads(request.data)
    # request_json = request.json
    if not request_json or not 'email' in request_json:
        abort(400)
    if not request_json or not 'password' in request_json:
        abort(400)
    user = find_user(request_json['email'])
    if not user:
        abort(400)
    print("User", user)
    if not request_json['password'] == user['password']:
        abort(400)
    user['token'] = jwt_encode(user)
    return jsonify(user), 200


def jwt_encode(user):
    payload = {
        'user_id': str(user['id']),
        'email': user['email']
    }
    encode = jwt.encode(payload, jwt_secret, algorithm='HS256')
    return str(encode, 'utf-8')


def find_user(email):
    for user in users:
        if user['email'] == email:
            return user


logging.getLogger('flask_cors').level = logging.DEBUG
logging._defaultFormatter = logging.Formatter(u"%(message)s")

if __name__ == '__main__':
    app.run(debug=True)
